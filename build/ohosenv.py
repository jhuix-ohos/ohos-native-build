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
    env['CFLAGS'] = '-DOHOS_NDK -fPIC -D__MUSL__=1'
    env['CXXFLAGS'] = '-DOHOS_NDK -fPIC -D__MUSL__=1'    
    env['LDFLAGS']=''      
    if arch == "armeabi-v7a":
        env['HOST_ARCH'] = 'linux-generic32'
        env['CC'] = sdkDir +'/native/llvm/bin/arm-linux-ohos-clang'
        env['CXX'] = sdkDir +'/native/llvm/bin/arm-linux-ohos-clang++'
        env['CFLAGS'] = env['CFLAGS'] + ' -march=armv7a'
        env['CXXFLAGS'] = env['CXXFLAGS'] + ' -march=armv7a'
    elif arch == "arm64-v8a":
        env['HOST_ARCH'] = 'linux-aarch64'
        env['CC'] = sdkDir +'/native/llvm/bin/aarch64-linux-ohos-clang'
        env['CXX'] = sdkDir +'/native/llvm/bin/aarch64-linux-ohos-clang++'
    elif arch == "x86_64":
        env['HOST_ARCH'] = 'linux-x86_64'
        env['CC'] = sdkDir +'/native/llvm/bin/x86_64-linux-ohos-clang'
        env['CXX'] = sdkDir +'/native/llvm/bin/x86_64-linux-ohos-clang++'
    else :
        print('[ERROR] ' + arch +' not support')
    return env
