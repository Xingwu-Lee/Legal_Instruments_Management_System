-- 用户表
CREATE TABLE usersusers (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '用户ID',
identity_number VARCHAR(20) NOT NULL COMMENT '身份识别号',
name VARCHAR(50) NOT NULL COMMENT '姓名',
password VARCHAR(255) NOT NULL COMMENT '登录密码',
avatar VARCHAR(255) COMMENT '头像',
role ENUM('lawyer', 'admin') NOT NULL DEFAULT 'lawyer' COMMENT '职务权限',
phone VARCHAR(20) COMMENT '手机号',
register_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
`key` VARCHAR(255) COMMENT '密钥',
UNIQUE KEY (identity_number)
)COMMENT '用户表';

ALTER TABLE users
ADD COLUMN salt VARCHAR(255) COMMENT '盐';


-- 文书表
CREATE TABLE documents (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '文书ID',
document_number VARCHAR(20) NOT NULL COMMENT '文书编号',
title VARCHAR(255) NOT NULL COMMENT '标题',
type VARCHAR(50) NOT NULL COMMENT '类型',
d_permission VARCHAR(50) NOT NULL COMMENT '权限要求',
UNIQUE KEY (document_number)
)COMMENT '文书表';

-- 记录表
CREATE TABLE records (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '记录ID',
document_id INT NOT NULL COMMENT '文书ID',
user_id INT NOT NULL COMMENT '用户ID',
action ENUM('create', 'read', 'update', 'download') NOT NULL COMMENT '操作类型',
action_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
location VARCHAR(100) NOT NULL COMMENT '地点',
operator VARCHAR(100) NOT NULL COMMENT '操作员',
creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成文书日期',
FOREIGN KEY (document_id) REFERENCES documents(id),
FOREIGN KEY (user_id) REFERENCES users(id)
)COMMENT '记录表';

-- 当事人表（个人）
CREATE TABLE parties_individual (
id INT PRIMARY KEY PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '个人当事人ID',
name VARCHAR(50) NOT NULL COMMENT '姓名',
phone VARCHAR(20) COMMENT '电话',
citizen_id VARCHAR(20) NOT NULL COMMENT '公民身份号码',
postal_code VARCHAR(10) COMMENT '邮政编码',
address VARCHAR(255) COMMENT '地址',
email VARCHAR(50) COMMENT '邮箱',
UNIQUE KEY (citizen_id)
)COMMENT '当事人表（个人）';

-- 当事人表（法人）
CREATE TABLE parties_legal (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '法人当事人ID',
company_name VARCHAR(100) NOT NULL COMMENT '委托单位',
legal_name VARCHAR(50) COMMENT '法人姓名',
phone VARCHAR(20) COMMENT '电话',
position VARCHAR(50) COMMENT '职务',
citizen_id VARCHAR(20) NOT NULL COMMENT '公民身份号码',
postal_code VARCHAR(10) COMMENT '邮政编码',
address VARCHAR(255) COMMENT '地址',
email VARCHAR(50) COMMENT '邮箱',
UNIQUE KEY (citizen_id)
)COMMENT '当事人表（法人）';

-- 案件表
CREATE TABLE cases (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '案件ID',
our_party_name VARCHAR(100) NOT NULL COMMENT '我方当事人/单位名称',
lawyer_id INT NOT NULL COMMENT '委托律师ID',
opposite_party_name VARCHAR(100) COMMENT '对方当事人/单位名称',
case_type VARCHAR(50) NOT NULL COMMENT '案由',
court VARCHAR(50) COMMENT '审理机关',
trial_level ENUM('1', '2', '3') NOT NULL DEFAULT '1' COMMENT '审级',
dispute_subject DECIMAL(10, 2) COMMENT '诉讼（仲裁）争议标的',
agency_fee DECIMAL(10, 2) COMMENT '代理费用',
c_permission ENUM('1', '2', '3', '4', '5', '6', '7', '8') NOT NULL DEFAULT '1' COMMENT '授权选项',
FOREIGN KEY (lawyer_id) REFERENCES users(id)
)COMMENT '案件表';

-- 委托关系表
CREATE TABLE engagements (
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '委托关系ID',
case_id INT NOT NULL COMMENT '案件ID',
party_individual_id INT COMMENT '个人当事人ID',
party_legal_id INT COMMENT '法人当事人ID',
lawyer_id INT NOT NULL COMMENT '律师ID',
FOREIGN KEY (case_id) REFERENCES cases(id),
FOREIGN KEY (party_individual_id) REFERENCES parties_individual(id),
FOREIGN KEY (party_legal_id) REFERENCES parties_legal(id),
FOREIGN KEY (lawyer_id) REFERENCES users(id)
)COMMENT '委托关系表';


