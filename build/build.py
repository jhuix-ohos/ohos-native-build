import os, sys, re, pathlib, hashlib, subprocess, glob, shutil, importlib.util, ohosenv

executePath = os.getcwd()
scriptPath = os.path.dirname(__file__ if not os.path.islink(__file__) else os.path.realpath(__file__))

def finish(code):
    global executePath
    os.chdir(executePath)
    sys.exit(code)

def error(text):
    print('[ERROR] ' + text)
    finish(1)

def nativeToolsError():
    error('Make sure to run from Native Tools Command Prompt.')

win = (sys.platform == 'win32')
mac = (sys.platform == 'darwin')
linux = (sys.platform == 'linux')

# if win and not 'Platform' in os.environ:
#    nativeToolsError()

if win and not 'COMSPEC' in os.environ:
    error('COMSPEC environment variable is not set.')

os.chdir(scriptPath + '/../..')

pathSep = ';' if win else ':'
libsLoc = 'libraries'
thirdPartyLoc = 'thirdparty'
keysLoc = 'cache_keys'

rootDir = os.getcwd()
buildDir = os.path.realpath(scriptPath + '/..') 
libsDir = os.path.realpath(os.path.join(rootDir, libsLoc))
thirdPartyDir = os.path.realpath(os.path.join(rootDir, thirdPartyLoc))
usedPrefix = os.path.realpath(os.path.join(libsDir, 'local'))
if win: usedPrefix = usedPrefix.replace('\\', '/')

optionsList = [
    '--ohos_sdk',
    '--archs',
    '--libs',
    '--proxy'
]
options = {}
runCommand = []
customRunCommand = False
optionArg = ''
for arg in sys.argv[1:]:
    if customRunCommand:
        runCommand.append(arg)
        continue

    if len(optionArg) != 0:
        options[optionArg] = arg
        optionArg = ''
        continue

    args = arg.split('=')
    arg = args[0].lower()
    if arg in optionsList:
        key = arg[2:]
        if len(args) > 1:
            options[key] = args[1]
        else:
            optionArg = key
        continue
    
    if arg == 'run':
        customRunCommand = True

if not customRunCommand and not 'libs' in options or len(options['libs']) == 0:
    error('build libs is not set.')

archs = 'arm64-v8a,x86_64'
if 'archs' in options and len(options['archs']) != 0 :
    archs = options['archs']

if not os.path.isdir(os.path.join(libsDir, keysLoc)):
    pathlib.Path(os.path.join(libsDir, keysLoc)).mkdir(parents=True, exist_ok=True)
if not os.path.isdir(os.path.join(thirdPartyDir, keysLoc)):
    pathlib.Path(os.path.join(thirdPartyDir, keysLoc)).mkdir(parents=True, exist_ok=True)

baseEnv = os.environ.copy()
if 'ohos_sdk' in options and len(options['ohos_sdk']) != 0:
    sdkDir = os.path.realpath(options['ohos_sdk'])
else:
    sdkDir = baseEnv['OHOS_SDK']
if 'proxy' in options and len(options['proxy']) != 0:
    baseEnv['HTTPS_PROXY'] = options['proxy']

pathSdkPrefixes = [
    'native\\build-tools\\cmake\\bin',
    'native\\llvm\\bin'
] if win else [
    'native/build-tools/cmake/bin',
    'native/llvm/bin'
]
pathThirdPartyPrefixes = [
    'thirdparty\\msys64\\usr\\bin',
    'thirdparty\\msys64\\mingw64\\bin',
    'thirdparty\\msys64\\usr\\bin\\core_perl',
    'thirdparty\\msys64\\usr\\bin\\site_perl',
    'thirdparty\\msys64\\usr\\bin\\vendor_perl',
] if win else [
    # 'thirdparty/msys64/usr/bin',
    # 'thirdparty/msys64/mingw64/bin',
    # 'thirdparty/msys64/usr/bin/core_perl',
    # 'thirdparty/msys64/usr/bin/site_perl',
    # 'thirdparty/msys64/usr/bin/vendor_perl',
]
pathPrefix = ''
for singlePrefix in pathSdkPrefixes:
     pathPrefix = pathPrefix + os.path.join(sdkDir, singlePrefix) + pathSep
for singlePrefix in pathThirdPartyPrefixes:
     pathPrefix = pathPrefix + os.path.join(rootDir, singlePrefix) + pathSep

