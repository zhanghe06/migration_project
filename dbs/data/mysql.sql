USE `migration_project`;

-- 插入任务信息
TRUNCATE TABLE `tasks`;
INSERT INTO `tasks` VALUES (1, 'table_name_from', 'table_name_to', 'latest_pk_from', 'latest_pk_to', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
