--
-- Current Database: `migration_project`
--

-- DROP DATABASE IF EXISTS `migration_project`;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `migration_project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `migration_project`;

DROP TABLE IF EXISTS `contrast`;
CREATE TABLE `contrast` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `table_name` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '表名',
  `pk_source` VARCHAR(36) NOT NULL DEFAULT '' COMMENT '来源主键（UUID）',
  `pk_target` INT NOT NULL DEFAULT 0 COMMENT '目标主键（整型自增）',
  `latest_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '来源数据最新时间（用作数据更新依据）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`pk_source`),
  KEY (`pk_target`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关系对照表';

# ALTER TABLE `contrast` ADD KEY (`pk_source`);
# ALTER TABLE `contrast` ADD KEY (`pk_target`);
