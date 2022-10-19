/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100137
 Source Host           : localhost:3306
 Source Schema         : medios_basicos

 Target Server Type    : MySQL
 Target Server Version : 100137
 File Encoding         : 65001

 Date: 07/10/2020 02:58:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for equipos_electricos
-- ----------------------------
DROP TABLE IF EXISTS `equipos_electricos`;
CREATE TABLE `equipos_electricos`  (
  `ee_id` int(11) NOT NULL AUTO_INCREMENT,
  `ee_numero_inventario` int(11) NULL DEFAULT NULL,
  `ee_nombre_objeto` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `ee_nombre_local` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `ee_ci_responsable` int(11) NULL DEFAULT NULL,
  `ee_consumo` int(255) NULL DEFAULT NULL,
  `ee_voltaje` int(255) NULL DEFAULT NULL,
  `ee_marca` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `ee_modelo` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ee_id`) USING BTREE,
  INDEX `equipos_electricos_ibfk_1`(`ee_ci_responsable`) USING BTREE,
  CONSTRAINT `equipos_electricos_ibfk_1` FOREIGN KEY (`ee_ci_responsable`) REFERENCES `responsable` (`r_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of equipos_electricos
-- ----------------------------
INSERT INTO `equipos_electricos` VALUES (3, 0, '', '', 7, 0, 110, '', '');
INSERT INTO `equipos_electricos` VALUES (4, 0, '', '', 62, 600, 110, 'sony', '');
INSERT INTO `equipos_electricos` VALUES (6, 1, 'khkjh', 'ffhgfgh', 60, 97, 110, 'lenovo', '');
INSERT INTO `equipos_electricos` VALUES (7, 0, '', '', 61, 0, 110, '', '');
INSERT INTO `equipos_electricos` VALUES (8, 0, '', '', 60, 0, 110, 'lenovo', '');
INSERT INTO `equipos_electricos` VALUES (9, 1, 'mouse', 'Laboratorio', 60, 80, 110, 'logitech', 'l-9299');
INSERT INTO `equipos_electricos` VALUES (10, 19, 'Computadora', 'Laboratorio', 6, 80, 220, 'lenovo', 'L-1092');

-- ----------------------------
-- Table structure for mueble
-- ----------------------------
DROP TABLE IF EXISTS `mueble`;
CREATE TABLE `mueble`  (
  `m_id` int(11) NOT NULL AUTO_INCREMENT,
  `m_numero_inventario` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `m_nombre_objeto` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `m_nombre_local` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `m_ci_responsable` int(255) NULL DEFAULT NULL,
  `m_descripcion` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `m_estado` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `m_matrial` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`m_id`) USING BTREE,
  INDEX `m_ci_responsable`(`m_ci_responsable`) USING BTREE,
  CONSTRAINT `mueble_ibfk_1` FOREIGN KEY (`m_ci_responsable`) REFERENCES `responsable` (`r_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of mueble
-- ----------------------------
INSERT INTO `mueble` VALUES (2, '4', 'mesa', 'Aula', 7, 'ajajjs', 'Bueno', 'Madera');
INSERT INTO `mueble` VALUES (16, '5', 'silla', 'Aula', 60, 'asd', 'Regular', 'madera');
INSERT INTO `mueble` VALUES (17, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (20, '56', 'asd', 'asd', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (29, '0', 'sdfsg', 'fsdf', 6, '', 'Bueno', '');
INSERT INTO `mueble` VALUES (33, '0', 'qwieuasd', 'kasdlk', 6, '', 'Bueno', '');
INSERT INTO `mueble` VALUES (34, '6', 'Computadora', 'Laboratorio', 7, 'Enseñanasa', 'Bueno', 'plástico');
INSERT INTO `mueble` VALUES (37, '56', 'aaaddas', 'assaads', 62, 'adada', 'Bueno', 'adasaad');
INSERT INTO `mueble` VALUES (38, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (42, '56', 'aaaddas', 'Laboratorio', 62, 'adada', 'Bueno', 'adasaad');
INSERT INTO `mueble` VALUES (43, '0', 'qwieuasd', 'kasdlk', 6, '', 'Bueno', '');
INSERT INTO `mueble` VALUES (45, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (46, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (47, '56', 'aaaddas', 'assaads', 62, 'adada', 'Bueno', 'adasaad');
INSERT INTO `mueble` VALUES (48, '56', 'asd', 'Laboratorio', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (49, '6', 'Computadora', 'Laboratorio', 7, 'Enseñanasa', 'Bueno', 'plástico');
INSERT INTO `mueble` VALUES (50, '56', 'asd', 'asd', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (51, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (52, '6', 'Computadora', 'Laboratorio', 7, 'Enseñanasa', 'Bueno', 'plástico');
INSERT INTO `mueble` VALUES (54, '56', 'llajdslkajkl', 'aklalksdjl', 60, 'kjkladjls', 'Bueno', 'adjlkjaklsdj');
INSERT INTO `mueble` VALUES (55, '6', 'asd', 'asd1', 7, 'asd', 'Bueno', 'asd');
INSERT INTO `mueble` VALUES (56, '4', 'mesa', 'Aula', 7, 'ajajjs', 'Bueno', 'Madera');

-- ----------------------------
-- Table structure for responsable
-- ----------------------------
DROP TABLE IF EXISTS `responsable`;
CREATE TABLE `responsable`  (
  `r_id` int(11) NOT NULL AUTO_INCREMENT,
  `r_ci` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `r_nombre` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `r_edad` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `r_sexo` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `r_rol` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `r_ocupacion` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`r_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of responsable
-- ----------------------------
INSERT INTO `responsable` VALUES (6, '97092716266', 'Avril', '32', 'Femenino', 'Jefe de Departamento', 'Jefa');
INSERT INTO `responsable` VALUES (7, '98123015672', 'Ana', '23', 'Femenino', 'Subdirector', 'Chef');
INSERT INTO `responsable` VALUES (60, '97092616366', 'Draker', '18', 'Masculino', 'Director', 'lolololololololololollo');
INSERT INTO `responsable` VALUES (61, '01010129999', 'lisa', '18', 'Femenino', 'Director', 'estudiante');
INSERT INTO `responsable` VALUES (62, '97092616266', 'Antonio', '18', 'Masculino', 'Director', 'Jefe');
INSERT INTO `responsable` VALUES (63, '97092616266', 'sdasd', '18', 'Masculino', 'Director', 'asda');
INSERT INTO `responsable` VALUES (64, '97092516222', 'adas', '18', 'Masculino', 'Director', 'dsf');
INSERT INTO `responsable` VALUES (65, '97092616266', 'asdas', '18', 'Masculino', 'Director', 'asdas');
INSERT INTO `responsable` VALUES (66, '97092616266', 'skakdj', '18', 'Masculino', 'Director', 'adjsl');
INSERT INTO `responsable` VALUES (67, '97090312355', 'asd', '18', 'Masculino', 'Director', 'asda');
INSERT INTO `responsable` VALUES (68, '97090312351', 'asdsa', '18', 'Masculino', 'Director', 'asds');

SET FOREIGN_KEY_CHECKS = 1;
