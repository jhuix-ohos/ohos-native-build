def build() :
    return {
    'name': 'libavif',
    'url': 'https://github.com/AOMediaCodec/libavif.git',
    'depends': ['dav1d', 'libyuv'],
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )

    set PKG_CONFIG_PATH=%USED_PREFIX%/%ARCH%/lib/pkgconfig;%PKG_CONFIG_PATH%
    cmake %CMAKE_PREFIX_ARGS% ^
        -DBUILD_SHARED_LIBS=OFF ^
        -DAVIF_ENABLE_WERROR=OFF ^
        -DAVIF_CODEC_DAV1D=SYSTEM ^
        -DLIBYUV_INCLUDE_DIR="$USED_PREFIX/$ARCH/include" ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%

    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi

    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    cmake $CMAKE_PREFIX_ARGS \\
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" \\
        -DBUILD_SHARED_LIBS=OFF \\
        -DAVIF_ENABLE_WERROR=OFF \\
        -DAVIF_CODEC_DAV1D=SYSTEM \\
        -DLIBYUV_INCLUDE_DIR="$USED_PREFIX/$ARCH/include" \\
        -B output/$OHOS_LIBNAME-$ARCH-build \\
        -S $OHOS_LIBNAME

    cmake --build output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel $MAKE_THREADS_CNT
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}