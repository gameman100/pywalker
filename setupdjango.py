#! /usr/bin/env python3
__author__=jinxizeng

"""
DO NOT run this script on Windows!
"""

import sys
import os
# import argparse # todo: add argparse

"""
You must install python3.4 before run this script!

--------------------------------------
How to install python3.4?

sudo tar -xf Python-3.4.3.taz
cd Python-3.4.3
./configure --prefix=/usr/local --with-universal-archs=64-bit --with-shared --with-ctypes
make all
sudo make altinstall


# add .so path to search path 
cd /etc/ld.so.conf
add '/usr/local/lib' to the .conf file
run 'ldconfig' apply the changes

--------------------------------------
/How to load wsgi?
Modify Apache httpd.conf as below: ( may need to change the path )

# Add this line to load 
# LoadModule wsgi_module /usr/local/apache/modules/mod_wsgi.so
LoadModule wsgi_module modules/mod_wsgi.so

--------------------------------------
How to setup app path?
Modify Apache httpd.conf as below:

# Add these to the end of httpd.conf ( may need to change the path )

Alias /media/ /home/wwwroot/pvpadmin/pvpadmin/media/
Alias /static/ /home/wwwroot/pvpadmin/pvpadmin/static/


<Directory /home/wwwroot/pvpadmin/pvpadmin/static>
Require all granted
</Directory>

<Directory /home/wwwroot/pvpadmin/pvpadmin/media>
Require all granted
</Directory>

WSGIScriptAlias / /home/wwwroot/pvpadmin/pvpadmin/wsgi.py
WSGIPythonPath /home/wwwroot/pvpadmin/

<Directory /home/wwwroot/pvpadmin/pvpadmin >
<Files wsgi.py>
Require all granted 
</Files>
</Directory>


-----------------------------------------
Restart Apache ( may need to change path )

cd /usr/local/apache/bin/
./httpd -k restart

"""

# module source path
django = './Django-1.7.8'
mysql = './mysql-connector-python-2.0.4'
wsgi = './mod_wsgi-4.4.11'

# get current abspath
current_path = os.path.abspath(os.curdir)

# install Django
os.chdir(django)
print('starting install Django from', os.path.abspath(os.curdir))
os.system("python3.4 setup.py install")

# install mysql connector
os.chdir(current_path)
os.chdir(mysql)
print('starting install mysql connector from', os.path.abspath(os.curdir))
os.system("python3.4 setup.py install")

# install wsgi
os.chdir(current_path)
os.chdir(wsgi)
print('starting install mysql connector from', os.path.abspath(os.curdir))
os.system("./configure --with-python=/usr/local/bin/python3.4")
os.system("make all")
os.system("sudo make install")


print("==job done==")
