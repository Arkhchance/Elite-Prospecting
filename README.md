# Elite-Prospecting
Elite-Prospecting is depreciated
use [EliteProspecting2](https://github.com/Arkhchance/EliteProspecting2)

Elite-Prospecting is an EDMC plugin design for miners and wing miners to help you prospecting.
It shows you (and your wing mates) the content of your prospector limpet only if above your threshold


Usage
--------
Once installed go to EDMC's settings, you should see a tab called EliteProspecting.
In order for Elite-Prospecting to work with your wing mates it needs to connect to a server.
You can use the one I provided by default or yours (you can use "server.py" in github).
You need to use the same server room in order to see each other prospector.

Elite-Prospecting can work from EDMC main window or it's own overlay.

About messages colors :
You can use a string specifying the proportion of red, green and blue in hexadecimal digits. For example, "#fff" is white, "#000000" is black, "#000fff000" is pure green, and "#00ffff" is pure cyan (green plus blue).
You can also use any locally defined standard color name. The colors "white", "black", "red", "green", "blue", "cyan", "yellow", and "magenta" will always be available.

Transparency only work on windows
(sorry fellow linux users) ¯\\\_(ツ)\_/¯


Installation
--------
Download the `.zip` file [here](https://github.com/Arkhchance/Elite-Prospecting/releases/latest)

Extract the content inside EDMC plugin's folder - (re)start EDMC

Elite-Prospecting can play sound but it require playsound library and it only works with beta version of [EDMC](https://github.com/Marginal/EDMarketConnector/releases/tag/rel-350-0)
```
pip install playsound
```

Idea by [CMDR Fank](https://inara.cz/cmdr/162442/)

Created by [CMDR Arkhchance](https://inara.cz/cmdr/10980/) and [CMDR Fank](https://inara.cz/cmdr/162442/)

under GPLv3
