def build() :
    return {
        'name': 'tdnapi',
        'src': 'td',
        'url' : 'https://github.com/tdlib/td.git',
        'depends': ['openssl'],
        'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone %OHOS_LIBURL%
    )
    if not exist "td\\example\\ohos" (
      cd td
      git apply %SCRIPT_DIR%/../scripts/tdnapi/0001-Add-tdnapi-example-for-HarmonyOS.patch
      cd ..
    )
    if not exist "output\\%OHOS_LIBNAME%-gen-build" (
      echo "Generating TDLib source files..."
      SET CFLAGS_BACKUP=%CFLAGS%
      SET CXXFLAGS_BACKUP=%CXXFLAGS%
      SET CFLAGS=
      SET CXXFLAGS=
      cmake -DTD_GENERATE_SOURCE_FILES=ON -Boutput/%OHOS_LIBNAME%-gen-build -Std
      cmake --build output/%OHOS_LIBNAME%-gen-build
      SET CFLAGS=%CFLAGS_BACKUP%
      SET CXXFLAGS=%CXXFLAGS_BACKUP%
    )

    set OPENSSL_INSTALL_DIR=%USED_PREFIX%/openssl/%ARCH%
    cmake -LH -DCMAKE_SKIP_RPATH=ON -DCMAKE_SKIP_INSTALL_RPATH=ON -G"Unix Makefiles" ^
          -DCMAKE_INSTALL_PREFIX=%USED_PREFIX%/harmony/%OHOS_LIBNAME% ^
          -DCMAKE_INSTALL_LIBDIR=%USED_PREFIX%/harmony/%OHOS_LIBNAME%/libs/%ARCH% ^
          -DCMAKE_INSTALL_TYPESDIR=%USED_PREFIX%/harmony/%OHOS_LIBNAME%/src/main/cpp/types ^
          -DOHOS_ARCH=%ARCH% ^
          -DOHOS_STL=c++_static ^
          -DTD_OHOS_JSON_NAPI:BOOL=ON ^
          -DCMAKE_BUILD_TYPE=RelWithDebInfo ^
          -DOPENSSL_ROOT_DIR:PATH="%OPENSSL_INSTALL_DIR%" ^
          -DCMAKE_TOOLCHAIN_FILE="%OHOS_SDK%/native/build/cmake/ohos.toolchain.cmake" ^
          -GNinja -DCMAKE_MAKE_PROGRAM="%OHOS_SDK%/native/build-tools/cmake/bin/ninja.exe" ^
          -Boutput/%OHOS_LIBNAME%-%ARCH%-build ^
          -Std/example/ohos
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --target tdnapi
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --component tdnapi
    xcopy %SCRIPT_DIR%\\..\\scripts\\tdnapi\\src local\\harmony\\%OHOS_LIBNAME%\\src\\ /S /Y
unix:
    if [ ! -d "$OHOS_LIBSRC" ] ; then
      git clone $OHOS_LIBURL
      cd td
      git apply $SCRIPT_DIR/../scripts/tdnapi/0001-Add-tdnapi-example-for-HarmonyOS.patch
      cd ..
    fi

    cleanComplieEnv() {
      export CFLAGS_BACKUP=$CFLAGS
      export CXXFLAGS_BACKUP=$CXXFLAGS
      export CC_BACKUP=$CC
      export CXX_BACKUP=$CXX
      export AS_BACKUP=$AS
      export LD_BACKUP=$LD
      export STRIP_BACKUP=$STRIP
      export RANLIB_BACKUP=$RANLIB
      export NM_BACKUP=$NM
      export AR_BACKUP=$AR
      export OBJDUMP_BACKUP=$OBJDUMP
      export OBJCOPY_BACKUP=$OBJCOPY
      export CFLAGS=
      export CXXFLAGS=
      export CC=
      export CXX=
      export AS=
      export LD=
      export STRIP=
      export RANLIB=
      export NM=
      export AR=
      export OBJDUMP=
      export OBJCOPY=
    }

    restoreComplieEnv() {
      export CFLAGS=$CFLAGS_BACKUP
      export CXXFLAGS=$CXXFLAGS_BACKUP
      export CC=$CC_BACKUP
      export CXX=$CXX_BACKUP
      export AS=$AS_BACKUP
      export LD=$LD_BACKUP
      export STRIP=$STRIP_BACKUP
      export RANLIB=$RANLIB_BACKUP
      export NM=$NM_BACKUP
      export AR=$AR_BACKUP
      export OBJDUMP=$OBJDUMP_BACKUP
      export OBJCOPY=$OBJCOPY_BACKUP
      export CFLAGS_BACKUP=
      export CXXFLAGS_BACKUP=
      export CC_BACKUP=
      export CXX_BACKUP=
      export AS_BACKUP=
      export LD_BACKUP=
      export STRIP_BACKUP=
      export RANLIB_BACKUP=
      export NM_BACKUP=
      export AR_BACKUP=
      export OBJDUMP_BACKUP=
      export OBJCOPY_BACKUP=
    }

    if [ ! -d "output/$OHOS_LIBNAME-gen-build" ] ; then
      echo "Generating TDLib source files..."
      cleanComplieEnv

      cmake -DTD_GENERATE_SOURCE_FILES=ON -B output/$OHOS_LIBNAME-gen-build -S td
      cmake --build output/$OHOS_LIBNAME-gen-build

      restoreComplieEnv
    fi

    export OPENSSL_INSTALL_DIR=$USED_PREFIX/openssl/$ARCH

    cmake -LH \\
          -DCMAKE_INSTALL_PREFIX=$USED_PREFIX/harmony/$OHOS_LIBNAME/libs/$ARCH \\
          -DCMAKE_SKIP_RPATH=ON \\
          -DCMAKE_SKIP_INSTALL_RPATH=ON \\
          -DOHOS_ARCH=$ARCH \\
          -DOHOS_STL=c++_static \\
          -DTD_OHOS_JSON_NAPI=1 \\
          -DCMAKE_BUILD_TYPE=RelWithDebInfo \\
          -DOPENSSL_ROOT_DIR:PATH="$OPENSSL_INSTALL_DIR" \\
          -DCMAKE_TOOLCHAIN_FILE="$OHOS_SDK/native/build/cmake/ohos.toolchain.cmake" \\
          -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja" \\
          -B output/$OHOS_LIBNAME-$ARCH-build \\
          -S td/example/ohos
    cmake --build output/$OHOS_LIBNAME-$ARCH-build --target tdnapi
    cmake --install output/$OHOS_LIBNAME-$ARCH-build --component tdnapi
    mkdir -p "$USED_PREFIX/harmony/$OHOS_LIBNAME"
    cp -rf "$SCRIPT_DIR/../scripts/$OHOS_LIBNAME/src" "$USED_PREFIX/harmony/$OHOS_LIBNAME/"
"""
    }