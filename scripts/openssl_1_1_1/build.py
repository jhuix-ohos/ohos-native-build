def build() :
    return {
        'name': 'openssl_1_1_1',
        'commands': """
win:
    if not exist "openssl_1_1_1" (
      git clone -b OpenSSL_1_1_1-stable https://github.com/openssl/openssl openssl_1_1_1
    )
    if not exist "output" mkdir output
    cd output
    if exist "openssl_1_1_1-%ARCH%-build" rmdir /S /Q openssl_1_1_1-%ARCH%-build
    mkdir openssl_1_1_1-%ARCH%-build
    cd openssl_1_1_1-%ARCH%-build

    perl ../../openssl_1_1_1/Configure --prefix=%USED_PREFIX%/openssl_1_1_1/%ARCH% no-shared no-tests %HOST_ARCH%
    make %MAKE_THREADS_CNT%
    make install
    make clean
unix:
    if ![ -d "openssl_1_1_1" ] ; then
      git clone -b OpenSSL_1_1_1-stable https://github.com/openssl/openssl openssl_1_1_1
    fi
    rm -rf output/openssl_1_1_1-$ARCH-build
    mkdir -p output/openssl_1_1_1-$ARCH-build
    cd output/openssl_1_1_1-$ARCH-build

    ../../openssl_1_1_1/Configure --prefix=$USED_PREFIX/openssl_1_1_1/$ARCH no-shared no-tests $HOST_ARCH
    make $MAKE_THREADS_CNT
    make install
    make clean
"""
    }