import os,sys,time,hashlib,base64,json
import threading,signal
import psutil
import logging
from datetime import datetime
from rich.progress import Progress,TextColumn,TimeElapsedColumn,TimeRemainingColumn
from rich.console import Console
from rich.logging import RichHandler
from plyer import notification #通知插件，纯CLI模式下不支持
console = Console()

try:
    from Config_fileHash import *
except ModuleNotFoundError:
    configFile = open("Config_fileHash.py","w",encoding="utf-8")
    configFile.write(base64.b64decode("IyDluLjop4Hlj4LmlbDosIPmlbQKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIOS4u+W3peS9nOebruW9lQojIOS4jeimgeaJi+i0seiuqei3r+W+hOS7peaWnOadoOe7k+Wwvgp3b3JrRm9sZGVyID0gIkg6L+WbvueJhyIKCiMg5Y2V54us5qOA5p+l5qih5byPCiMg5aGr5YWl6ZyA6KaB5Y2V54us5qOA5p+l55qE5paH5Lu25aS577yM5pSv5oyB5aSa5LiqCiMg6Iul5LiN6ZyA6KaB6K+l5qih5byP77yM6K+35rOo6YeK5oiW5L+d5oyB5YiX6KGo5Li656m6CiMgc2luZ2xlRm9sZGVyTmFtZUxpc3QgPSBbImFhYSIsImJiYiJdCgojIOaVsOaNruW6k+ivu+WGmeaooeW8jwojIEZhbHNl5Li65Y+q6K+777yM55So5LqO5pWw5o2u5q+U5a+5CnNxbFdyaXRhYmxlID0gVHJ1ZQojIOaWh+S7tuWkueWFs+mUruWtl+m7keWQjeWNlei/h+a7pOW8gOWFswpmb2xkZXJLZXl3b3JkQmxhY2tsaXN0U3dpdGNoID0gVHJ1ZQojIOaWh+S7tuWkueWFs+mUruWtl+m7keWQjeWNlQpmb2xkZXJLZXl3b3JkQmxhY2tsaXN0ID0gW10KCiMg5aSa57q/56iL57q/56iL5pWwCiMg5pyA5aSaMTAwMAojIOWKoOWkquWkmue6v+eoi+aXoOaEj+S5iSAKIyDnur/nqIvmlbA9MTDog73lr7nku5jlpKflpJrmlbDmg4XlhrUKdGhyZWFkV29ya2VyID0gMTAKCiMgW+WunumqjOaAp13mmK/lkKblhYjor7vlj5bkv67mlLnml7bpl7QKIyDmo4Dmn6Xor7vlj5bmlofku7bnmoTkv67mlLnml7bpl7TmmK/lkKblpKfkuo7or7vlj5bliLDmlbDmja7lupPmnIDmmZrnmoTml7bpl7TmiLMKIyDoi6XmmK/vvIzooajnpLrmlofku7bmnInkv67mlLnvvIzmiafooYzmlofku7blk4jluIzorqHnrpfvvIzlkKbliJnot7Pov4cKbXRpbWVNb2RlID0gVHJ1ZQoKIyDlpITnkIbmgLvnu5Pmlofku7bovpPlh7rot6/lvoTvvIxqc29u5qC85byPCnN1bW1hcnlQYXRoID0gImZpbGVIYXNoU3VtbWFyeS5qc29uIiAKCiMg5oC757uT5paH5Lu255qE57yp6L+b562J57qnCnN1bW1hcnlJbmRlbnQgPSA0CgojIOaYr+WQpumcgOimgeWwhuaAu+e7k+aWh+S7tuWGheWuueiwg+aVtOS4uuS4gOihjAojIOS4gOiIrOeUqOS6juaOqOmAgeacjeWKoQpzdW1tYXJ5T25lTGluZSA9IFRydWUKCiMg6auY57qn5Y+C5pWw6LCD5pW0CiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KIyDmmK/lkKbkvb/nlKhTUUxpdGUzCiMgRmFsc2Ut5L2/55SoTXlTUUwvTWFyaWFEQgp1c2VTcWxpdGUzID0gVHJ1ZQoKIyDmlbDmja7lupPphY3nva7vvJoKIyBTUUxpdGXmlbDmja7lupPkvY3nva4KU1FMSVRFX0RCRklMRSA9ICJwaG90by5kYiIKIyDmlbDmja7lupNVUkwKTVlTUUxfSE9TVD0ibG9jYWxob3N0IgojIOaVsOaNruW6k+err+WPowpNWVNRTF9QT1JUPTMzMDYKIyDmlbDmja7lupPov57mjqXnlKjmiLflkI0KTVlTUUxfVVNFUj0ncm9vdCcKIyDmlbDmja7lupPov57mjqXlr4bnoIEKTVlTUUxfUEFTU1dPUkQ9JzEyMzQ1NicKIyDmlbDmja7lupPlkI3np7DvvIznoa7kv53mraTmlbDmja7lupPlrZjlnKgKIyDnqIvluo/kuI3kvJrliJvlu7rmlbDmja7lupPvvIzkvYbmmK/kvJroh6rliqjliJvlu7rmlbDmja7ooagKTVlTUUxfREFUQUJBU0U9InBob3RvIgojIOihqOWtl+espumbhu+8jOW7uuiuruaYr3V0ZjhtYjQKTVlTUUxfQ0hBUlNFVD0idXRmOG1iNCIK").decode("utf-8"))
    configFile.close()
    print("无配置文件，已创建，请配置后重新运行程序")
    sys.exit(0)
