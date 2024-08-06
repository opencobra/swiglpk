# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    ADD_CFLAGS=""
    ADD_CONFIG_FLAGS=""
    GMP_VERSION="6.3.0"
    if [ -n "$IS_OSX" ]; then
        export CC=clang
        export CXX=clang++
        export BUILD_PREFIX="${BUILD_PREFIX:-/usr/local}"
        brew update
        brew install swig
        # Avoid mixing compiled files from different archs.
        rm -rf glpk-* /usr/local/lib/libgmp*.*
        rm -rf gmp-* /usr/local/lib/libglpk*.*
        if [[ "$ARCHFLAGS" == *"arm64"* ]]; then
            echo "Looks like we are cross-compiling, adjusting compiler flags."
            export ADD_CFLAGS="--target=arm64-apple-macos"
            export ADD_CONFIG_FLAGS="--host=aarch64-apple-darwin --build=x86_64-apple-darwin"
        fi
        export CFLAGS="-I/usr/local/include $ADD_CFLAGS $CFLAGS"
        export LDFLAGS="-L/usr/local/lib $ARCHFLAGS"
        echo "Downloading GMP"
        curl -O https://ftp.gnu.org/gnu/gmp/gmp-${GMP_VERSION}.tar.lz
        tar xzf gmp-$GMP_VERSION.tar.lz
        (cd gmp-$GMP_VERSION \
            && ./configure --prefix=$BUILD_PREFIX $ADD_CONFIG_FLAGS \
            && make install -j 2
        )
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

    # Check for latest GLP and compile it for the target platform
    export NEW_GLPK_VERSION=$(python scripts/find_newest_glpk_release.py)
	fi
	echo "Downloading http://ftp.gnu.org/gnu/glpk/glpk-$NEW_GLPK_VERSION.tar.gz"
    curl -O "http://ftp.gnu.org/gnu/glpk/glpk-$NEW_GLPK_VERSION.tar.gz"
    tar xzf "glpk-$NEW_GLPK_VERSION.tar.gz"
    (cd "glpk-$NEW_GLPK_VERSION" \
            && ./configure --disable-reentrant --prefix=$BUILD_PREFIX --with-gmp $ADD_CONFIG_FLAGS \
            && make install -j 2) || cat "glpk-$NEW_GLPK_VERSION/config.log"
    echo "Installed to $BUILD_PREFIX"
}
