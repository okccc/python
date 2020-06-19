### flume
```bash
# flume是基于流式架构的分布式日志采集系统,实时读取本地磁盘数据然后写入hdfs

# 修改配置文件
[root@master1 ~]# vim flume-env.sh
export JAVA_HOME=/usr/java/jdk1.8.0_181-cloudera

# flume优点
1.可以和任意存储进程集成
2.输入数据速率大于写入存储速率,flume会进行缓冲减轻hdfs压力
3.flume使用receiver和sender两个独立事务模型来确保消息能可靠发送
receiver：事务中所有数据全部成功提交到channel之后source才认为该数据读取完成
sender：事务中所有数据全部被sink写出去才会从channel中移除,否则会回滚,所有事件回到channel等待重新传输

# flume组件
event：flume传输数据的基本单元
agent：jvm运行flume的最小独立单元,由source-channel-sink组成
source：接收数据,包括avro/exec/syslog/http/spool dir等各种格式的日志数据
channel：数据缓冲区,相当于消息队列,允许source和sink运行在不同的速率上,包括memory channel(不关心数据丢失)和file channel(落地到磁盘)
channel selectors：包括replicating(将source过来的events发往所有channel)和multiplexing(将source过来的events发往指定channel)
sink：不断轮询channel中的事件并将其移除到存储系统或下一个agent,目的地通常是hdfs/logger等

# web应用通常分布在多台服务器,可以部署多个flume采集日志然后集中到一个flume,再输出到hdfs进行日志分析
```

#### nginx-hdfs.conf
```bash
# 命名agent组件
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# source是文件
a1.sources.r1.type = exec  # execute,表示通过执行linux命令来读取文件
a1.sources.r1.command = tail -f /var/log/hive/hadoop-cmf-hive-HIVESERVER2.log.out  # 要监控的日志文件
# 添加拦截器
a1.sources.r1.interceptors = regex
a1.sources.r1.interceptors.regex.type=REGEX_FILTER
a1.sources.r1.interceptors.regex.regex=^.+uid=.+&uname=.+spuId=.+$
a1.sources.r1.interceptors.regex.excludeEvents=false

# source是目录
a2.sources.r2.type = spooldir
a2.sources.r2.spoolDir = /opt/module/flume/upload
a2.sources.r2.fileSuffix = .COMPLETED
a2.sources.r2.fileHeader = true
a2.sources.r2.ignorePattern = ([^ ]*\.tmp)  # 忽略所有以.tmp结尾的文件2

# source是kafka
a3.sources.r3.type = org.apache.flume.source.kafka.KafkaSource
a3.sources.r3.zookeeperConnect = cdh1:2181
a3.sources.r3.topic = test
a3.sources.r3.groupId = flume
a3.sources.r3.kafka.consumer.auto.offset.reset = earliest
a3.sources.r3.kafka.consumer.timeout.ms = 100

# 配置channel
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000             # 表示channel总容量是1000个event
a1.channels.c1.transactionCapacity = 100   # 表示channel收集到100个event才会提交事务
# 配置sink
a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = hdfs://nameservice1/user/flume/qbsite-events/%y-%m-%d/%H
a1.sinks.k1.hdfs.filePrefix = logs-        # 文件前缀
a1.sinks.k1.hdfs.round = true              # 是否按照时间滚动文件夹
a1.sinks.k1.hdfs.roundUnit = hour          # 定义时间单位
a1.sinks.k1.hdfs.roundValue = 1            # 多久创建一个新的文件夹
a1.sinks.k1.hdfs.useLocalTimeStamp = true  # 是否使用本地时间戳
a1.sinks.k1.hdfs.batchSize = 1000          # 积攒多少个event才flush到hdfs
a1.sinks.k1.hdfs.fileType = DataStream     # 文件类型,默认SequenceFile
a1.sinks.k1.hdfs.rollInterval = 60         # 多久生成一个新的文件
a1.sinks.k1.hdfs.rollSize = 134217728      # 设置每个文件的字节数
a1.sinks.k1.hdfs.rollCount = 0             # 文件的滚动与event数量无关
# 给source和sink绑定channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1

# 启动flume
bin/flume-ng agent -c conf -f conf/nginx-hdfs.conf -n a1
-c  # flume配置文件目录
-f  # 要执行的文件
-n  # agent的名字
-Dflume.root.logger=INFO,console  # 测试监听端口时使用
```

