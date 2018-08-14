import sys
import git
import requests

g = git.Git('.')
current_swiglpk_tag = g.describe()
major, minor = current_swiglpk_tag.split('.')
major, minor = int(major), int(minor)

request = requests.head('http://ftp.gnu.org/gnu/glpk/glpk-{}.{}.tar.gz'.format(major, minor+1))
if request.status_code == 200:
    print('{}.{}'.format(major, minor+1))
    sys.exit(0)
else:
    sys.exit(-1)