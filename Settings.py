import json
import os


def readSettings():
    # open file
    try:
        with open("Setting_File.json", "r+") as file:
            Data = json.load(file)
            print(Data["Dir"])
    except FileNotFoundError:
        # create file with default settings if - > file not found
        file = open("Setting_File.json", "w+")
        json.dump(defaultData, file)
        file.close()
        Data = defaultData
        # reCall function
        readSettings()
    finally:
        return Data["Dir"]


def writeSettings(newDir):
    newSetting = {
        "Dir": newDir
    }
    with open("Setting_File.json", "w+") as file:
        json.dump(newSetting, file)


default = os.path.expanduser("~\\Desktop\\myKey.txt")
defaultData = {
    "Dir": str(default)
}
