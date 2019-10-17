#!/usr/bin/python
import tailhead
import time
import glob
import os
import json
from king_chat import Client

#username
name = "Arkhchance"

#log path
path = "/home/arkhchance/gamessd/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/"

#refresh rate in seconds
polling = 0.1

#comodity
lookFor = "LowTemperatureDiamond"

#threshold
threshold = 18

#serveraddr
#ip = "127.0.0.1"

#port
#port = "44987"


def taifFile(logfile,client):
    for line in tailhead.follow_path(logfile):
        if line is not None:
            data = json.loads(line)
            if data['event'] == "ProspectedAsteroid" :
                for i in data['Materials']:
                    if i['Name'] == lookFor and i['Proportion'] > threshold :
                        print("Found " + i['Name_Localised'] + " => " + str(i['Proportion']) + " %")
                        client.send("test")
        else:
            time.sleep(polling)

def main():
    #setup file
    fileList = glob.glob(path + "*.log")
    latestFile = max(fileList,key=os.path.getctime)

    client = Client(name="Arkhchance", ip="arkhchance.ovh", port=44987)
    @client.on_received
    def on_received(protocol, text):
        print(text)

    client.start(wait=False)
    time.sleep(3)
    client.send("test")
    print(latestFile)
    taifFile(latestFile,client)


if __name__ == "__main__":
    main()
