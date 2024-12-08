# fileHash
文件哈希值变化比对提醒工具(checksum based file diff check&amp;remind tool)
# 语言支持/Language Support
| Language | Supported?  |
| -------- | ----------- |
| 中文     | √            |
| English  | Processing   |
| 日本語    | Processing  |

# 这个适合给谁用？
一般适合摄影师/媒体从业人员管理自己的资源文件，若资源文件出现变动，可以及时提醒用户，以便进行及时备份或处理

他们的资源文件夹结构可能是这样的，也是本程序支持的文件夹结构

即主资源文件夹会存放多个子资源文件夹，这些子资源文件夹一般会以工程名称/日期等命名

    主资源文件夹
    ├───子资源文件夹1
    │   └───子资源文件夹1
    │        └───子资源文件夹1
    │           ├───资源1
    │           ├───资源2
    │           ├───资源3
    │───────资源1
    │───────资源2
    │───────资源3
    ├───子资源文件夹2
    │   ├───资源1
    │   ├───资源2
    │   ├───资源3
    └───子资源文件夹3
        ├───资源1
        ├───资源2
        ├───资源3

# 使用
**Release版本将在之后发布，可到issue催更**

使用源码的同学请确保自己有一定的独立思考能力和解决相关问题的能力，建议`Python版本>3.10`

### 下载
下载主程序`fileHash.py`、环境配置文件`requirements.txt`和配置文件`Config_fileHash.py(可选)`

配置文件会在第一次运行主程序且工作路径下无配置文件时自动生成

### 安装第三方库

打开命令提示符/终端，进入主程序所在目录

假设你下载到了`C:\Users\olaf\Download`，在命令行分别执行：

    cd C:\Users\olaf\Download
    pip install -r requirements.txt

先不要关闭命令行，看下一步

### 初始化配置文件

如果你没下载配置文件，在命令行执行(注意：Linux/macOS用户可能需要将`python`改为`python3`)：

    python fileHash.py 

如果执行成功或你已经下载了配置文件，继续往下看

### 修改配置文件

配置文件中各个变量名称和用途如下，也可参考配置文件内注释，注意，不要删除/修改配置文件中的引号/中括号/大括号

| 变量名 | 用途 | 是否必须 | 数据类型 | 备注 |
| -------- | ----------- | -------- | ----------- | -------- |
| workFolder | 主工作目录 | 是 | 字符串 | |
| singleFolderNameList | 指定检查的子文件夹 | 否 | 列表 | 可以留空或注释 |
| sqlWritable | 数据库读写/只读模式开关 | 是 | 布尔值 | `True`是可读写，`False`时只读 |
| folderKeywordBlacklistSwitch | 文件夹关键字黑名单过滤开关 | 是 | 布尔值 |  |
| folderKeywordBlacklist | 文件夹关键字黑名单 | 否 | 列表 | |
| threadWorker | 线程数 | 是 | 整数 | 为`10`时可以满足大部分场景 |
| mtimeMode | 是否先读取修改时间 | 是 | 布尔值 | **实验性功能**，若为`True`，只有检测到文件修改日期大于读取到数据库最晚的时间戳时才会计算文件哈希|
| summaryPath | 处理总结文件输出路径 | 是 | 字符串 | 扩展名建议为`.json` |
| summaryIndent | 总结文件的缩进等级 | 是 | 整数 |  |
| summaryOneLine | 是否需要将总结文件内容调整为一行 | 是 | 布尔值 |一般用于传递到推送服务 |
| useSqlite3 | 是否使用SQLite3 | 是 |  | False-使用MySQL/MariaDB，使用SQLite3时，不存在的数据库文件会被自动创建 | 
| SQLITE_DBFILE | SQLite数据库位置 | useSqlite3为`True`时 | 字符串 |  | 
| MYSQL_HOST | MySQL/MariaDB URL | useSqlite3为`False`时 | 字符串 |  | 
| MYSQL_PORT | MySQL/MariaDB端口号 | useSqlite3为`False`时 | 整数 |  | 
| MYSQL_USER | MySQL/MariaDB连接用户名 | useSqlite3为`False`时 | 字符串 |  | 
| MYSQL_PASSWORD | MySQL/MariaDB连接密码 | useSqlite3为`False`时 | 字符串 |  | 
| MYSQL_DATABASE | MySQL/MariaDB数据库名称 | useSqlite3为`False`时 | 字符串 | 确保此数据库存在，程序不会创建数据库，但是会自动创建数据表 | 
| MYSQL_CHARSET | MySQL/MariaDB数据库表字符集 | useSqlite3为`False`时 | 字符串 | 建议为`utf8mb4`，改为其它值极大可能出现问题 | 

### 运行

如果使用MySQL/MariaDB，确保已经创建了数据库，数据表会在运行程序时自动创建

在命令行执行(注意：Linux/macOS用户可能需要将`python`改为`python3`)：

    python fileHash.py 

可能可以通过双击`fileHash.py`来运行程序

# 原理？

这个程序会做三件事：`计算文件哈希值`，`检查新加/修改文件`，`检查删除文件`

如果使用`mtimeMode`参数，会先检查文件的修改时间是否大于读取到数据库最晚的时间戳，若是或数据库找不到文件，表示文件有变化，执行文件哈希计算，否则跳过

程序运行结束后，如果没有使用`singleFolderNameList`参数，会根据数据库中所有文件的哈希值和文件路径生成dump文件哈希值，方便跨平台或快速比对工作目录下是否发生文件变动

