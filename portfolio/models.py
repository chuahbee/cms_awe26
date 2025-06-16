# portfolio/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, HelpPanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from django.utils.safestring import mark_safe
from django.templatetags.static import static

class WorkIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["portfolio.WorkPage"]

    # 🔸 关键：把原本写在模板里的查询搬到这里
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["works"] = (
            self.get_children()
                .live()
                .order_by("-first_published_at")
                .specific()
        )
        return context


class AboutPage(Page):
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("main_image"),
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("body"),
        APIField("main_image", serializer=ImageRenditionField('fill-800x400')),
    ]

    parent_page_types = ["home.HomePage"]


class WorkPage(Page):
    date = models.DateField("Published date")
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("main_image"),
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("date"),
        APIField("body"),
        APIField("main_image", serializer=ImageRenditionField('fill-400x250')),
    ]

    parent_page_types = ["portfolio.WorkIndexPage"]


class BaseSectionPage(Page):
    body = RichTextField(blank=True)
    code_block = models.TextField(blank=True)
    is_code = models.BooleanField(default=True, help_text="if you want to show code layout, please check the box below")

    content_panels = Page.content_panels + [
        HelpPanel(content=mark_safe(
            f'<a href="#" onclick="window.open(\'{static("images/section_info.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img class="help-img" src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;"><span class="hugeicons--touchpad-04"></span>'
            '</a><br/>'
        )),
        FieldPanel("body"),
        FieldPanel("code_block"),

        HelpPanel(content=mark_safe(
            f'<a href="#" onclick="window.open(\'{static("images/iscode.jpg") }\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img class="help-img" src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;"><span class="hugeicons--touchpad-04"></span>'
            '</a><br/>'
        )),
        FieldPanel("is_code"),
    ]

    class Meta:
        abstract = True  # 不会生成页面类型，只能继承

    @property
    def anchor_id(self):
        # self.get_parent() 是 Tab 页
        tab_slug = self.get_parent().slug
        return f"{tab_slug}-section-{self.slug}"


class BaseSubsectionPage(Page):
    body = RichTextField(blank=True)
    code_block = models.TextField(blank=True)
    is_code = models.BooleanField(default=True, help_text="if you want to show code layout, please check the box below")

    content_panels = Page.content_panels + [
        HelpPanel(content=mark_safe(
            f'<a href="#" onclick="window.open(\'{static("images/section_level.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img class="help-img" src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;"><span class="hugeicons--touchpad-04"></span>'
            '</a><br/>'
        )),
        FieldPanel("body"),
        FieldPanel("code_block"),

        HelpPanel(content=mark_safe(
            f'<a href="#" onclick="window.open(\'{static("images/iscode.jpg") }\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img class="help-img" src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;"><span class="hugeicons--touchpad-04"></span>'
            '</a><br/>'
        )),
        FieldPanel("is_code"),
    ]

    class Meta:
        abstract = True

    @property
    def anchor_id(self):
        tab_slug = self.get_parent().get_parent().slug  # Tab Page
        section_slug = self.get_parent().slug           # Section Page
        return f"{tab_slug}-section-{section_slug}-{self.slug}"


class TabPage(Page):
    body = RichTextField(blank=True)
    code_block = models.TextField(blank=True, help_text="if you want to show code, please check the box below")

    content_panels = Page.content_panels + [
        HelpPanel(content=mark_safe(
            f'<a href="#" onclick="window.open(\'{static("images/section_title.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img class="help-img" src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;"><span class="hugeicons--touchpad-04"></span>'
            '</a><br/>'
        )),

        FieldPanel("body"),
        FieldPanel("code_block"),
    ]

    # 如果有新页面：parent_page_types这里加上新页面名字
    parent_page_types = ["portfolio.AwesomeIndexPage", "portfolio.BitfinexIndexPage", "CreditCardsIndexPage", "P2PIndexPage", "CryptoIndexPage"]
    subpage_types = ["portfolio.SectionPage"]


class SectionPage(BaseSectionPage):
    parent_page_types = ["portfolio.TabPage"]
    subpage_types = ["portfolio.SubsectionPage"]


class SubsectionPage(BaseSubsectionPage):
    parent_page_types = ["portfolio.SectionPage"]


class BaseIndexPage(Page):
    intro = RichTextField(blank=True)
    code_block = models.TextField(blank=True, help_text="if you want to show code, please check the box below")
    show_in_nav = models.BooleanField(default=True)
    is_dropdown = models.BooleanField(default=False)

    nav_parent = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="if no setting, it will auto become a dropdwon menu"
    )

    content_panels = Page.content_panels + [

        HelpPanel(content=mark_safe("<i>Page Title</i>")),
        FieldPanel("intro"),

        FieldPanel("code_block"),

        HelpPanel(content=mark_safe(
            f'<a href="#" class="help-img" onclick="window.open(\'{static("images/main_menu.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;">'
            '<span class="hugeicons--touchpad-04"></span></a>'
        )),

        FieldPanel("show_in_nav"),

        HelpPanel(content=mark_safe(
            f'<a href="#" class="help-img" onclick="window.open(\'{static("images/main_menu_drop.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;">'
            '<span class="hugeicons--touchpad-04"></span></a>'
        )),
        FieldPanel("is_dropdown"),

        HelpPanel(content=mark_safe(
            f'<a href="#" class="help-img" onclick="window.open(\'{static("images/drop_menu.jpg")}\', \'_blank\', \'width=800,height=600\'); return false;">'
            f'<img src="{static("images/howtodo.jpg")}" alt="说明图片" style="width:40px; height:40px; border:1px solid #ccc;">'
            '<span class="hugeicons--touchpad-04"></span></a>'
        )),
        PageChooserPanel("nav_parent"),
    ]

    subpage_types = ["portfolio.TabPage"]

    class Meta:
        abstract = True  # 不会出现在 admin 中

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["pages"] = (
            self.get_children()
                .live()
                .order_by("-first_published_at")
                .specific()
        )
        return context


# no section
# class CryptoIndexPage(Page):
#     parent_page_types = ["home.HomePage"]  # 只允许挂在 HomePage 下
#     subpage_types = ["portfolio.BitfinexIndexPage", "portfolio.AwesomeIndexPage"]

#     # 可选：页面内容可以是空的，也可以重定向或展示子页面列表
#     def get_context(self, request, *args, **kwargs):
#         context = super().get_context(request, *args, **kwargs)
#         context["crypto_sections"] = self.get_children().live().specific()
#         return context


# 如果要加类似AwesomeIndexPage，BitfinexIndexPage，CreditCardsIndexPage，P2PIndexPage新页面
# 譬如 1： class 页面名称(BaseIndexPage):
#     pass
# 如果页面要tab 就要在class TabPage(Page)/parent_page_types里加上新页面名称

class CryptoIndexPage(BaseIndexPage):
    pass

class AwesomeIndexPage(BaseIndexPage):
    pass
    

class BitfinexIndexPage(BaseIndexPage):
    pass
    

class CreditCardsIndexPage(BaseIndexPage):
    pass
    

class P2PIndexPage(BaseIndexPage):
    pass
    

class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title