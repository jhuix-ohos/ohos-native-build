def build() :
    return {
        'name': 'tdnapi',
        'commands': """
win:
    if not exist "td" (
      git clone https://github.com/tdlib/td.git
      cd td
      git apply %SCRIPT_DIR%/../scripts/tdnapi/0001-Add-tdnapi-example-for-HarmonyOS.patch
      cd ..
    )
    if not exist "output" mkdir output
    cd output
    if not exist "tdjson-gen-build" (
      echo "Generating TDLib source files..."
      mkdir tdjson-gen-build
      cd tdjson-gen-build
      SET CFLAGS_BACKUP_=%CFLAGS%
      SET CXXFLAGS_BACKUP_=%CXXFLAGS%
      SET CFLAGS=
      SET CXXFLAGS=
      cmake -DTD_GENERATE_SOURCE_FILES=ON ../../td
      cmake --build .
      SET CFLAGS=%CFLAGS_BACKUP_%
      SET CXXFLAGS=%CXXFLAGS_BACKUP_%
      cd ..
    )

    if exist "tdnapi-%ARCH%-build" rmdir /S /Q tdnapi-%ARCH%-build
    mkdir tdnapi-%ARCH%-build
    cd tdnapi-%ARCH%-build
    set OPENSSL_INSTALL_DIR=%USED_PREFIX%

    cmake -LH ^
          -DCMAKE_INSTALL_PREFIX=%USED_PREFIX%/tdnapi/%ARCH% ^
          -DCMAKE_SKIP_RPATH=ON ^
          -DCMAKE_SKIP_INSTALL_RPATH=ON ^
          -DOHOS_ARCH=%ARCH% ^
          -DOHOS_STL=c++_static ^
          -DTD_OHOS_JSON_NAPI=1 ^
          -DCMAKE_BUILD_TYPE=RelWithDebInfo ^
          -DOPENSSL_ROOT_DIR:PATH="%OPENSSL_INSTALL_DIR%/openssl/%ARCH%" ^
          -DCMAKE_TOOLCHAIN_FILE="%OHOS_SDK%/native/build/cmake/ohos.toolchain.cmake" ^
          -GNinja -DCMAKE_MAKE_PROGRAM="%OHOS_SDK%/native/build-tools/cmake/bin/ninja.exe" ^
          ../../td/example/ohos
    cmake --build . --target tdnapi
    xcopy libtd*.so* ..\\..\\local\\tdnapi\\%ARCH%\\lib\\ /S /Y
    xcopy %SCRIPT_DIR%\\..\\scripts\\tdnapi\\cpp ..\\..\\local\\tdnapi\\%ARCH%\\ /S /Y
unix:
    if ![ -d "td" ] ; then
      git clone https://github.com/tdlib/td.git
      cd td
      git apply $SCRIPT_DIR/../scripts/tdnapi/0001-Add-tdnapi-example-for-HarmonyOS.patch
      cd ..
    fi

    if ![ -d "tdjson-gen-build" ] ; then
      echo "Generating TDLib source files..."
      mkdir tdjson-gen-build
      cd tdjson-gen-build
      cmake -DTD_GENERATE_SOURCE_FILES=ON ../../td
      cmake --build .
      cd ..
    fi

    rm -rf output/tdnapi-$ARCH-build
    mkdir -p output/tdnapi-$ARCH-build
    cd output/tdnapi-$ARCH-build
    export OPENSSL_INSTALL_DIR=$USED_PREFIX

    cmake -LH \
          -DCMAKE_INSTALL_PREFIX=$USED_PREFIX/tdnapi/$ARCH \
          -DCMAKE_SKIP_RPATH=ON \
          -DCMAKE_SKIP_INSTALL_RPATH=ON \
          -DOHOS_ARCH=$ARCH \
          -DOHOS_STL=c++_static \
          -DTD_OHOS_JSON_NAPI=1 \
          -DCMAKE_BUILD_TYPE=RelWithDebInfo \
          -DOPENSSL_ROOT_DIR:PATH="$OPENSSL_INSTALL_DIR/openssl/$ARCH" \
          -DCMAKE_TOOLCHAIN_FILE="$OHOS_SDK/native/build/cmake/ohos.toolchain.cmake" \
          -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja.exe" \
          ../../td/example/ohos
    cmake --build . --target tdnapi
    mkdir -p ../../local/tdnapi/$ARCH/bin
    cp -p libtd*.so* ../../local/tdnapi/$ARCH/bin/
    cp -p $SCRIPT_DIR/../scripts/tdnapi/cpp ../../local/tdnapi/$ARCH/
"""
    }