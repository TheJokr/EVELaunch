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


# Usage: python EVELaunch.py <USERNAME> <PASSWORD> <CHAR NAME> [triPlatform]
# <CHAR NAME> is the name of one of the characters of the Account


import sys
import os
import subprocess

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests


# Command line arguments
try:
    user = sys.argv[1]
    pwd = sys.argv[2]
    char = sys.argv[3]
except IndexError:
    print("Missing information. "
          "Usage: python EVELaunch.py <USERNAME> <PASSWORD> "
          "<CHAR NAME> [triPlatform]")
    sys.exit(1)

try:
    dx = sys.argv[4]
except IndexError:
    dx = "dx9"


# Get access token
s = requests.Session()
authURI = "https://login.eveonline.com/Account/LogOn"
payload = {'ReturnURL': "/oauth/authorize/?client_id=eveLauncherTQ"
                        "&lang=en&response_type=token"
                        "&redirect_uri=https://login.eveonline.com/launcher"
                        "?client_id=eveLauncherTQ"
                        "&scope=eveClientToken%20user"}
r = s.post(authURI, params=payload, data={"UserName": user, "Password": pwd},
           allow_redirects=True, timeout=5)

# Login challenge
if not r.history:
    challengeURI = "https://login.eveonline.com/Account/Challenge"
    r = s.post(challengeURI, params=payload, data={"Challenge": char},
               allow_redirects=True, timeout=5)

# Extract access token
try:
    rFragment = urlparse.urlparse(r.url).fragment
    accToken = urlparse.parse_qs(rFragment)['access_token'][0]
except KeyError:
    print("Couldn't log in using provided credentials")
    sys.exit(1)


# Get SSO token
ssoURI = "https://login.eveonline.com/launcher/token"
r = s.get(ssoURI, params={'accesstoken': accToken},
          allow_redirects=True, timeout=5)

# Extract SSO token
rFragment = urlparse.urlparse(r.url).fragment
ssoToken = urlparse.parse_qs(rFragment)['access_token'][0]


# Locate exefile
# CCP replaces whitespaces and '\' with underscores in their folder names
# Who thought this would be a good idea?
def getUnderscoredPath(base, fragments):
    if "_" not in fragments:
        # Last fragment
        checkPath = os.path.join(base, fragments)
        return checkPath if os.path.isdir(checkPath) else None

    folder, path = fragments.split("_", 1)
    checkPath = os.path.join(base, folder)
    if os.path.isdir(checkPath):
        # Path doesn't contain whitespaces (so far)
        return getUnderscoredPath(checkPath, path)
    else:
        # Path either contains whitespaces or is invalid (deleted)
        possiblePaths = []
        pathParts = path.split("_")
        for idx, part in enumerate(pathParts):
            checkPath += " " + part
            if os.path.isdir(checkPath):
                wP = getUnderscoredPath(checkPath, "_".join(pathParts[idx+1:]))
                if wP:
                    possiblePaths.append(wP)
        return possiblePaths


# Flatten list of unkown depth
def flatten(_list):
    if not _list:
        return _list
    if isinstance(_list[0], list):
        return flatten(_list[0]) + flatten(_list[1:])
    return _list[:1] + flatten(_list[1:])


EVEConfig = os.path.join(os.environ['LOCALAPPDATA'], "CCP", "EVE")
cfgDirs = [_dir[:-len("_tranquility")] for _dir in os.listdir(EVEConfig)
           if os.path.isdir(os.path.join(EVEConfig, _dir)) and
           _dir.endswith("_tranquility")]

rootDirs = []
for _dir in cfgDirs:
    try:
        drive, path = _dir.split('_', 1)
    except ValueError:
        # Path contains just a drive letter
        drive, path = _dir.split('_', 1), ""

    drive = "{}:\\".format(drive.upper())
    rootDirs.append(getUnderscoredPath(drive, path))

rootDirs = flatten(rootDirs)
rootDirs = [item for item in rootDirs if item is not None]

# Default exefile path
exefile = os.path.join(os.environ['PROGRAMFILES(x86)'], "CCP",
                       "EVE", "bin", "ExeFile.exe")
for _dir in rootDirs:
    _exe = os.path.join(_dir, "bin", "ExeFile.exe")
    if os.path.isfile(_exe):
        exefile = _exe
        break

# Open client
if os.path.isfile(exefile):
    subprocess.Popen([exefile, "/noconsole", "/ssoToken={}".format(ssoToken),
                      "/triPlatform={}".format(dx)])
else:
    print("Couldn't find ExeFile.exe at \"{}\"".format(exefile))
    sys.exit(1)
