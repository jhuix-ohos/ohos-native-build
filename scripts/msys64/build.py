def build() :
    return {
        'name': 'msys64',
        'location': 'thirdparty',
        'commands': """
win:
    SET PATH_BACKUP_=%PATH%
    SET PATH=%ROOT_DIR%\\thirdparty\\msys64\\usr\\bin;%PATH%

    SET CHERE_INVOKING=enabled_from_arguments
    SET MSYS2_PATH_TYPE=inherit

    if not exist "msys64" (
      powershell -Command "iwr -OutFile ./msys64.exe https://repo.msys2.org/distrib/x86_64/msys2-base-x86_64-20240727.sfx.exe"
      msys64.exe
      del msys64.exe
      bash -c "pacman-key --init; pacman-key --populate; pacman -Syu --noconfirm"
      pacman -Syu --noconfirm unzip gzip gperf make perl-Pod-Parser diffutils git mingw-w64-x86_64-perl mingw-w64-x86_64-meson mingw-w64-x86_64-nasm mingw-w64-x86_64-binutils
    )
    SET PATH=%PATH_BACKUP_%
"""
    }
