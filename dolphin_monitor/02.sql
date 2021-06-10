select
    t3.process_definition_id,
    t3.name as peocess_name,
    t6.name as project_name,
    case when t3.state = 5 then '停止'
         when t3.state = 6 then '失败'
         when t3.state = 1 then '正在运行'
         else '未完成' end as state,
    t5.user_name,
    t3.run_times
from
    (
        select
            t2.process_definition_id,
            substr(t2.name, 1, instr(t2.name, '-') - 1) as name,
            t2.state,
            t2.run_times
        from
        (
            select
                t1.process_definition_id,
                SUBSTRING_INDEX(GROUP_CONCAT(t1.name order by start_time desc), ',', 1) as name,
                SUBSTRING_INDEX(GROUP_CONCAT(t1.state order by start_time desc), ',', 1) as state,
                SUBSTRING_INDEX(GROUP_CONCAT(t1.run_times order by start_time desc), ',', 1) as run_times
            from
                (select * from t_ds_process_instance where substr(start_time, 1, 10) = '%s') t1
            group by process_definition_id
        ) t2
        where
            t2.state != 7
    ) t3
join
    (select id,user_id,project_id from t_ds_process_definition where project_id in (1, 3, 18, 20, 21, 22, 23, 24, 25)) t4 on t3.process_definition_id = t4.id
join
    t_ds_user t5 on t4.user_id = t5.id
join
    t_ds_project t6 on t4.project_id = t6.id;