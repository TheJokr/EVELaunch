# EVELaunch [![Build Status](https://travis-ci.org/TheJokr/EVELaunch.svg?branch=master)](https://travis-ci.org/TheJokr/EVELaunch)
EVELaunch is a Python script created to launch EVE Online without entering your credentials each time.  
Inspired by [Rapid Heavy EVE Launcher](https://github.com/raylu/rhel).

# Requirements
- [Python (&ge; 2.6)](http://python.org/)
  - [Requests](http://docs.python-requests.org/en/latest/)

# Usage
`python launchEve.py <USERNAME> <PASSWORD> <CHAR NAME> [triPlatform]` to launch an EVE Online Client with the given credentials.  
A character name is required to bypass the login challenge upon first log in.  
`triPlatform` specifies which DirectX version to use ("dx9" or "dx11", "dx9" is used by default)  
You can also create a shortcut to log in with one click: `"PATH/TO/EVELaunch.py" "USERNAME" "PASSWORD" "CHAR NAME" "triPlatform"`.

# Credits
EVELaunch is released under the GNU General Public License, version 3. The full license is available in the `COPYING` file.  
Copyright (C) 2015  Leo Bl&ouml;cher

# Contact
[TheJokr@GitHub](https://github.com/TheJokr)
