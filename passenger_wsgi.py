import os
import sys
import pathlib
import dotenv

# 项目根目录
BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 读取 .env
dotenv.load_dotenv(BASE_DIR / ".env")

# 告诉 Django 用哪个 settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings.production")

# WSGI 入口
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
