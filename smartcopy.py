import sys, shutil, io, re, os

class SmartCopy:

    def __init__( self ):
        print("create SmartCopy instance")

    # pure virtaul function, you may want to override it for the special case
    # check if the file is with special case
    def specialcase(self, file):
        return False

    # copy data: copy data from the input path to the output path with filter pattern
    # inputpath: input path, not ends with '/'
    # outputpath: output path, not ends with '/'
    # patterns: string(with lower case) list, format filter (the files with filter format will be not included)
    def copydata ( self, inputpath, outputpath, patterns ):

        # check if output path exist
        if not os.path.exists ( outputpath ):
            print("out put path is not exist!".format(outputpath))
            return

        # change current dir to input dir
        os.chdir(inputpath)

        # walk all path
        dirs = os.walk(inputpath)
        
        for top in dirs:
            print("copy...{0}".format(top[0]))
            for file in top[2]:
                path = top[0]
                
                inputfile = os.path.join( path, file )
                subpath = inputfile.replace( inputpath, "" )
                
                #outputfile = os.path.join(outputpath, subpath)
                outputfile = "{0}{1}".format( outputpath, subpath )
                print(outputfile)

                # check if output dir exist
                outputsubpath = outputfile.rpartition('\\')
                outputsubpath = outputsubpath[0]
                if len(outputsubpath)>0 and not os.path.exists( outputsubpath ):
                    print( "create new dir: {0}".format( outputsubpath ) )
                    dirs = outputsubpath.split('\\')
                    dr = ''
                    for d in dirs:
                        dr =dr+d +'\\'
                        if not os.path.exists(dr):
                            os.mkdir ( dr )
                  

                # check pattern
                ispass = False
                for pa in patterns:
                    lowerstr = pa.lower()
                    filename = file.lower()
                    if filename.endswith(lowerstr):
                        ispass = True
                        break

                if ispass:
                    continue

                # check special case
                if self.specialcase(outputfile):
                    continue
                
                # ok, we can copy the file now
                shutil.copy (inputfile, outputfile)

# example class
class MLAniamtionCopy(SmartCopy):
    def __init___(self, pattern ):
        print("create MLAniamtionCopy instance")
        
    # override
    def specialcase(self, file):
        filename = file.lower()
        if filename.endswith(".max"):
            nodot = file.rpartition(".")
            if len(nodot[0])>0:
                result = re.search("[0-9][0-9]$", nodot[0])

                if result:
                    return True
        return False


if __name__=='__main__':
    # donot copy psd files
    patterns = [".psd", ".exe", ".rar"]
    smart = MLAniamtionCopy()
    smart.copydata("D:/Card2/trunk/Art/rawdata/", "D:/output/", patterns )

