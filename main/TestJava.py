import jpype

convertStrings=False
# jvmPath = r"C:\Program Files (x86)\Java\jre8\bin\server\jvm.dll"  # java虚拟机的路径
jvmPath = r"C:\\Program Files (x86)\\jdk1.8.0_77\\jre\\bin\\server\\jvm.dll"

ext_classpath = r"E:\workspaces\workspace_idea\CowNewSQL-src\transql\out\artifacts\transql_jar\transql.jar"  # 所有调用的方法的绝对路径

# 加载进方法,如果JVM没有启动，就启动JVM
if not jpype.isJVMStarted():  # 这个判断非常重要，因为JVM在一个进程内就会自动关闭，后面在调用就会报错
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % ext_classpath)

# RcpClass = jpype.JClass("com.Test")
RcpClass = jpype.JClass("Runner")  # 继承类及方法，Test为类名
rcp = RcpClass()  # 实例化
# EncryptData = rcp.getSum(1, 2)  # 调用getSum方法
EncryptData = rcp.getRet("select top 10 * from t", "MYSQL", "")  # 调用getSum方法
print(EncryptData)
if jpype.isJVMStarted():
    jpype.shutdownJVM()  # 关闭java虚拟机
