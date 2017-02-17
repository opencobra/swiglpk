# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    if [ -n "$IS_OSX" ]; then
        export CC=clang
        export CXX=clang++
        export CFLAGS="-fPIC -O3 -arch i386 -arch x86_64 -g -DNDEBUG -mmacosx-version-min=10.6"
        brew tap homebrew/science
        brew update
        brew install swig # automake
    else
        yum install -y pcre-devel
		# yum install automake
        curl -O -L http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz
        tar xzf swig-3.0.10.tar.gz
        (cd swig-3.0.10 \
				&& ./configure --prefix=$BUILD_PREFIX \
				&& make \
				&& make install)
	fi
    curl -O http://ftp.gnu.org/gnu/glpk/glpk-4.61.tar.gz
    tar xzf glpk-4.61.tar.gz
    (cd glpk-4.61 \
            && ./configure --disable-reentrant --prefix=$BUILD_PREFIX \
            && make \
            && make install)

 	# git clone https://github.com/swig/swig.git
    # (cd swig \
	# 		&& git checkout rel-3.0.10 \
	# 		&& ./autogen.sh \
	# 		&& ./configure --prefix=$BUILD_PREFIX \
	# 		&& make \
	# 		&& make install)
}

function build_wheel {
    # Set default building method to pip
    build_bdist_wheel $@
}

function run_tests {
    # Runs tests on installed distribution from an empty directory
    export NOSE_PROCESS_TIMEOUT=600
    export NOSE_PROCESSES=0
    echo "OS X? $IS_OSX"
    if [ -n "$IS_OSX" ]; then
        echo "uninstalling glpk for tests"
        brew uninstall -y glpk  # remove glpk to make sure that the OS X wheel works standalone.
    else
        rm -f /usr/local/lib/libglpk*
    fi
    # Run Pillow tests from within source repo
    cp ../test_swiglpk.py .
    nosetests -v
}
