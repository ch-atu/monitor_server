"""
Django settings for monitor_server project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
python manage.py runserver

"""

import os
import sys
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#z!nrh$bn536iwb+#_9cp#lv3s(fdslwud(1()9he3qsnw@rzx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'system.apps.SystemConfig',
    'bootstrap3',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_swagger',
    'assets.apps.AssetsConfig',
    'linux.apps.LinuxConfig',
    'mysql.apps.MysqlConfig',
    'rds.apps.RdsConfig',
    'windows.apps.WindowsConfig',
    'django_filters',
]

GRAPHENE = {
    'SCHEMA': 'monitor_server.schema.schema'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitor_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitor_server.wsgi.application'
AUTH_USER_MODEL = 'system.users'
AUTHENTICATION_BACKENDS = ('system.views.CustomBackend',)  ## 重新登录验证,增加邮箱名字也可以用作登录

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'db_monitor',
        'USER': 'root',
        'PASSWORD': '1234',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 432000
LOGIN_URL = '/auth/login'


LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = True
# USE_TZ = True
USE_TZ = False
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# logging
# 数据采集日志
CHECK_LOG_DIR = os.path.join(BASE_DIR, 'logs')
# 控制台日志存放目录
CONSOLE_LOG = os.path.join(BASE_DIR, 'logs')
# 配置日志
# 这么配置日志最终celery异步执行时间没打印出来
LOGGING = {
    'version': 1,  # 指定版本，目前也就一个版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 暂不使用过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    # 用来定义具体处理日志的方式，可以定义多种
    # "default"就是默认方式，"console"就是打印到控制台方式。file是写入到文件的方式，注意使用的class不同
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONSOLE_LOG + '/django-web.log',  # 日志的存放路径
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False  # 可以基于每个记录器控制该传播。 如果您不希望特定记录器传播到其父项，则可以关闭此行为。
        },
    }
}

# 表格table
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 3,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# 表格table 一页 展示数据
DISPLAY_PER_PAGE = 15

# # celery 4
# 结果存储地址
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND = 'django-db'
# Broker地址
# todo 官网：BROKER_URL
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'
# 默认调度程序，与django-celery-beat扩展一起使用
# todo 官网：CELERYBEAT_SCHEDULER
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# celery worker的并发数， 默认值为cpu内核数
CELERYD_CONCURRENCY = 4
# celery指定的时区
CELERY_TIMEZONE = 'Asia/Shanghai'
# todo 每个worker执行了多少任务就会死掉。工作进程在被新任务替换之前可以执行的最大任务数。默认是没有限制。
CELERYD_MAX_TASKS_PER_CHILD = 10

# 有些情况可以防止死锁  官网无
CELERYD_FORCE_EXECV = True

# 某个程序中出现的队列，在broker中不存在，则立刻创建它，默认值为True
# todo 官网：CELERY_TASK_CREATE_MISSING_QUEUES
CELERY_CREATE_MISSING_QUEUES = True

# 启用速率限制
CELERY_DISABLE_RATE_LIMITS = True

# 软时间限制，单位：秒
# todo 官网：CELERYD_SOFT_TIME_LIMIT
CELERYD_TASK_SOFT_TIME_LIMIT = 600

# 周期性任务的过期时间
# todo 官网：CELERY_RESULT_EXPIRES
CELERY_TASK_RESULT_EXPIRES = 600
# 不使用UTC时间
CELERY_ENABLE_UTC = False

# todo celery-beat???
# 为了防止爆发
# MySQL backend does not support timezone-ae datetimes when USE_TZ is False.
DJANGO_CELERY_BEAT_TZ_AWARE = False

# 标识要使用的默认序列化方法的字符串,默认值是json
CELERY_TASK_SERIALIZER = 'json'
# 结果序列化格式，默认值是json
CELERY_RESULT_SERIALIZER = 'json'

# # rest api
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'  # 注释掉 可以关闭  api web界面
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
)
MIDDLEWARE_CLASSES = ('system.views.DisableCSRFCheck',)

# 配置ASGI
ASGI_APPLICATION = "monitor_server.routing.application"

SWAGGER_SETTINGS = {
    # 基础样式
    # 'SECURITY_DEFINITIONS': {
    #     "basic": {
    #         'type': 'basic'
    #     }
    # },
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'authorization'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    # 'LOGIN_URL': '/api/v1/login/',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}



# send email
IS_SEND_EMAIL = 0
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '*******'
EMAIL_HOST_PASSWORD = '*********'
EMAIL_TO_USER = ['*********@qq.com', '********@hotmail.com']

# send dingding
IS_SEND_DING_MSG = 0
DING_WEBHOOK = '*********'
