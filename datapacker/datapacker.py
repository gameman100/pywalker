#!/bin/usr/env python3   
import sys
import shutil, io, os, glob, subprocess
import csv
import types
import xlrd # must install xlrd!

TYPE_INT32='int32'
TYPE_FLOAT='float'
TYPE_Bool='bool'
TYPE_STRING='string'


def CsvToTxt( csvpath, outputpath ):
    """
    DESC: convert .csv(ascii format) files to .txt(utf-8 format) files
    """
    #stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
    #reload(sys)
    #sys.stdin, sys.stdout, sys.stderr = stdin, stdout, stderr
    #sys.setdefaultencoding("utf-8")
    curpath = os.getcwd()
    print('curdir:' + os.getcwd())

    inputpath = curpath + csvpath
    print('inputidr:' + os.getcwd())
    
    os.chdir( inputpath )
    
    csvfiles = glob.glob('*.csv')
    print ( 'found ({0}) csv files'.format( len(csvfiles) ) )
    print('')
    
    for f in csvfiles:
        print ( 'process: {0}'.format(f) )
        with open(f, 'r' ) as openfile:
            content = openfile.read()
            #content = content.decode("cp936")
            #content = content.encode("UTF-8")
            txtname = f.partition('.')
            txtname = txtname[0] + '.txt'
            with open (txtname, 'w', encoding = 'utf-8') as outputfile:
                outputfile.write(content)
    
    txtfiles = glob.glob('*.txt')
    for f in txtfiles:
         target = '{0}{1}'.format( curpath + outputpath, f )
         shutil.copy( f, target )
         print('copy {0} to {1}'.format(f, target))

    os.chdir(curpath)


def ExcelToDotNet( inpu_path, namespace, gameinfoclass ):
    """
    DESC: Export .Net class files from excel sheet
    eg: ExcelToDotNet("", "Game", "GameInfo")
    @inpu_path: excel path
    @namespace: class namespace
    @gameinfoclass: gameinfo class name
    """
    current_path = os.getcwd()
    
    # change dir to current dir
    os.chdir(current_path + inpu_path)

    # get all excel file names
    excel_files = glob.glob('*.xlsx')

    # create empty list for gameinfo properties
    gameinfo_property = []

    # create empty list for .net file names
    dotnet_files = []

    # check each excel
    for excel in excel_files:
        if excel.startswith("~"):
            continue
        book = xlrd.open_workbook( excel )
        print ( "The number of worksheets is", book.nsheets )
        print ( "Worksheet name(s):", book.sheet_names() )
        if book.nsheets == 0:
            continue
        
        # check each excel sheet
        for sheetname in book.sheet_names():

            # get sheet name
            sheet = book.sheet_by_name(sheetname)

            # every sheet is a class and put it into gameinfo class
            gameinfo_property.append(sheetname)

            # output .cs file
            output_filename = sheetname + '.cs'

            # 
            dotnet_files.append(sheetname)

            with open( output_filename, 'w', encoding='utf-8' ) as targetf:
  
                targetf.write('using System.Collections;\n\n' )
                targetf.write('namespace {0}{1}\n\n'.format(namespace,"{") )
                targetf.write('    public class {0}{1} \n'.format(sheetname,"{") )
                # write class name
                for r in range(0,sheet.nrows):
                    for c in range(0,sheet.ncols):
                        #print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                        data = sheet.cell_value(rowx=r, colx=c)
                        parts = data.partition('.')
                        data_type = parts[0]
                        data_real = parts[2]
                        #if c == sheet.ncols-1:
                        #    sep='\n'
                        targetf.write('        public {0} {1};\n'.format(data_type, data_real) )
                    break
                targetf.write('    }\n}')
                
    # create game info below
    gameinfo_output_path =  gameinfoclass + '.cs'
    print ( 'oupput game info:' + gameinfo_output_path )
    with open( gameinfo_output_path, 'w', encoding='utf-8' ) as targetf:
        targetf.write('using System.Collections;\n\n' )
        targetf.write('using System.Collections.Generic;\n\n' )
        targetf.write('namespace {0}{1}\n\n'.format(namespace,"{") )
        targetf.write('    public class {0}{1} \n'.format(gameinfoclass,"{") )
        
        for datatype in gameinfo_property:
            print ( datatype )
            dataname = datatype.lower()
            targetf.write('        public List<{0}> {1};\n'.format(datatype, dataname) )
            
        targetf.write('    }\n}')

    os.chdir(current_path)



