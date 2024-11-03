def build() :
    return {
        'name': 'zlib',
        'commands': """
win:
    if not exist "zlib" (
      git clone https://github.com/madler/zlib.git
      cd zlib
      git checkout 643e17b749
      cd ..
    )
    if not exist "output" mkdir output
    cd output
    if exist "zlib-%ARCH%-build" rmdir /S /Q zlib-%ARCH%-build
    mkdir zlib-%ARCH%-build
    cd zlib-%ARCH%-build
        
    perl ../../zlib/configure ^
        --static ^
        --prefix=%USED_PREFIX%/zlib/%ARCH%
    make %MAKE_THREADS_CNT%
    make install
mac:
    if ![ -d "zlib" ] ; then
      git clone https://github.com/madler/zlib.git
      cd zlib
      git checkout 643e17b749
      cd ..
    fi
    rm -rf output/zlib-$ARCH-build
    mkdir -p output/zlib-$ARCH-build
    cd output/zlib-$ARCH-build
    
    ../../zlib/configure \\
        --static \\
        --prefix=$USED_PREFIX/zlib/$ARCH
    make $MAKE_THREADS_CNT
    make install
"""
    }