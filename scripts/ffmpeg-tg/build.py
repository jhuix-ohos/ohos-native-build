def build() :
    return {
    'name': 'ffmpeg-tg',
    'src': 'ffmpeg',
    'url': 'https://github.com/FFmpeg/FFmpeg.git',
    'commands': """
win:
    if not exist "%OHOS_LIBSRC%" (
      git clone "%OHOS_LIBURL%" "%OHOS_LIBSRC%"
    )
    if not exist "output\\%OHOS_LIBNAME%-%ARCH%-build" mkdir "output\\%OHOS_LIBNAME%-%ARCH%-build"
    cd "output\\%OHOS_LIBNAME%-%ARCH%-build"

    set TARGET_OPT=--enable-neon --disable-x86asm
    if "%TARGET%" == "x86_64" set TARGET_OPT=
    
    set PKG_CONFIG_PATH=%USED_PREFIX%/%ARCH%/lib/pkgconfig
    perl ../../%OHOS_LIBSRC%/configure --prefix=%USED_PREFIX%/%OHOS_LIBNAME%/%ARCH% ^
        --enable-cross-compile ^
        --target-os=linux ^
        --arch=%TARGET% ^
        --cc="%CC%" --cxx="%CXX%" --ld="%CXX%" --nm="%NM%" --strip="%STRIP%" --ar="%AR%" --ranlib="%RANLIB%" ^
        --host-cc="%CC%" --host-ld="%CXX%" --host-os=linux ^
        --extra-cflags="-DCONFIG_SAFE_BITSTREAM_READER=1 -Wno-unused-command-line-argument -Wno-int-conversion -Wno-unused-label -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --extra-cxxflags="-DCONFIG_SAFE_BITSTREAM_READER=1 -Wno-unused-command-line-argument -Wno-int-conversion -Wno-unused-label -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --disable-programs ^
        --disable-doc ^
        --disable-htmlpages ^
        --disable-network ^
        --disable-everything ^
        --disable-vulkan ^
        --enable-static ^
        --disable-shared ^
        %TARGET_OPT% ^
        --enable-asm ^
        --enable-protocol=file ^
        --enable-libdav1d ^
        --enable-libopenh264 ^
        --enable-libopus ^
        --enable-libvpx ^
        --enable-decoder=aac ^
        --enable-decoder=aac_fixed ^
        --enable-decoder=aac_latm ^
        --enable-decoder=aasc ^
        --enable-decoder=ac3 ^
        --enable-decoder=alac ^
        --enable-decoder=av1 ^
        --enable-decoder=eac3 ^
        --enable-decoder=flac ^
        --enable-decoder=gif ^
        --enable-decoder=h264 ^
        --enable-decoder=hevc ^
        --enable-decoder=libdav1d ^
        --enable-decoder=libvpx_vp8 ^
        --enable-decoder=libvpx_vp9 ^
        --enable-decoder=mp1 ^
        --enable-decoder=mp1float ^
        --enable-decoder=mp2 ^
        --enable-decoder=mp2float ^
        --enable-decoder=mp3 ^
        --enable-decoder=mp3adu ^
        --enable-decoder=mp3adufloat ^
        --enable-decoder=mp3float ^
        --enable-decoder=mp3on4 ^
        --enable-decoder=mp3on4float ^
        --enable-decoder=mpeg4 ^
        --enable-decoder=msmpeg4v2 ^
        --enable-decoder=msmpeg4v3 ^
        --enable-decoder=opus ^
        --enable-decoder=pcm_alaw ^
        --enable-decoder=pcm_f32be ^
        --enable-decoder=pcm_f32le ^
        --enable-decoder=pcm_f64be ^
        --enable-decoder=pcm_f64le ^
        --enable-decoder=pcm_lxf ^
        --enable-decoder=pcm_mulaw ^
        --enable-decoder=pcm_s16be ^
        --enable-decoder=pcm_s16be_planar ^
        --enable-decoder=pcm_s16le ^
        --enable-decoder=pcm_s16le_planar ^
        --enable-decoder=pcm_s24be ^
        --enable-decoder=pcm_s24daud ^
        --enable-decoder=pcm_s24le ^
        --enable-decoder=pcm_s24le_planar ^
        --enable-decoder=pcm_s32be ^
        --enable-decoder=pcm_s32le ^
        --enable-decoder=pcm_s32le_planar ^
        --enable-decoder=pcm_s64be ^
        --enable-decoder=pcm_s64le ^
        --enable-decoder=pcm_s8 ^
        --enable-decoder=pcm_s8_planar ^
        --enable-decoder=pcm_u16be ^
        --enable-decoder=pcm_u16le ^
        --enable-decoder=pcm_u24be ^
        --enable-decoder=pcm_u24le ^
        --enable-decoder=pcm_u32be ^
        --enable-decoder=pcm_u32le ^
        --enable-decoder=pcm_u8 ^
        --enable-decoder=vorbis ^
        --enable-decoder=vp8 ^
        --enable-decoder=wavpack ^
        --enable-decoder=wmalossless ^
        --enable-decoder=wmapro ^
        --enable-decoder=wmav1 ^
        --enable-decoder=wmav2 ^
        --enable-decoder=wmavoice ^
        --enable-encoder=aac ^
        --enable-encoder=libopus ^
        --enable-encoder=libopenh264 ^
        --enable-filter=atempo ^
        --enable-parser=aac ^
        --enable-parser=aac_latm ^
        --enable-parser=flac ^
        --enable-parser=gif ^
        --enable-parser=h264 ^
        --enable-parser=hevc ^
        --enable-parser=mpeg4video ^
        --enable-parser=mpegaudio ^
        --enable-parser=opus ^
        --enable-parser=vorbis ^
        --enable-demuxer=aac ^
        --enable-demuxer=flac ^
        --enable-demuxer=gif ^
        --enable-demuxer=h264 ^
        --enable-demuxer=hevc ^
        --enable-demuxer=matroska ^
        --enable-demuxer=m4v ^
        --enable-demuxer=mov ^
        --enable-demuxer=mp3 ^
        --enable-demuxer=ogg ^
        --enable-demuxer=wav ^
        --enable-muxer=mp4 ^
        --enable-muxer=ogg ^
        --enable-muxer=opus
    
    make %MAKE_THREADS_CNT%
    make install
unix:
    if ![ -d "$OHOS_LIBSRC" ] ; then
      git clone "$OHOS_LIBURL" "$OHOS_LIBSRC"
    fi

    mkdir -p "output\\$OHOS_LIBNAME-$ARCH-build"

    export TARGET_OPT=--enable-neon --disable-x86asm
    if [ "$TARGET" e "x86_64" ]; then
      export TARGET_OPT=
    fi
    export PKG_CONFIG_PATH=$USED_PREFIX/$ARCH/lib/pkgconfig
    ../../$OHOS_LIBSRC/configure --prefix=$USED_PREFIX/$OHOS_LIBNAME/$ARCH ^
        --enable-cross-compile ^
        --target-os=linux ^
        --arch=$TARGET ^
        --cc="${CC}" --cxx="${CXX}" --ld="${CXX}" --nm="${NM}" --strip="${STRIP}" --ar="${AR}" --ranlib="${RANLIB}" ^
        --host-cc="${CC}" --host-ld="${CXX}" --host-os=linux ^
        --extra-cflags="-DCONFIG_SAFE_BITSTREAM_READER=1 -Wno-unused-command-line-argument -Wno-int-conversion -Wno-unused-label -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --extra-cxxflags="-DCONFIG_SAFE_BITSTREAM_READER=1 -Wno-unused-command-line-argument -Wno-int-conversion -Wno-unused-label -Wno-deprecated-declarations -Wno-enum-conversion" ^
        --disable-programs ^
        --disable-doc ^
        --disable-htmlpages ^
        --disable-network ^
        --disable-everything ^
        --disable-vulkan ^
        --enable-static ^
        --disable-shared ^
        $TARGET_OPT ^
        --enable-asm ^
        --enable-protocol=file ^
        --enable-libdav1d ^
        --enable-libopenh264 ^
        --enable-libopus ^
        --enable-libvpx ^
        --enable-decoder=aac ^
        --enable-decoder=aac_fixed ^
        --enable-decoder=aac_latm ^
        --enable-decoder=aasc ^
        --enable-decoder=ac3 ^
        --enable-decoder=alac ^
        --enable-decoder=av1 ^
        --enable-decoder=eac3 ^
        --enable-decoder=flac ^
        --enable-decoder=gif ^
        --enable-decoder=h264 ^
        --enable-decoder=hevc ^
        --enable-decoder=libdav1d ^
        --enable-decoder=libvpx_vp8 ^
        --enable-decoder=libvpx_vp9 ^
        --enable-decoder=mp1 ^
        --enable-decoder=mp1float ^
        --enable-decoder=mp2 ^
        --enable-decoder=mp2float ^
        --enable-decoder=mp3 ^
        --enable-decoder=mp3adu ^
        --enable-decoder=mp3adufloat ^
        --enable-decoder=mp3float ^
        --enable-decoder=mp3on4 ^
        --enable-decoder=mp3on4float ^
        --enable-decoder=mpeg4 ^
        --enable-decoder=msmpeg4v2 ^
        --enable-decoder=msmpeg4v3 ^
        --enable-decoder=opus ^
        --enable-decoder=pcm_alaw ^
        --enable-decoder=pcm_f32be ^
        --enable-decoder=pcm_f32le ^
        --enable-decoder=pcm_f64be ^
        --enable-decoder=pcm_f64le ^
        --enable-decoder=pcm_lxf ^
        --enable-decoder=pcm_mulaw ^
        --enable-decoder=pcm_s16be ^
        --enable-decoder=pcm_s16be_planar ^
        --enable-decoder=pcm_s16le ^
        --enable-decoder=pcm_s16le_planar ^
        --enable-decoder=pcm_s24be ^
        --enable-decoder=pcm_s24daud ^
        --enable-decoder=pcm_s24le ^
        --enable-decoder=pcm_s24le_planar ^
        --enable-decoder=pcm_s32be ^
        --enable-decoder=pcm_s32le ^
        --enable-decoder=pcm_s32le_planar ^
        --enable-decoder=pcm_s64be ^
        --enable-decoder=pcm_s64le ^
        --enable-decoder=pcm_s8 ^
        --enable-decoder=pcm_s8_planar ^
        --enable-decoder=pcm_u16be ^
        --enable-decoder=pcm_u16le ^
        --enable-decoder=pcm_u24be ^
        --enable-decoder=pcm_u24le ^
        --enable-decoder=pcm_u32be ^
        --enable-decoder=pcm_u32le ^
        --enable-decoder=pcm_u8 ^
        --enable-decoder=vorbis ^
        --enable-decoder=vp8 ^
        --enable-decoder=wavpack ^
        --enable-decoder=wmalossless ^
        --enable-decoder=wmapro ^
        --enable-decoder=wmav1 ^
        --enable-decoder=wmav2 ^
        --enable-decoder=wmavoice ^
        --enable-encoder=aac ^
        --enable-encoder=libopus ^
        --enable-encoder=libopenh264 ^
        --enable-filter=atempo ^
        --enable-parser=aac ^
        --enable-parser=aac_latm ^
        --enable-parser=flac ^
        --enable-parser=gif ^
        --enable-parser=h264 ^
        --enable-parser=hevc ^
        --enable-parser=mpeg4video ^
        --enable-parser=mpegaudio ^
        --enable-parser=opus ^
        --enable-parser=vorbis ^
        --enable-demuxer=aac ^
        --enable-demuxer=flac ^
        --enable-demuxer=gif ^
        --enable-demuxer=h264 ^
        --enable-demuxer=hevc ^
        --enable-demuxer=matroska ^
        --enable-demuxer=m4v ^
        --enable-demuxer=mov ^
        --enable-demuxer=mp3 ^
        --enable-demuxer=ogg ^
        --enable-demuxer=wav ^
        --enable-muxer=mp4 ^
        --enable-muxer=ogg ^
        --enable-muxer=opus
    
    make $MAKE_THREADS_CNT
    make install    
"""}