
# 1. 分布式计算框架
## 1. Hadoop
Hadoop的组成：HDFS(分布式文件系统)，YARN(资源调度框架)，MapReduce(分布式计算框架)

- HDFS：Hadoop Distributed File System，分布式文件系统，用于存储大数据。本质上是一个文件系统，将一个大文件划分为小文件库存储在各个机器上(DataNode),
    通过NameNode管理各个DataNode，提供文件系统的访问接口。
  - NameNode：管理各个DataNode，提供文件系统的访问接口
  - DataNode：存储文件的数据块
- YARN：Yet Another Resource Negotiator，资源调度框架，用于管理集群资源
- MapReduce：分布式计算框架，用于分布式计算
    - map: 将输入的数据切分为若干个小数据，然后将小数据分发到各个机器上进行计算
    - shuffle: 将map的输出结果按照key进行排序，然后将相同key的value进行合并
    - reduce: 将shuffle的结果进行合并，得到最终的结果

优点： 不用传输数据，每次计算只需要将对应任务(算法)分发到数据所在的服务器上进行计算，然后将结果返回即可。\
缺点： 由于每次计算时的结果都要写入本地磁盘，所以效率很低，而且只能进行批处理，不能进行实时计算。

## 2. Spark
1. Spark是一个分布式计算框架，可以进行批处理，也可以进行实时计算，而且效率比MapReduce高很多。
2. spark基于内存计算，提高了大数据处理的实时性，保证高容错性和高伸缩性。
3. spark的核心是RDD(弹性分布式数据集)，是一个抽象的数据集，可以对其进行各种操作，包括map，reduce，join等，这些操作都是在内存中进行的，所以效率很高。
4. spark的运行模式有两种：local模式和cluster模式
    - local模式：在本地运行，不需要启动集群
    - cluster模式：在集群上运行，需要启动集群
5. spark使用函数式编程，将数据集合转换成流(stream)，每个元素一次经过需要的函数，最后得到结果。时间复杂度为O(n)，空间复杂度为O(1)。\
相比面向对象的编程，函数式编程更加简洁，更加高效，更加容易实现并行计算。
6. 引入惰性计算机制，只有当需要输出结果时，才会进行计算，这样可以减少不必要的计算，提高效率。
7. _spark streaming_: Apache Spark生态系统的一个组件，用于处理**实时数据流**。它允许你从各种数据源（如Kafka、Flume、HDFS、Socket等）实时获取数据，并进行高吞吐量的处理和分析。Spark Streaming提供了一种微批处理的模型，它将实时数据切分成小的批次，然后对每个批次应用Spark的批处理引擎。
8. 流计算（Stream Processing）: 是一种用于处理实时数据流的计算模型，它允许数据在进入系统时立即进行处理和分析，而不需要等待数据存储在批处理或离线存储中。流计算通常用于实时监控、实时分析、实时决策和事件驱动应用程序中。

## 3. Flink
1. Flink是一个分布式流处理框架，采用真正的流处理模型。
2. Flink的核心是DataStream，是一个抽象的数据集，可以对其进行各种操作，包括map，reduce，join等，这些操作都是在内存中进行的，所以效率很高。
3. Flink可以与多个数据源集成，包括Kafka、HDFS、Kinesis等。

## 4. Kafka
1. Kafka是一个分布式流处理***平台***，用于处理实时数据流。
2. Kafka的核心是消息队列，用于存储数据，然后将数据分发到各个机器上进行计算。
3. Kafka基于发布-订阅模型，它允许生产者将消息发布到一个或多个主题，而消费者可以订阅这些主题来接收消息。
Kafka的持久性和高吞吐量使其适用于日志收集、事件驱动架构、实时监控和流数据处理。



##  _**Hive**_
Hive是一个基于Hadoop的数据仓库工具软件，可以将结构化的数据文件映射为一张数据库表，并提供简单的sql查询功能，可以将sql语句转换为MapReduce任务进行运行。\
Hive的核心是将**sql**语句转换为MapReduce任务进行运行，所以效率很低，而且只能进行批处理，不能进行实时计算。

实际上hive本身可看作sql语义解析器(将sql转换成mapreduce),本身hive没有计算能力，只能借助外部框架如Map
Reduce、Spark等进行计算。

