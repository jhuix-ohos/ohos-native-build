# OHOS-Native-Build

A build set of native C/C++ third-party libraries for HarmonyOS on the Windows|MacOS|Linux platform. 

## Build

Download Python >=3 installer from https://www.python.org/downloads/ and install it with adding to PATH.

* Windows

        mkdir ohos
        cd ohos
        git clone https://github.com/jhuix-ohos/ohos-native-build.git
        cd ohos-native-build\build
        build --ohos_sdk=%YOUR_OHOS_SDK%  --archs=arm64-v8a,x86_64 --libs=zlib,tdnapi

* Mac or Linux

        mkdir ohos
        cd ohos
        git clone https://github.com/jhuix-ohos/ohos-native-build.git
        cd ohos-native-build\build
        build --ohos_sdk=$YOUR_OHOS_SDK  --archs=arm64-v8a,x86_64 --libs=zlib,tdnapi

