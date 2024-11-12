def build() :
    return {
    'name': 'libvpx',
    'url': 'https://github.com/webmproject/libvpx.git',
    'depends': ['mozjpeg', 'dav1d', 'libwebp', 'openh264', 'libde265'],
    'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone %OHOS_LIBURL%
    )
    if not exist "output\\%OHOS_LIBNAME%-%ARCH%-build" mkdir "output\\%OHOS_LIBNAME%-%ARCH%-build"
    cd "output\\%OHOS_LIBNAME%-%ARCH%-build"

    perl ../../"%OHOS_LIBSRC%"/configure --prefix=%USED_PREFIX%/%ARCH% ^
    --disable-examples ^
    --disable-unit-tests ^
    --disable-tools ^
    --disable-docs ^
    --enable-vp8 ^
    --enable-vp9 ^
    --enable-webm-io

    make $MAKE_THREADS_CNT
    make install

    perl ../../%OHOS_LIBSRC%/configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% ^
    --disable-examples ^
    --disable-unit-tests ^
    --disable-tools ^
    --disable-docs ^
    --enable-vp8 ^
    --enable-vp9 ^
    --enable-webm-io
    make install
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi
    mkdir -p output/$OHOS_LIBNAME-$ARCH-build

    ../../$OHOS_LIBSRC/configure --prefix=$USED_PREFIX/$ARCH ^
    --disable-examples ^
    --disable-unit-tests ^
    --disable-tools ^
    --disable-docs ^
    --enable-vp8 ^
    --enable-vp9 ^
    --enable-webm-io

    make $MAKE_THREADS_CNT
    make install

    ../../$OHOS_LIBSRC/configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH ^
    --disable-examples ^
    --disable-unit-tests ^
    --disable-tools ^
    --disable-docs ^
    --enable-vp8 ^
    --enable-vp9 ^
    --enable-webm-io
    make install    
"""}