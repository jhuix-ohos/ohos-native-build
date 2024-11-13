def build() :
    return {
        'name': 'openssl',
        'src': 'openssl-openssl-3.3.2',
        'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      if not exist "%OHOS_LIBSRC%.tar.gz" (
        echo "Downloading OpenSSL sources..."
        powershell -Command "iwr -OutFile ./%OHOS_LIBSRC%.tar.gz https://github.com/openssl/openssl/archive/refs/tags/openssl-3.3.2.tar.gz"
      )
      tar xzf %OHOS_LIBSRC%.tar.gz
    )
    if not exist "output" mkdir output
    cd output
    if exist "%OHOS_LIBNAME%-%ARCH%-build" rmdir /S /Q %OHOS_LIBNAME%-%ARCH%-build
    mkdir %OHOS_LIBNAME%-%ARCH%-build
    cd %OHOS_LIBNAME%-%ARCH%-build

    perl ../../%OHOS_LIBSRC%/Configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% no-shared no-docs no-tests %HOST_ARCH%
    make %MAKE_THREADS_CNT%
    make install

unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      if [ ! -d "$OHOS_LIBSRC.tar.gz" ] ; then
        echo "Downloading OpenSSL sources..."
        wget -q https://github.com/openssl/openssl/archive/refs/tags/openssl-3.3.2.tar.gz -O $OHOS_LIBSRC.tar.gz
      fi
      tar xzf $OHOS_LIBSRC.tar.gz
    fi
    rm -rf output/$OHOS_LIBNAME-$ARCH-build
    mkdir -p output/$OHOS_LIBNAME-$ARCH-build
    cd output/$OHOS_LIBNAME-$ARCH-build

    ../../$OHOS_LIBSRC/Configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH no-shared no-docs no-tests $HOST_ARCH
    make $MAKE_THREADS_CNT
    make install
"""
    }