#### nginx-kafka-spark-redis.conf
```bash
# 下载flume整合kafka插件flumeng-kafka-plugin.jar放入flume/lib,启动flume-ng时需要用到的kafka的jar包
# zkclient-0.3.jar、kafka_2.10-0.8.2.2.jar、kafka-clients-0.8.2.2.jar、scala-library-2.10.4.jar、metrics-core-2.2.0.jar也放入flume/lib
# 命名agent组件
a1.sources = r1
a1.channels = c1
a1.sinks = k1
# 配置source
a1.sources.r1.type = exec
a1.sources.r1.command = tail -f /opt/test.log
# 添加拦截器
a1.sources.r1.interceptors = regex
a1.sources.r1.interceptors.regex.type=REGEX_FILTER
a1.sources.r1.interceptors.regex.regex=^.+uid=.+&uname=.+spuId=.+$
a1.sources.r1.interceptors.regex.excludeEvents=false
# 配置channel
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100
# 配置sink
a1.sinks.k1.type = org.apache.flume.plugins.KafkaSink
a1.sinks.k1.metadata.broker.list = ubuntu:9092                            # kafka地址
a1.sinks.k1.partition.key = 0
a1.sinks.k1.partitioner.class = org.apache.flume.plugins.SinglePartition  # kafka分区
a1.sinks.k1.serializer.class = kafka.serializer.StringEncoder             # 序列化
a1.sinks.k1.request.required.acks = 0                                     # 设置ack
a1.sinks.k1.max.message.size = 1000000                                    # message最大尺寸
a1.sinks.k1.producer.type = sync                                          # 同步
a1.sinks.k1.custom.encoding = UTF-8                                       # 编码
a1.sinks.k1.custom.topic.name = test                                      # topic名称
# 给source和sink绑定channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1

# 先启动kafka：
kafka-server-start.sh config/server.properties &
kafka-topics.sh --create --zookeeper ubuntu:2181 --replication-factor 1 --partitions 1 --topic test
kafka-console-consumer.sh --zookeeper ubuntu:2181 --from-beginning --topic test
# 再启动flume-ng：
flume-ng agent -c conf/ -f conf/flume-kafka.conf -n a1 -Dflume.root.logger=INFO,console
# 往监测文件写数据,kafka的consumer接收到消息说明成功
for i in {1..10000}; do echo "hello spark ${i}" >> test.log; echo ${i}; sleep 0.01; done
```

