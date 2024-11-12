def build() :
    return {
        'name': 'openssl_1_0_2',
        'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone -b OpenSSL_1_0_2-stable https://github.com/openssl/openssl %OHOS_LIBSRC%
    )

    cd %OHOS_LIBSRC%
    perl ./Configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% no-shared no-docs no-tests %HOST_ARCH%
    make %MAKE_THREADS_CNT%
    make install
    make clean
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone -b OpenSSL_1_0_2-stable https://github.com/openssl/openssl $OHOS_LIBSRC
    fi

    cd $OHOS_LIBSRC
    ./$OHOS_LIBSRC/Configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH no-shared no-docs no-tests $HOST_ARCH
    make $MAKE_THREADS_CNT
    make install
    make clean
"""
    }