# EVELaunch [![Build Status](https://travis-ci.org/TheJokr/EVELaunch.svg?branch=master)](https://travis-ci.org/TheJokr/EVELaunch)
EVELaunch is a Python script created to launch EVE Online without entering your credentials manually.  
Inspired by [Rapid Heavy EVE Launcher](https://github.com/raylu/rhel).

# Requirements
- [Python (&ge; 2.7)](https://python.org/)
  - [Requests](http://docs.python-requests.org/en/latest/)

# Usage
`python EVELaunch.py <Username> <Password> <Character name> [triPlatform]` launches EVE Online with the given credentials. Use qutotation marks for values with whitespace(s) in them.  
`<Character name>` can be any character on that account. You will still be able to select a character within the client.  
`[triPlatform]` specifies which DirectX version to use (`dx9` or `dx11`, default is `dx9`)

You can also create a shortcut to log in with one click: `PATH/TO/EVELaunch.py <Username> <Password> <Character name> [triPlatform]`.
### Warning: By saving your password as a shortcut it can be read by anyone with access to your PC as well as any program!

# Credits
EVELaunch is released under the GNU General Public License, version 3. The full license is available in the `COPYING` file.  
Copyright (C) 2015-2016  Leo Blöcher

# Contact
[TheJokr@GitHub](https://github.com/TheJokr)
