import os
import glob
import json
import xlrd  # must install xlrd!


class Excel2Data(object):
    """
    export data from excels
    """
    # define types
    TYPE_INT32 = 'int32'
    TYPE_INT64 = 'int64'
    TYPE_FLOAT = 'float'
    TYPE_DOUBLE = 'double'
    TYPE_Bool = 'bool'
    TYPE_STRING = 'string'

    def __init__(self, filename, input_path='./', output_path='dist/'):
        """
        :param filename: output filename
        :param input_path: relative path
        :param output_path: relative path, default 'dist'
        """
        self.filename = filename
        self.input_path = input_path
        self.output_path = output_path
        self.excel_sheets = []
        self.class_files = []



    def make_json(self):
        """
        export json format file from excel sheet
        :return: None
        """

        curpath = os.path.abspath(os.getcwd())
        print('curdir:', curpath)

        inputpath = os.path.normpath(os.path.join(curpath, self.input_path))
        os.chdir(inputpath)
        excel_files = glob.glob('*.xlsx')

        jsondata = "{"
        for excel in excel_files:
            if '~' in excel:
                continue
            book = xlrd.open_workbook(inputpath+excel)
            print("The number of worksheets is", book.nsheets)
            print("Worksheet name(s):", book.sheet_names())

            # for in excel sheet
            listlenght = len(book.sheet_names())
            listindex = 0
            for sheetname in book.sheet_names():
                listindex += 1
                print('==sheet name:{0}=='.format(sheetname))

                msgname = sheetname.lower()

                sheet = book.sheet_by_name(sheetname)  # get sheet content
                row = 0
                fileds = []

                jsondata += "\"{0}\":{1}".format(msgname, "[")
                for r in range(0, sheet.nrows):
                    row += 1
                    index = 0  # col index
                    if row > 1:
                        jsondata += "{"

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
                            # sys.stdout.write('{0},'.format(field_real))
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

                            # sys.stdout.write('{0},'.format(data))

                            if fieldtype == 'string':
                                jsondata += "\"{0}\":\"{1}\"".format(fieldname, data)
                            else:
                                jsondata += "\"{0}\":{1}".format(fieldname, data)
                            if index < sheet.ncols-1:
                                jsondata += ","

                        index += 1
                    if row > 1:
                        jsondata += "}"
                        if row < sheet.nrows:
                            jsondata += ","
                jsondata += "]"
                if listindex < listlenght:
                    jsondata += ','

            jsondata += "}"
            os.chdir(curpath)
            print("json:" + jsondata)
            # io output
            output = os.path.normpath(os.path.join(curpath, self.output_path))
            output = output+self.filename+'.bin'
            with open(output, 'w', encoding='utf-8') as targetf:
                jsondata = json.dump(jsondata)
                targetf.write(jsondata)
            print("\noutput:{0}".format(output))

        os.chdir(curpath)
