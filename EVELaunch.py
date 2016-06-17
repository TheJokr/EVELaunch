#!/usr/bin/env python
# coding=utf-8

# Copyright (C) 2015-2016  Leo Blöcher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, unicode_literals, print_function

import sys
import os
import subprocess
try:
    # Python 3
    from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
except ImportError:
    # Python 2.7
    from urlparse import urlparse, urlunparse, parse_qs
    from urllib import urlencode

import requests


# Command line arguments
try:
    user = sys.argv[1]
    pwd = sys.argv[2]
    char = sys.argv[3]
except IndexError:
    print("Missing information.", file=sys.stderr)
    print(("Usage: {} <Username> <Password> <Character name> "
           "[SettingsProfile] [triPlatform]").format(sys.argv[0]),
          file=sys.stderr)
    sys.exit(1)

settings = ""
dx = "dx11"
if len(sys.argv) > 4:
    if sys.argv[4].startswith("dx"):
        dx = sys.argv[4]
    else:
        settings = sys.argv[4]
        if len(sys.argv) > 5:
            dx = sys.argv[5]


# Get access token
s = requests.Session()
url = "https://login.eveonline.com/Account/LogOn"
params = {
    'ReturnURL': urlunparse((
        "", "", "/oauth/authorize/", "",
        urlencode({'client_id': "eveLauncherTQ",
                   'response_type': "token",
                   'redirect_uri': urlunparse((
                       "https", "login.eveonline.com", "launcher", "",
                       urlencode({'client_id': "eveLauncherTQ"}), ""
                   )),
                   'scope': "eveClientToken user"}), ""
    ))
}
r = s.post(url, params=params, data={"UserName": user, "Password": pwd},
           allow_redirects=True, timeout=5)

# Login challenge
if not r.history:
    url = "https://login.eveonline.com/Account/Challenge"
    r = s.post(url, params=params, data={"Challenge": char},
               allow_redirects=True, timeout=5)

# Extract access token
try:
    token = urlparse(r.url).fragment
    token = parse_qs(token)['access_token'][0]
except KeyError:
    print("Failed to log in using your credentials", file=sys.stderr)
    sys.exit(1)


# Get SSO token
url = "https://login.eveonline.com/launcher/token"
r = s.get(url, params={'accesstoken': token}, allow_redirects=True, timeout=5)

# Extract SSO token
token = urlparse(r.url).fragment
token = parse_qs(token)['access_token'][0]


# Locate exefile
# CCP replaces whitespaces and '\' with underscores in their folder names
# Who thought this would be a good idea?
def parse_eve_dir(abs_path):
    def replace_underscore(val, replacements=(' ', '\\', '_')):
        if '_' not in val:
            yield val
            return

        base, ext = val.split('_', 1)
        for alt in replace_underscore(ext):
            for repl in replacements:
                yield base + repl + alt

    if '_' in abs_path:
        drive, path = abs_path.split('_', 1)
    else:
        drive, path = abs_path, ""
    drive = "{}:\\".format(drive.upper())

    for repl_path in replace_underscore(path):
        check_path = os.path.join(drive, repl_path)
        if os.path.isdir(check_path):
            yield check_path


eve_data_dir = os.path.join(os.environ['LOCALAPPDATA'], "CCP", "EVE")
try:
    cfg_dirs = (dir_ for dir_ in os.listdir(eve_data_dir)
                if os.path.isdir(os.path.join(eve_data_dir, dir_)) and
                dir_.endswith("_tranquility"))
except OSError:
    print('Failed to locate EVE configuration at "{}"'.format(eve_data_dir),
          file=sys.stderr)
    sys.exit(1)
root_dirs = ((dir_, parse_eve_dir(dir_[:-len("_tranquility")]))
             for dir_ in cfg_dirs)

exefile = None
cfg_path = None
for cfg, paths in root_dirs:
    for dir_ in paths:
        exe = os.path.join(dir_, "bin", "ExeFile.exe")
        if os.path.isfile(exe):
            exefile = exe
            cfg_path = os.path.join(eve_data_dir, cfg)
            break

    if exefile is not None:
        break

if exefile is None:
    print("Failed to locate ExeFile.exe", file=sys.stderr)
    sys.exit(1)


# Open client
cmd = [exefile, "/noconsole", "/ssoToken={}".format(token),
       "/server:tranquility", "/triPlatform={}".format(dx)]

if not settings:
    settings = next(
        (profile[len("settings_"):] for profile in os.listdir(cfg_path)
         if os.path.isdir(os.path.join(cfg_path, profile)) and
         profile.startswith("settings_")), None
    )

if settings:
    cmd.append("/settingsprofile={}".format(settings))

subprocess.Popen(cmd)
