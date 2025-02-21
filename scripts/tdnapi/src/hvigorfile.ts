import os from 'os';
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { harTasks } from '@ohos/hvigor-ohos-plugin';

let prebuildScripts =
  'cmake -B src/main/cpp/td/build-gen -S src/main/cpp/td -DTD_GENERATE_SOURCE_FILES=ON && cmake --build src/main/cpp/td/build-gen'

if (os.type() == 'Windows_NT') {
  prebuildScripts = 'set PATH=./src/main/cpp/thirdparty/bin;%PATH% &&' + prebuildScripts
}

export function prebuildPlugin(str?: string) {
  return {
    pluginId: 'prebuildPlugin',
    apply(pluginContext) {
      pluginContext.registerTask({
        // 预编译自动化生成tl相关的C++文件
        name: 'prebuild@TdGenerateBuild',
        run: (taskContext) => {
          const mtpApiFile = __dirname + '/src/main/cpp/td/td/generate/auto/td/mtproto/mtproto_api.cpp';
          const tdApiFile = __dirname + '/src/main/cpp/td/td/generate/auto/td/telegram/td_api.cpp';
          if (!existsSync(mtpApiFile) || !existsSync(tdApiFile)) {
            console.log('prebuild C++ files of td generating ...');
            const res = execSync(prebuildScripts, { 'cwd': __dirname });
            console.log(res.toString());
          } else {
            console.log('prebuild C++ files of td already generated.');
          }
        },
        // 任务插入位置为 'default@PreBuild' 前
        postDependencies: ['default@PreBuild']
      });
    }
  }
}

export default {
  system: harTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: [prebuildPlugin()]         /* Custom plugin to extend the functionality of Hvigor. */
}
