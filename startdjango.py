#!/usr/bin/env python3
import sys, os
import argparse

DIR_BIN = "D:/Python34/Lib/site-packages/Django-1.7.7-py3.4.egg/django/bin"

"""
最后修改:2015.05.11
创建django工程基本步骤:
1. 为工程创建文件夹，复制本角本到这个文件夹中。
2. 修改角本的 DIR_BIN
3. cmd运行本角本创建新的工程: python createproject.py [projectname]
4. 在settings.py中添加Mysql数据库支持(mysql.connector.django)
5. 创建MySQL数据库
6. cmd运行manage.py创建基本的数据表: python manage.py migrate contenttypes, sessions, auth, admin
7. cmd运行manage.py创建app: python manage.py startapp [appname]
8. 在settings.py中添加app
9. 在App中添加urls.py
10.在project.urls.py中添加app.urls
11.在app中创建 templates/app，在这里添加.html文件
12.在app中创建 static/app，在这里添加bootstrap(javascript, css,font)和jquery.js文件
13.下载bootstrap(getbootstrap.com),下载jquery(jquery.com)，重命名jquery-2.x.x.min.js为jquery.js
14.在.html头中添加{% load staticfiles %}，下面添加资源文件连接(<link href="{% static app/style.css %}" rel="stylesheet" ... />)
"""

def CreateProject(django_admin_dir, web_site_name):
    """
    create a new django project
    """
    # put dir including django-admin.py to env
    os.putenv("Path",django_admin_dir)
    # execute django-admin.py script
    os.system( "django-admin.py startproject {0}".format(web_site_name) )


# run
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sitename", help="your site folder name")
    args = parser.parse_args()

    if args.sitename:
        CreateProject(DIR_BIN,  args.sitename)
        print("finish job!")
    else:
        print("you must provide a site name")