```java
package org.com.qbao.dc.spark.streaming;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.log4j.Logger;
import org.apache.spark.Accumulator;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.StorageLevels;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.VoidFunction;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka.KafkaUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import com.qbao.dc.redis.IRedisService;
import com.qbao.dc.redis.common.RedisModel;
import com.qbao.dc.redis.factory.RedisModelFactory;
import com.qbao.dc.redis.impl.IRedisServiceImpl;
import com.qbao.dc.redis.model.SpuCount;
import com.qbao.dc.redis.model.UserViewCountData;
import redis.clients.jedis.Jedis;
import scala.Tuple2;
public final class KafkaToRedis {
//    private static final Pattern SPACE = Pattern.compile(" ");
    private static Logger logger = Logger.getLogger(KafkaToRedis.class);
    private static IRedisService iRedisService= null;
    private static boolean isInitXml = true;
    @SuppressWarnings({ "deprecation", "serial" })
    public static void main(String[] args) throws InterruptedException {
        //错误提示
        if(args.length < 4){
            System.err.println("Usage: KafkaWordCount <zkQuorum> <group> <topics> <numThreads>");
            System.exit(1);
        }
        //加载配置文件
        SparkConf conf = new SparkConf().setAppName("KafkaToRedis");
        //生成stream context
        JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(3));
        //指定topic的线程数
        int numThreads = Integer.parseInt(args[3]);
        //封装topic
        HashMap<String, Integer> topicMap = new HashMap<String, Integer>();
        String[] topics = args[2].split(",");
        for (String topic : topics) {
            topicMap.put(topic, numThreads);
        }
        //获取kafka数据流
        JavaPairReceiverInputDStream<String, String> messages =
                KafkaUtils.createStream(jssc, args[0], args[1], topicMap,StorageLevels.MEMORY_AND_DISK_SER);
        //将messages转换为DStream数据流
        JavaDStream<String> lines = messages.map(new Function<Tuple2<String,String>, String>() {
            public String call(Tuple2<String, String> tuple2) throws Exception {
                return tuple2._2();
            }
        });
        //将JavaDStream类型转换成String类型
        lines.foreach(new Function<JavaRDD<String>, Void>() {
            @Override
            public Void call(JavaRDD<String> rdd) throws Exception {
                //遍历循环每条记录
                rdd.foreachPartition(new VoidFunction<Iterator<String>>() {
                    @Override
                    public void call(Iterator<String> records) throws Exception {
                        if(isInitXml){
                            //加载spring配置文件
                            String paths[] = new String[]{"qbao_dc_redis_application.xml"};
                            ApplicationContext ctx = new ClassPathXmlApplicationContext(paths);
                            //获取iRedisService接口
                            iRedisService = ctx.getBean(IRedisServiceImpl.class);
                            isInitXml = false;
                        }
                        while(records.hasNext()){
                            //拿到一条记录
                            String record = records.next();
                            //添加regex
                            Pattern p1 = Pattern.compile("uid=(\\d+)");
                            Pattern p2 = Pattern.compile("spuId=(\\d+)");
                            //匹配当前记录
                            Matcher m1 = p1.matcher(record);
                            Matcher m2 = p2.matcher(record);
                            //获取字段值
                            if(m1.find() && m2.find()){
                                UserViewCountData data = new UserViewCountData();
                                String uid = m1.group(1);
                                String spuId = m2.group(1);
                                //获取QueryModel
                                RedisModel queryModel = RedisModelFactory.getQueryModel(uid, UserViewCountData.class);
                                //调用find方法
                                RedisModel model=iRedisService.find(queryModel);
                                //如果该uid已经存在
                                if(model.getValue()!=null){
                                    //获取该uid
                                    data = (UserViewCountData) model.getValue();
                                    //获取该uid对应的所有spus
                                    List<SpuCount> list = data.getSpus();
                                    //判断spuId是否存在
                                    boolean isExist = false;
                                    //循环spucount
                                    for(SpuCount spucount : list){
                                        //spuId已存在
                                        if(spucount.getSpuId().equals(spuId)){
                                            //次数直接+1
                                            spucount.setCount(spucount.getCount()+1);
                                            isExist=true;
                                            break;
                                        }
                                    }
                                    //如果spuId不存在
                                    if(!isExist){
                                        SpuCount spucount = new SpuCount();
                                        //添加该spuId
                                        spucount.setSpuId(spuId);
                                        //给个初始值1
                                        spucount.setCount(1);
                                        //将该spuId添加到spus集合中
                                        list.add(spucount);
                                    }
                                //如果该uid不存在
                                }else{
                                    //先添加该uid
                                    data.setUid(uid);
                                    List<SpuCount> list  = new ArrayList<SpuCount> ();
                                    SpuCount spucount = new SpuCount();
                                    //添加该spuId
                                    spucount.setSpuId(spuId);
                                    //给个初始值1
                                    spucount.setCount(1);
                                    //将该spuId添加到spus集合中
                                    list.add(spucount);
                                    //添加到UserViewCountData
                                    data.setSpus(list);
                                }
                              //获取RedisModel
                              RedisModel redisModel=RedisModelFactory.getRedisModel(data.getUid(), data);
                              //保存到redis
                              iRedisService.save(redisModel);
                            }
//                            Jedis jedis = new Jedis("172.16.14.128", 6379);
//
//                                //jedis.set(m1.group(1), m2.group(1));
//                                jedis.set(m1.group(),m2.group());
//                                jedis.close();
//                            }
                        }
                    }
                });
                return null;
            }
        });
//        //切割
//        JavaDStream<String> words = lines.flatMap(new FlatMapFunction<String, String>() {
//
//            public Iterable<String> call(String s) throws Exception {
//                return Arrays.asList(SPACE.split(s));
//            }
//        });
//        //统计次数
//        JavaPairDStream<String, Integer> wordCounts = words.mapToPair(new PairFunction<String, String, Integer>() {
//
//            public Tuple2<String, Integer> call(String s) throws Exception {
//                return new Tuple2<String, Integer>(s, 1);
//            }
//        }).reduceByKey(new Function2<Integer, Integer, Integer>() {
//
//            public Integer call(Integer a, Integer b) throws Exception {
//                return a + b;
//            }
//        });
//        //输出操作
//        wordCounts.foreachRDD(new Function<JavaPairRDD<String,Integer>, Void>() {
//
//            @Override
//            public Void call(JavaPairRDD<String, Integer> rdd) throws Exception {
//                //遍历循环rdd
//                rdd.foreach(new VoidFunction<Tuple2<String,Integer>>() {
//
//                    @Override
//                    public void call(Tuple2<String, Integer> wordcount) throws Exception {
//                        //看是否打印结果
//                        System.out.println(wordcount._1() + ":" + wordcount._2());
//                        //将wordcount以(k,v)键值对形式存入redis
//                        Jedis jedis = new Jedis("172.16.14.128", 6379);
//                        jedis.select(0);
//                        jedis.set(wordcount._1(), wordcount._2().toString());
//                    }
//                });
//                return null;
//            }
//        });
        //启动程序
        jssc.start();
        jssc.awaitTermination();
    }

```