# 4. ETL技术
ETL（提取、转换、加载）是一种用于数据集成和数据处理的关键技术，通常用于将数据从一个数据源提取，进行必要的转换，然后加载到目标数据存储中。ETL技术在数据仓库、数据湖、数据集成、数据分析等领域起着重要的作用。以下是ETL技术的基本概念和步骤：

1. 提取（Extract）：\
提取是指<u>从一个或多个数据源中收集数据的过程</u>。数据源可以包括数据库、日志文件、API、外部数据服务等。
提取可以包括增量提取（只提取新数据）、全量提取（提取全部数据）或者按特定条件进行过滤。
提取的数据通常以原始格式提取，并暂存到一个临时存储区域。

2. 转换（Transform）：\
转换是指对提取的数据进行<u>清洗、处理和结构化</u>的过程，以满足目标数据存储的要求。
转换可以包括数据清理、数据格式转换、字段映射、计算衍生字段、数据合并、数据分割等操作。
数据转换通常需要编写转换规则和脚本，以确保数据的一致性和质量。

3. 加载（Load）：\
加载是<u>将经过提取和转换的数据加载到目标数据存储中的过程</u>。目标数据存储可以是数据仓库、数据湖、数据库、云存储等。
数据加载可以包括插入、更新、删除等操作，具体取决于目标存储的类型和需求。
数据加载需要考虑性能、容错性和数据完整性。

ETL技术的关键目标包括数据清洗、数据整合、数据质量保障和数据可用性。ETL流程通常由ETL工具或自定义脚本来执行，以自动化和简化数据处理任务。一些常见的ETL工具包括Apache Nifi、Talend、Informatica、Apache Spark等。

**常用ETL工具：** Kettle，DataX(阿里巴巴)，Sqoop(用于Hadoop和关系型数据库之间的数据传输)，Flume(用于Hadoop和非结构化数据之间的数据传输)

# 5. 数据仓库（Data Warehouse）
数据仓库是一个面向主题的、集成的、相对稳定的、反映历史变化的数据集合，用于支持管理决策。

离线数据仓库（Offline Data Warehouse）和实时数据仓库（Real-time Data Warehouse）是两种不同的数据仓库体系结构，用于存储和处理企业数据，但它们在数据处理和访问方面有一些显著的区别。

1. 离线数据仓库（Offline Data Warehouse）：\
离线数据仓库通常是基于批处理的，它处理已经存储在数据仓库中的数据。
数据处理是周期性的，通常按照每日、每周或每月的批次处理数据。
离线数据仓库主要用于历史数据分析、报表生成和决策支持。
数据在批处理过程中经过清洗、转换和加载（ETL），以满足分析和报告的需求。
离线数据仓库通常使用传统的数据仓库技术，如关系型数据库和OLAP（联机分析处理）。

2. 实时数据仓库（Real-time Data Warehouse）：\
实时数据仓库是基于流处理的，它可以在数据到达时立即处理数据。
数据处理是连续的，实时数据仓库可以即时响应新数据的到达。
实时数据仓库用于监控、实时分析、实时报告和决策支持。
数据处理通常以流处理或复杂事件处理（CEP）的方式进行，以实现低延迟和实时性。
实时数据仓库可能使用分布式流处理引擎，如Apache Kafka、Apache Flink、Apache Spark Streaming等，以处理数据流。

# 6. 大数据架构
大数据架构是指用于存储和处理大数据的软件系统架构，通常包括数据采集、数据存储、数据处理、数据分析和数据可视化等组件。

##### 1. lambda架构：
lambda架构是一种用于大数据处理的通用架构，它将批处理和流处理结合起来，以实现低延迟和高吞吐量的数据处理。
lambda架构通常包括三个层次：批处理层、速度层和服务层。
    - 批处理层：用于批量处理历史数据，通常使用Hadoop MapReduce、Apache Spark等技术。
    - 速度层：用于处理实时数据，通常使用Apache Storm、Apache Flink等技术。
lambda架构主要是离线数仓+实时数仓结合。

##### 2. kappa架构：

Kappa架构是一种简化的大数据架构，它专注于使用实时流处理来处理数据，而不需要维护两个独立的层。\
Kappa架构使用流处理引擎（如Apache Kafka和Flink）来处理实时数据流，然后将数据存储在持久化存储中（如Hadoop HDFS或云存储）以供查询和分析。\
Kappa架构的一个主要优势是它的简化性，因为它只使用了一个数据处理流程，而不需要维护复杂的批处理和速度处理逻辑。