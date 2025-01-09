import pandas as pd
import subprocess
import os
import re

codeFilePath = r'C:\test\usr\common\linSlaveTask.h'                         # 要修改的代码文件路径
ewpFilePath = r'C:\test\application.ewp'                                    # IAR .ewp文件路径
IarBuildPath = r'D:\IAR\common\bin\IarBuild.exe'                            # IAR根目录下的IarBuild.exe路径
outputFileSrcPath = 'C:\\test\\Release\\Exe\\rugby_hp_cs01_app.bin'         # IAR编译输出位置\\文件名
outputFileDesPath = 'C:\\test\\Release\\Exe\\'                              # IAR编译输出位置
IAR_dict = {'H77B_83213A_亮度60%': 0xCCCC, 'H77B_83213A_亮度50%': 0x7FFF}    # 输出文件名:修改数值 键值对字典
pattern1 = r'#define DEFAULT_LIGHT_LV\s+\((0x[0-9A-Fa-f]+)\)'               # 代码中待修改位置的正则匹配式，若需修改多处则继续添加pattern并新增sub语句

compileFileNum = 0
keys = [key for key, value in IAR_dict.items()]
for key in keys:
    iarPairsKey = key
    #修改代码中的值
    with open(codeFilePath, 'r') as file:
        code = file.read()
    iarPairsValue = IAR_dict[iarPairsKey]
    try:
        new_code = re.sub(pattern1, f'#define DEFAULT_LIGHT_LV                ({hex(iarPairsValue)})', code)
    except re.error as e:
        print(f"匹配代码阶段正则表达式错误：{e}")
        break
    except Exception as e:
        print(f"替换代码阶段发生其他错误：{e}")
        break

    #将替换后的内容写回文件
    try:
        with open(codeFilePath, 'w') as file:
            file.write(new_code)
        print(f"成功替换亮度为:{hex(iarPairsValue)}")
    except IOError as e:
        print(f"写入文件阶段发生错误：{e}")
        break

    #编译代码
    try:
        subprocessRunResult = subprocess.run([IarBuildPath, ewpFilePath, '-build', 'Release'])
        print(f"命令输出: {subprocessRunResult.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，返回码: {e.returncode}")
        print(f"错误输出: {e.stderr}")
        break
    except FileNotFoundError as e:
        print(f"命令未找到: {e}")
        break
    except Exception as e:
        print(f"发生其他错误: {e}")
        break


    # 自动命名生成的hex文件
    try:
        os.rename(outputFileSrcPath, f'{outputFileDesPath + iarPairsKey}.bin')
        compileFileNum = compileFileNum + 1
        print(f"编译完成，文件路径名为: {outputFileDesPath + iarPairsKey},亮度值为:{hex(iarPairsValue)}")
    except FileNotFoundError:
        print(f"编译失败，文件路径名 {outputFileSrcPath} 不存在")
        break
    except FileExistsError:
        print(f"编译失败，文件路径名文件 {iarPairsKey} 已经存在，请清空exe路径下的所有文件再执行")
        break
    except Exception as e:
        print(f"编译失败，重命名文件时发生错误: {e}")
        break

print(f"*************成功编译并命名了{compileFileNum}个文件*************")