# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    if [ -n "$IS_OSX" ]; then
        export CC=clang
        export CXX=clang++
        export BUILD_PREFIX="${BUILD_PREFIX:-/usr/local}"
        brew update
        brew install swig # automake
        brew install gmp
        export CFLAGS="-I`brew --prefix gmp`/include $CFLAGS"
        export LDFLAGS="-L`brew --prefix gmp`/lib $LDFLAGS"
    else
        yum install -y pcre-devel gmp-devel
		# yum install automake
        curl -O -L http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz
        tar xzf swig-3.0.10.tar.gz
        (cd swig-3.0.10 \
				&& ./configure --prefix=$BUILD_PREFIX \
				&& make \
				&& make install)
		pip install requests
    export NEW_GLPK_VERSION=$(python scripts/find_newest_glpk_release.py)
	fi
	echo "Downloading http://ftp.gnu.org/gnu/glpk/glpk-$NEW_GLPK_VERSION.tar.gz"
    curl -O "http://ftp.gnu.org/gnu/glpk/glpk-$NEW_GLPK_VERSION.tar.gz"
    tar xzf "glpk-$NEW_GLPK_VERSION.tar.gz"
    (cd "glpk-$NEW_GLPK_VERSION" \
            && ./configure --disable-reentrant --prefix=$BUILD_PREFIX --with-gmp\
            && make \
            && make install) || cat "glpk-$NEW_GLPK_VERSION/config.log"
    echo "Installed to $BUILD_PREFIX"
    ls -ls /include
    ls -ls .
}
