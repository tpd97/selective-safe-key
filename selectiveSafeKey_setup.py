#set path to safe key
import maya.cmds as cmds
import sys
import os
import json

def configure_tdTools(*args):
    
    def getMayaPath():
        return os.path.expanduser("~/Documents/maya/scripts")
    
    def getConfigPath():
        return os.path.join(getMayaPath(), "tdTools_config.json")

    def saveConfig(data):
        configPath = getConfigPath()
        with open(configPath, "w") as f:
            json.dump(data, f, indent=4)
            print(f"Saved tdTools config to: {configPath}")
    
    
    def setPath(*args):
        
        path = cmds.textField("pathField", query=True, text=True)
        
        if not path:
            cmds.warning("No path entered.")
            return    
        
        if path not in sys.path:            
            result = cmds.confirmDialog(
                    title="Path Confirm",
                    message=f"set path to: \n{path}?",
                    button=["Confirm", "Reset Path"],
                    defaultButton="Reset Path",
                    cancelButton="Reset Path",
                    dismissString="Reset Path"
                )
            if result == "Confirm":
                
                sys.path.append(path)
                saveConfig({"tdToolsPath": path})
                print(f"Path set to {path}")
                

            if result == "Reset Path":
                cmds.warning("re enter path.")
                return  
        else:
            cmds.warning("Path already in sys.path")
        
        if cmds.window("pathSetter", exists=True):
                cmds.deleteUI("pathSetter")

    ############### CREATE PATH SET UI #################

    #delete old ui if exists
    if cmds.window("pathSetter", exists=True):
        cmds.deleteUI("pathSetter")

    #build ui
    cmds.window("pathSetter", title="Path Setter", widthHeight=(300, 120))
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=10, style="in")

    cmds.text(label="Input Path to tdTools:")

    cmds.separator(height=10, style="in")

    cmds.textField("pathField", placeholderText="Example: E:/Dropbox/Shared - Thomas/tdTools")

    cmds.separator(height=10, style="in")

    cmds.button(label="Set Path", command=setPath)

    cmds.showWindow("pathSetter")

configure_tdTools()
