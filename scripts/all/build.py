def build() :
    return {
        'name': 'all',
        'depends': ['zlib', 'mozjpeg', 'opus', 'openssl'],
        'commands': """
win:
    if not exist "all" mkdir all
    echo "More libs of harmony on %TARGET% platform be building..."
unix:
    if [ ! -d "all" ] ; then
       mkdir all
    fi
    echo "More libs of harmony on $TARGET platform be building..."
"""
    }