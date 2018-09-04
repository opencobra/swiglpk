import re
import htmllistparse
cwd, listing = htmllistparse.fetch_listing("http://ftp.gnu.org/gnu/glpk/", timeout=30)

major, minor = 0, 0
for item in listing:
    if item.name.startswith('glpk-') and item.name.endswith('.tar.gz'):
        match = re.findall('(\d+)\.(\d+)', item.name)
        assert len(match) == 1
        assert len(match[0]) == 2
        new_major, new_minor = int(match[0][0]), int(match[0][1])
        if new_major > major:
            major = new_major
        if new_minor > minor:
            minor = new_minor

print('{}.{}'.format(major, minor))