# 常见参数调整
# -----------------------------------------------------------------------------------
# 主工作目录
# 不要手贱让路径以斜杠结尾
workFolder = "H:/图片"

# 单独检查模式
# 填入需要单独检查的文件夹，支持多个
# 若不需要该模式，请注释或保持列表为空
# singleFolderNameList = ["aaa","bbb"]

# 数据库读写模式
# False为只读，用于数据比对
sqlWritable = True
# 文件夹关键字黑名单过滤开关
folderKeywordBlacklistSwitch = True
# 文件夹关键字黑名单
folderKeywordBlacklist = []

# 多线程线程数
# 最多1000
# 加太多线程无意义 
# 线程数=10能对付大多数情况
threadWorker = 10

# [实验性]是否先读取修改时间
# 检查读取文件的修改时间是否大于读取到数据库最晚的时间戳
# 若是，表示文件有修改，执行文件哈希计算，否则跳过
mtimeMode = True

# 处理总结文件输出路径，json格式
summaryPath = "fileHashSummary.json" 

# 总结文件的缩进等级
summaryIndent = 4

# 是否需要将总结文件内容调整为一行
# 一般用于推送服务
summaryOneLine = True

# 高级参数调整
# -----------------------------------------------------------------------------------
# 是否使用SQLite3
# False-使用MySQL/MariaDB
useSqlite3 = True

# 数据库配置：
# SQLite数据库位置
SQLITE_DBFILE = "photo.db"
# 数据库URL
MYSQL_HOST="localhost"
# 数据库端口
MYSQL_PORT=3306
# 数据库连接用户名
MYSQL_USER='root'
# 数据库连接密码
MYSQL_PASSWORD='123456'
# 数据库名称，确保此数据库存在
# 程序不会创建数据库，但是会自动创建数据表
MYSQL_DATABASE="photo"
# 表字符集，建议是utf8mb4
MYSQL_CHARSET="utf8mb4"
