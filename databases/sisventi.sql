-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: sisventi
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `almacenes`
--

DROP TABLE IF EXISTS `almacenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `almacenes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `pv` int(11) DEFAULT NULL,
  `tiempo` datetime NOT NULL,
  `estado` int(11) NOT NULL DEFAULT '1',
  `user_ing` int(11) DEFAULT NULL,
  `operacion_logistica` int(11) DEFAULT NULL,
  `compra_n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `compra_n_doc_base` int(11) NOT NULL DEFAULT '0',
  `compra_n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `proveedor_n_doc` varchar(255) NOT NULL DEFAULT '',
  `modo_doc` int(11) NOT NULL DEFAULT '0',
  `tipo_doc` int(11) NOT NULL DEFAULT '0',
  `fecha_doc` date NOT NULL,
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_base` int(11) NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `proveedor` int(11) DEFAULT NULL,
  `proveedor_tipo_doc` varchar(255) NOT NULL DEFAULT '',
  `proveedor_condicion` int(11) NOT NULL DEFAULT '0',
  `proveedor_fecha_doc` date NOT NULL,
  `proveedor_moneda_doc` int(11) NOT NULL DEFAULT '0',
  `proveedor_total_doc` double NOT NULL DEFAULT '0',
  `almacen_origen` int(11) DEFAULT NULL,
  `almacen_destino` int(11) DEFAULT NULL,
  `articulo` int(11) DEFAULT NULL,
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `pedido` int(11) NOT NULL DEFAULT '1',
  `cantidad_exp` double NOT NULL DEFAULT '0',
  `cantidad_ing` double NOT NULL DEFAULT '0',
  `peso_exp` double NOT NULL DEFAULT '0',
  `peso_ing` double NOT NULL DEFAULT '0',
  `tipo` varchar(255) NOT NULL DEFAULT '',
  `precio` double NOT NULL DEFAULT '0',
  `fecha_prod` date NOT NULL,
  `fecha_venc` date NOT NULL,
  `extra_data` varchar(255) NOT NULL DEFAULT '',
  `transportista` int(11) DEFAULT NULL,
  `vehiculo` varchar(255) NOT NULL DEFAULT '',
  `grupo` int(11) NOT NULL DEFAULT '0',
  `turno` int(11) DEFAULT NULL,
  `masa` varchar(255) NOT NULL DEFAULT '',
  `temperatura` double NOT NULL DEFAULT '0',
  `peso` double NOT NULL DEFAULT '0',
  `hora_inicial` time NOT NULL,
  `hora_final` time NOT NULL,
  `n_serie` varchar(255) NOT NULL DEFAULT '',
  `n_prefijo_relacion` varchar(255) NOT NULL DEFAULT '',
  `n_doc_relacion` int(11) NOT NULL DEFAULT '0',
  `observaciones` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `user_ing__idx` (`user_ing`),
  KEY `operacion_logistica__idx` (`operacion_logistica`),
  KEY `proveedor__idx` (`proveedor`),
  KEY `almacen_origen__idx` (`almacen_origen`),
  KEY `almacen_destino__idx` (`almacen_destino`),
  KEY `articulo__idx` (`articulo`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `transportista__idx` (`transportista`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `almacenes_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_10` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_2` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_3` FOREIGN KEY (`operacion_logistica`) REFERENCES `operaciones_logisticas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_4` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_5` FOREIGN KEY (`almacen_origen`) REFERENCES `almacenes_lista` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_6` FOREIGN KEY (`almacen_destino`) REFERENCES `almacenes_lista` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_7` FOREIGN KEY (`articulo`) REFERENCES `articulos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_8` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `almacenes_ibfk_9` FOREIGN KEY (`transportista`) REFERENCES `transportistas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenes`
--

