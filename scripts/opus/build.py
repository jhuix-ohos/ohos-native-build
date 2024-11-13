def build() :
    return {
    'name': 'opus',
    'url': 'https://github.com/xiph/opus.git',
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )
    cmake %CMAKE_PREFIX_ARGS% ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --config Release %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config Release
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --config Release --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi
    cmake -LH \\
        -DCMAKE_INSTALL_PREFIX=$USED_PREFIX/$ARCH \\
        -DCMAKE_SKIP_RPATH=ON \\
        -DCMAKE_SKIP_INSTALL_RPATH=ON \\
        -DOHOS_ARCH=$ARCH \\
        -DOHOS_STL=c++_static \\
        -DCMAKE_TOOLCHAIN_FILE="$OHOS_SDK/native/build/cmake/ohos.toolchain.cmake" \\
        -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja" \\
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" \\
        -Boutput/$OHOS_LIBNAME-$ARCH-build \\
        -S$OHOS_LIBNAME
    cmake --build output/$OHOS_LIBNAME-$ARCH-build $MAKE_THREADS_CNT
    cmake --install output/$OHOS_LIBNAME-$ARCH-build
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}