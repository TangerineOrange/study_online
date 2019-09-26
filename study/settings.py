"""
Django settings for study project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import time
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i5cr+%-xqu8#4%s^r@)%x&u97)%ej#htn51ek6-s94s99lwomt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = "users.UserProfile"

# Application definition
AUTHENTICATION_BACKENDS = {
    'users.views.CustomBackend',
}

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'origanization',
    'operation',
    'captcha',
    # 'apps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'study.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'study.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'study_online',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

SIMPLEUI_HOME_INFO = True

SIMPLEUI_ICON = {
    'Users': 'fa fa-user',
}

SIMPLEUI_CONFIG = {
    'system_keep': False,
    # 'menu_display': ['Simpleui', '测试', '权限认证', '动态菜单测试'],
    # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    # 'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    # 'menus': [{
    #     'name': 'Simpleui',
    #     'icon': 'fas fa-code',
    #     'url': 'https://gitee.com/tompeppa/simpleui'
    # }, {
    #     'app': 'auth',
    #     'name': '权限认证',
    #     'icon': 'fas fa-user-shield',
    #     'models': [{
    #         'name': '用户',
    #         'icon': 'fa fa-user',
    #         'url': 'auth/user/'
    #     }]
    # }, {
    #     'name': '测试',
    #     'icon': 'fa fa-file',
    #     'models': [{
    #         'name': 'Baidu',
    #         'url': 'http://baidu.com',
    #         'icon': 'far fa-surprise'
    #     }, {
    #         'name': '内网穿透',
    #         'url': 'https://www.wezoz.com',
    #         'icon': 'fab fa-github'
    #     }]
    # }, {
    #     'name': '动态菜单测试',
    #     'icon': 'fa fa-desktop',
    #     'models': [{
    #         'name': time.time(),
    #         'url': 'http://baidu.com',
    #         'icon': 'far fa-surprise'
    #     }]
    # }]
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.office365.com"  # 设置服务器
EMAIL_PORT = 587  # 设置服务器
EMAIL_HOST_USER = "likeOrangeForWork@outlook.com"  # 用户名
EMAIL_HOST_PASSWORD = "LOFWasdasd346"
# EMAIL_USE_TLS = False
EMAIL_FROM = "likeOrangeForWork@outlook.com"
