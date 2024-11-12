# OHOS-Native-Build

A build set of native C/C++ third-party libraries for HarmonyOS on the Windows|MacOS|Linux platform. 

## Build

Download Python >=3 installer from https://www.python.org/downloads/ and install it with adding to PATH.

* Params

|name|desc.|
|----|----|
|ohos_sdk|HarmonyOS's sdk path. For expamle on windows platform: <br> I:\DevTools\Huawei\OpenHarmony\Sdk\12 |
|proxy|Proxy address for download or git. |
|archs|CPU architecture identifier for compiling libraries, separated by commas for multiple CPU architecture. For examples: <br> arm64-v8a,x86_64,armeabi-v7a |
|libs|Library names that need to be compiled, separated by commas for multiple libraries.|



* Windows example

        mkdir ohos
        cd ohos
        git clone https://github.com/jhuix-ohos/ohos-native-build.git
        cd ohos-native-build\build
        build --ohos_sdk=%YOUR_OHOS_SDK%  --archs=arm64-v8a,x86_64 --libs=zlib,tdnapi --proxy=http://127.0.0.1:10808

* Mac or Linux example

        mkdir ohos
        cd ohos
        git clone https://github.com/jhuix-ohos/ohos-native-build.git
        cd ohos-native-build\build
        build --ohos_sdk=$YOUR_OHOS_SDK  --archs=arm64-v8a,x86_64 --libs=zlib,tdnapi
