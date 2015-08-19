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


# Usage: python launchEve.py <USERNAME> <PASSWORD> <CHAR NAME>
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
          "Usage: python launchEve.py <USERNAME> <PASSWORD> <CHAR NAME>")
    sys.exit(1)


# Get access token
s = requests.Session()
authURI = ("https://login.eveonline.com/Account/LogOn"
           "?ReturnUrl=%2Foauth%2Fauthorize%2F%3Fclient_id%3DeveLauncherTQ"
           "%26lang%3Den%26response_type%3Dtoken%26redirect_uri%3D"
           "https%3A%2F%2Flogin.eveonline.com%2F"
           "launcher%3Fclient_id%3DeveLauncherTQ"
           "%26scope%3DeveClientToken")
r = s.post(authURI, data={"UserName": user, "Password": pwd},
           headers={"referer": authURI,
                    "Origin": "https://login.eveonline.com"},
           allow_redirects=True, timeout=5)

# Character name challenge
if not r.history:
    challengeURI = ("https://login.eveonline.com/Account/Challenge"
                    "?ReturnUrl=%2Foauth%2Fauthorize%2F"
                    "%3Fclient_id%3DeveLauncherTQ"
                    "%26lang%3Den%26response_type%3Dtoken%26redirect_uri%3D"
                    "https%3A%2F%2Flogin.eveonline.com%2F"
                    "launcher%3Fclient_id%3DeveLauncherTQ"
                    "%26scope%3DeveClientToken")
    r = s.post(challengeURI, data={"Challenge": char})

# Extract access token
try:
    accToken = re.search("#access_token=([\w\d_-]+)", r.url).group(1)
except AttributeError:
    print("Couldn't log in using provided credentials")
    sys.exit(1)


# Get SSO token
ssoURI = ("https://login.eveonline.com/"
          "launcher/token?accesstoken={}").format(accToken)
r = requests.get(ssoURI, allow_redirects=True, timeout=5)

# Extract SSO token
ssoToken = re.search("#access_token=([\w\d_-]+)", r.url).group(1)

# Start client
exefile = os.path.join(os.environ['PROGRAMFILES(x86)'], "CCP",
                       "EVE", "bin", "ExeFile.exe")
if os.path.isfile(exefile):
    subprocess.Popen([exefile, "/noconsole", "/ssoToken={}".format(ssoToken),
                      "/triPlatform=dx9"])
else:
    print("Couldn't find ExeFile.exe at \"{}\"".format(exefile))
    sys.exit(1)