# 这些变量修改之后会影响程序正常运行
sqlCounter = 0 #新加/修改文件时数据库操作数
getLastUpdate = 0 #读取数据库得到的最新文件时间戳
singleFolderMode = 0 #是否只检查指定文件，此变量会自动调整
fileTotalbytes = 0 #工作目录下所有文件的总字节数
nowFileCount = 0 #目前已读取文件数量
lastNowFileCount = 0 #计算哈希进度条在上一个循环得到的已读取文件数量，用于进度条刷新
hashTimeFormated = "" #计算哈希格式化用时
sqlTimeFormated = "" #新加/修改文件时数据库操作格式化用时
sqlSpeed = "" #新加/修改文件时数据库操作速度
changedFoldersJsonList = [] #此次运行发现存在变化的子文件夹及变化描述（用于展示）
status="" #用于进度条展示当前操作文件
readSpeed = "[0 Byte/s]" #初始化磁盘读取速度展示文本
folderBlacklist = [] #根据关键词黑名单推出的子文件夹黑名单
workItem = [] #当前工作目录的所有文件（[子文件夹,文件名,文件绝对路径]）
hashList = [] #暂时保存到内存的哈希结果
preReadDBlist = [] #预读取数据库中的全部数据
changedFolders = {} #发现存在变化的子文件夹及变化描述（用于数据处理）
threadWorker = 1 if threadWorker <= 0 else 1000 if threadWorker >= 1000 else threadWorker

def log_write(message,level,outprint=True):
    FORMAT = "%(message)s"
    logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger("rich")
    level_no = int(level)
    if outprint:
        if level_no == 1:
            logger.info(message)
        elif level_no == 2 or level_no == 3:
            logger.warning(message)
        elif level_no == 4:
            logger.error(message)
        elif level_no >= 5 and level_no <= 7:
            logger.critical(message)
        else:
            logger.debug(message)
    return
def getFileHashMD5(fileFullPath):
    with open(fileFullPath, 'rb') as fp:
        data = fp.read()
        fp.close()
    file_md5 = hashlib.md5(data).hexdigest()
    return file_md5
