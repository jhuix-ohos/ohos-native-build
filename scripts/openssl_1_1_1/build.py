def build() :
    return {
        'name': 'openssl_1_1_1',
        'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone -b OpenSSL_1_1_1-stable https://github.com/openssl/openssl %OHOS_LIBSRC%
    )
    if not exist "output" mkdir output
    cd output
    if exist "%OHOS_LIBNAME%-%ARCH%-build" rmdir /S /Q %OHOS_LIBNAME%-%ARCH%-build
    mkdir open%OHOS_LIBNAME%ssl_1_1_1-%ARCH%-build
    cd %OHOS_LIBNAME%-%ARCH%-build

    perl ../../%OHOS_LIBSRC%/Configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% no-shared no-docs no-tests %HOST_ARCH%
    make %MAKE_THREADS_CNT%
    make install
    make clean
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone -b OpenSSL_1_1_1-stable https://github.com/openssl/openssl $OHOS_LIBSRC
    fi
    rm -rf output/$OHOS_LIBNAME-$ARCH-build
    mkdir -p output/$OHOS_LIBNAME-$ARCH-build
    cd output/$OHOS_LIBNAME-$ARCH-build

    ../../$OHOS_LIBSRC/Configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH no-shared no-docs no-tests $HOST_ARCH
    make $MAKE_THREADS_CNT
    make install
    make clean
"""
    }