import json
import sys
import os
import importlib
import traceback
import maya.cmds as cmds

for p in sys.path:
    print(p)

################## GET TDTOOLS ####################

def loadConfig():

    config_path = os.path.expanduser("~/Documents/maya/scripts/tdTools_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
    
        tdToolsPath = config.get("tdToolsPath")
        print(f"[tdTools] path:{tdToolsPath}")
        
        if tdToolsPath and tdToolsPath not in sys.path:
            sys.path.insert(0, tdToolsPath)
            print(f"tdTools path:{tdToolsPath}")
            
        return tdToolsPath

    else:
        print("Config not found.")
        return none

tdToolsPath = loadConfig()

if tdToolsPath:
    try:
        from selectiveSafeKey import selectiveSafeKey_UI as UI
        importlib.reload(UI)
        UI.openWindow()
    except Exception as e:
        import traceback
        traceback.print_exc()
        cmds.warning(f"[tdTools] failed to load selectiveSafeKey_UI: {e}")
else:
    cmds.warning("[tdTools] Could not load tdToolsPath. Aborting.")
    