def hashCheck(fileList):
    global fileTotalbytes,status,nowFileCount,fileCount,folderKeywordBlacklist,folderBlacklist
    count = 0
    thisFileTotalbytes = 0
    for fileListItem in fileList:
        thisTimePass = False
        thisFolder = str(fileListItem[0])
        relative_file_name = str(fileListItem[1])
        full_file_name = str(fileListItem[2])
        if thisFolder in folderBlacklist:
            thisTimePass = True
        else:
            if folderKeywordBlacklistSwitch:
                for keyword in folderKeywordBlacklist:
                    if str(keyword) in thisFolder:
                        log_write(f"[SKIPPED]文件夹 {thisFolder} 不会被读取，因为 “{keyword}” 在文件夹关键字黑名单中",2,True)
                        thisTimePass = True
                        if thisFolder not in folderBlacklist:
                            folderBlacklist.append(thisFolder)
                        break
        if not thisTimePass:
            try:
                needHash = True
                if mtimeMode:
                    if [relative_file_name.replace("\\","/"),thisFolder] in preReadDBlist:
                        mtime = os.path.getmtime(full_file_name)
                        if mtime <= getLastUpdate:
                            needHash = False
                if not needHash:
                    hashList.append([thisFolder,relative_file_name,-1,-1])
                else:
                    hashList.append([thisFolder,relative_file_name,getFileHashMD5(full_file_name),f"{int(time.time())}"])
            except PermissionError:
                log_write(f"[SKIPPED]读取 {full_file_name} 失败，因为没有该文件的权限",2,True)
            thisFileTotalbytes += os.path.getsize(full_file_name)
            status = f"{thisFolder}/{relative_file_name}"
        count+=1
        nowFileCount+=1
    fileTotalbytes += thisFileTotalbytes
def timeFormat(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    returnFormat = ""
    if hours != 0:
        returnFormat += f"{int(hours)}小时"
    if minutes != 0:
        returnFormat += f"{int(minutes)}分"
    if seconds != 0:
        returnFormat += f"{int(seconds)}秒"
    return returnFormat
def byteFormat(byteInt):
    return str(byteInt) if byteInt < 1024 else '{:.2f}'.format(byteInt/1024) if 1024 <= byteInt < 1048576 else '{:.2f}'.format(byteInt/1024/1024) if 1048576 <= byteInt < 1073741824 else '{:.2f}'.format(byteInt/1024/1024/1024),"Byte" if byteInt < 1024 else "KB" if 1024 <= byteInt < 1048576 else "MB" if 1048576 <= byteInt < 1073741824 else "GB"
def diskReadStatus():
    global pid,readSpeed
    try:
        p = psutil.Process(pid)
        while True:
            Read_bytes_1 = p.io_counters().read_bytes
            time.sleep(1)
            a,b = byteFormat(p.io_counters().read_bytes-Read_bytes_1)
            readSpeed = f"[{a} {b}/s]"
    except Exception as ex:
        readSpeed = "ERROR"
        print(ex)
def killThread(signum, frame):
    log_write("程序中止",0,True)
    sys.exit(0)
def getIndex(intIndex):
    return f"00{intIndex}" if intIndex < 10 else f"0{intIndex}" if intIndex < 100 else f"{intIndex}"
def executeSQL(sqlCommand,commit=True):
    global db,sqlWritable
    cursor = db.cursor()
    cursor.execute(sqlCommand)
    returnItem = cursor.fetchall()
    if commit and sqlWritable:
        db.commit()
    cursor.close()
    return returnItem
signal.signal(signal.SIGINT, killThread) #按下Ctrl+C后触发SIGINT

if os.path.exists(summaryPath):
    os.remove(summaryPath)
pid = os.getpid()
print("fileHash-文件哈希值变化比对提醒工具")
log_write(f"PID：{pid}",0,True)
log_write("使用SQLite3，尝试连接数据库",1,True) if useSqlite3 else log_write("使用MySQL，尝试连接数据库",1,True)

try:
    if useSqlite3:
        import sqlite3
        db = sqlite3.connect(SQLITE_DBFILE)
        try:
            executeSQL("select filePath,fileFolder,md5,lastUpdate from photohash limit 1",False)
        except sqlite3.OperationalError:
            log_write("无photohash表，创建中",2,True)
            executeSQL("CREATE TABLE `photohash` (`filePath` varchar(100) NOT NULL,`fileFolder` varchar(100) NOT NULL,`md5` varchar(500) NOT NULL,`lastUpdate` varchar(20) NOT NULL DEFAULT '0')",True)
            log_write("photohash表已创建",1,True)
    else:          
        import pymysql                                            
        db = pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DATABASE,charset=MYSQL_CHARSET)
        try:
            executeSQL("select filePath,fileFolder,md5,lastUpdate from photohash limit 1",False)
        except pymysql.err.ProgrammingError:
            log_write("无photohash表，创建中",2,True)
            executeSQL("CREATE TABLE `photohash` (`filePath` varchar(100) NOT NULL,`fileFolder` varchar(100) NOT NULL,`md5` varchar(500) NOT NULL,`lastUpdate` varchar(20) NOT NULL DEFAULT '0') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci",True)
            log_write("photohash表已创建",1,True)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    log_write("数据库连接失败，请检查设置",5,True)
    log_write(f"Traceback:{exc_type}\n{exc_value}",0,True)
    sys.exit(1) 
