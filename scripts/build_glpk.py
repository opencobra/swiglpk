# taken from https://github.com/opencobra/cobrapy/blob/devel/appveyor/build_glpk.py

import os
import tarfile
import struct
import shutil
import urllib.request as urllib2
import subprocess

GUESS_VCVARS = (
    "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\"
    "VC\\Auxiliary\\Build\\vcvarsall.bat"
)

# these need to be set to the latest glpk version
glpk_version = os.getenv('NEW_GLPK_VERSION')

glpk_build_dir = "glpk_build/glpk-%s" % glpk_version
url = "http://ftp.gnu.org/gnu/glpk/glpk-%s.tar.gz" % glpk_version
bitness = struct.calcsize("P") * 8
arch = "x86_amd64" if bitness == 64 else "x86"

def find_vcvarsall():
    if os.path.isfile(GUESS_VCVARS):
        return(GUESS_VCVARS)
    for root, dirs, files in os.walk("C:\\Program Files\\Microsoft Visual Studio\\"):
        for f in files:
            if f == "vcvarsall.bat":
                return(os.path.join(root, *dirs, f))
    raise RuntimeError("Could not find vcvarsall.bat :(")


if not os.path.isdir("glpk_build/"):
    os.mkdir("glpk_build")
if not os.path.isdir(glpk_build_dir):
    response = urllib2.urlopen(url)
    with open("glpk-download.tar.gz", "wb") as outfile:
        outfile.write(response.read())
    # assert md5("glpk-download.tar.gz") == glpk_md5
    with tarfile.open("glpk-download.tar.gz") as infile:
        infile.extractall("glpk_build")

os.chdir("%s/w%d" % (glpk_build_dir, bitness))
if not os.path.isfile("glpk.lib"):
    shutil.copy2("config_VC", "config.h")
    vc_setup = find_vcvarsall()
    subprocess.run(
        f'"{vc_setup}" {arch} & nmake /f Makefile_VC',
        check=True, shell=True
    )
shutil.copy2("glpk.lib", "../../..")
os.chdir("../../..")
shutil.copy2(glpk_build_dir + "/src/glpk.h", ".")
