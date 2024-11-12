def build() :
    return {
    'name': 'libheif',
    'url': 'https://github.com/strukturag/libheif.git',
    'depends': ['mozjpeg', 'dav1d', 'libwebp', 'openh264', 'libde265'],
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )
    set PKG_CONFIG_PATH=%USED_PREFIX%/%ARCH%/lib/pkgconfig;%PKG_CONFIG_PATH%
    cmake %CMAKE_PREFIX_ARGS% ^
        -D BUILD_SHARED_LIBS=OFF ^
        -D BUILD_TESTING=OFF ^
        -D ENABLE_PLUGIN_LOADING=OFF ^
        -D WITH_AOM_ENCODER=OFF ^
        -D WITH_AOM_DECODER=OFF ^
        -D WITH_X265=OFF ^
        -D WITH_SvtEnc=OFF ^
        -D WITH_RAV1E=OFF ^
        -D WITH_DAV1D=ON ^
        -D WITH_LIBDE265=ON ^
        -D WITH_EXAMPLES=OFF ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi
    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    cmake $CMAKE_PREFIX_ARGS ^
        -D BUILD_SHARED_LIBS=OFF ^
        -D BUILD_TESTING=OFF ^
        -D ENABLE_PLUGIN_LOADING=OFF ^
        -D WITH_AOM_ENCODER=OFF ^
        -D WITH_AOM_DECODER=OFF ^
        -D WITH_X265=OFF ^
        -D WITH_SvtEnc=OFF ^
        -D WITH_RAV1E=OFF ^
        -D WITH_DAV1D=ON ^
        -D WITH_LIBDE265=ON ^
        -D WITH_EXAMPLES=OFF ^
        -B output/$OHOS_LIBNAME-$ARCH-build ^
        -S $OHOS_LIBNAME
    cmake --build output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel $MAKE_THREADS_CNT
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}