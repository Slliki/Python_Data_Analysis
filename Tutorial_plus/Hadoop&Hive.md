# Hadoop and Hive
## 1. Hadoop
### 1. HDFS的部署<big>
1. 首先，通过克隆得到的三个虚拟机node1，2，3，分别作为三个节点，其中node1作为主节点，node2，3作为从节点。\
主节点:内存为4gb，配置为NameNode，SecondaryNameNode， DataNode
从节点：内存为2gb，配置为DataNode

2. 上传Hadoop安装包到node1，
解压安装包到之前创建好的文件夹：`tar -zxvf hadoop-3.3.4.tar.gz -C /export/server/`\
cd到/export/server内构建软连接：`ln -s /export/server/hadoop-3.3.4 hadoop` 构建为hadoop方便使用\
cd到hadoop安装包内：`cd hadoop`\
查看hadoop文件的内容：

![](.Hadoop&Hive_images/f7c8fd94e6ab83bf50289f004a98527.png)

3. 修改配置文件/etc，应用自定义设置\
下述文件均存在于`$HADOOP_HOME/etc/hadoop`目录下
- workers: 从节点的ip地址
```
cd /export/server/hadoop/etc/hadoop
vim workers
# 填入以下内容
node1
node2
node3
```
- hadoop-env.sh: 配置环境变量
```
# 填入以下内容
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.292.b10-0.el7_9.x86_64--->由于设置过软连接，该命令可写为：
export JAVA_HOME=/export/server/jdk # 指明jdk环境位置

export HADOOP_HOME=/export/server/hadoop # 指明hadoop环境位置
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop # 指明hadoop配置文件目录位置
export HADOOP_LOG_DIR=$HADOOP_HOME/logs # 指明hadoop运行日志文件目录位置
```
- core-site.xml: hadoop核心配置信息
```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://node1:8020</value>
    </property>
    
    <property>
        <name>io.file.buffer.size</name>
        <value>131072</value>
    </property>
</configuration>
```
由于该文件是xml文件，需要设置kv对，其中name为key，value为value，\
上述配置中，fs.defaultFS指明了hdfs内部的地通讯址，表名DataNode和node1的通讯地址为8020，node1是NameNode所在机器\
该配置固定了node1必须启动NameNode进程。\
io.file.buffer.size指明了文件缓冲区大小。
- hdfs-site.xml: HDFS的核心配置信息
```
<configuration>
  <property>
    <name>dfs.datanode.data.dir.perm</name>
    <value>700</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/data/nn</value>
  </property>
  <property>
    <name>dfs.namenode.hosts</name>
    <value>node1,node2,node3</value>
  </property>
<property>
    <name>dfs.blocksize</name>
    <value>268435456</value>
  </property>
  <property>
    <name>dfs.namenode.handler.count</name>
    <value>100</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data/dn</value>
  </property>
</configuration>
```
![](.Hadoop&Hive_images/5966735e.png)
![](.Hadoop&Hive_images/87575d36.png)

4. 准备数据的文件目录，创建文件夹
![](.Hadoop&Hive_images/56e9be1d.png)

所以应该在node1节点创建文件夹：
```
mkdir -p /data/nn #表示nameNode的数据存储目录
mkdir /data/dn  #表示dataNode的数据存储目录
```
在node2，3节点创建文件夹：
```
mkdir -p /data/dn
```

5. 分发Hadoop到各个节点\
分发-在node1节点执行：
```
cd /export/server
# 注意：scp命令只能复制原文件到其他node，不可以复制软连接（看作快捷方式）
scp -r hadoop-3.3.4 node2:`pwd`/  #注意不是单引号！！！
scp -r hadoop-3.3.4 node3:`pwd`/

```
软连接-在node2执行:
```
ln -s /export/server/hadoop-3.3.4 hadoop
```
软连接：在node3执行:
```
ln -s /export/server/hadoop-3.3.4 hadoop
```

6. 配置环境变量：三台机器均执行
```
cd /export/server
vim /etc/profile
# 在文件末尾添加以下内容
export HADOOP_HOME=/export/server/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
# 保存退出，再生效环境变量
source /etc/profile
```

7. 授权Hadoop用户，以root身份在三个机器均执行
为了保证安全，不应该每次用root启动，而应该使用普通用户hadoop启动整个服务，因此需要授权hadoop用户
```
# chown表示修改文件的所有者，-R表示递归修改，语法：chown -R 用户名:用户组 文件名
chown -R hadoop:hadoop /data
chown -R hadoop:hadoop /export
```

8. 格式化整个文件系统
前期准备完成，现在对整个文件系统执行初始化

格式化namenode，在node1执行：
```
# 确保以hadoop用户执行
su - hadoop
# 格式化namenode
hadoop namenode -format
```

**启动hdfs集群**：
```
#启动
start-dfs.sh
#关闭
stop-dfs.sh
```
只需要在node1一键启动后，即可通过`jps`命令查看进程，发现node1有NameNode，DataNode和SecondaryNameNode，
node2，3均启动了DataNode进程，说明启动成功。

9. 验证HDFS集群，通过web页面查看
```
http://node1:9870
```
出现以下网页说明集群启动成功

![](.Hadoop&Hive_images/ada9a952.png)