environment = {
    'MAKE_THREADS_CNT': '-j8',
    'SCRIPT_DIR': scriptPath,
    'ROOT_DIR': rootDir,
    'LIBS_DIR': libsDir,
    'USED_PREFIX': usedPrefix,    
    'THIRDPARTY_DIR': thirdPartyDir,
    'SPECIAL_TARGET': 'win' if win else 'mac' if mac else 'linux',
    'PATH_PREFIX': pathPrefix,
}
ignoreInCacheForThirdParty = [
    'USED_PREFIX',
    'LIBS_DIR',
    'SPECIAL_TARGET',
    'PATH_PREFIX',
]

environmentKeyString = ''
envForThirdPartyKeyString = ''
for key in environment:
    part = key + '=' + environment[key] + ';'
    environmentKeyString += part
    if not key in ignoreInCacheForThirdParty:
        envForThirdPartyKeyString += part
environmentKey = hashlib.sha1(environmentKeyString.encode('utf-8')).hexdigest()
envForThirdPartyKey = hashlib.sha1(envForThirdPartyKeyString.encode('utf-8')).hexdigest()

for key in environment:
    baseEnv[key] = environment[key]

# crossCompilePath = os.path.join(sdkDir, 'native', 'llvm', 'bin')
# crossComplier = os.path.join(crossCompilePath, 'aarch64-linux-ohos-clang')
# if not os.path.exists(crossComplier):
#     shutil.copyfile(os.path.join(crossCompilePath, 'aarch64-unknown-linux-ohos-clang'), crossComplier)
#     shutil.copyfile(os.path.join(crossCompilePath, 'aarch64-unknown-linux-ohos-clang++'), os.path.join(crossCompilePath, 'aarch64-linux-ohos-clang++'))
#     shutil.copyfile(os.path.join(crossCompilePath, 'armv7-unknown-linux-ohos-clang'), os.path.join(crossCompilePath, 'armv7-linux-ohos-clang'))
#     shutil.copyfile(os.path.join(crossCompilePath, 'armv7-unknown-linux-ohos-clang++'), os.path.join(crossCompilePath, 'armv7-linux-ohos-clang++'))
#     shutil.copyfile(os.path.join(crossCompilePath, 'x86_64-unknown-linux-ohos-clang'), os.path.join(crossCompilePath, 'x86_64-linux-ohos-clang'))
#     shutil.copyfile(os.path.join(crossCompilePath, 'x86_64-unknown-linux-ohos-clang++'), os.path.join(crossCompilePath, 'x86_64-linux-ohos-clang++'))

if len(environment['PATH_PREFIX']) != 0:
    baseEnv['PATH'] = environment['PATH_PREFIX'] + 'C:\\Windows\\System32' if win else environment['PATH_PREFIX'] + baseEnv['PATH']

baseEnv['OHOS_SDK'] = sdkDir.replace('\\', '/') if win else sdkDir

def computeFileHash(path):
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(256 * 1024)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def computeCacheKey(stage):
    if (stage['location'] == thirdPartyLoc):
        envKey = envForThirdPartyKey
    else:
        envKey = environmentKey
    objects = [
        envKey,
        stage['location'],
        stage['name'],
        stage['src'],
        stage['url'],
        stage['version'],
        stage['commands']
    ]
    for pattern in stage['dependencies']:
        pathlist = glob.glob(os.path.join(libsDir, pattern))
        items = [pattern]
        if len(pathlist) == 0:
            pathlist = glob.glob(os.path.join(thirdPartyDir, pattern))
        if len(pathlist) == 0:
            error('Nothing found: ' + pattern)
        for path in pathlist:
            if not os.path.exists(path):
                error('Not found: ' + path)
            items.append(computeFileHash(path))
        objects.append(':'.join(items))
    return hashlib.sha1(';'.join(objects).encode('utf-8')).hexdigest()

def keyPath(stage):
    return os.path.join(stage['directory'], keysLoc, stage['src'])

def checkCacheKey(stage):
    if not 'key' in stage:
        error('Key not set in stage: ' + stage['name'])
    key = keyPath(stage)
    if not os.path.exists(os.path.join(stage['directory'], stage['src'])):
        return 'NotFound'
    if not os.path.exists(key):
        return 'Stale'
    with open(key, 'r') as file:
        return 'Good' if (file.read() == stage['key']) else 'Stale'

