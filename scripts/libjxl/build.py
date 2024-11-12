def build() :
    return {
    'name': 'libjxl',
    'url': 'https://github.com/libjxl/libjxl.git',
    'depends': ['mozjpeg', 'dav1d', 'libwebp', 'openh264', 'libde265'],
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone --recursive --shallow-submodules %OHOS_LIBURL%
    )
    set PKG_CONFIG_PATH=%USED_PREFIX%/%ARCH%/lib/pkgconfig;%PKG_CONFIG_PATH%
    cmake %CMAKE_PREFIX_ARGS% ^
        -DBUILD_SHARED_LIBS=OFF ^
        -DBUILD_TESTING=OFF ^
        -DJPEGXL_ENABLE_FUZZERS=OFF ^
        -DJPEGXL_ENABLE_DEVTOOLS=OFF ^
        -DJPEGXL_ENABLE_TOOLS=OFF ^
        -DJPEGXL_ENABLE_DOXYGEN=OFF ^
        -DJPEGXL_ENABLE_MANPAGES=OFF ^
        -DJPEGXL_ENABLE_EXAMPLES=OFF ^
        -DJPEGXL_ENABLE_JNI=OFF ^
        -DJPEGXL_ENABLE_JPEGLI_LIBJPEG=OFF ^
        -DJPEGXL_ENABLE_SJPEG=OFF ^
        -DJPEGXL_ENABLE_OPENEXR=OFF ^
        -DJPEGXL_ENABLE_SKCMS=ON ^
        -DJPEGXL_ENABLE_VIEWERS=OFF ^
        -DJPEGXL_ENABLE_TCMALLOC=OFF ^
        -DJPEGXL_ENABLE_PLUGINS=OFF ^
        -DJPEGXL_ENABLE_COVERAGE=OFF ^
        -DJPEGXL_WARNINGS_AS_ERRORS=OFF ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone --recursive --shallow-submodules $OHOS_LIBURL
    fi
    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    cmake $CMAKE_PREFIX_ARGS ^
        -DBUILD_SHARED_LIBS=OFF ^
        -DBUILD_TESTING=OFF ^
        -DJPEGXL_ENABLE_FUZZERS=OFF ^
        -DJPEGXL_ENABLE_DEVTOOLS=OFF ^
        -DJPEGXL_ENABLE_TOOLS=OFF ^
        -DJPEGXL_ENABLE_DOXYGEN=OFF ^
        -DJPEGXL_ENABLE_MANPAGES=OFF ^
        -DJPEGXL_ENABLE_EXAMPLES=OFF ^
        -DJPEGXL_ENABLE_JNI=OFF ^
        -DJPEGXL_ENABLE_JPEGLI_LIBJPEG=OFF ^
        -DJPEGXL_ENABLE_SJPEG=OFF ^
        -DJPEGXL_ENABLE_OPENEXR=OFF ^
        -DJPEGXL_ENABLE_SKCMS=ON ^
        -DJPEGXL_ENABLE_VIEWERS=OFF ^
        -DJPEGXL_ENABLE_TCMALLOC=OFF ^
        -DJPEGXL_ENABLE_PLUGINS=OFF ^
        -DJPEGXL_ENABLE_COVERAGE=OFF ^
        -DJPEGXL_WARNINGS_AS_ERRORS=OFF ^
        -B output/$OHOS_LIBNAME-$ARCH-build ^
        -S $OHOS_LIBNAME
    cmake --build output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel $MAKE_THREADS_CNT
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}