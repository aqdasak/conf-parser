# CONFIG PARSER

This module provides functions to read and write data from and to config files having a structure similar to what’s found in Microsoft Windows INI files.

The conf file is converted to python dict. All the variables and values are strings. List is not supported for now.


## Quick Start

Let’s take a very basic configuration file that looks like this:

```conf
# This is a comment
ServerAliveInterval = 45
Compression = yes
CompressionLevel = 9
ForwardX11 = yes

[bitbucket.org]
User = hg

[topsecret.server.com]
Port = 50022
ForwardX11 = no
```

```python
>>> import conf_parser
>>>
>>> st = '''# This is a comment
... ServerAliveInterval = 45
... Compression = yes
... CompressionLevel = 9
... ForwardX11 = yes
... 
... [bitbucket.org]
... User = hg
... 
... [topsecret.server.com]
... Port = 50022
... ForwardX11 = no
... '''
>>> config = conf_parser.loads(st)
>>> print(config)
{'meta0': '# This is a comment', 'ServerAliveInterval': '45', 'Compression': 'yes', 'CompressionLevel': '9', 'ForwardX11': 'yes', 'meta1': '', 'bitbucket.org': {'User': 'hg', 'meta2': ''}, 'topsecret.server.com': {'Port': '50022', 'ForwardX11': 'no', 'meta3': ''}}
>>>
>>> with open('file.conf','w') as f:
...     conf_parser.dump(config, f)
...
```