def clearCacheKey(stage):
    key = keyPath(stage)
    if os.path.exists(key):
        os.remove(key)

def writeCacheKey(stage):
    if not 'key' in stage:
        error('Key not set in stage: ' + stage['name'])
    key = keyPath(stage)
    with open(key, 'w') as file:
        file.write(stage['key'])

stages = []

def removeDir(folder):
    if win:
        return 'if exist ' + folder + ' rmdir /Q /S ' + folder + '\nif exist ' + folder + ' exit /b 1'
    return 'rm -rf ' + folder

def filterByPlatform(commands):
    commands = commands.split('\n')
    result = ''
    dependencies = []
    version = '0'
    skip = False
    for command in commands:
        m = re.match(r'(!?)([a-z0-9_]+):', command)
        if m and m.group(2) != 'depends' and m.group(2) != 'version':
            scopes = m.group(2).split('_')
            inscope = 'common' in scopes
            if win and 'win' in scopes:
                inscope = True
            if mac and ('mac' or 'unix') in scopes:
                inscope = True
            if linux and ('linux' or 'unix') in scopes:
                inscope = True
            if 'release' in scopes:
                if 'skip-release' in options:
                    inscope = False
                elif len(scopes) == 1:
                    continue
            skip = inscope if m.group(1) == '!' else not inscope
        elif not skip and not re.match(r'\s*#', command):
            if m and m.group(2) == 'version':
                version = version + '.' + command[len(m.group(0)):].strip()
            elif m and m.group(2) == 'depends':
                pattern = command[len(m.group(0)):].strip()
                dependencies.append(pattern)             
            else:
                command = command.strip()
                result = result + command + '\n'
    return [result, dependencies, version]

def stage(name, src, url, commands, location = libsLoc):
    if checkExistStage(name):
        print('[WARNING] ' + name + 'lib has be existed in states')
        return

    if location is None or len(location) == 0 or location == libsLoc:
        directory = libsDir
    elif location == thirdPartyLoc:
        directory = thirdPartyDir
    else:
        error('Unknown location: ' + location)
    if len(src) == 0: src = name
    [commands, dependencies, version] = filterByPlatform(commands)
    if len(commands) > 0:
        stages.append({
            'name': name,
            'src': src,
            'url': url,
            'location': location,
            'directory': directory,
            'commands': commands,
            'version': version,
            'dependencies': dependencies,
        })

def winFailOnEach(command):
    commands = command.split('\n')
    result = ''
    startingCommand = True
    for command in commands:
        command = re.sub(r'\$([A-Za-z0-9_]+)', r'%\1%', command)
        if re.search(r'\$[^<]', command):
            error('Bad command: ' + command)
        appendCall = startingCommand and len(command) != 0 and not re.match(r'(if |for |rem |echo |\))', command)
        called = 'call ' + command if appendCall else command
        result = result + called
        if command.endswith('^'):
            startingCommand = False
            result = result[:-1]
        else:
            startingCommand = True
            result = result = result + '\r\n' if not appendCall or len(command) == 0 else result + '\r\nif %errorlevel% neq 0 exit /b %errorlevel%\r\n'
    return result

def printCommands(commands):
    print('---------------------------------COMMANDS-LIST----------------------------------')
    print(commands, end='')
    print('--------------------------------------------------------------------------------')

def genChildEnv(name, src, url, arch=''):
    env = baseEnv.copy()
    env['OHOS_LIBNAME'] = name
    env['OHOS_LIBSRC'] = src
    env['OHOS_LIBURL'] = url
    if len(arch) == 0:
        return env
    
    buildEnv = ohosenv.setEnv(arch, env['OHOS_SDK'])
    for key in buildEnv:
        env[key] = buildEnv[key]
    return env