log_write("已连接数据库，数据库可读写",3,True) if sqlWritable else log_write("已连接数据库，数据库只读",3,True)
preReadDB = executeSQL("select * from photohash",False)
if mtimeMode:
    result = executeSQL("select lastUpdate from photohash order by lastUpdate desc limit 1",False)
    if len(result) == 0:
        log_write("未在数据库找到上次更新时间戳，mtimeMode参数无效，将直接计算文件哈希",3,True)
        mtimeMode = False
    else:
        getLastUpdate = int(result[0][0])
        log_write("将会先读取文件修改时间",3,True)
        for line in preReadDB:
            preReadDBlist.append([str(line[0]),str(line[1])])
else:
    log_write("将直接计算文件哈希",1,True)
try:
    singleFolderMode = 1 if isinstance(singleFolderNameList, list) and len(singleFolderNameList)>=1 else 0          
except Exception:
    pass
if singleFolderMode:
    log_write("仅检查指定子文件夹中的文件",3,True)
    isError = False
    for singleFolder in singleFolderNameList:
        fullPath = workFolder+"/"+singleFolder
        if os.path.exists(fullPath):
            log_write(f"'{fullPath}' 路径有效",1,True)
        else:
            log_write(f"'{fullPath}' 不是一个合法/存在路径，请检查",5,True)
            isError = True
    if isError:
        sys.exit(1)
else:
    log_write("检查全部文件",3,True)
    if os.path.exists(workFolder):
        log_write(f"'{workFolder}' 路径有效",1,True)
    else:
        log_write(f"'{workFolder}' 不是一个合法/存在路径，请检查",5,True)
        sys.exit(1)

for root, dirs, files in os.walk(workFolder):
    for i in files:
        full_file_name = f"{root}/{i}".replace("\\","/")
        first_level_path = full_file_name.replace(workFolder+"/","")
        thisFolder = "." if "/" not in first_level_path else first_level_path.split("/")[0]
        relative_file_name = first_level_path if "/" not in first_level_path else first_level_path.replace(thisFolder+"/","")
        if singleFolderMode and thisFolder not in singleFolderNameList:
            continue
        workItem.append([thisFolder,relative_file_name,full_file_name])
fileCount = len(workItem)
workItemCount = fileCount
log_write(f"在工作目录下发现{fileCount}个待处理文件",1,True)
log_write(f"初始化{threadWorker}个线程并启动",1,True)  
while workItemCount % threadWorker != 0:
    workItemCount += 1
for i in range(0,threadWorker):
    exec(f"workItem_{getIndex(i)}=[]")
for i in range(0,workItemCount,threadWorker):
    try:
        for index in range(0,threadWorker):
            exec(f"workItem_{getIndex(index)}.append(workItem[i+{index}])")
    except IndexError:
        break
for i in range(0,threadWorker):
    exec(f"t{getIndex(i)}=threading.Thread(target=hashCheck, args=(workItem_{getIndex(i)},))")
    exec(f"t{getIndex(i)}.daemon=True")
    exec(f"t{getIndex(i)}.start()")
diskSpeedMonitor = threading.Thread(target=diskReadStatus, args="")
diskSpeedMonitor.daemon=True
diskSpeedMonitor.start()

start_time = time.time()
with Progress(TextColumn("计算哈希...[progress.description]"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),TimeRemainingColumn(),TextColumn("{task.description}")) as progress:
    check1_tqdm = progress.add_task(description="", total=fileCount,status=status)
    while fileCount > nowFileCount:
        catch_nowFileCount = nowFileCount
        progress.update(check1_tqdm, description=f"{readSpeed} {status}", refresh=True)
        progress.advance(check1_tqdm, advance=catch_nowFileCount-lastNowFileCount)
        lastNowFileCount = catch_nowFileCount
        time.sleep(00.1)
