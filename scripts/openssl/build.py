def build() :
    return {
        'name': 'openssl',
        'commands': """
win:
    if not exist "openssl-openssl-3.3.2.tar.gz" (
      echo "Downloading OpenSSL sources..."
      powershell -Command "iwr -OutFile ./openssl-openssl-3.3.2.tar.gz https://github.com/openssl/openssl/archive/refs/tags/openssl-3.3.2.tar.gz"
      tar xzf openssl-openssl-3.3.2.tar.gz
      rem del openssl-openssl-3.3.2.tar.gz
    )
    if not exist "output" mkdir output
    cd output
    if exist "openssl-%ARCH%-build" rmdir /S /Q openssl-%ARCH%-build
    mkdir openssl-%ARCH%-build
    cd openssl-%ARCH%-build

    perl ../../openssl-openssl-3.3.2/Configure --prefix=%USED_PREFIX%/openssl/%ARCH% no-shared no-tests %HOST_ARCH%
    make %MAKE_THREADS_CNT%
    make install
    make clean
unix:
    if ![ -d "openssl-openssl-3.3.2" ] ; then
      echo "Downloading OpenSSL sources..."
      wget -q https://github.com/openssl/openssl/archive/refs/tags/openssl-3.3.2.tar.gz
      tar xzf openssl-openssl-3.3.2.tar.gz
      rm -f openssl-openssl-3.3.2.tar.gz
    fi
    rm -rf output/openssl-$ARCH-build
    mkdir -p output/openssl-$ARCH-build
    cd output/openssl-$ARCH-build

    ../../openssl-openssl-3.3.2/Configure --prefix=$USED_PREFIX/openssl/$ARCH no-shared no-tests $HOST_ARCH
    make $MAKE_THREADS_CNT
    make install
    make clean
"""
    }
