# Somehow in x86 Debug build dav1d crashes on AV1 10bpc videos.
def build() :
    return {
    'name': 'dav1d',
    'url': 'https://code.videolan.org/videolan/dav1d.git',
    'commands': """
win:
    if not exist "%OHOS_LIBNAME%" (
      git clone %OHOS_LIBURL%
    )

    cd %OHOS_LIBNAME%
    set FILE=cross-file.txt
    echo [constants] > %FILE%
    echo ohos_sdk='%OHOS_SDK%' >> %FILE%
    echo pkg_path='%THIRDPARTY_DIR%/msys64/mingw64/bin' >> %FILE%

    meson setup --cross-file %FILE% ^
          --cross-file "%SCRIPT_DIR%/meson/ohos_meson_%TARGET%.txt" ^
          --prefix %USED_PREFIX%/%ARCH% ^
          --default-library=static ^
          --buildtype=minsize ^
          -Denable_tools=false ^
          -Denable_tests=false ^
          ../output/%OHOS_LIBNAME%-%ARCH%-build
    meson compile -C ../output/%OHOS_LIBNAME%-%ARCH%-build
    meson install -C ../output/%OHOS_LIBNAME%-%ARCH%-build
    meson install -C ../output/%OHOS_LIBNAME%-%ARCH%-build --destdir %USED_PREFIX%/%OHOS_LIBNAME%/%ARCH%
    del /Q cross-file.txt
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
    fi

    cd $OHOS_LIBSRC
    export FILE=cross-file.txt
    echo [constants] > $FILE
    echo ohos_sdk="\'"${OHOS_SDK}"\'" >> $FILE
    echo pkg_path="\'"/usr/bin"\'" >> $FILE
    
    meson setup --cross-file $FILE \\
          --cross-file "$SCRIPT_DIR/meson/ohos_meson_$TARGET.txt" \\
          --prefix $USED_PREFIX/$ARCH \\
          --default-library=static \\
          --buildtype=minsize \\
          -Denable_tools=false \\
          -Denable_tests=false \\
          ../output/$OHOS_LIBNAME-$ARCH-build
    meson compile -C ../output/$OHOS_LIBNAME-$ARCH-build
    meson install -C ../output/$OHOS_LIBNAME-$ARCH-build
    meson install -C ../output/$OHOS_LIBNAME-$ARCH-build --destdir $USED_PREFIX/$OHOS_LIBNAME/$ARCH
    rm -f cross-file.txt
"""}