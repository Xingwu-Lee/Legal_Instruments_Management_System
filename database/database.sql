/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : layer

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 22/11/2023 13:57:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cases
-- ----------------------------
DROP TABLE IF EXISTS `cases`;
CREATE TABLE `cases`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '案件ID',
  `our_party_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '我方当事人/单位名称',
  `lawyer_id` int(0) NOT NULL COMMENT '委托律师ID',
  `opposite_party_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '对方当事人/单位名称',
  `case_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '案由',
  `court` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '审理机关',
  `trial_level` enum('1','2','3') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '1' COMMENT '审级',
  `dispute_subject` decimal(10, 2) NULL DEFAULT NULL COMMENT '诉讼（仲裁）争议标的',
  `agency_fee` decimal(10, 2) NULL DEFAULT NULL COMMENT '代理费用',
  `c_permission` enum('1','2','3','4','5','6','7','8') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '1' COMMENT '授权选项',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `lawyer_id`(`lawyer_id`) USING BTREE,
  CONSTRAINT `cases_ibfk_1` FOREIGN KEY (`lawyer_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '案件表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cases
-- ----------------------------

-- ----------------------------
-- Table structure for documents
-- ----------------------------
DROP TABLE IF EXISTS `documents`;
CREATE TABLE `documents`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '文书ID',
  `document_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文书编号',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题',
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型',
  `d_permission` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '权限要求',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `document_number`(`document_number`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '文书表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of documents
-- ----------------------------

-- ----------------------------
-- Table structure for engagements
-- ----------------------------
DROP TABLE IF EXISTS `engagements`;
CREATE TABLE `engagements`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '委托关系ID',
  `case_id` int(0) NOT NULL COMMENT '案件ID',
  `party_individual_id` int(0) NULL DEFAULT NULL COMMENT '个人当事人ID',
  `party_legal_id` int(0) NULL DEFAULT NULL COMMENT '法人当事人ID',
  `lawyer_id` int(0) NOT NULL COMMENT '律师ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `case_id`(`case_id`) USING BTREE,
  INDEX `party_individual_id`(`party_individual_id`) USING BTREE,
  INDEX `party_legal_id`(`party_legal_id`) USING BTREE,
  INDEX `lawyer_id`(`lawyer_id`) USING BTREE,
  CONSTRAINT `engagements_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `cases` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `engagements_ibfk_2` FOREIGN KEY (`party_individual_id`) REFERENCES `parties_individual` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `engagements_ibfk_3` FOREIGN KEY (`party_legal_id`) REFERENCES `parties_legal` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `engagements_ibfk_4` FOREIGN KEY (`lawyer_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '委托关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of engagements
-- ----------------------------

-- ----------------------------
-- Table structure for parties_individual
-- ----------------------------
DROP TABLE IF EXISTS `parties_individual`;
CREATE TABLE `parties_individual`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '个人当事人ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电话',
  `citizen_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公民身份号码',
  `postal_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮政编码',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地址',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `citizen_id`(`citizen_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '当事人表（个人）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of parties_individual
-- ----------------------------

-- ----------------------------
-- Table structure for parties_legal
-- ----------------------------
DROP TABLE IF EXISTS `parties_legal`;
CREATE TABLE `parties_legal`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '法人当事人ID',
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '委托单位',
  `legal_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '法人姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电话',
  `position` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '职务',
  `citizen_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公民身份号码',
  `postal_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮政编码',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地址',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `citizen_id`(`citizen_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '当事人表（法人）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of parties_legal
-- ----------------------------

-- ----------------------------
-- Table structure for records
-- ----------------------------
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `document_id` int(0) NOT NULL COMMENT '文书ID',
  `user_id` int(0) NOT NULL COMMENT '用户ID',
  `action` enum('create','read','update','download') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作类型',
  `action_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '操作时间',
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '地点',
  `operator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作员',
  `creation_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '生成文书日期',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `document_id`(`document_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `records_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of records
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `identity_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份识别号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像',
  `role` enum('lawyer','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'lawyer' COMMENT '职务权限',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `register_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '注册时间',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密钥',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `identity_number`(`identity_number`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
