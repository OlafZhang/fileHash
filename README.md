# fileHash
文件哈希值变化比对提醒工具(checksum based file diff check&amp;remind tool)
# 语言支持/Language Support
| Language | Supported?  |
| -------- | ----------- |
| 中文     | √            |
| English  | Processing   |
| 日本語    | Processing  |
# 使用
**Release版本将在之后发布，可到issue催更**

使用源码的同学请确保自己有一定的独立思考能力和解决相关问题的能力，建议`Python版本>3.10`

1、下载主程序`fileHash.py`、环境配置文件`requirements.txt`和配置文件`Config_fileHash.py(可选)`

配置文件会在第一次运行主程序且工作路径下无配置文件时自动生成

2、安装第三方库

打开命令提示符/终端，进入主程序所在目录

假设你下载到了`C:\Users\olaf\Download`，在命令行分别执行：

  `cd C:\Users\olaf\Download`
  `pip install -r requirements.txt`

先不要关闭命令行，看下一步

3、初始化配置文件

如果你没下载配置文件，在命令行执行(注意：Linux/macOS用户可能需要将`python`改为`python3`)：

  `python fileHash.py`

如果执行成功或你已经下载了配置文件，继续往下看

4、修改配置文件

配置文件中各个变量名称和用途如下，也可参考配置文件内注释，注意，不要删除/修改配置文件中的引号/中括号/大括号

| 变量名 | 用途 | 是否必须 | 数据类型 | 备注 |
| -------- | ----------- | -------- | ----------- | -------- |
| workFolder | 主工作目录 | 是 | 字符串 | |
| singleFolderNameList | 指定检查的子文件夹 | 否 | 列表 | 可以留空或注释 |
| sqlWritable | 数据库读写/只读模式开关 | 是 | 布尔值 | True是可读写，False时只读 |
| folderKeywordBlacklistSwitch | 文件夹关键字黑名单过滤开关 | 是 | 布尔值 |  |
| folderKeywordBlacklist | 文件夹关键字黑名单 | 否 | 列表 | |



