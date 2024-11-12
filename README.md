# OHOS-Native-Build

A build set of native C/C++ third-party libraries for HarmonyOS on the Windows|MacOS|Linux platform. 

## Build

- Download Python >=3.7 installer from https://www.python.org/downloads/ and install it with adding to PATH.

- Install meson build on Mac or Linux platform: 
  
       python3 -m pip install meson

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

## The supported libraries

|Name|Version|
|----|----|
|[zlib](https://github.com/madler/zlib.git)|main|
|[mozjpeg](https://github.com/mozilla/mozjpeg.git)|main|
|[opus](https://github.com/xiph/opus.git)|main|
|[openssl](https://github.com/openssl/openssl/archive/refs/tags/openssl-3.3.2.tar.gz)|3.3.2|
|[openssl_1_1_1](https://github.com/openssl/openssl.git)|OpenSSL_1_1_1-stable|
|[openssl_1_0_2](https://github.com/openssl/openssl.git)|OpenSSL_1_0_2-stable|
|[libyuv](https://chromium.googlesource.com/libyuv/libyuv)|main|
|[libwebp](https://github.com/webmproject/libwebp.git)|main|
|[openh264](https://github.com/cisco/openh264.git)|main|
|[dav1d](https://code.videolan.org/videolan/dav1d.git)|main|
|[libde265](https://github.com/strukturag/libde265.git)|main|
|[libvpx](https://github.com/webmproject/libvpx.git)|main|
|[libjxl](https://github.com/libjxl/libjxl.git)|main|
|[libavif](https://github.com/AOMediaCodec/libavif.git)|main|
|[libheif](https://github.com/strukturag/libheif.git)|main|
|[ffmepg](https://github.com/FFmpeg/FFmpeg.git)|main|
|[ffmepg](https://github.com/FFmpeg/FFmpeg.git) for telegram|main|
|tdnapi|[tdlib](https://github.com/tdlib/td.git) main|

## License

[MIT](https://github.com/jhuix-ohos/ohos-native-build/blob/master/LICENSE)

Copyright © 2023-present, Jhuix (Hui Jin) All Rights Reserved.