def run(name, src, url, commands, isLib):
    printCommands(commands)
    if win:
        command = '@echo OFF\r\n' + winFailOnEach(commands)
        cmdFile = 'command' + str(hash(command)) +'.bat'
        if os.path.exists(cmdFile):
            os.remove(cmdFile)
        with open(cmdFile, 'w') as file:
            file.write(command)

        result = False
        if not isLib or len(archs) == 0:
            runEnv = genChildEnv(name, src, url)
            result = subprocess.run(cmdFile, shell=True, env=runEnv).returncode == 0
        else:
            for arch in archs.split(','):
                runEnv = genChildEnv(name, src, url, arch)
                result = subprocess.run(cmdFile, shell=True, env=runEnv).returncode == 0
                if not result:
                    break
        if result and os.path.exists(cmdFile):
            os.remove(cmdFile)
        return result
    elif re.search(r'\%', commands):
        error('Bad' + name + ' command: ' + commands)
    else:
        if not isLib or len(archs) == 0:
            runEnv = genChildEnv(name, src, url)
            return subprocess.run('set -e\n' + commands, shell=True, env=runEnv).returncode == 0
        
        result = False
        for arch in archs.split(','):
            runEnv = genChildEnv(name, src, url, arch)
            result = subprocess.run('set -e\n' + commands, shell=True, env=runEnv).returncode == 0
            if not result:
                break
        return result

# Thanks https://stackoverflow.com/a/510364
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode('ascii')

getch = _Getch()

def checkExistStage(name):
    for stage in stages:
        if name == stage['name']: return True
    return False

def runStages():
    rebuildStale = False
    for arg in sys.argv[1:]:
        if arg in options:
            continue
        elif arg == '--silent':
            rebuildStale = True
            break
    count = len(stages)
    index = 0
    for stage in stages:
        index = index + 1
        version = ('#' + str(stage['version'])) if (stage['version'] != '0') else ''
        prefix = '[' + str(index) + '/' + str(count) + '](' + stage['location'] + '/' + stage['name'] + version + ')'
        print(prefix + ': ', end = '', flush=True)
        stage['key'] = computeCacheKey(stage)
        commands = stage['commands']
        checkResult = checkCacheKey(stage)
        if checkResult == 'Good':
            print('SKIPPING')
            continue
        elif checkResult == 'NotFound':
            print('NOT FOUND, ', end='')
        elif checkResult == 'Stale' or checkResult == 'Forced':
            if checkResult == 'Stale':
                print('CHANGED, ', end='')
            if rebuildStale:
                checkResult == 'Rebuild'
            else:
                print('(r)ebuild, rebuild (a)ll, (s)kip, (p)rint, (q)uit?: ', end='', flush=True)
                while True:
                    ch = 'r' if rebuildStale else getch()
                    if ch == 'q':
                        finish(0)
                    elif ch == 'p':
                        printCommands(commands)
                        checkResult = 'Printed'
                        break
                    elif ch == 's':
                        checkResult = 'Skip'
                        break
                    elif ch == 'r':
                        checkResult = 'Rebuild'
                        break
                    elif ch == 'a':
                        checkResult = 'Rebuild'
                        rebuildStale = True
                        break
        if checkResult == 'Printed':
            continue
        if checkResult == 'Skip':
            print('SKIPPING')
            continue
        clearCacheKey(stage)
        print('BUILDING:')
        os.chdir(stage['directory'])
        if not run(stage['name'], stage['src'], stage['url'], commands, stage['directory'] == libsDir):
            print(prefix + ': FAILED')
            finish(1)
        writeCacheKey(stage)

if customRunCommand:
    archs = ''
    os.chdir(executePath)
    command = ' '.join(runCommand) + '\n'
    if not run('', '', '', command, False):
        print('FAILED :(')
        finish(1)
    finish(0)

def loadLib(name):
    moduleFile = os.path.join(buildDir, 'scripts', name, 'build.py')
    if not os.path.exists(moduleFile):
        error(' build script of ' + name + ' is not exist')
        finish(1)
        return False
    
    spec = importlib.util.spec_from_file_location('build', moduleFile)
    libModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(libModule)
    result = libModule.build()
    if 'depends' in result:
        for depend in result['depends']:
            if not checkExistStage(depend) and not loadLib(depend):
                return False
    url = result['url'] if 'url' in result else ''
    src = result['src'] if 'src' in result else ''
    if not 'location' in result:
        stage(result['name'], src, url, result['commands'])
    else:
        stage(result['name'], src, url, result['commands'], result['location'])
    return True        

if win: loadLib('msys64')
for libName in options['libs'].split(','):
    if not loadLib(libName): break

if win:
    currentCodePage = subprocess.run('chcp', capture_output=True, shell=True, text=True, env=baseEnv).stdout.strip().split()[-1]
    subprocess.run('chcp 65001 > nul', shell=True, env=baseEnv)
    runStages()
    subprocess.run('chcp ' + currentCodePage + ' > nul', shell=True, env=baseEnv)
else:
    runStages()
