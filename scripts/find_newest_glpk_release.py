from __future__ import print_function
import re
import requests

response = requests.get("http://ftp.gnu.org/gnu/glpk/", timeout=30)
if response.ok:
    major, minor = 0, 0
    for item in set(re.findall('glpk-\d+\.\d+\.tar\.gz', response.text)):
        match = re.findall('(\d+)\.(\d+)', item)
        assert len(match) == 1
        assert len(match[0]) == 2
        new_major, new_minor = int(match[0][0]), int(match[0][1])
        if new_major > major:
            major = new_major
            minor = new_minor
        if new_major >= major and new_minor > minor:
            minor = new_minor

    print('{}.{}'.format(major, minor), end='')
else:
    print("Couldn't reaction GNU FTP server. Status code {}".format(response.status))

