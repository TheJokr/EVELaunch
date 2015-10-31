#!/usr/bin/python
# vim: set fileencoding=utf-8 :

# EVELaunch.py: launches EVE Online without entering credentials
# Copyright (C) 2015  Leo Blöcher

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Usage: python launchEve.py <USERNAME> <PASSWORD> <CHAR NAME> [triPlatform]
# <CHAR NAME> is the name of one of the characters of the Account


import sys
import os
import subprocess
import re

import requests


# Command line arguments
try:
    user = sys.argv[1]
    pwd = sys.argv[2]
    char = sys.argv[3]
except IndexError:
    print("Missing information. "
          "Usage: python launchEve.py <USERNAME> <PASSWORD> "
          "<CHAR NAME> [triPlatform]")
    sys.exit(1)


# Get access token
s = requests.Session()
authURI = "https://login.eveonline.com/Account/LogOn"
payload = {'ReturnUrl': "/oauth/authorize/?client_id=eveLauncherTQ&"
                        "lang=en&response_type=token&"
                        "redirect_uri=https://login.eveonline.com/launcher?"
                        "client_id=eveLauncherTQ&"
                        "scope=eveClientToken"}
r = s.post(authURI, params=payload,
           data={"UserName": user, "Password": pwd},
           headers={"referer": authURI,
                    "Origin": "https://login.eveonline.com"},
           allow_redirects=True,
           timeout=5)

# Login challenge
if not r.history:
    challengeURI = "https://login.eveonline.com/Account/Challenge"
    r = s.post(challengeURI, params=payload, data={"Challenge": char})

# Extract access token
try:
    accToken = re.search("#access_token=([\w\d_-]+)", r.url).group(1)
except AttributeError:
    print("Couldn't log in using provided credentials")
    sys.exit(1)


# Get SSO token
ssoURI = "https://login.eveonline.com/launcher/token"
r = requests.get(ssoURI, params={'accesstoken': accToken},
                 allow_redirects=True, timeout=5)

# Extract SSO token
ssoToken = re.search("#access_token=([\w\d_-]+)", r.url).group(1)

# Open client
exefile = os.path.join(os.environ['PROGRAMFILES(x86)'], "CCP",
                       "EVE", "bin", "ExeFile.exe")
if os.path.isfile(exefile):
    try:
        dx = sys.argv[4]
    except IndexError:
        dx = "dx9"
    subprocess.Popen([exefile, "/noconsole", "/ssoToken={}".format(ssoToken),
                      "/triPlatform={}".format(dx)])
else:
    print("Couldn't find ExeFile.exe at \"{}\"".format(exefile))
    sys.exit(1)
