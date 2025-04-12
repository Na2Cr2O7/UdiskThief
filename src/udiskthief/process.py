import psutil
import shutil
import os
from configparser import ConfigParser
from time import sleep,asctime
import hashlib

DEST=r"D:\I"
uncopied=['*.iso']
doProcessFiles=True

def setConfig(dest=r"D:\I",Uncopied=['*.iso','*.asf'],processfiles=True):
    '''
    Sets the configuration for the program.
    @param dest: The destination folder for the copied files.
    @param Uncopied: A list of file extensions that should not be copied.
    @param processfiles: A boolean value indicating whether to process the copied files or not.
    @return: None
    '''
    global DEST,uncopied,doProcessFiles
    DEST=dest
    uncopied=Uncopied
    doProcessFiles=processfiles

    config=ConfigParser()
    config['DEFAULT']={'destination':DEST,'uncopied':','.join(uncopied),'processfiles':str(doProcessFiles)}
    with open('config.ini','w') as configfile:
        config.write(configfile)



def getConfig():
    global DEST,uncopied,doProcessFiles
    config=ConfigParser()
    config.read('config.ini')
    DEST=config['DEFAULT']['destination']
    uncopied=config['DEFAULT']['uncopied'].split(',')
    doProcessFiles=config.getboolean('DEFAULT','processfiles')


getConfig()


def getAllFiles(pth):
    allFiles=[]
    for root,dirs,files in os.walk(pth):
        for file in files:
            allFiles.append(os.path.join(root,file))
    return allFiles

            
def getHash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def timeStamp():
    return asctime().replace(':','').replace(' ','')


def fileProcessor():
    folders=os.listdir(DEST)
    for folder in folders:
        destination=os.path.join(DEST,folder)
        if os.path.isdir(destination):
            print(getAllFiles(destination))
            for file in getAllFiles(destination):
                print(file)
                if os.path.isfile(file):
                    try:
                        shutil.move(file,DEST)
                    except:
                        newFile=os.path.splitext(file)[0]+'_'+timeStamp()+os.path.splitext(file)[1]
                        print(newFile)
                        os.rename(file,newFile)
                        try:
                            shutil.move(newFile,DEST)
                        except Exception as e:
                            print(e)
                            pass

def removeFiles(destination):
    try:
        for ext in uncopied:
            for file in os.listdir(destination):

                if os.path.splitext(file)[1]==ext.replace('*',''):
                    print('×',os.path.join(destination,file))
                    os.remove(os.path.join(destination,file))
    except:
        pass

def processUdisk():
    getConfig()
    disks=psutil.disk_partitions()
    while True:
        sleep(1)
        newDisks=psutil.disk_partitions()
        for disk in newDisks:
            if disk in disks:
                continue
            pth=disk.mountpoint
            pth=getHash(''.join(os.listdir(pth)))
            if os.path.exists(pth):
                os.rename(pth,pth+timeStamp())
            try:
                destination=os.path.join(DEST,pth)
                shutil.copytree(disk.mountpoint,destination)

                    
        
            except:
                pass
            
            if doProcessFiles:
                fileProcessor()
            removeFiles(getAllFiles(DEST))
        disks=newDisks
if __name__=='__main__':
    processUdisk()