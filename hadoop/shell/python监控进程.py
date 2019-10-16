# coding=utf-8
import os

def monitor_process():
    # 先判断该进程是否卡死
    process = "/home/mhfq.lock"
    os.system(command="ps -aux|grep mhfq_sentiment.py|grep -v grep|awk '{print $2}' > %s" % process)
    if os.path.getsize(process) > 1:
        with open(process) as f:
            lines = f.readlines()
            for line in lines:
                # 杀掉卡死进程
                os.system(command="kill -9 %d" % int(line[:-1]))
        # 重启进程
        os.system(command='/data/anaconda/bin/python /data/app/reports/mhfq_sentiment.py')


if __name__ == '__main__':
    monitor_process()