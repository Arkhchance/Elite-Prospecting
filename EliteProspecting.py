#!/usr/bin/python
import tailhead
import time
import glob
import os
import json

#log path
path = "/home/arkhchance/gamessd/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/"

#refresh rate in seconds
polling = 0.1

#comodity
lookFor = "LowTemperatureDiamond"

#threshold
threshold = 1

def taifFile(logfile):
    for line in tailhead.follow_path(logfile):
        if line is not None:
            data = json.loads(line)
            if data['event'] == "ProspectedAsteroid" :
                for i in data['Materials']:
                    if i['Name'] == lookFor and i['Proportion'] > threshold :
                        print("Found " + i['Name_Localised'] + " => " + str(i['Proportion']) + " %")
        else:
            time.sleep(polling)

def main():
    fileList = glob.glob(path + "*.log")
    latestFile = max(fileList,key=os.path.getctime)
    print(latestFile)
    taifFile(latestFile)


if __name__ == "__main__":
    main()
