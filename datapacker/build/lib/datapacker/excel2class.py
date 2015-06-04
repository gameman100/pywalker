import os
import glob
import xlrd  # must install xlrd!


class Excel2Class(object):
    """
    export classes from excels
    """
    # define types
    TYPE_INT32 = 'int32'
    TYPE_INT64 = 'int64'
    TYPE_FLOAT = 'float'
    TYPE_DOUBLE = 'double'
    TYPE_Bool = 'bool'
    TYPE_STRING = 'string'

    # List
    TYPE_IARRAY = 'array'  # List<int>
    TYPE_FARRAY = 'farray'  # List<float>
    TYPE_DARRAY = 'darray'  # List<double>
    TYPE_SARRAY = 'sarray'  # List<string>

    # Dictionary, the key must be a int
    TYPE_IDIC = 'dic'  # Dictionary<int,int>
    TYPE_FDIC = 'fdic'  # Dictionary<int,float>
    TYPE_DDIC = 'ddic'  # Dictionary<int,double>
    TYPE_SDIC = 'sdic'  # Dictionary<int,string>

    # support languages
    LANG_CS = 'cs'  # c sharp
    LANG_PY = 'py'  # python

    def __init__(self, input_path='./', output_path='dist/'):
        """
        :param input_path: relative path
        :param output_path: relative path, default 'dist'
        """
        self.input_path = input_path
        self.output_path = output_path
        self.excel_sheets = []
        self.class_files = []
        self.namespace = ''
        self.gameinfoclass = 'GameInfo'
        self.lang = Excel2Class.LANG_CS


    def make(self, namespace='', gameinfoclass='GameInfo', lang=LANG_CS):
        """
        export class files from excel sheet
        :param namespace: class namespace
        :param gameinfoclass: gameinfo class name
        :param lang: support language
        :return: None
        """
        self.namespace = namespace
        self.gameinfoclass = gameinfoclass
        self.lang = lang

        current_path = os.path.abspath(os.getcwd())
        os.chdir(current_path + self.input_path)
        excel_files = glob.glob('*.xlsx')

        # all output files saved int a folder called 'dist'
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        # init array
        self.excel_sheets = []
        self.class_files = []

        # check each excel
        for excel in excel_files:
            if excel.startswith("~"):
                continue
            book = xlrd.open_workbook(excel)
            print("The number of worksheet is", book.nsheets)
            print("Worksheet name(s):", book.sheet_names())
            if book.nsheets == 0:
                continue
        
            # check each excel sheet
            for sheetname in book.sheet_names():
                sheet = book.sheet_by_name(sheetname)
                self.excel_sheets.append(sheetname)
                self.class_files.append(sheetname)

                # write c shart class files
                if lang == Excel2Class.LANG_CS:
                    self.write_cs(sheet, sheetname)
                elif lang == Excel2Class.LANG_PY:
                    pass
        if lang == Excel2Class.LANG_CS:
            self.write_cs_gameinfo()
        elif lang == Excel2Class.LANG_PY:
            pass
        # done!           
        os.chdir(current_path)


    def write_cs(self, sheet: xlrd.sheet.Sheet, sheetname):
        """
        """
        output_filename = os.path.normpath('{0}/{1}.cs'.format(self.output_path, sheetname))

        with open(output_filename, 'w', encoding='utf-8') as targetf:
            targetf.write('using System.Collections;\n')
            targetf.write('using System.Collections.Generic;\n\n')
            if len(self.namespace) > 0:
                targetf.write('namespace {0}{1}\n\n'.format(self.namespace, "{"))
            targetf.write('    public class {0}{1} \n'.format(sheetname, "{"))
                   
            for r in range(0, sheet.nrows):   # write class name
                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                    parts = data.partition('.')
                    data_type = parts[0]
                    data_real = parts[2]
                    # if c == sheet.ncols-1:
                    #    sep='\n'
                    if data_type == Excel2Class.TYPE_IARRAY:
                        data_type = 'List<int>'
                    if data_type == Excel2Class.TYPE_FARRAY:
                        data_type = 'List<float>'
                    if data_type == Excel2Class.TYPE_DARRAY:
                        data_type = 'List<double>'
                    if data_type == Excel2Class.TYPE_SARRAY:
                        data_type = 'List<string>'
                    elif data_type == Excel2Class.TYPE_IDIC:
                        data_type = 'Dictionary<int,int>'
                    elif data_type == Excel2Class.TYPE_FDIC:
                        data_type = 'Dictionary<int,float>'
                    elif data_type == Excel2Class.TYPE_DDIC:
                        data_type = 'Dictionary<int,double>'
                    elif data_type == Excel2Class.TYPE_SDIC:
                        data_type = 'Dictionary<int,string>'
                    targetf.write('        public {0} {1};\n'.format(data_type, data_real))
                break
            if len(self.namespace) > 0:
                targetf.write('    }')
            targetf.write('\n}')


    def write_cs_gameinfo(self):
        # wirte game info
        gameinfo_output_path = os.path.normpath('{0}/{1}.cs'.format(self.output_path, self.gameinfoclass))
        print('output game info:', gameinfo_output_path)
        with open(gameinfo_output_path, 'w', encoding='utf-8') as targetf:
            targetf.write('using System.Collections;\n\n')
            targetf.write('using System.Collections.Generic;\n\n')
            if len(self.namespace) > 0:
                targetf.write('namespace {0}{1}\n\n'.format(self.namespace, "{"))
            targetf.write('    public class {0}{1} \n'.format(self.gameinfoclass, "{"))
        
            # write fields
            for datatype in self.excel_sheets:
                dataname = datatype.lower()
                targetf.write('        public List<{0}> {1};\n'.format(datatype, dataname))

            if len(self.namespace) > 0:
                targetf.write('    }')
            targetf.write('\n}')
