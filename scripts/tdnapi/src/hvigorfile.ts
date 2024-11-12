import { hapTasks } from '@ohos/hvigor-ohos-plugin';
import { execSync } from 'node:child_process';
import os from 'os';

let genTLScripts =
  'cmake -B src/main/cpp/td/build-gen -S src/main/cpp/td -DTD_GENERATE_SOURCE_FILES=ON && cmake --build src/main/cpp/td/build-gen'

if (os.type() == 'Windows_NT') {
  genTLScripts = 'set PATH=./src/main/cpp/thirdparty/bin;%PATH% &&' + genTLScripts
}

export function prebuildPlugin(str?: string) {
  return {
    pluginId: 'prebuildPlugin',
    apply(pluginContext) {
      pluginContext.registerTask({
        // 编写自定义任务
        name: 'prebuild@GenerateBuild',
        run: (taskContext) => {
          console.log('prebuild td generate ...');
          const res = execSync(genTLScripts, { 'cwd': __dirname });
          console.log(res.toString());
        },
        // 确认自定义任务插入位置
        postDependencies: ['default@PreBuild']
      })
    }
  }
}

export default {
  system: hapTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: [prebuildPlugin()]         /* Custom plugin to extend the functionality of Hvigor. */
}
