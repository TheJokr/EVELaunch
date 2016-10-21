# EVELaunch [![Build Status](https://travis-ci.org/TheJokr/EVELaunch.svg?branch=master)](https://travis-ci.org/TheJokr/EVELaunch)
EVELaunch is a Python script that launches EVE Online directly using CLI parameters to authenticate.  
**Note: This script was created before the new [EVE Launcher](https://community.eveonline.com/support/download/) was released.
It is recommended to use CCP's launcher instead of EVELaunch nowadays.**  
Inspired by [Rapid Heavy EVE Launcher](https://github.com/raylu/rhel).

# Requirements
- [Python](https://www.python.org/) &ge; 2.7
    - [Requests](http://docs.python-requests.org/en/latest/)

# Usage
`EVELaunch.py <Username> <Password> <Character name> [SettingsProfile] [triPlatform]` launches EVE Online with the given credentials.  
Any character on the account can be used as `<Character name>`. You will still be able to select a character within the client afterwards.  
`[SettingsProfile]` is the name of the settings profile to be used. If it is not set or empty, EVELaunch defaults to the first profile found.   
`[triPlatform]` specifies which DirectX version to use (`dx9` or `dx11`, default is `dx11`).

You can create a shortcut to EVELaunch.py to log in with one click. Add the required CLI parameters after the path.
**Warning: By saving your password in a shortcut it can be read by anyone and any program with access to your files!**

# License
EVELaunch is released under the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html).
The full license is available in the `COPYING` file.  
Copyright (C) 2015-2016  Leo Blöcher

# Contact
[TheJokr@GitHub](https://github.com/TheJokr)
