def build() :
    return {
    'name': 'libyuv',
    'url': 'https://chromium.googlesource.com/libyuv/libyuv',
    'depends': ['mozjpeg'],
    'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone %OHOS_LIBURL%
    )

    set PKG_CONFIG_PATH=%USED_PREFIX%/%ARCH%/lib/pkgconfig;%PKG_CONFIG_PATH%
    cmake %CMAKE_PREFIX_ARGS% ^
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON ^
        -DCMAKE_BUILD_TYPE=Release ^
        -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
        -S%OHOS_LIBNAME%
    
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --target yuv %MAKE_THREADS_CNT%
    xcopy output\\%OHOS_LIBNAME%-%ARCH%-build\\libyuv.a "local\\%ARCH%\\lib\\" /S /Y
    xcopy %OHOS_LIBNAME%\\include "local\\%ARCH%\\include" /S /Y
    xcopy output\\%OHOS_LIBNAME%-%ARCH%-build\\libyuv.a "local\\%OHOS_LIBNAME%\%ARCH%\\lib\\" /S /Y
    xcopy %OHOS_LIBNAME%\\include "local\\%OHOS_LIBNAME%\\%ARCH%\\include" /S /Y
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi

    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    cmake $CMAKE_PREFIX_ARGS \\
        -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument" \\
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON \\
        -DCMAKE_BUILD_TYPE=Release \\
        -B output/$OHOS_LIBNAME-$ARCH-build \\
        -S $OHOS_LIBNAME
    
    cmake --build output/$OHOS_LIBNAME-$ARCH-build --target yuv $MAKE_THREADS_CNT
    mkdir -p local/$ARCH/lib
    mkdir -p local/$ARCH/include
    cp -f output/$OHOS_LIBNAME-$ARCH-build/libyuv.a "local/$ARCH/lib/"
    cp -rf $OHOS_LIBNAME/include "local/$ARCH/include"
    mkdir -p local/$OHOS_LIBNAME/$ARCH/lib
    mkdir -p local/$OHOS_LIBNAME/$ARCH/include
    cp -f output/$OHOS_LIBNAME-$ARCH-build/libyuv.a "local/$OHOS_LIBNAME/$ARCH/lib/"
    cp -rf $OHOS_LIBNAME/include "local/$OHOS_LIBNAME/$ARCH/include"
"""}