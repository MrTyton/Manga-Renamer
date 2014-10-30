import zipfile
import os
import shutil
from os import listdir
from os.path import isfile, join

def fixBadZipfile(zipFile):  
 f = open(zipFile, 'r+b')  
 data = f.read()  
 pos = data.find('\x50\x4b\x05\x06') # End of central directory signature  
 if (pos > 0):   
     f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
     f.truncate()  
     f.close()  
 else:  
     print "wtf"# raise error, file is truncated 

while (True):
    folder = raw_input("Directory please: ")
    if folder == "": break
    for filename in [ f for f in listdir(folder) if isfile(join(folder,f)) ]:
        if ".zip" not in filename: continue
        print "Working on %s" % (filename)
        filename = folder + "/" + filename
        fixBadZipfile(filename)
        
        try:
            file = zipfile.ZipFile(filename, "r")
        except:
            fixBadZipfile(filename)
            file = zipfile.ZipFile(filename, "r")
        names = file.namelist()
        
        total = 0
        
        if not os.path.exists("./extraction"):
            os.makedirs("./extraction")
        else:
            shutil.rmtree("./extraction")
            os.makedirs("./extraction")
        if not os.path.exists("./renaming"):
            os.makedirs("./renaming")
        else:
            shutil.rmtree("./renaming")
            os.makedirs("./renaming")
            
        
        for i,(info, name) in enumerate(zip(file.infolist(), names)):
            if (".jpg" in name or ".gif" in name or ".png" in name) and (".txt" not in name and "recruit" not in name and "credit" not in name):
                #print i, name
                file.extract(info, "./extraction/")
                os.rename("./extraction/%s" % (name), "./renaming/%04d.png" % (total))
                total += 1
        
        shutil.rmtree("./extraction")
        
        file.close()
        
        os.remove(filename)
        
        newfile = zipfile.ZipFile(filename, "w")
        
        for x in range(total):
            os.rename("./renaming/%04d.png" % (x), "./%04d.png" % (x))
            newfile.write("./%04d.png" % (x))
            os.remove("./%04d.png" % (x))
            
        newfile.close()
        
        shutil.rmtree("./renaming")