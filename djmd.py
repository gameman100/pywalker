#!/bin/usr/env python3
__author__ = 'jinxizeng'

import os
import sys
import argparse
import mysql.connector
from mysql.connector import FieldType

# default database config
USER = 'root'
PASSWORD = '123456'
DB_NAME = 'demodb'
HOST = '127.0.0.1'
PORT = 3306
DIST_PATH = ''

# Language config
PY = 'python'  # django model
CS = 'csharp'
CPP = 'cplus'
Java = 'java'
JS = 'js'
PHP = 'php'

USE_LANG = PY  # use which language


class ModelBuilder(object):

    def __init__(self, lang=PY):
        self.lang = lang
        self.output = []
        pass

    def build(self, username, password, host_addr, dbname):

        try:
            cnx = mysql.connector.connect(user=username, password=password, host=host_addr, database=dbname)
        except:
            print("can not connect database, exit!")
            exit()

        cursor = cnx.cursor();

        cursor.execute("show tables")
        print("query...")

        tables = []  # list store table names

        row = cursor.fetchone()
        while row is not None:
            tablename = row[0]
            if not tablename.startswith('auth_') and not tablename.startswith('django_'):
                #print("get table ", row[0])
                tables.append(tablename)
            else:
                print("pass table ", tablename)
            row = cursor.fetchone()

        print("\ntotal {0} app tables:".format(len(tables)))

        self.parse_head()

        for table in tables:

            self.parse_class_head(table)

            query = "describe {0}".format(table)
            print(query)
            cursor.execute(query)  # get field name and type

            row = cursor.fetchone()

            while row is not None:
                fieldname = row[0]
                fieldtype = row[1]
                notnull = row[2]
                pri = row[3]

                self.parse_body(fieldname, fieldtype, pri)
                row = cursor.fetchone()

            self.parse_foot()

        cursor.close()
        cnx.close()

        print("=====================")
        for p in self.output:
            print(p)


    def parse_head(self):
        if self.lang == PY:
            self.output.append("from django.db import models")
            self.output.append('')
        elif self.lang == CS:
            self.output.append("using System.Collections;")
            self.output.append("using System.Collections.Generic;")
            self.output.append('')
        else:
            self.output.append("unsupported language {0}!".format(self.lang))


    def parse_class_head(self, tablename):
        tablename = tablename.partition('_')
        tablename = tablename[2]
        clsname = []
        for s in tablename:
            if len(clsname)==0:
                s=s.upper()
            clsname.append(s)

        clsname = ''.join(clsname)
        if self.lang == PY:
            p = "class {0}(model.Models):".format(clsname)
            self.output.append(p)
        elif self.lang == CS:
            p = "public class {0}{".format(clsname)
            self.output.append(p)


    def parse_body(self, fieldname, fieldtype, pri):

        if self.lang == PY:
            if pri == "PRI" and fieldname == "id":
                return
            elif pri =='MUL':
                clsname = []
                for s in fieldname:
                    if len(clsname)==0:
                        s=s.upper()
                    clsname.append(s)
                clsname = ''.join(clsname)
                fieldtype="ForeignKey('{0}')".format(clsname)
            elif 'int' in fieldtype:
                fieldtype = 'IntegerField()'
            elif 'datetime' in fieldtype:
                fieldtype = "DateTimeField('{0}')".format(fieldname)

            p = "    {0}=models.{1}".format(fieldname, fieldtype)
            self.output.append(p)
        elif self.lang == CS:
            default_value = ''
            p = "   public {0} {1}={2})".format(fieldtype, fieldname, default_value)
            self.output.append("using System.Collections;")


    def parse_foot(self):
        if self.lang == PY:
            self.output.append('')
            self.output.append('')
            return ""
        elif self.lang == CS:
            self.output.append("}")
            self.output.append('')



if __name__=='__main__':
    # run code...
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", help="choose a language")
    parser.add_argument("--password", help="database password")
    args= parser.parse_args()

    if args.lang:
        USE_LANG = args.lang
    if args.lang:
        PASSWORD = args.password

    mb = ModelBuilder(USE_LANG)
    mb.build(USER, PASSWORD, HOST, DB_NAME)

