import sys
import requests
import json
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse


URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json. Adapted from https://stackoverflow.com/a/34366589"""
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        # j = json.loads(req.text.encode(req.encoding))
        j = req.json()
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version

version = get_version('swiglpk')
print(version)
major, minor = version.public.split('.')[0:2]
print(major)
print(minor)
major, minor = int(major), int(minor)
print(major)
print(minor)

request = requests.head('http://ftp.gnu.org/gnu/glpk/glpk-{}.{}.tar.gz'.format(major, minor+1))
if request.status_code == 200:
    print('{}.{}'.format(major, minor+1))
    sys.exit(0)
else:
    sys.exit(-1)