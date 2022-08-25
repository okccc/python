select
    case when state = 1 then '运行中'
         when state = 5 then '停止'
         when state = 6 then '失败'
         when state = 7 then '成功'
    else '未完成' end as state,
    count(*) as num
from
    (
        SELECT
            process_definition_id,
            -- 任务可能会多次错误重试,只取最后一次的执行状态,mysql5不支持row_number,这里使用组合函数代替
            SUBSTRING_INDEX(group_concat(state ORDER BY start_time DESC), ',', 1) as state
        FROM
            -- 查询今天所有工作流实例
            (select * from t_ds_process_instance where substr(start_time,1,10) = '%s') t1
        JOIN
            -- 只监控指定项目下的工作流
            (select id from t_ds_process_definition where project_id in(1, 3, 18, 20, 21, 22, 23, 24, 25)) t2 on t1.process_definition_id = t2.id
        group by process_definition_id
    ) t3
group by state;