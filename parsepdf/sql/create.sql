CREATE TABLE `user_info` (
  `id` varchar(50) NOT NULL DEFAULT '0' COMMENT '编号',
  `name` varchar(10) DEFAULT NULL COMMENT '姓名',
  `card_id` varchar(20) DEFAULT NULL COMMENT '证件号码',
  `currency` varchar(10) DEFAULT NULL COMMENT '币种',
  `account` varchar(50) DEFAULT NULL COMMENT '支付宝账号',
  `begin_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `income_total` decimal(15,2) DEFAULT NULL COMMENT '收入总金额',
  `income_num` int(10) DEFAULT NULL COMMENT '收入总笔数',
  `income_total_capital` varchar(30) DEFAULT NULL COMMENT '收入总金额大写',
  `pay_total` decimal(15,2) DEFAULT NULL COMMENT '支出总金额',
  `pay_num` int(10) DEFAULT NULL COMMENT '支出总笔数',
  `pay_total_capital` varchar(30) DEFAULT NULL COMMENT '支出总金额大写',
  `insert_time` datetime DEFAULT NULL COMMENT '插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户基本信息';

CREATE TABLE `income_pay_detail` (
  `id` varchar(50) DEFAULT NULL COMMENT '编号',
  `flow_id` varchar(50) NOT NULL DEFAULT '0' COMMENT '流水号',
  `create_time` datetime DEFAULT NULL COMMENT '生成时间',
  `remark` text COMMENT '备注',
  `income` decimal(15,2) DEFAULT NULL COMMENT '收入',
  `pay` decimal(15,2) DEFAULT NULL COMMENT '支出',
  `account_surplus` decimal(15,2) DEFAULT NULL COMMENT '账户余额',
  `fund_channel` varchar(10) DEFAULT NULL COMMENT '资金渠道',
  `insert_time` datetime DEFAULT NULL COMMENT '插入时间',
  PRIMARY KEY (`flow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收支明细表';