def ExcelTOJSON( excel_path, output_path, output_filename, classname ):
    """
    DESC: export to json format file
    eg: ExcelTOJSON("\\", "\\", 'test.bin', 'GameInfo')
    """
    curpath = os.getcwd()
    print('curdir:' + os.getcwd())

    inputpath = curpath + excel_path
    os.chdir( inputpath )
    excel_files = glob.glob('*.xlsx')
    
    jsondata = "{"
    for excel in excel_files:
        if '~' in excel:
            continue
        book = xlrd.open_workbook(inputpath  + excel)
        print ("The number of worksheets is", book.nsheets)
        print ("Worksheet name(s):", book.sheet_names())
        
        # for in excel sheet
        listlenght = len(book.sheet_names())
        listindex = 0
        for sheetname in book.sheet_names():
            listindex+=1
            print('==sheet name:{0}=='.format(sheetname))
            
            msgname = sheetname.lower()

            sheet = book.sheet_by_name(sheetname)  # get sheet content
            row = 0
            fileds = []
            
            jsondata+="\"{0}\":{1}".format( msgname,"[")
            for r in range(0, sheet.nrows):
                #exec('property = gameinfo.{0}.add()'.format(msgname))
                row += 1
                index = 0  # col index
                if row > 1:
                    jsondata+="{"

                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                   
                    if row == 1:
                        parts = data.partition('.')
                        # field_type = parts[0] # field type
                        field_real = parts[2]  # filed name
                        # fileds[index]=field_real
                        fileds.append(data)
                        # print('field name:{0}'.format(field_real),)
                        #sys.stdout.write('{0},'.format(field_real))
                    else:
                        # if type(data) is types.StringType:  
                        #    data = data.encode('utf-8')
                        # print('{0}:{1}'.format(fileds[index],data) )
                        fieldname = fileds[index]
                        parts = fieldname.partition('.')
                        fieldtype = parts[0]
                        fieldname = parts[2]
                        if fieldtype == 'int':
                            data = int(data)
                        elif fieldtype == 'float':
                            data = float(data)
                        elif fieldtype == 'double':
                            data = float(data)
                        elif fieldtype == 'string':
                            data = str(data)

                        #sys.stdout.write('{0},'.format(data))
                        
                        if fieldtype =='string':
                            jsondata+="\"{0}\":\"{1}\"".format(fieldname, data)
                        else:
                            jsondata+="\"{0}\":{1}".format(fieldname, data)
                        if index < sheet.ncols-1:
                            jsondata+=","

                    index += 1
                if row > 1:
                    jsondata+="}"
                    if row < sheet.nrows:
                        jsondata+=","
            jsondata+="]"
            if listindex<listlenght:
                jsondata+=','
        
        jsondata+="}"  
        os.chdir(curpath)
        print("json:" + jsondata)
        # io output
        output = curpath + output_path;
        with open(output + output_filename, 'w', encoding = 'utf-8') as targetf:
            targetf.write(jsondata)
        print("\noutput:{0}".format(output + output_filename))


