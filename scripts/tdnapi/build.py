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
      SET CFLAGS_BACKUP_=%CFLAGS%
      SET CXXFLAGS_BACKUP_=%CXXFLAGS%
      SET CFLAGS=
      SET CXXFLAGS=
      cmake -DTD_GENERATE_SOURCE_FILES=ON -Boutput/%OHOS_LIBNAME%-gen-build -Std
      cmake --build output/%OHOS_LIBNAME%-gen-build
      SET CFLAGS=%CFLAGS_BACKUP_%
      SET CXXFLAGS=%CXXFLAGS_BACKUP_%
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
    if ![ -d "td" ] ; then
      git clone $OHOS_LIBURL
      cd td
      git apply $SCRIPT_DIR/../scripts/tdnapi/0001-Add-tdnapi-example-for-HarmonyOS.patch
      cd ..
    fi

    if ![ -d "output/%OHOS_LIBNAME%-gen-build" ] ; then
      echo "Generating TDLib source files..."
      cmake -DTD_GENERATE_SOURCE_FILES=ON -Boutput/%OHOS_LIBNAME%-gen-build -Std
      cmake --build output/%OHOS_LIBNAME%-gen-build
    fi

    export OPENSSL_INSTALL_DIR=$USED_PREFIX/%ARCH%

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
          -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja.exe" \\
          -Boutput/%OHOS_LIBNAME%-%ARCH%-build \\
          -Std/example/ohos
    cmake --build output/%OHOS_LIBNAME%-%ARCH%-build --target tdnapi
    cmake --install output/%OHOS_LIBNAME%-%ARCH%-build --component tdnapi
    cp -p $SCRIPT_DIR/../scripts/tdnapi/src $USED_PREFIX/harmony/$OHOS_LIBNAME/src/
"""
    }