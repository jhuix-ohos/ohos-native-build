# --enable-librtmp
def build() :
    return {
    'name': 'ffmpeg',
    'url': 'https://github.com/FFmpeg/FFmpeg.git',
    'depends': ['openssl_1_0_2'],
    'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone "%OHOS_LIBURL%" "%OHOS_LIBSRC%"
    )
    if not exist "output\\%OHOS_LIBNAME%-%ARCH%-build" mkdir "output\\%OHOS_LIBNAME%-%ARCH%-build"
    cd "output\\%OHOS_LIBNAME%-%ARCH%-build"

    if "%TARGET%" neq "x86_64" set TARGET_OPT="--enable-neon --disable-x86asm"
    set PKG_CONFIG_PATH=%USED_PREFIX%/openssl_1_0_2/%ARCH%/lib/pkgconfig;%USED_PREFIX%/%ARCH%/lib/pkgconfig
    perl ../../%OHOS_LIBSRC%/configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% ^
        --target-os=linux ^
        --arch=%TARGET% ^
        --cc="%CC%" --cxx="%CXX%" --ld="%CXX%" --nm="%NM%" --strip="%STRIP%" --ar="%AR%" --ranlib="%RANLIB%" ^
        --host-cc="%CC%" --host-ld="%CXX%" --host-os=linux ^
        --extra-cflags="-Wno-unused-command-line-argument -Wno-int-conversion -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --extra-cxxflags="-Wno-unused-command-line-argument -Wno-int-conversion -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --enable-static --disable-shared --disable-programs ^
        %TARGET_OPT% ^
        --enable-cross-compile --enable-asm --enable-network ^
        --disable-vulkan --enable-openssl --enable-protocols ^
        --disable-doc --disable-htmlpages
    
    make %MAKE_THREADS_CNT%
    make install
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone "$OHOS_LIBURL" "$OHOS_LIBSRC"
    fi

    mkdir -p "output/$OHOS_LIBNAME-$ARCH-build"
    cd output/$OHOS_LIBNAME-$ARCH-build

    if [ "$TARGET" != "x86_64" ]; then
      export TARGET_OPT="--enable-neon --disable-x86asm"
    fi
    export PKG_CONFIG_PATH=$USED_PREFIX/openssl_1_0_2/$ARCH/lib/pkgconfig:$USED_PREFIX/$ARCH/lib/pkgconfig
    ../../$OHOS_LIBSRC/configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH \\
        --target-os=linux \\
        --arch=$TARGET \\
        --cc="${CC}" --cxx="${CXX}" --ld="${CXX}" --nm="${NM}" --strip="${STRIP}" --ar="${AR}" --ranlib="${RANLIB}" \\
        --host-cc="${CC}" --host-ld="${CXX}" --host-os=linux \\
        --extra-cflags="-Wno-unused-command-line-argument -Wno-int-conversion -Wno-deprecated-declarations -Wno-enum-conversion" \\
        --extra-cxxflags="-Wno-unused-command-line-argument -Wno-int-conversion -Wno-deprecated-declarations -Wno-enum-conversion" \\
        --enable-static --disable-shared --disable-programs \\
        $TARGET_OPT \\
        --enable-cross-compile --enable-asm --enable-network \\
        --disable-vulkan --enable-openssl --enable-protocols \\
        --disable-doc --disable-htmlpages
    
    make $MAKE_THREADS_CNT
    make install
"""}