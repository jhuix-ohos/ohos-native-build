def build() :
    return {
    'name': 'libwebp',
    'url': 'https://github.com/webmproject/libwebp.git',
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
        -DCMAKE_BUILD_TYPE=Release ^
        -DWEBP_BUILD_ANIM_UTILS=OFF ^
        -DWEBP_BUILD_CWEBP=OFF ^
        -DWEBP_BUILD_DWEBP=OFF ^
        -DWEBP_BUILD_GIF2WEBP=OFF ^
        -DWEBP_BUILD_IMG2WEBP=OFF ^
        -DWEBP_BUILD_VWEBP=OFF ^
        -DWEBP_BUILD_WEBPMUX=OFF ^
        -DWEBP_BUILD_WEBPINFO=OFF ^
        -DWEBP_BUILD_EXTRAS=OFF ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build %MAKE_THREADS_CNT%
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --prefix %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi

    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    cmake $CMAKE_PREFIX_ARGS ^
        -DCMAKE_BUILD_TYPE=Release ^
        -DWEBP_BUILD_ANIM_UTILS=OFF ^
        -DWEBP_BUILD_CWEBP=OFF ^
        -DWEBP_BUILD_DWEBP=OFF ^
        -DWEBP_BUILD_GIF2WEBP=OFF ^
        -DWEBP_BUILD_IMG2WEBP=OFF ^
        -DWEBP_BUILD_VWEBP=OFF ^
        -DWEBP_BUILD_WEBPMUX=OFF ^
        -DWEBP_BUILD_WEBPINFO=OFF ^
        -DWEBP_BUILD_EXTRAS=OFF ^
        -B output/$OHOS_LIBNAME-$ARCH-build ^
        -S $OHOS_LIBNAME
    cmake --build output/output/$OHOS_LIBNAME-$ARCH-build $MAKE_THREADS_CNT
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build
    cmake --install output/output/$OHOS_LIBNAME-$ARCH-build --prefix $USED_PREFIX/$OHOS_LIBNAME/$ARCH
"""}