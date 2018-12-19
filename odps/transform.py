# coding=utf-8
import json
import time
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


def transform(list_data):
    """
    将data字段转换成要插入的sql语句
    :return:
    """

    # 存放多条记录的列表
    values = []

    for data in list_data:

        # mysql表字段
        fields = [
            "id", "createdBy", "createdOn", "lastModifiedBy", "lastModifiedOn", "createdByName", "lastModifiedByName", 
            "parentId", "projectId", "projectName", "objectType", "type", "name", "displayName", "owner", "ownerName", 
            "status", "deleted", "lockedBy", "lockedByName", "lockedOn", "extend", "folderId", "dataVersion", "deployStatus", 
            "commitStatus", "currentVersion", "content", "enableScheduler", "parentFlowIds", "parameters", "startEffectedDate", 
            "endEffectedDate", "suspend", "dryRun", "cronExpression", "dependentedType", "dependentedNodes", "taskRerunTime", 
            "taskRerunInterval", "manualTrigger", "parentFlows"
        ]

        # 单条sql的value
        value = []
        # 遍历mysql表字段
        for field in fields:
            # 判断字段值类型, 有些值是list类型要转换成字符串
            if type(data.get(field)) is list:
                # 往value添加字段值
                value.append(json.dumps(data.get(field),  ensure_ascii=False))
            else:
                # 其他正常数据类型直接添加
                value.append(data.get(field))
        # 添加系统时间
        value.append(time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime()))

        # 将单条value添加到values集合
        values.append(value)

    return values


if __name__ == "__main__":
    # 加载中间件结果
    data_list = json.load(open("data_list.txt",  encoding="utf-8"))
    res = transform(data_list)
    # 将结果缓存到中间件
    json.dump(res,  open("value_list.txt",  "w",  encoding="utf-8"),  ensure_ascii=False)