"""
Export excel data to protobuf file
eg:ExcelToProtobuf("", "gameinfo", "GameInfo" )
@inpu_path: excel path
@packagename: package name
@gameinfoname: gameinfo file name
"""
def ExcelToProtobuf( inpu_path, packagename, gameinfoname ):

    current_path = os.getcwd()
    
    # change dir to current dir
    os.chdir(current_path + inpu_path)

    # get all excel file names
    excel_files = glob.glob('*.xlsx')

    # create empty list for gameinfo properties
    gameinfo_property = []

    # create empty list for protobuf file names
    proto_files = []

    # check each excel
    for excel in excel_files:
        if excel.startswith("~"):
            continue
        book = xlrd.open_workbook(  excel )
        print ("The number of worksheets is", book.nsheets )
        print ("Worksheet name(s):", book.sheet_names())
        
        # check each excel sheet
        for sheetname in book.sheet_names():

            # get sheet name
            sheet = book.sheet_by_name(sheetname)

            # every sheet is a class and put it into gameinfo class
            gameinfo_property.append(sheetname)

            # output .proto file
            output_filename = sheetname + '.proto'

            # 
            proto_files.append(sheetname)

            index =0
            with open( output_filename, 'w', encoding='utf-8' ) as targetf:
            #with open( output_filename, 'w') as targetf:
                # write package gename
                targetf.write('package {0};\n\n'.format(packagename) )
                targetf.write('message {0}{1} \n'.format(sheetname,'{') )
                # write class name
                for r in range(0,sheet.nrows):
                    for c in range(0,sheet.ncols):
                        #print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                        data = sheet.cell_value(rowx=r, colx=c)
                        parts = data.partition('.')
                        data_type = parts[0]
                        data_real = parts[2]
                        index+=1
                        #if c == sheet.ncols-1:
                        #    sep='\n'
                        targetf.write('    optional {0} {1}={2};\n'.format(data_type,data_real,index) )
                    break
                targetf.write('}')
                
    # create game info below
    gameinfo_output_path =  gameinfoname + '.proto'
    print ( 'oupput game info:' + gameinfo_output_path )
    with open( gameinfo_output_path, 'w', encoding='utf-8' ) as targetf:
    #with open( gameinfo_output_path, 'w' ) as targetf:
        targetf.write('package {0};\n\n'.format(packagename) )
        
        for dataname in gameinfo_property:
            targetf.write('import \"{0}.proto\";\n'.format(dataname) )
        
        targetf.write('\n')
        targetf.write('message {0}{1} \n'.format(gameinfoname,'{') )
        
        index =0
        for datatype in gameinfo_property:
            print ( datatype )
            index+=1
            dataname = datatype.lower()
            targetf.write('    repeated {0} {1}={2};\n'.format(datatype, dataname, index) )
        targetf.write('}')

    os.chdir(current_path)


"""
Compile .proto files to python files
@ input_path: path contains .proto files
@ output_path: path export .py files
@ packagename: py package name
@ protocpath protoc.exe path
"""
def ProtobufToPy(input_path, output_path, packagename, protocpath):
    # from .proto file to generate python file
    # protoc path
    current_path = os.getcwd()
    os.chdir(current_path)
    print("ProtobufToPy == >current dir: "+ current_path )
    
    PROTOC_PATH = current_path + protocpath
    os.putenv('Path', PROTOC_PATH)

    os.chdir(current_path + input_path)
    proto_files = glob.glob( '*.proto' )
    for protofile in proto_files:
        # remove .proto
        fullpath = protofile.partition('.proto')
        protoname = fullpath[0]
        
        cmd = 'protoc -I=\"{0}\" --python_out=\"{1}\" {2}{3}.proto'.format( current_path + input_path, current_path + input_path, current_path + input_path, protoname)
        print ( cmd )
        #os.system( cmd )
        subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True )
        
        pyfile = protoname + '_pb2.py'
        shutil.move( current_path + input_path + pyfile, '{0}{1}'.format( current_path + output_path , pyfile ))
        
    os.chdir(current_path)


