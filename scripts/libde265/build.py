def build() :
    return {
    'name': 'libde265',
    'url': 'https://github.com/strukturag/libde265.git',
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )

    cmake %CMAKE_PREFIX_ARGS% ^
        -D ENABLE_SDL=OFF ^
        -D BUILD_SHARED_LIBS=OFF ^
        -D ENABLE_DECODER=ON ^
        -D ENABLE_ENCODER=OFF ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config MinSizeRel --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi

    cmake $CMAKE_PREFIX_ARGS \\
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" \\
        -D ENABLE_SDL=OFF \\
        -D BUILD_SHARED_LIBS=OFF \\
        -D ENABLE_DECODER=ON \\
        -D ENABLE_ENCODER=OFF \\
        -B output/$OHOS_LIBNAME-$ARCH-build \\
        -S $OHOS_LIBNAME
    cmake --build output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel $MAKE_THREADS_CNT
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --config MinSizeRel --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}