LOCK TABLES `almacenes` WRITE;
/*!40000 ALTER TABLE `almacenes` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacenes_lista`
--

DROP TABLE IF EXISTS `almacenes_lista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `almacenes_lista` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `almacen` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `area` varchar(255) NOT NULL DEFAULT '',
  `pv` varchar(255) NOT NULL DEFAULT '',
  `usuario` varchar(255) NOT NULL DEFAULT '',
  `ubigeo` varchar(255) NOT NULL DEFAULT '',
  `direccion` varchar(255) NOT NULL DEFAULT '',
  `tipo_doc` int(11) NOT NULL DEFAULT '0',
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenes_lista`
--

LOCK TABLES `almacenes_lista` WRITE;
/*!40000 ALTER TABLE `almacenes_lista` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacenes_lista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacenes_ubicacion`
--

DROP TABLE IF EXISTS `almacenes_ubicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `almacenes_ubicacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `almacen` varchar(255) NOT NULL DEFAULT '',
  `codbarras` varchar(255) NOT NULL DEFAULT '',
  `ubicacion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenes_ubicacion`
--

LOCK TABLES `almacenes_ubicacion` WRITE;
/*!40000 ALTER TABLE `almacenes_ubicacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacenes_ubicacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `areas`
--

DROP TABLE IF EXISTS `areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `areas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `area` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articulos`
--

DROP TABLE IF EXISTS `articulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articulos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `articulo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articulos`
--

LOCK TABLES `articulos` WRITE;
/*!40000 ALTER TABLE `articulos` DISABLE KEYS */;
/*!40000 ALTER TABLE `articulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_cas`
--

DROP TABLE IF EXISTS `auth_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_cas`
--

LOCK TABLES `auth_cas` WRITE;
/*!40000 ALTER TABLE `auth_cas` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_cas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_event`
--

DROP TABLE IF EXISTS `auth_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
INSERT INTO `auth_event` VALUES (2,'2011-06-08 23:27:50','127.0.0.1',1,'auth','Usuario \'root\' cerró sesión'),(3,'2011-06-08 23:28:04','127.0.0.1',1,'auth','Usuario \'root\' inició sesión'),(4,'2011-06-09 10:57:42','127.0.0.1',1,'auth','Usuario \'root\' inició sesión'),(5,'2011-06-15 10:05:05','127.0.0.1',1,'auth','Usuario \'root\' cerró sesión'),(6,'2011-06-15 10:05:22','127.0.0.1',1,'auth','Usuario \'root\' inició sesión');
/*!40000 ALTER TABLE `auth_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'root','Administrador del sistema'),(2,'administrador','Administrador de punto de venta'),(3,'ventas','Encargado de ventas'),(4,'compras','Encargado de compras'),(5,'almacenes','Encargado de almacenes'),(6,'reportes','Encargado de Reportes');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_membership`
--

DROP TABLE IF EXISTS `auth_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_membership`
--

LOCK TABLES `auth_membership` WRITE;
/*!40000 ALTER TABLE `auth_membership` DISABLE KEYS */;
INSERT INTO `auth_membership` VALUES (1,1,1);
/*!40000 ALTER TABLE `auth_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `table_name` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) DEFAULT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `registration_key` varchar(255) DEFAULT NULL,
  `reset_password_key` varchar(255) DEFAULT NULL,
  `registration_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'root','César','Bustíos Benites','cesar.bustios@ictec.biz','63a9f0ea7bb98050796b649e85481845','2011-06-08','','','');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup`
--

DROP TABLE IF EXISTS `backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `tiempo` datetime NOT NULL,
  `log` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup`
--

LOCK TABLES `backup` WRITE;
/*!40000 ALTER TABLE `backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bancos`
--

DROP TABLE IF EXISTS `bancos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bancos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) NOT NULL DEFAULT '0',
  `fechav` date NOT NULL,
  `fechad` date NOT NULL,
  `banco` varchar(255) NOT NULL DEFAULT '',
  `monto` double NOT NULL DEFAULT '0',
  `cambio` double NOT NULL DEFAULT '0',
  `glosa1` varchar(255) NOT NULL DEFAULT '',
  `glosa2` varchar(255) NOT NULL DEFAULT '',
  `agencia` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancos`
--

LOCK TABLES `bancos` WRITE;
/*!40000 ALTER TABLE `bancos` DISABLE KEYS */;
/*!40000 ALTER TABLE `bancos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `casas`
--

DROP TABLE IF EXISTS `casas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `casas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `casa` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `casas`
--

LOCK TABLES `casas` WRITE;
/*!40000 ALTER TABLE `casas` DISABLE KEYS */;
/*!40000 ALTER TABLE `casas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `categoria` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catmod`
--

DROP TABLE IF EXISTS `catmod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catmod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `catmod` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catmod`
--

LOCK TABLES `catmod` WRITE;
/*!40000 ALTER TABLE `catmod` DISABLE KEYS */;
/*!40000 ALTER TABLE `catmod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_preferentes`
--

DROP TABLE IF EXISTS `clientes_preferentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes_preferentes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  `tiempo` datetime NOT NULL,
  `promocion` varchar(255) NOT NULL DEFAULT '',
  `tarjeta` varchar(255) NOT NULL DEFAULT '',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `clientes_preferentes_ibfk_1` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_preferentes`
--

LOCK TABLES `clientes_preferentes` WRITE;
/*!40000 ALTER TABLE `clientes_preferentes` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes_preferentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras_ordenes`
--

DROP TABLE IF EXISTS `compras_ordenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compras_ordenes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `tiempo` datetime NOT NULL,
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_base` int(11) NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `estado` int(11) NOT NULL DEFAULT '1',
  `area` int(11) DEFAULT NULL,
  `forma_pago` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  `cantidad_proveedor` double NOT NULL DEFAULT '0',
  `moneda` int(11) DEFAULT NULL,
  `precio_neto` double NOT NULL DEFAULT '0',
  `precio_imp` double NOT NULL DEFAULT '0',
  `precio_bruto` double NOT NULL DEFAULT '0',
  `sub_total_neto` double NOT NULL DEFAULT '0',
  `sub_total_imp` double NOT NULL DEFAULT '0',
  `sub_total_bruto` double NOT NULL DEFAULT '0',
  `proveedor` int(11) DEFAULT NULL,
  `total_neto` double NOT NULL DEFAULT '0',
  `total_imp` double NOT NULL DEFAULT '0',
  `total_bruto` double NOT NULL DEFAULT '0',
  `total_texto` varchar(255) NOT NULL DEFAULT '',
  `fecha_entrega` date NOT NULL,
  `lugar_entrega` varchar(255) NOT NULL DEFAULT '',
  `user_req` varchar(255) NOT NULL DEFAULT '',
  `user_ing` int(11) DEFAULT NULL,
  `user_aut1` int(11) DEFAULT NULL,
  `user_aut2` int(11) DEFAULT NULL,
  `user_anul` int(11) DEFAULT NULL,
  `tiempo_anul` datetime NOT NULL,
  `observaciones` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `area__idx` (`area`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `moneda__idx` (`moneda`),
  KEY `proveedor__idx` (`proveedor`),
  KEY `user_ing__idx` (`user_ing`),
  KEY `user_aut1__idx` (`user_aut1`),
  KEY `user_aut2__idx` (`user_aut2`),
  KEY `user_anul__idx` (`user_anul`),
  CONSTRAINT `compras_ordenes_ibfk_1` FOREIGN KEY (`area`) REFERENCES `areas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_3` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_4` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_5` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_6` FOREIGN KEY (`user_aut1`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_7` FOREIGN KEY (`user_aut2`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `compras_ordenes_ibfk_8` FOREIGN KEY (`user_anul`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_ordenes`
--

LOCK TABLES `compras_ordenes` WRITE;
/*!40000 ALTER TABLE `compras_ordenes` DISABLE KEYS */;
/*!40000 ALTER TABLE `compras_ordenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condiciones_comerciales`
--

DROP TABLE IF EXISTS `condiciones_comerciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condiciones_comerciales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `condicion` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `codigo` int(11) NOT NULL DEFAULT '0',
  `dias` int(11) NOT NULL DEFAULT '0',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condiciones_comerciales`
--

LOCK TABLES `condiciones_comerciales` WRITE;
/*!40000 ALTER TABLE `condiciones_comerciales` DISABLE KEYS */;
/*!40000 ALTER TABLE `condiciones_comerciales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_insumos`
--

DROP TABLE IF EXISTS `control_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_insumos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(255) NOT NULL DEFAULT '',
  `gramos` double NOT NULL DEFAULT '0',
  `adicional` double NOT NULL DEFAULT '0',
  `estado` int(11) NOT NULL DEFAULT '0',
  `truco` int(11) NOT NULL DEFAULT '0',
  `orden` int(11) NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_insumos`
--

LOCK TABLES `control_insumos` WRITE;
/*!40000 ALTER TABLE `control_insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_produccion`
--

DROP TABLE IF EXISTS `control_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_produccion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `turno` varchar(255) NOT NULL DEFAULT '',
  `producto` varchar(255) NOT NULL DEFAULT '',
  `producto_derivado` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_produccion`
--

LOCK TABLES `control_produccion` WRITE;
/*!40000 ALTER TABLE `control_produccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `criterio`
--

DROP TABLE IF EXISTS `criterio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `criterio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cp` varchar(255) NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(255) NOT NULL DEFAULT '',
  `turno` varchar(255) NOT NULL DEFAULT '',
  `porcentaje` double NOT NULL DEFAULT '100',
  `codbarras` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `criterio_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `criterio`
--

LOCK TABLES `criterio` WRITE;
/*!40000 ALTER TABLE `criterio` DISABLE KEYS */;
/*!40000 ALTER TABLE `criterio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `criterio2`
--

DROP TABLE IF EXISTS `criterio2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `criterio2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `turno` varchar(255) NOT NULL DEFAULT '',
  `cp` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `criterio2`
--

LOCK TABLES `criterio2` WRITE;
/*!40000 ALTER TABLE `criterio2` DISABLE KEYS */;
/*!40000 ALTER TABLE `criterio2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas_por_cobrar`
--

DROP TABLE IF EXISTS `cuentas_por_cobrar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuentas_por_cobrar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha_doc` date NOT NULL,
  `documento` varchar(255) NOT NULL,
  `cliente` varchar(255) NOT NULL,
  `accion` varchar(255) NOT NULL,
  `neto_ingreso` double NOT NULL DEFAULT '0',
  `impuesto_ingreso` double NOT NULL DEFAULT '0',
  `bruto_ingreso` double NOT NULL DEFAULT '0',
  `neto_salida` double NOT NULL DEFAULT '0',
  `impuesto_salida` double NOT NULL DEFAULT '0',
  `bruto_salida` double NOT NULL DEFAULT '0',
  `fecha_venc` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas_por_cobrar`
--

LOCK TABLES `cuentas_por_cobrar` WRITE;
/*!40000 ALTER TABLE `cuentas_por_cobrar` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuentas_por_cobrar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas_por_pagar`
--

DROP TABLE IF EXISTS `cuentas_por_pagar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuentas_por_pagar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha_doc` date NOT NULL,
  `documento` varchar(255) NOT NULL,
  `proveedor` varchar(255) NOT NULL,
  `accion` varchar(255) NOT NULL,
  `neto_ingreso` double NOT NULL DEFAULT '0',
  `impuesto_ingreso` double NOT NULL DEFAULT '0',
  `bruto_ingreso` double NOT NULL DEFAULT '0',
  `neto_salida` double NOT NULL DEFAULT '0',
  `impuesto_salida` double NOT NULL DEFAULT '0',
  `bruto_salida` double NOT NULL DEFAULT '0',
  `fecha_venc` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas_por_pagar`
--

LOCK TABLES `cuentas_por_pagar` WRITE;
/*!40000 ALTER TABLE `cuentas_por_pagar` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuentas_por_pagar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery`
--

DROP TABLE IF EXISTS `delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `delivery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `tiempo` datetime NOT NULL,
  `numero` int(11) NOT NULL DEFAULT '0',
  `cliente` varchar(255) NOT NULL DEFAULT '',
  `docnum` int(11) NOT NULL DEFAULT '0',
  `carac1` varchar(255) NOT NULL DEFAULT '',
  `carac2` varchar(255) NOT NULL DEFAULT '',
  `carac3` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery`
--

LOCK TABLES `delivery` WRITE;
/*!40000 ALTER TABLE `delivery` DISABLE KEYS */;
/*!40000 ALTER TABLE `delivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directorio`
--

DROP TABLE IF EXISTS `directorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `directorio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `razon_social` varchar(255) NOT NULL DEFAULT '',
  `nombre_corto` varchar(255) DEFAULT NULL,
  `rubro` int(11) NOT NULL DEFAULT '0',
  `nombres` varchar(255) NOT NULL DEFAULT '',
  `apellidos` varchar(255) NOT NULL DEFAULT '',
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  `doc_id_aux` varchar(255) DEFAULT NULL,
  `pais` varchar(255) NOT NULL DEFAULT 'Perú',
  `ubigeo` varchar(255) NOT NULL DEFAULT '',
  `direccion` varchar(255) NOT NULL DEFAULT '',
  `codigo_postal` varchar(255) DEFAULT NULL,
  `referencia` varchar(255) DEFAULT NULL,
  `condicion` int(11) DEFAULT NULL,
  `tiempo_cred` int(11) NOT NULL DEFAULT '0',
  `intervalo` int(11) NOT NULL DEFAULT '0',
  `interes` double NOT NULL DEFAULT '0',
  `linea_credito` double NOT NULL DEFAULT '0',
  `representante_legal` varchar(255) DEFAULT NULL,
  `cargo` varchar(255) DEFAULT NULL,
  `fecha` date NOT NULL,
  `sexo` varchar(255) DEFAULT NULL,
  `preferente` char(1) DEFAULT NULL,
  `modo` varchar(255) DEFAULT NULL,
  `tipo_doc` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `condicion__idx` (`condicion`),
  KEY `tipo_doc__idx` (`tipo_doc`),
  CONSTRAINT `directorio_ibfk_1` FOREIGN KEY (`condicion`) REFERENCES `condiciones_comerciales` (`id`) ON DELETE CASCADE,
  CONSTRAINT `directorio_ibfk_2` FOREIGN KEY (`tipo_doc`) REFERENCES `documentos_identidad` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directorio`
--

LOCK TABLES `directorio` WRITE;
/*!40000 ALTER TABLE `directorio` DISABLE KEYS */;
/*!40000 ALTER TABLE `directorio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directorio_auxiliar`
--

DROP TABLE IF EXISTS `directorio_auxiliar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `directorio_auxiliar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime DEFAULT NULL,
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  `telefono` varchar(255) NOT NULL DEFAULT '',
  `tel_prio` int(11) NOT NULL DEFAULT '0',
  `fax` varchar(255) NOT NULL DEFAULT '',
  `fax_prio` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL DEFAULT '',
  `ema_prio` int(11) NOT NULL DEFAULT '0',
  `web` varchar(255) NOT NULL DEFAULT '',
  `web_prio` int(11) NOT NULL DEFAULT '0',
  `contacto` varchar(255) NOT NULL DEFAULT '',
  `con_prio` int(11) NOT NULL DEFAULT '0',
  `telefono_c` varchar(255) NOT NULL DEFAULT '',
  `tec_prio` int(11) NOT NULL DEFAULT '0',
  `email_c` varchar(255) NOT NULL DEFAULT '',
  `emc_prio` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directorio_auxiliar`
--

LOCK TABLES `directorio_auxiliar` WRITE;
/*!40000 ALTER TABLE `directorio_auxiliar` DISABLE KEYS */;
/*!40000 ALTER TABLE `directorio_auxiliar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documentos_comerciales`
--

DROP TABLE IF EXISTS `documentos_comerciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documentos_comerciales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `documento` int(11) NOT NULL DEFAULT '0',
  `doc_reg` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `pv` int(11) DEFAULT NULL,
  `caja` int(11) NOT NULL DEFAULT '0',
  `prefijo` varchar(255) NOT NULL DEFAULT '',
  `correlativo` int(11) NOT NULL DEFAULT '0',
  `sufijo` varchar(255) NOT NULL DEFAULT '',
  `copia` int(11) NOT NULL DEFAULT '0',
  `detalle` int(11) NOT NULL DEFAULT '0',
  `limite` int(11) NOT NULL DEFAULT '0',
  `impresion` int(11) NOT NULL DEFAULT '0',
  `impuestos` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  CONSTRAINT `documentos_comerciales_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos_comerciales`
--

LOCK TABLES `documentos_comerciales` WRITE;
/*!40000 ALTER TABLE `documentos_comerciales` DISABLE KEYS */;
/*!40000 ALTER TABLE `documentos_comerciales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documentos_identidad`
--

DROP TABLE IF EXISTS `documentos_identidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documentos_identidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `nombre` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos_identidad`
--

LOCK TABLES `documentos_identidad` WRITE;
/*!40000 ALTER TABLE `documentos_identidad` DISABLE KEYS */;
INSERT INTO `documentos_identidad` VALUES (1,'2011-06-09 12:11:14','D.N.I.'),(2,'2011-06-09 12:11:21','R.U.C.');
/*!40000 ALTER TABLE `documentos_identidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docventa`
--

DROP TABLE IF EXISTS `docventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docventa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `caja` int(11) NOT NULL DEFAULT '0',
  `fecha_vta` date NOT NULL,
  `tiempo` datetime NOT NULL,
  `n_doc_base` int(11) NOT NULL DEFAULT '0',
  `estado` varchar(255) NOT NULL DEFAULT '',
  `comprobante` int(11) NOT NULL DEFAULT '0',
  `cliente` varchar(255) NOT NULL DEFAULT '',
  `cv_ing` int(11) NOT NULL DEFAULT '0',
  `fp` int(11) NOT NULL DEFAULT '0',
  `vales` varchar(255) NOT NULL DEFAULT '',
  `sello` varchar(255) NOT NULL DEFAULT '',
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `detalle` varchar(255) NOT NULL DEFAULT '',
  `precio` double NOT NULL DEFAULT '0',
  `cantidad` int(11) NOT NULL DEFAULT '0',
  `sub_total_bruto` double NOT NULL DEFAULT '0',
  `sub_total_impto` varchar(255) NOT NULL DEFAULT '',
  `sub_total_neto` double NOT NULL DEFAULT '0',
  `total` double NOT NULL DEFAULT '0',
  `detalle_impto` varchar(255) NOT NULL DEFAULT '',
  `total_neto` double NOT NULL DEFAULT '0',
  `mntsol` double NOT NULL DEFAULT '0',
  `mntdol` double NOT NULL DEFAULT '0',
  `cv_anul` int(11) NOT NULL DEFAULT '0',
  `imod` int(11) NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `data_1` varchar(255) NOT NULL DEFAULT '',
  `fecha_vto` date NOT NULL,
  `condicion_comercial` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `condicion_comercial__idx` (`condicion_comercial`),
  CONSTRAINT `docventa_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `docventa_ibfk_2` FOREIGN KEY (`condicion_comercial`) REFERENCES `condiciones_comerciales` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docventa`
--

LOCK TABLES `docventa` WRITE;
/*!40000 ALTER TABLE `docventa` DISABLE KEYS */;
/*!40000 ALTER TABLE `docventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empaques`
--

DROP TABLE IF EXISTS `empaques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empaques` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `empaque` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empaques`
--

LOCK TABLES `empaques` WRITE;
/*!40000 ALTER TABLE `empaques` DISABLE KEYS */;
/*!40000 ALTER TABLE `empaques` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factores_merma`
--

DROP TABLE IF EXISTS `factores_merma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `factores_merma` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `cp` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `valor` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `factores_merma_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factores_merma`
--

LOCK TABLES `factores_merma` WRITE;
/*!40000 ALTER TABLE `factores_merma` DISABLE KEYS */;
/*!40000 ALTER TABLE `factores_merma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `formas_pago`
--

DROP TABLE IF EXISTS `formas_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formas_pago` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `forma_pago` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formas_pago`
--

LOCK TABLES `formas_pago` WRITE;
/*!40000 ALTER TABLE `formas_pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `formas_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generos`
--

DROP TABLE IF EXISTS `generos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `generos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `genero` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generos`
--

LOCK TABLES `generos` WRITE;
/*!40000 ALTER TABLE `generos` DISABLE KEYS */;
/*!40000 ALTER TABLE `generos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupo_distribucion`
--

DROP TABLE IF EXISTS `grupo_distribucion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_distribucion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `grupo_distribucion` varchar(255) NOT NULL DEFAULT '',
  `registro` datetime NOT NULL,
  `turno` int(11) DEFAULT NULL,
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `prioridad` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `grupo_distribucion_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_distribucion`
--

LOCK TABLES `grupo_distribucion` WRITE;
/*!40000 ALTER TABLE `grupo_distribucion` DISABLE KEYS */;
/*!40000 ALTER TABLE `grupo_distribucion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `impuestos`
--

DROP TABLE IF EXISTS `impuestos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `impuestos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `abreviatura` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `valor` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `impuestos`
--

LOCK TABLES `impuestos` WRITE;
/*!40000 ALTER TABLE `impuestos` DISABLE KEYS */;
/*!40000 ALTER TABLE `impuestos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro`
--

DROP TABLE IF EXISTS `maestro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras` varchar(255) NOT NULL DEFAULT '',
  `pv` int(11) DEFAULT NULL,
  `grupo_venta` varchar(255) NOT NULL DEFAULT '',
  `articulo` int(11) DEFAULT NULL,
  `casa` int(11) DEFAULT NULL,
  `sub_casa` int(11) DEFAULT NULL,
  `genero` int(11) DEFAULT NULL,
  `sub_genero` int(11) DEFAULT NULL,
  `empaque` int(11) DEFAULT NULL,
  `sello` int(11) DEFAULT NULL,
  `sub_sello` int(11) DEFAULT NULL,
  `tipo` int(11) DEFAULT NULL,
  `catmod` int(11) DEFAULT NULL,
  `categoria` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `proveedor` int(11) DEFAULT NULL,
  `moneda` int(11) DEFAULT NULL,
  `precio` double NOT NULL DEFAULT '0',
  `modo_impuesto` int(11) NOT NULL DEFAULT '0',
  `impuesto` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `alias` varchar(255) NOT NULL DEFAULT '',
  `descuento` int(11) NOT NULL DEFAULT '0',
  `dependencia` int(11) NOT NULL DEFAULT '0',
  `unidad_medida_valor` double NOT NULL DEFAULT '0',
  `aux_num_data` int(11) NOT NULL DEFAULT '0',
  `stock_min` double NOT NULL DEFAULT '0',
  `stock_max` double NOT NULL DEFAULT '0',
  `reposicion` int(11) NOT NULL DEFAULT '0',
  `ventas_key` int(11) NOT NULL DEFAULT '0',
  `fecha` date NOT NULL,
  `unidad_medida` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `articulo__idx` (`articulo`),
  KEY `casa__idx` (`casa`),
  KEY `sub_casa__idx` (`sub_casa`),
  KEY `genero__idx` (`genero`),
  KEY `sub_genero__idx` (`sub_genero`),
  KEY `empaque__idx` (`empaque`),
  KEY `sello__idx` (`sello`),
  KEY `sub_sello__idx` (`sub_sello`),
  KEY `tipo__idx` (`tipo`),
  KEY `catmod__idx` (`catmod`),
  KEY `categoria__idx` (`categoria`),
  KEY `status__idx` (`status`),
  KEY `proveedor__idx` (`proveedor`),
  KEY `moneda__idx` (`moneda`),
  KEY `unidad_medida__idx` (`unidad_medida`),
  CONSTRAINT `maestro_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_10` FOREIGN KEY (`tipo`) REFERENCES `tipos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_11` FOREIGN KEY (`catmod`) REFERENCES `catmod` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_12` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_13` FOREIGN KEY (`status`) REFERENCES `status` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_14` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_15` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_16` FOREIGN KEY (`unidad_medida`) REFERENCES `unidades_medida` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_2` FOREIGN KEY (`articulo`) REFERENCES `articulos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_3` FOREIGN KEY (`casa`) REFERENCES `casas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_4` FOREIGN KEY (`sub_casa`) REFERENCES `sub_casas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_5` FOREIGN KEY (`genero`) REFERENCES `generos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_6` FOREIGN KEY (`sub_genero`) REFERENCES `sub_generos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_7` FOREIGN KEY (`empaque`) REFERENCES `empaques` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_8` FOREIGN KEY (`sello`) REFERENCES `sellos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_ibfk_9` FOREIGN KEY (`sub_sello`) REFERENCES `sub_sellos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro`
--

LOCK TABLES `maestro` WRITE;
/*!40000 ALTER TABLE `maestro` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_auxiliar`
--

DROP TABLE IF EXISTS `maestro_auxiliar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_auxiliar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `valor` varchar(255) NOT NULL DEFAULT '',
  `prioridad` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `maestro_auxiliar_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_auxiliar`
--

LOCK TABLES `maestro_auxiliar` WRITE;
/*!40000 ALTER TABLE `maestro_auxiliar` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_auxiliar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_dependencias`
--

DROP TABLE IF EXISTS `maestro_dependencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_dependencias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `modo` int(11) DEFAULT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `data` varchar(255) NOT NULL DEFAULT '',
  `estado` int(11) NOT NULL DEFAULT '1',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `maestro_dependencias_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_dependencias_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_dependencias_ibfk_3` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_dependencias`
--

LOCK TABLES `maestro_dependencias` WRITE;
/*!40000 ALTER TABLE `maestro_dependencias` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_dependencias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_descuentos`
--

DROP TABLE IF EXISTS `maestro_descuentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_descuentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `tiempo` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `codbarras` int(11) DEFAULT NULL,
  `descuento` double NOT NULL DEFAULT '0',
  `monto_req` double NOT NULL DEFAULT '0',
  `user_nivel` int(11) NOT NULL DEFAULT '0',
  `fecha_inicio` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `fecha_fin` date NOT NULL,
  `hora_fin` time NOT NULL,
  `estado` int(11) NOT NULL DEFAULT '1',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `maestro_descuentos_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_descuentos_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_descuentos_ibfk_3` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_descuentos`
--

LOCK TABLES `maestro_descuentos` WRITE;
/*!40000 ALTER TABLE `maestro_descuentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_descuentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_posiciones`
--

DROP TABLE IF EXISTS `maestro_posiciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_posiciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `codbarras` int(11) DEFAULT NULL,
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `maestro_posiciones_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_posiciones`
--

LOCK TABLES `maestro_posiciones` WRITE;
/*!40000 ALTER TABLE `maestro_posiciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_posiciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_proveedores`
--

DROP TABLE IF EXISTS `maestro_proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `proveedor` int(11) DEFAULT NULL,
  `unidad_medida` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `proveedor__idx` (`proveedor`),
  KEY `unidad_medida__idx` (`unidad_medida`),
  CONSTRAINT `maestro_proveedores_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_proveedores_ibfk_2` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_proveedores_ibfk_3` FOREIGN KEY (`unidad_medida`) REFERENCES `unidades_medida` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_proveedores`
--

LOCK TABLES `maestro_proveedores` WRITE;
/*!40000 ALTER TABLE `maestro_proveedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestro_valores`
--

DROP TABLE IF EXISTS `maestro_valores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestro_valores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `tiempo` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `precio` double NOT NULL DEFAULT '0',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `maestro_valores_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_valores_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maestro_valores_ibfk_3` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_valores`
--

LOCK TABLES `maestro_valores` WRITE;
/*!40000 ALTER TABLE `maestro_valores` DISABLE KEYS */;
/*!40000 ALTER TABLE `maestro_valores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modos_logisticos`
--

DROP TABLE IF EXISTS `modos_logisticos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modos_logisticos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo_logistico` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modos_logisticos`
--

LOCK TABLES `modos_logisticos` WRITE;
/*!40000 ALTER TABLE `modos_logisticos` DISABLE KEYS */;
/*!40000 ALTER TABLE `modos_logisticos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modos_pvr`
--

DROP TABLE IF EXISTS `modos_pvr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modos_pvr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tabla` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `modo_tabla` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modos_pvr`
--

LOCK TABLES `modos_pvr` WRITE;
/*!40000 ALTER TABLE `modos_pvr` DISABLE KEYS */;
/*!40000 ALTER TABLE `modos_pvr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monedas`
--

DROP TABLE IF EXISTS `monedas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monedas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `simbolo` varchar(255) NOT NULL DEFAULT '',
  `orden` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monedas`
--

LOCK TABLES `monedas` WRITE;
/*!40000 ALTER TABLE `monedas` DISABLE KEYS */;
/*!40000 ALTER TABLE `monedas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operaciones_logisticas`
--

DROP TABLE IF EXISTS `operaciones_logisticas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operaciones_logisticas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `operacion` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `operacion_relac` varchar(255) NOT NULL DEFAULT '',
  `almacen_relac` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operaciones_logisticas`
--

LOCK TABLES `operaciones_logisticas` WRITE;
/*!40000 ALTER TABLE `operaciones_logisticas` DISABLE KEYS */;
/*!40000 ALTER TABLE `operaciones_logisticas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `turno` int(11) DEFAULT NULL,
  `grupo_distribucion` int(11) DEFAULT NULL,
  `area` int(11) DEFAULT NULL,
  `genero` int(11) DEFAULT NULL,
  `tipo` int(11) NOT NULL DEFAULT '0',
  `user_req` int(11) DEFAULT NULL,
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_base` int(11) NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  `peso` double NOT NULL DEFAULT '0',
  `detalle` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  `estado` int(11) NOT NULL DEFAULT '1',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `turno__idx` (`turno`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  KEY `area__idx` (`area`),
  KEY `genero__idx` (`genero`),
  KEY `user_req__idx` (`user_req`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_4` FOREIGN KEY (`area`) REFERENCES `areas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_5` FOREIGN KEY (`genero`) REFERENCES `generos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_6` FOREIGN KEY (`user_req`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_7` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_8` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos_emergencia_produccion`
--

DROP TABLE IF EXISTS `pedidos_emergencia_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedidos_emergencia_produccion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date DEFAULT NULL,
  `pv` int(11) DEFAULT NULL,
  `turno` int(11) DEFAULT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `turno__idx` (`turno`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `pedidos_emergencia_produccion_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_emergencia_produccion_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_emergencia_produccion_ibfk_3` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_emergencia_produccion`
--

LOCK TABLES `pedidos_emergencia_produccion` WRITE;
/*!40000 ALTER TABLE `pedidos_emergencia_produccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos_emergencia_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pesos_operaciones`
--

DROP TABLE IF EXISTS `pesos_operaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pesos_operaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `peso_neto` double NOT NULL DEFAULT '0',
  `peso_tara` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `pesos_operaciones_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pesos_operaciones`
--

LOCK TABLES `pesos_operaciones` WRITE;
/*!40000 ALTER TABLE `pesos_operaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `pesos_operaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_administracion`
--

DROP TABLE IF EXISTS `pos_administracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pos_administracion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `caja` int(11) NOT NULL DEFAULT '0',
  `user_ing` int(11) DEFAULT NULL,
  `user_out` int(11) DEFAULT NULL,
  `apertura` datetime NOT NULL,
  `cierre` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `user_ing__idx` (`user_ing`),
  KEY `user_out__idx` (`user_out`),
  CONSTRAINT `pos_administracion_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pos_administracion_ibfk_2` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pos_administracion_ibfk_3` FOREIGN KEY (`user_out`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_administracion`
--

LOCK TABLES `pos_administracion` WRITE;
/*!40000 ALTER TABLE `pos_administracion` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_administracion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_datos`
--

DROP TABLE IF EXISTS `produccion_datos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_datos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `turno` int(11) DEFAULT NULL,
  `grupo_distribucion` int(11) DEFAULT NULL,
  `pv` int(11) DEFAULT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `codbarras_hijo` varchar(255) NOT NULL DEFAULT '',
  `cantidad` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  KEY `pv__idx` (`pv`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `produccion_datos_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_datos_ibfk_2` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_datos_ibfk_3` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_datos_ibfk_4` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_datos`
--

LOCK TABLES `produccion_datos` WRITE;
/*!40000 ALTER TABLE `produccion_datos` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_datos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_derivados`
--

DROP TABLE IF EXISTS `produccion_derivados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_derivados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `turno` int(11) DEFAULT NULL,
  `tipo` int(11) NOT NULL DEFAULT '0',
  `cp_base` varchar(255) NOT NULL DEFAULT '',
  `cp_aux` varchar(255) NOT NULL DEFAULT '',
  `user_ing` int(11) DEFAULT NULL,
  `fecha` date NOT NULL,
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_base` varchar(255) NOT NULL DEFAULT '',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `ing_produccion` double NOT NULL DEFAULT '0',
  `ing_traslado` double NOT NULL DEFAULT '0',
  `ing_varios` double NOT NULL DEFAULT '0',
  `sal_ventas` double NOT NULL DEFAULT '0',
  `sal_merma` double NOT NULL DEFAULT '0',
  `sal_consumo_int` double NOT NULL DEFAULT '0',
  `sal_traslado` double NOT NULL DEFAULT '0',
  `sal_varios` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `user_ing__idx` (`user_ing`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `produccion_derivados_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_derivados_ibfk_2` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_derivados_ibfk_3` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_derivados`
--

LOCK TABLES `produccion_derivados` WRITE;
/*!40000 ALTER TABLE `produccion_derivados` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_derivados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_estadistica`
--

DROP TABLE IF EXISTS `produccion_estadistica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_estadistica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `turno` int(11) DEFAULT NULL,
  `pv` int(11) DEFAULT NULL,
  `codbarras_abuelo` varchar(255) NOT NULL DEFAULT '',
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(255) NOT NULL DEFAULT '',
  `cantidad_abuelo` double NOT NULL DEFAULT '0',
  `cantidad_padre` double NOT NULL DEFAULT '0',
  `porcentaje_padre` double NOT NULL DEFAULT '0',
  `cantidad_hijo` double NOT NULL DEFAULT '0',
  `porcentaje_hijo` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  `porcentaje_general` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `pv__idx` (`pv`),
  CONSTRAINT `produccion_estadistica_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_estadistica_ibfk_2` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_estadistica`
--

LOCK TABLES `produccion_estadistica` WRITE;
/*!40000 ALTER TABLE `produccion_estadistica` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_estadistica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_pedidos`
--

DROP TABLE IF EXISTS `produccion_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `turno` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `turno__idx` (`turno`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `produccion_pedidos_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_pedidos_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_pedidos_ibfk_3` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_pedidos`
--

LOCK TABLES `produccion_pedidos` WRITE;
/*!40000 ALTER TABLE `produccion_pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_planeamiento`
--

DROP TABLE IF EXISTS `produccion_planeamiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_planeamiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date NOT NULL,
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras` int(11) DEFAULT NULL,
  `codbarras_hijo` varchar(255) NOT NULL DEFAULT '',
  `cantidad_prod` double NOT NULL DEFAULT '0',
  `condicion_pedido` varchar(255) NOT NULL DEFAULT '',
  `grupo_distribucion` int(11) DEFAULT NULL,
  `cp` varchar(255) NOT NULL DEFAULT '',
  `turno` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `produccion_planeamiento_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_planeamiento_ibfk_2` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_planeamiento_ibfk_3` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_planeamiento`
--

LOCK TABLES `produccion_planeamiento` WRITE;
/*!40000 ALTER TABLE `produccion_planeamiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_planeamiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_planeamiento_aux`
--

DROP TABLE IF EXISTS `produccion_planeamiento_aux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_planeamiento_aux` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date NOT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `cantidad_prod` double NOT NULL DEFAULT '0',
  `condicion_pedido` varchar(255) NOT NULL DEFAULT '',
  `grupo_distribucion` int(11) DEFAULT NULL,
  `cp` varchar(255) NOT NULL DEFAULT '',
  `turno` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `produccion_planeamiento_aux_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_planeamiento_aux_ibfk_2` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_planeamiento_aux_ibfk_3` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_planeamiento_aux`
--

LOCK TABLES `produccion_planeamiento_aux` WRITE;
/*!40000 ALTER TABLE `produccion_planeamiento_aux` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_planeamiento_aux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_rendimiento`
--

DROP TABLE IF EXISTS `produccion_rendimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produccion_rendimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `fecha` date NOT NULL,
  `turno` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '1',
  `tipo` int(11) NOT NULL DEFAULT '0',
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  `masa` varchar(255) NOT NULL DEFAULT '',
  `peso` double NOT NULL DEFAULT '0',
  `temperatura` double NOT NULL DEFAULT '0',
  `hora_inicial` time NOT NULL,
  `hora_final` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `produccion_rendimiento_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `produccion_rendimiento_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_rendimiento`
--

LOCK TABLES `produccion_rendimiento` WRITE;
/*!40000 ALTER TABLE `produccion_rendimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `produccion_rendimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promociones`
--

DROP TABLE IF EXISTS `promociones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promociones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `porcentaje` double NOT NULL DEFAULT '0',
  `valor` double NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  `codbarras` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL DEFAULT '1',
  `limite` int(11) NOT NULL DEFAULT '0',
  `cond_modo` int(11) NOT NULL DEFAULT '0',
  `cond_valor` int(11) NOT NULL DEFAULT '0',
  `cond_fecha_inic` date NOT NULL,
  `cond_hora_inic` time NOT NULL,
  `cond_fecha_term` date NOT NULL,
  `cond_hora_term` time NOT NULL,
  `estado` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `promociones_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `promociones_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promociones`
--

LOCK TABLES `promociones` WRITE;
/*!40000 ALTER TABLE `promociones` DISABLE KEYS */;
/*!40000 ALTER TABLE `promociones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_venta`
--

DROP TABLE IF EXISTS `puntos_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `puntos_venta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `distrito` varchar(255) NOT NULL DEFAULT '',
  `direccion` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  `posicion2` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(255) NOT NULL DEFAULT '',
  `cab1` varchar(255) NOT NULL DEFAULT '',
  `cab2` varchar(255) NOT NULL DEFAULT '',
  `cab3` varchar(255) NOT NULL DEFAULT '',
  `cab4` varchar(255) NOT NULL DEFAULT '',
  `impt` varchar(255) NOT NULL DEFAULT '',
  `modimp` int(11) NOT NULL DEFAULT '0',
  `modmon` int(11) NOT NULL DEFAULT '0',
  `moneda` int(11) DEFAULT NULL,
  `wincha` varchar(255) NOT NULL DEFAULT '',
  `money_drawer` varchar(255) NOT NULL DEFAULT '',
  `area` int(11) NOT NULL DEFAULT '0',
  `replic_srv` varchar(255) NOT NULL DEFAULT '',
  `replic_db` varchar(255) NOT NULL DEFAULT '',
  `replic_user` varchar(255) NOT NULL DEFAULT '',
  `replic_passwd` varchar(255) NOT NULL DEFAULT '',
  `prodimp` varchar(255) NOT NULL DEFAULT '',
  `prodkey` varchar(255) NOT NULL DEFAULT '',
  `facmerma` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `moneda__idx` (`moneda`),
  CONSTRAINT `puntos_venta_ibfk_1` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_venta`
--

LOCK TABLES `puntos_venta` WRITE;
/*!40000 ALTER TABLE `puntos_venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntos_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_venta_grupos`
--

DROP TABLE IF EXISTS `puntos_venta_grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `puntos_venta_grupos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cp` varchar(255) NOT NULL DEFAULT '',
  `grupo_distribucion` int(11) DEFAULT NULL,
  `turno` int(11) DEFAULT NULL,
  `porcentaje` double NOT NULL DEFAULT '100',
  `codbarras` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  KEY `turno__idx` (`turno`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `puntos_venta_grupos_ibfk_1` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `puntos_venta_grupos_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `puntos_venta_grupos_ibfk_3` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_venta_grupos`
--

LOCK TABLES `puntos_venta_grupos` WRITE;
/*!40000 ALTER TABLE `puntos_venta_grupos` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntos_venta_grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_venta_relaciones`
--

DROP TABLE IF EXISTS `puntos_venta_relaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `puntos_venta_relaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv_padre` varchar(255) NOT NULL DEFAULT '',
  `pv_hijo` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_venta_relaciones`
--

LOCK TABLES `puntos_venta_relaciones` WRITE;
/*!40000 ALTER TABLE `puntos_venta_relaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntos_venta_relaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_venta_satelites`
--

DROP TABLE IF EXISTS `puntos_venta_satelites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `puntos_venta_satelites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv_padre` varchar(255) NOT NULL DEFAULT '',
  `pv_hijo` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_venta_satelites`
--

LOCK TABLES `puntos_venta_satelites` WRITE;
/*!40000 ALTER TABLE `puntos_venta_satelites` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntos_venta_satelites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recetas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras_padre` int(11) DEFAULT NULL,
  `cantidad` double NOT NULL DEFAULT '0',
  `codbarras_hijo` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `estado` int(11) NOT NULL DEFAULT '1',
  `orden` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras_padre__idx` (`codbarras_padre`),
  KEY `codbarras_hijo__idx` (`codbarras_hijo`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`codbarras_padre`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `recetas_ibfk_2` FOREIGN KEY (`codbarras_hijo`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relaciones`
--

DROP TABLE IF EXISTS `relaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras_padre` int(11) DEFAULT NULL,
  `codbarras_hijo` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `orden` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras_padre__idx` (`codbarras_padre`),
  KEY `codbarras_hijo__idx` (`codbarras_hijo`),
  CONSTRAINT `relaciones_ibfk_1` FOREIGN KEY (`codbarras_padre`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `relaciones_ibfk_2` FOREIGN KEY (`codbarras_hijo`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relaciones`
--

LOCK TABLES `relaciones` WRITE;
/*!40000 ALTER TABLE `relaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `relaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rendimientos_sintesis`
--

DROP TABLE IF EXISTS `rendimientos_sintesis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rendimientos_sintesis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `turno` int(11) DEFAULT NULL,
  `tipo` int(11) NOT NULL DEFAULT '0',
  `cantidad` double NOT NULL DEFAULT '0',
  `peso` double NOT NULL DEFAULT '0',
  `merma` double NOT NULL DEFAULT '0',
  `rendimiento` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `rendimientos_sintesis_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rendimientos_sintesis`
--

LOCK TABLES `rendimientos_sintesis` WRITE;
/*!40000 ALTER TABLE `rendimientos_sintesis` DISABLE KEYS */;
/*!40000 ALTER TABLE `rendimientos_sintesis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reportes_configuracion`
--

DROP TABLE IF EXISTS `reportes_configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reportes_configuracion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_reporte` varchar(255) NOT NULL DEFAULT '',
  `detalle_reporte` varchar(255) NOT NULL DEFAULT '',
  `turno` int(11) DEFAULT NULL,
  `pv` int(11) DEFAULT NULL,
  `grupo_distribucion` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `codigo_dato` varchar(255) NOT NULL DEFAULT '',
  `array` varchar(255) NOT NULL DEFAULT '',
  `codbarras_abuelo` varchar(255) NOT NULL DEFAULT '',
  `codbarras_padre` varchar(255) NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `pv__idx` (`pv`),
  KEY `grupo_distribucion__idx` (`grupo_distribucion`),
  CONSTRAINT `reportes_configuracion_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reportes_configuracion_ibfk_2` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reportes_configuracion_ibfk_3` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reportes_configuracion`
--

LOCK TABLES `reportes_configuracion` WRITE;
/*!40000 ALTER TABLE `reportes_configuracion` DISABLE KEYS */;
/*!40000 ALTER TABLE `reportes_configuracion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rubros`
--

DROP TABLE IF EXISTS `rubros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rubros` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `rubro` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rubros`
--

LOCK TABLES `rubros` WRITE;
/*!40000 ALTER TABLE `rubros` DISABLE KEYS */;
/*!40000 ALTER TABLE `rubros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellos`
--

DROP TABLE IF EXISTS `sellos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sellos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `sello` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellos`
--

LOCK TABLES `sellos` WRITE;
/*!40000 ALTER TABLE `sellos` DISABLE KEYS */;
/*!40000 ALTER TABLE `sellos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `status` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_casas`
--

DROP TABLE IF EXISTS `sub_casas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sub_casas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `sub_casa` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_casas`
--

LOCK TABLES `sub_casas` WRITE;
/*!40000 ALTER TABLE `sub_casas` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_casas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_generos`
--

DROP TABLE IF EXISTS `sub_generos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sub_generos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `genero` int(11) DEFAULT NULL,
  `sub_genero` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `genero__idx` (`genero`),
  CONSTRAINT `sub_generos_ibfk_1` FOREIGN KEY (`genero`) REFERENCES `generos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_generos`
--

LOCK TABLES `sub_generos` WRITE;
/*!40000 ALTER TABLE `sub_generos` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_generos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_sellos`
--

DROP TABLE IF EXISTS `sub_sellos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sub_sellos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `sub_sello` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_sellos`
--

LOCK TABLES `sub_sellos` WRITE;
/*!40000 ALTER TABLE `sub_sellos` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_sellos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tablas_modos`
--

DROP TABLE IF EXISTS `tablas_modos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tablas_modos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tabla` varchar(255) NOT NULL DEFAULT '',
  `modo` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tablas_modos`
--

LOCK TABLES `tablas_modos` WRITE;
/*!40000 ALTER TABLE `tablas_modos` DISABLE KEYS */;
/*!40000 ALTER TABLE `tablas_modos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos`
--

DROP TABLE IF EXISTS `tipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `tipo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos`
--

LOCK TABLES `tipos` WRITE;
/*!40000 ALTER TABLE `tipos` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_cambio`
--

DROP TABLE IF EXISTS `tipos_cambio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipos_cambio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `moneda` int(11) DEFAULT NULL,
  `area` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `valor` double NOT NULL DEFAULT '0',
  `user_ing` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `moneda__idx` (`moneda`),
  KEY `area__idx` (`area`),
  KEY `user_ing__idx` (`user_ing`),
  CONSTRAINT `tipos_cambio_ibfk_1` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tipos_cambio_ibfk_2` FOREIGN KEY (`area`) REFERENCES `areas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tipos_cambio_ibfk_3` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_cambio`
--

LOCK TABLES `tipos_cambio` WRITE;
/*!40000 ALTER TABLE `tipos_cambio` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipos_cambio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transferencias_produccion`
--

DROP TABLE IF EXISTS `transferencias_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transferencias_produccion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codbarras` int(11) DEFAULT NULL,
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `total` int(11) NOT NULL DEFAULT '0',
  `transferencia` int(11) NOT NULL DEFAULT '0',
  `produccion` int(11) NOT NULL DEFAULT '0',
  `turno` int(11) DEFAULT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `transferencias_produccion_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `transferencias_produccion_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transferencias_produccion`
--

LOCK TABLES `transferencias_produccion` WRITE;
/*!40000 ALTER TABLE `transferencias_produccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `transferencias_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transportistas`
--

DROP TABLE IF EXISTS `transportistas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transportistas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `emp_doc_id` varchar(255) NOT NULL DEFAULT '',
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  `nombres` varchar(255) NOT NULL DEFAULT '',
  `apellidos` varchar(255) NOT NULL DEFAULT '',
  `ubigeo` varchar(255) NOT NULL DEFAULT '',
  `direccion` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportistas`
--

LOCK TABLES `transportistas` WRITE;
/*!40000 ALTER TABLE `transportistas` DISABLE KEYS */;
/*!40000 ALTER TABLE `transportistas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnos`
--

DROP TABLE IF EXISTS `turnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `turno` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnos`
--

LOCK TABLES `turnos` WRITE;
/*!40000 ALTER TABLE `turnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `turnos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubigeo_departamentos`
--

DROP TABLE IF EXISTS `ubigeo_departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ubigeo_departamentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departamento` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubigeo_departamentos`
--

LOCK TABLES `ubigeo_departamentos` WRITE;
/*!40000 ALTER TABLE `ubigeo_departamentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `ubigeo_departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubigeo_detalle`
--

DROP TABLE IF EXISTS `ubigeo_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ubigeo_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departamento` varchar(255) NOT NULL DEFAULT '',
  `provincia` varchar(255) NOT NULL DEFAULT '',
  `ubigeo` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubigeo_detalle`
--

LOCK TABLES `ubigeo_detalle` WRITE;
/*!40000 ALTER TABLE `ubigeo_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `ubigeo_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubigeo_provincias`
--

DROP TABLE IF EXISTS `ubigeo_provincias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ubigeo_provincias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departamento` varchar(255) NOT NULL DEFAULT '',
  `provincia` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubigeo_provincias`
--

LOCK TABLES `ubigeo_provincias` WRITE;
/*!40000 ALTER TABLE `ubigeo_provincias` DISABLE KEYS */;
/*!40000 ALTER TABLE `ubigeo_provincias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_medida` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `descripcion` varchar(255) NOT NULL DEFAULT '',
  `modo` int(11) NOT NULL DEFAULT '0',
  `abreviatura_origen` varchar(255) NOT NULL DEFAULT '',
  `abreviatura_destino` varchar(255) NOT NULL DEFAULT '',
  `factor` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variaciones_derivados`
--

DROP TABLE IF EXISTS `variaciones_derivados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variaciones_derivados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `tiempo_ini` datetime NOT NULL,
  `tiempo_fin` datetime NOT NULL,
  `porcentaje` double NOT NULL DEFAULT '0',
  `cp` varchar(255) NOT NULL DEFAULT '',
  `turno` int(11) DEFAULT NULL,
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras__idx` (`codbarras`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `variaciones_derivados_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `variaciones_derivados_ibfk_2` FOREIGN KEY (`turno`) REFERENCES `turnos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variaciones_derivados`
--

LOCK TABLES `variaciones_derivados` WRITE;
/*!40000 ALTER TABLE `variaciones_derivados` DISABLE KEYS */;
/*!40000 ALTER TABLE `variaciones_derivados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiculos`
--

DROP TABLE IF EXISTS `vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehiculos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `doc_id` varchar(255) NOT NULL DEFAULT '',
  `registro` varchar(255) NOT NULL DEFAULT '',
  `marca` varchar(255) NOT NULL DEFAULT '',
  `modelo` varchar(255) NOT NULL DEFAULT '',
  `tipo` varchar(255) NOT NULL DEFAULT '',
  `caracteristicas` varchar(255) NOT NULL DEFAULT '',
  `posicion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiculos`
--

LOCK TABLES `vehiculos` WRITE;
/*!40000 ALTER TABLE `vehiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehiculos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_bancos_cuentas`
--

DROP TABLE IF EXISTS `ventas_bancos_cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas_bancos_cuentas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `entidad` varchar(255) NOT NULL DEFAULT '',
  `moneda` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `moneda__idx` (`moneda`),
  CONSTRAINT `ventas_bancos_cuentas_ibfk_1` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_bancos_cuentas`
--

LOCK TABLES `ventas_bancos_cuentas` WRITE;
/*!40000 ALTER TABLE `ventas_bancos_cuentas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_bancos_cuentas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_bancos_operaciones`
--

DROP TABLE IF EXISTS `ventas_bancos_operaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas_bancos_operaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `fechav` date NOT NULL,
  `fechad` date NOT NULL,
  `banco` varchar(255) NOT NULL DEFAULT '',
  `monto` double NOT NULL DEFAULT '0',
  `cambio` double NOT NULL DEFAULT '0',
  `glosa1` varchar(255) NOT NULL DEFAULT '',
  `glosa2` varchar(255) NOT NULL DEFAULT '',
  `agencia` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  CONSTRAINT `ventas_bancos_operaciones_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_bancos_operaciones`
--

LOCK TABLES `ventas_bancos_operaciones` WRITE;
/*!40000 ALTER TABLE `ventas_bancos_operaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_bancos_operaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_grupos`
--

DROP TABLE IF EXISTS `ventas_grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas_grupos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `codigo` varchar(255) NOT NULL DEFAULT '',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `atajo` varchar(255) NOT NULL DEFAULT '',
  `articulo` varchar(255) NOT NULL DEFAULT '',
  `casa` int(11) DEFAULT NULL,
  `sello` int(11) DEFAULT NULL,
  `genero` int(11) DEFAULT NULL,
  `subgenero` int(11) DEFAULT NULL,
  `categoria` int(11) DEFAULT NULL,
  `aux_data` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `casa__idx` (`casa`),
  KEY `sello__idx` (`sello`),
  KEY `genero__idx` (`genero`),
  KEY `subgenero__idx` (`subgenero`),
  KEY `categoria__idx` (`categoria`),
  CONSTRAINT `ventas_grupos_ibfk_1` FOREIGN KEY (`casa`) REFERENCES `casas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_grupos_ibfk_2` FOREIGN KEY (`sello`) REFERENCES `sellos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_grupos_ibfk_3` FOREIGN KEY (`genero`) REFERENCES `generos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_grupos_ibfk_4` FOREIGN KEY (`subgenero`) REFERENCES `sub_generos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_grupos_ibfk_5` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_grupos`
--

LOCK TABLES `ventas_grupos` WRITE;
/*!40000 ALTER TABLE `ventas_grupos` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_operaciones`
--

DROP TABLE IF EXISTS `ventas_operaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas_operaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `caja` int(11) NOT NULL DEFAULT '0',
  `tiempo` datetime NOT NULL,
  `n_doc_prefijo` varchar(255) NOT NULL DEFAULT '',
  `n_doc_base` varchar(255) NOT NULL DEFAULT '',
  `n_doc_sufijo` varchar(255) NOT NULL DEFAULT '',
  `estado` int(11) NOT NULL DEFAULT '0',
  `documento` int(11) NOT NULL DEFAULT '0',
  `cliente` varchar(255) NOT NULL DEFAULT '',
  `user_ing` int(11) DEFAULT NULL,
  `user_null` int(11) DEFAULT NULL,
  `forma_pago` varchar(255) NOT NULL DEFAULT '',
  `vales` varchar(255) NOT NULL DEFAULT '',
  `sello` int(11) DEFAULT NULL,
  `codbarras` int(11) DEFAULT NULL,
  `precio` double NOT NULL DEFAULT '0',
  `cantidad` int(11) NOT NULL DEFAULT '0',
  `total` double NOT NULL DEFAULT '0',
  `monto_local` double NOT NULL DEFAULT '0',
  `monto_dolar` double NOT NULL DEFAULT '0',
  `data_1` varchar(255) NOT NULL DEFAULT '',
  `data_2` varchar(255) NOT NULL DEFAULT '',
  `imod` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  KEY `user_ing__idx` (`user_ing`),
  KEY `user_null__idx` (`user_null`),
  KEY `sello__idx` (`sello`),
  KEY `codbarras__idx` (`codbarras`),
  CONSTRAINT `ventas_operaciones_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_operaciones_ibfk_2` FOREIGN KEY (`user_ing`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_operaciones_ibfk_3` FOREIGN KEY (`user_null`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_operaciones_ibfk_4` FOREIGN KEY (`sello`) REFERENCES `sellos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ventas_operaciones_ibfk_5` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_operaciones`
--

LOCK TABLES `ventas_operaciones` WRITE;
/*!40000 ALTER TABLE `ventas_operaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_operaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_resumen`
--

DROP TABLE IF EXISTS `ventas_resumen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas_resumen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registro` datetime NOT NULL,
  `pv` int(11) DEFAULT NULL,
  `fecha` date NOT NULL,
  `cnt_doc` int(11) NOT NULL DEFAULT '0',
  `total_neto` double NOT NULL DEFAULT '0',
  `total_igv` double NOT NULL DEFAULT '0',
  `total_srv` double NOT NULL DEFAULT '0',
  `total_bruto` double NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '1',
  `condicion_comercial` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `pv__idx` (`pv`),
  CONSTRAINT `ventas_resumen_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_resumen`
--

LOCK TABLES `ventas_resumen` WRITE;
/*!40000 ALTER TABLE `ventas_resumen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_resumen` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-06-15 10:06:26