end_time = time.time()
avgSpeed,avgSpeedUnit = byteFormat(fileTotalbytes / float(end_time - start_time))
totalSize,totalSizeUnit = byteFormat(fileTotalbytes)
hashTimeFormated = timeFormat(float(end_time - start_time))
log_write(f"计算哈希完成，总大小：{totalSize} {totalSizeUnit}，计算总耗时：{hashTimeFormated}，磁盘平均读速：{avgSpeed} {avgSpeedUnit}/s",1,True)

start_time = time.time()
with Progress(TextColumn("检查新加/修改文件[progress.description]"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),TimeRemainingColumn(),TextColumn("{task.description}")) as progress:
    check1_tqdm = progress.add_task(description="", total=len(hashList),status=status)
    for i in hashList:
        thisFolder,relative_file_name,file_md5,thisTime  = str(i[0]),str(i[1]),str(i[2]),str(i[3])
        status = thisFolder + "/" + relative_file_name
        progress.update(check1_tqdm, description=status, refresh=True)
        if mtimeMode == True and file_md5 == "-1":
            progress.advance(check1_tqdm, advance=1)
            continue
        if [f"{relative_file_name}",f"{thisFolder}"] not in preReadDBlist:
            log_write(f"[ADD]无 文件夹 {thisFolder} 中文件 {relative_file_name} 的记录，准备写入",4,True)
            executeSQL(f"insert into photohash values('{relative_file_name}','{thisFolder}','{file_md5}','{thisTime}')",True)
            sqlCounter+=1
            if thisFolder not in changedFolders:
                changedFolders[thisFolder] = ["新增"]
            else:
                if "新增" not in changedFolders[thisFolder]:
                    changedFolders[thisFolder].append("新增")
        else:
            result = executeSQL(f"select * from photohash where fileFolder='{thisFolder}' and filePath='{relative_file_name}'",False)
            sqlCounter+=1
            thisHash = str(result[0][2])
            if thisHash != file_md5:
                log_write(f"[MOD]文件夹 {thisFolder} 中文件 {relative_file_name} 的哈希值发生改变，准备修改",4,True)
                executeSQL(f"update photohash set md5='{file_md5}',lastUpdate='{thisTime}' where fileFolder='{thisFolder}' and filePath='{relative_file_name}'",True)
                sqlCounter+=1
                if thisFolder not in changedFolders:
                    changedFolders[thisFolder] = ["修改"]
                else:
                    if "修改" not in changedFolders[thisFolder]:
                        changedFolders[thisFolder].append("修改")
        progress.advance(check1_tqdm, advance=1)