"""
make gameinfo.bin
eg: MakeGameinfo("/../protobuf/Projects/TowerDefense/gameinfo/", "/testdir/", "gameinfo.txt", "GameInfo")
"""
"""
def MakeGameinfo( excel_path, output_path, output_filename, classname ):
    #stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
    #reload(sys)
    #sys.stdin, sys.stdout, sys.stderr = stdin, stdout, stderr
    #sys.setdefaultencoding("utf-8")
    #print("???ии????????")
    exec('import {0}_pb2'.format(classname))

    curpath = os.getcwd()
    print('curdir:' + os.getcwd())

    inputpath = curpath + excel_path
    os.chdir( inputpath )
    excel_files = glob.glob('*.xlsx')
    
    #gameinfo = GameInfo_pb2.GameInfo()
    exec('gameinfo = {0}_pb2.{1}()'.format(classname, classname))
    
    for excel in excel_files:
        if '~' in excel:
            continue
        book = xlrd.open_workbook(inputpath + excel)
        print ("The number of worksheets is", book.nsheets)
        print ("Worksheet name(s):", book.sheet_names())
        
        # for in excel sheet
        for sheetname in book.sheet_names():
            print('==message name:{0}=='.format(sheetname))
            
            msgname = sheetname.lower()
            has = hasattr(gameinfo, msgname)
            if has:
                print('gameinfo has {0}:{1}'.format(msgname, has))
            else:
                print('[ERROR]gameinfo has {0}:{1}'.format(msgname, has))
                exit()
                
            # property = gameinfo.skill.add()
            #exec('property = gameinfo.{0}.add()'.format(msgname))
            
            sheet = book.sheet_by_name(sheetname)  # get sheet content
            row = 0
            fileds = []
            
            for r in range(0, sheet.nrows):
                exec('property = gameinfo.{0}.add()'.format(msgname))
                row += 1
                index = 0  # col index
                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                   
                    if row == 1:
                        parts = data.partition('.')
                        # field_type = parts[0] # field type
                        field_real = parts[2]  # filed name
                        # fileds[index]=field_real
                        fileds.append(data)
                        # print('field name:{0}'.format(field_real),)
                        sys.stdout.write('{0},'.format(field_real))
                    else:
                        # if type(data) is types.StringType:  
                        #    data = data.encode('utf-8')
                        # print('{0}:{1}'.format(fileds[index],data) )
                        fieldname = fileds[index]
                        parts = fieldname.partition('.')
                        fieldtype = parts[0]
                        fieldname = parts[2]
                        if fieldtype == 'int32':
                            data = int(data)
                        elif fieldtype == 'float':
                            data = float(data)
                        elif fieldtype == 'string':
                            data = unicode(str(data))
                            
                        
                        sys.stdout.write('{0},'.format(data))
                        setattr(property, fieldname, data)  # set data
                    if index == sheet.ncols - 1:
                        print('')
                    index += 1

        os.chdir(curpath)

        # io output
        output = curpath + output_path;
        with open(output + output_filename, 'wb', encoding = 'utf-8') as targetf:
            targetf.write(gameinfo.SerializeToString())
        print("\noutput:{0}".format(output + output_filename))

        # copy one to unity, and copy another to server
        #shutil.copy(output_filename, output + output_filename)
        #print( 'copy {0} to {1}'.format(output_filename, output + output_filename) )
"""

"""
Make Version file
"""
"""
def makeversion( versionpath, filename ):
    os.chdir(versionpath)
    
    v = Version_pb2.Version()
    
    # read current version
    if os.path.exists(versionpath + filename):
        with open (filename, 'r') as targetf:
            content = targetf.read()
            v.ParseFromString(content)
            v.gameinfo+=1
            print ( v.gameinfo )
    else:
        v.gameinfo=1
        
    with open (filename, 'w') as targetf:
        targetf.write(v.SerializeToString())
    print ('current version {0}'.format(v.gameinfo))
    return
        
"""
