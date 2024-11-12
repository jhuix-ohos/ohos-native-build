import sys

def setEnv(arch, sdkDir) :
    env = {}
    env['ARCH'] = arch
    env['AS'] = sdkDir +'/native/llvm/bin/llvm-as'
    env['LD'] = sdkDir +'/native/llvm/bin/ld.lld'
    env['STRIP'] = sdkDir +'/native/llvm/bin/llvm-strip'
    env['RANLIB'] = sdkDir +'/native/llvm/bin/llvm-ranlib'
    env['OBJDUMP'] = sdkDir +'/native/llvm/bin/llvm-objdump'
    env['OBJCOPY'] = sdkDir +'/native/llvm/bin/llvm-objcopy'
    env['NM'] = sdkDir +'/native/llvm/bin/llvm-nm'
    env['AR'] = sdkDir +'/native/llvm/bin/llvm-ar'
    env['CFLAGS'] = '-DOHOS_NDK -fPIC'
    env['CXXFLAGS'] = '-DOHOS_NDK -fPIC'
    env['LDFLAGS'] = ''
    env['BUILD_OS'] = sys.platform
    env['CMAKE_PREFIX_ARGS'] = '-LH -DCMAKE_SKIP_RPATH=ON -DCMAKE_SKIP_INSTALL_RPATH=ON'
    if env['BUILD_OS'] == "win": 
        env['CMAKE_PREFIX_ARGS'] = env['CMAKE_PREFIX_ARGS'] + ' -G"Unix Makefiles"'
        env['CMAKE_PREFIX_ARGS'] = env['CMAKE_PREFIX_ARGS'] \
                             + ' -DCMAKE_INSTALL_PREFIX=%USED_PREFIX%/%ARCH%' \
                             + ' -DCMAKE_FIND_ROOT_PATH=%USED_PREFIX%/%ARCH%' \
                             + ' -DOHOS_ARCH=%ARCH%' \
                             + ' -DOHOS_STL=c++_static' \
                             + ' -DCMAKE_TOOLCHAIN_FILE="%OHOS_SDK%/native/build/cmake/ohos.toolchain.cmake"' \
                             + ' -GNinja -DCMAKE_MAKE_PROGRAM="%OHOS_SDK%/native/build-tools/cmake/bin/ninja.exe"' \
                             + ' -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument -Wno-unused-parameter -Wno-unused-variable"' \
                             + ' -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument -Wno-unused-parameter -Wno-unused-variable"'
    else:
        env['CMAKE_PREFIX_ARGS'] = env['CMAKE_PREFIX_ARGS'] \
                             + ' -DCMAKE_INSTALL_PREFIX=$USED_PREFIX/$ARCH' \
                             + ' -DCMAKE_FIND_ROOT_PATH=$USED_PREFIX/$ARCH' \
                             + ' -DOHOS_ARCH=$ARCH' \
                             + ' -DOHOS_STL=c++_static' \
                             + ' -DCMAKE_TOOLCHAIN_FILE="$OHOS_SDK/native/build/cmake/ohos.toolchain.cmake"' \
                             + ' -GNinja -DCMAKE_MAKE_PROGRAM="$OHOS_SDK/native/build-tools/cmake/bin/ninja.exe"' \
                             + ' -DCMAKE_C_FLAGS="-Wno-unused-command-line-argument -Wno-unused-parameter -Wno-unused-variable"' \
                             + ' -DCMAKE_CXX_FLAGS="-Wno-unused-command-line-argument -Wno-unused-parameter -Wno-unused-variable"'

    if arch == "armeabi-v7a":
        env['TARGET'] = 'arm'
        env['PLATFORM_NAME'] = 'arm'
        env['HOST_ARCH'] = 'linux-generic32'
        # env['CC'] = sdkDir +'/native/llvm/bin/arm-linux-ohos-clang'
        # env['CXX'] = sdkDir +'/native/llvm/bin/arm-linux-ohos-clang++'
        # env['CFLAGS'] = env['CFLAGS'] + ' -march=armv7a'
        # env['CXXFLAGS'] = env['CXXFLAGS'] + ' -march=armv7a'
        env['CC'] = sdkDir +'/native/llvm/bin/clang -target arm-linux-ohos --sysroot=' + sdkDir +'/native/sysroot' + ' -D__MUSL__ -march=armv7-a -mfloat-abi=softfp -mtune=generic-armv7-a -mthumb'
        env['CXX'] = sdkDir +'/native/llvm/bin/clang++ -target arm-linux-ohos --sysroot=' + sdkDir +'/native/sysroot' + ' -D__MUSL__ -march=armv7-a -mfloat-abi=softfp -mtune=generic-armv7-a -mthumb'
    elif arch == "arm64-v8a":
        env['TARGET'] = 'aarch64'
        env['PLATFORM_NAME'] = 'arm64'
        env['HOST_ARCH'] = 'linux-aarch64'
        # env['CC'] = sdkDir +'/native/llvm/bin/aarch64-linux-ohos-clang'
        # env['CXX'] = sdkDir +'/native/llvm/bin/aarch64-linux-ohos-clang++'
        env['CC'] = sdkDir +'/native/llvm/bin/clang -target aarch64-linux-ohos --sysroot='+ sdkDir +'/native/sysroot -D__MUSL__'
        env['CXX'] = sdkDir +'/native/llvm/bin/clang++ -target aarch64-linux-ohos --sysroot='+ sdkDir +'/native/sysroot -D__MUSL__'
    elif arch == "x86_64":
        env['TARGET'] = 'x86_64'
        env['PLATFORM_NAME'] = 'x64'
        env['HOST_ARCH'] = 'linux-x86_64'
        # env['CC'] = sdkDir +'/native/llvm/bin/x86_64-linux-ohos-clang'
        # env['CXX'] = sdkDir +'/native/llvm/bin/x86_64-linux-ohos-clang++'
        env['CC'] = sdkDir +'/native/llvm/bin/clang -target x86_64-linux-ohos --sysroot='+ sdkDir +'/native/sysroot -D__MUSL__'
        env['CXX'] = sdkDir +'/native/llvm/bin/clang++ -target x86_64-linux-ohos --sysroot='+ sdkDir +'/native/sysroot -D__MUSL__'
    else :
        print('[ERROR] ' + arch +' not support')
    return env
