def build() :
    return {
    'name': 'mozjpeg',
    'url': 'https://github.com/mozilla/mozjpeg.git',
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )

    cmake -LH -DCMAKE_SKIP_RPATH=ON -DCMAKE_SKIP_INSTALL_RPATH=ON -G"Unix Makefiles" ^
        -DCMAKE_INSTALL_PREFIX=%USED_PREFIX%/%ARCH% ^
        -DOHOS_ARCH=%ARCH% ^
        -DOHOS_STL=c++_static ^
        -DCMAKE_TOOLCHAIN_FILE="%OHOS_SDK%/native/build/cmake/ohos.toolchain.cmake" ^
        -GNinja -DCMAKE_MAKE_PROGRAM="%OHOS_SDK%/native/build-tools/cmake/bin/ninja.exe" ^
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" ^
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" ^
        -DWITH_JPEG8=ON ^
        -DENABLE_SHARED=OFF ^
        -DPNG_SUPPORTED=OFF ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi
    cmake -LH -DCMAKE_SKIP_RPATH=ON -DCMAKE_SKIP_INSTALL_RPATH=ON \\
        -DCMAKE_INSTALL_PREFIX=$USED_PREFIX/$ARCH \\
        -DOHOS_ARCH=$ARCH \\
        -DOHOS_STL=c++_static \\
        -DCMAKE_TOOLCHAIN_FILE="$OHOS_SDK/native/build/cmake/ohos.toolchain.cmake" \\
        -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja" \\
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" \\
        -D WITH_JPEG8=ON \\
        -D ENABLE_SHARED=OFF \\
        -D PNG_SUPPORTED=OFF \\
        -B output/$OHOS_LIBNAME-$ARCH-build \\
        -S $OHOS_LIBNAME
    cmake --build output/$OHOS_LIBNAME-$ARCH-build $MAKE_THREADS_CNT
    cmake --install output/$OHOS_LIBNAME-$ARCH-build
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}