end_time = time.time()
sqlTimeFormated = timeFormat(float(end_time - start_time))
sqlSpeed = str(int(sqlCounter//float(end_time - start_time)))
log_write(f"检查新加/修改文件完成，操作总耗时：{sqlTimeFormated}，操作数：{sqlCounter} 条，速度：{sqlSpeed} 条/秒",1,True)  

with Progress(TextColumn("检查删除文件[progress.description]"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),TimeRemainingColumn()) as progress:
    check1_tqdm = progress.add_task(description="", total=len(preReadDB))
    for line in preReadDB:
        relative_file_name,thisFolder,file_md5 = str(line[0]),str(line[1]),str(line[2])
        if not os.path.exists(f"{workFolder}/{relative_file_name}".replace("\\","/") if thisFolder == "." else f"{workFolder}/{thisFolder}/{relative_file_name}".replace("\\","/")):
            log_write(f"[DEL]文件夹 {thisFolder} 中文件 {relative_file_name} 不在 {workFolder} 上，准备删除记录",4,True)
            executeSQL(f"delete from photohash where filePath='{relative_file_name}' and fileFolder='{thisFolder}'",True)
            if thisFolder not in changedFolders:
                changedFolders[thisFolder] = ["删除"]
            else:
                if "删除" not in changedFolders[thisFolder]:
                    changedFolders[thisFolder].append("删除")
        progress.advance(check1_tqdm, advance=1)
log_write("检查删除文件完成",1,True)  

if len(changedFolders) == 0:
    log_write("[SUMMARY]没有发生改变的文件",1,True)
else:
    log_write(f"[SUMMARY]发生改变的文件夹数量：{len(changedFolders)}",5,True)
    indexNO = 1
    for folder,stateList in changedFolders.items():
        stateList = str(stateList).replace("'","").replace('"',"").replace('[',"").replace(']',"").replace(',',"、").replace(' ',"")
        changedFoldersString = f"{folder}（涉及{stateList}操作）"
        changedFoldersJsonList.append(changedFoldersString)
        log_write(f"[SUMMARY]发生改变的文件夹-{indexNO}：{changedFoldersString}",5,True)
        indexNO += 1

if not singleFolderMode:
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d%H%M%S")
    dump_fileName = f"photohash_{formatted_time}.dump"
    if os.path.exists(dump_fileName):
        os.remove(dump_fileName)
    dump_file = open(dump_fileName,"wb")
    result = executeSQL("select filePath,fileFolder,md5 from photohash ORDER BY md5",True)
    result = list(result)
    result.sort()
    for i in result:
        dump_file.write(bytes(str(i)[1:-1]+'\n',encoding='utf-8'))
    dump_file.close()
    file_md5=getFileHashMD5(dump_fileName)
    log_write(f"dump哈希值：{file_md5}",1,True)
    os.remove(dump_fileName)

summaryJson = {
    "dump文件哈希":file_md5,
    "读取根目录":workFolder,
    "指定读取子目录":"",
    "关键词黑名单":"",
    "预读取修改时间模式":"",
    "数据库可写":"",
    "处理文件总数":fileCount,
    "文件总大小":totalSize+" "+totalSizeUnit,
    "磁盘平均读速":f"{avgSpeed} {avgSpeedUnit}/s",
    "计算哈希耗时":hashTimeFormated,
    "检查新加/修改文件数据库操作总耗时":sqlTimeFormated,
    "检查新加/修改文件数据库操作数":f"{sqlCounter} 条",
    "检查新加/修改文件操作速度":f"{sqlSpeed} 条/s",
    } 
summaryJson["预读取修改时间模式"] = "是" if mtimeMode else "否"
summaryJson["数据库可写"] = "是" if sqlWritable else "否"
if singleFolderMode:
    del summaryJson["dump文件哈希"]
    singleFolderNameList = str(singleFolderNameList).replace("'","").replace('"',"").replace('[',"").replace(']',"").replace(',',"、").replace(' ',"")
    summaryJson["指定读取子目录"] = singleFolderNameList
else:
    del summaryJson["指定读取子目录"]
if folderKeywordBlacklistSwitch and len(folderKeywordBlacklist) != 0:
    folderKeywordBlacklist = str(folderKeywordBlacklist).replace("'","").replace('"',"").replace('[',"").replace(']',"").replace(',',"、").replace(' ',"")
    summaryJson["关键词黑名单"] = folderKeywordBlacklist
else:
    del summaryJson["关键词黑名单"]

if len(changedFoldersJsonList) >= 1:
    summaryJson["文件夹变动情况"] = str(changedFoldersJsonList).replace("'","").replace('"',"").replace('[',"").replace(']',"").replace(',',"、").replace(' ',"")
summaryJsonData = json.dumps(summaryJson,ensure_ascii=False,indent=summaryIndent) if not summaryOneLine else str(summaryJson)
with open(summaryPath,"w",encoding="utf-8") as summaryFile:
    summaryFile.write(summaryJsonData)
    summaryFile.close()

toastInfo = f"启用预读取修改时间模式\n处理文件总数：{fileCount}\n计算哈希耗时：{hashTimeFormated}\n" if mtimeMode else f"处理文件总数：{fileCount}\n计算哈希耗时：{hashTimeFormated}\n"
toastInfo = toastInfo+f"存在文件变动：{len(changedFolders)}" if len(changedFoldersJsonList) >= 1 else toastInfo + "不存在文件变动"
try:
    notification.notify(app_name="photoHash",title='photoHash执行完毕',message=toastInfo,timeout=10)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    log_write("调用plyer.notification失败，可能是没有图形化界面？",5,True)
    log_write(f"Traceback:{exc_type}\n{exc_value}",0,True)
finally:
    log_write("10秒后退出程序",1,True)
    time.sleep(10)
    sys.exit(0)