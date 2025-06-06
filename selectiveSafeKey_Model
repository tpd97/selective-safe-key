import maya.cmds as cmds
import maya.mel as mel
import json
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial 
import sys
import os
import importlib

################## GET TOOLS ####################

def loadConfig():

    config_path = os.path.expanduser("~/Documents/maya/scripts/tdTools_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
    
        tdToolsPath = config.get("tdToolsPath")
        print(tdToolsPath)
        if tdToolsPath and tdToolsPath not in sys.path:
            sys.path.insert(0, tdToolsPath)
            
        return tdToolsPath

    else:
        print("Config not found.")
        return none

tdToolsPath = loadConfig()

################## LINK PYQT UI ####################

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)
    
class selectiveSafeKey(QtWidgets.QWidget):

    window = None
    
    def __init__(self, parent = None):   
    
        #BuildUI
        super(selectiveSafeKey, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = os.path.join(tdToolsPath, "selectiveSafeKey", "selectiveSafeKeyUI.ui")
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath)
        self.widget.setParent(self)

        self.resize(190, 200)    
          
        #connect ui widgets
        self.safeKeyBtn = self.widget.findChild(QtWidgets.QPushButton, 'safeKeyBtn')        
        self.addBtn = self.widget.findChild(QtWidgets.QPushButton, 'addBtn')  
        self.clearSlBtn = self.widget.findChild(QtWidgets.QPushButton, 'clearSlBtn')  
        self.clearAllBtn = self.widget.findChild(QtWidgets.QPushButton, 'clearAllBtn')
        self.lockList = self.widget.findChild(QtWidgets.QListView, 'lockList') 
        
        #lock list that will store data for objects animators dont want to key
        self.keyLockList = []  

        # Create and assign model
        self.lockListModel = QtCore.QStringListModel()
        self.lockList.setModel(self.lockListModel)

        self.safeKeyBtn.clicked.connect(self.runSelectiveSafeKey)
        self.addBtn.clicked.connect(self.runAddToList)
        self.clearSlBtn.clicked.connect(self.clearSelected)
        self.clearAllBtn.clicked.connect(self.clearList)
      
################## FUNCTIONS ####################
        
    def runSelectiveSafeKey(self):
        
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("no objects selected.")
            return

        for obj in selection:
            short_name = obj.split("|")[-1]
            if short_name in self.keyLockList:
                result = cmds.confirmDialog(
                    title="Key Warning",
                    message=f"{short_name} is in the key lock list.\nKey it anyway?",
                    button=["Yes", "No"],
                    defaultButton="No",
                    cancelButton="No",
                    dismissString="No"
                )
                if result == "No":
                    cmds.warning(f"not keying {short_name}")
                    continue

            cmds.undoInfo(openChunk=True)  
            try:
                anim_curves = cmds.listConnections(obj, type="animCurve", destination=False) or []
                for curve in anim_curves:
                    cmds.setKeyframe(curve)
            finally:
                cmds.undoInfo(closeChunk=True) 

    def runAddToList(self):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("no objects selected to add.")
            return

        updated = False
        for obj in selection:
            short_name = obj.split("|")[-1]
            if short_name not in self.keyLockList:
                self.keyLockList.append(short_name)
                updated = True
                print(f"{short_name} added to {self.keyLockList}")

        if updated:
            self.lockListModel.setStringList(self.keyLockList)
    
    def clearList(self):
            if not self.keyLockList:
                print("list is empty")
                return
            self.keyLockList.clear()  
            self.lockListModel.setStringList(self.keyLockList) 
            print("list cleared.")

    def clearSelected(self):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("no objects selected to clear.")
            return
        updated = False
        for obj in selection:
            short_name = obj.split("|")[-1]
            if short_name in self.keyLockList:
                self.keyLockList.remove(short_name)
                updated = True
                print(f"{short_name} removed to key lock list")

        if updated:
            self.lockListModel.setStringList(self.keyLockList) 
        
    def resizeEvent(self, event):

        self.widget.resize(self.width(), self.height())
        
    def closeEvent(self, event):
        result = cmds.confirmDialog(
            title="Close Tool",
            message="Key lock list will be cleared on close. Continue?",
            button=["Yes", "Cancel"],
            defaultButton="Cancel",
            cancelButton="Cancel",
            dismissString="Cancel"
        )
        if result == "Yes":
            self.clearList()  
            event.accept()
        else:
            event.ignore()
            
def openWindow():

    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'selectiveSafeKey' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    selectiveSafeKey.window = selectiveSafeKey(parent = mayaMainWindow)
    selectiveSafeKey.window.setObjectName('selectiveSafeKey') # code above uses this to ID any existing windows
    selectiveSafeKey.window.setWindowTitle('selectiveSafeKey')
    selectiveSafeKey.window.show()
    
openWindow()
