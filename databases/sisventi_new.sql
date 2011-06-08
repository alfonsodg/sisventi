-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: sisventi_old
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
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `estado` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `operacion_logistica` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `compra_n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `compra_n_doc_base` bigint(20) unsigned NOT NULL DEFAULT '0',
  `compra_n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor_n_doc` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo_doc` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `tipo_doc` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `fecha_doc` date NOT NULL DEFAULT '0000-00-00',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_base` bigint(20) unsigned NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor_tipo_doc` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor_condicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `proveedor_fecha_doc` date NOT NULL DEFAULT '0000-00-00',
  `proveedor_moneda_doc` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `proveedor_total_doc` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `almacen_origen` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `almacen_destino` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `articulo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pedido` tinyint(1) unsigned NOT NULL DEFAULT '1',
  `cantidad_exp` double(12,4) NOT NULL DEFAULT '0.0000',
  `cantidad_ing` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso_exp` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso_ing` double(12,4) NOT NULL DEFAULT '0.0000',
  `tipo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `fecha_prod` date NOT NULL DEFAULT '0000-00-00',
  `fecha_venc` date NOT NULL DEFAULT '0000-00-00',
  `extra_data` varchar(150) COLLATE latin1_bin NOT NULL DEFAULT '',
  `transportista` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `vehiculo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `masa` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `temperatura` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `hora_inicial` time NOT NULL DEFAULT '00:00:00',
  `hora_final` time NOT NULL DEFAULT '00:00:00',
  `n_serie` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_prefijo_relacion` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_relacion` bigint(20) unsigned NOT NULL DEFAULT '0',
  `observaciones` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `pv` (`pv`),
  KEY `user_ing` (`user_ing`),
  KEY `almacen_origen` (`almacen_origen`),
  KEY `almacen_destino` (`almacen_destino`),
  KEY `operacion_logistica` (`operacion_logistica`),
  KEY `transportista` (`transportista`),
  KEY `proveedor` (`proveedor`),
  KEY `articulo` (`articulo`),
  KEY `turno` (`turno`),
  CONSTRAINT `almacenes_ibfk_1` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_10` FOREIGN KEY (`turno`) REFERENCES `turnos` (`turno`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_11` FOREIGN KEY (`transportista`) REFERENCES `transportistas` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_2` FOREIGN KEY (`user_ing`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_3` FOREIGN KEY (`almacen_origen`) REFERENCES `almacenes_lista` (`almacen`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_4` FOREIGN KEY (`almacen_destino`) REFERENCES `almacenes_lista` (`almacen`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_5` FOREIGN KEY (`operacion_logistica`) REFERENCES `operaciones_logisticas` (`operacion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_7` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`doc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_8` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `almacenes_ibfk_9` FOREIGN KEY (`articulo`) REFERENCES `articulos` (`articulo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin COMMENT='Warehouse Management';
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `almacen` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `descripcion` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `area` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `usuario` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ubigeo` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `direccion` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo_doc` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `almacen` (`almacen`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `almacen` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ubicacion` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `area` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(8) NOT NULL DEFAULT '',
  `descripcion` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `area` (`area`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `articulo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `articulo` (`articulo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
INSERT INTO `auth_event` VALUES (1,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 1 created'),(2,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 2 created'),(3,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 3 created'),(4,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 4 created'),(5,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 5 created'),(6,'2011-06-06 10:51:50','127.0.0.1',NULL,'auth','Group 6 created'),(7,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 7 created'),(8,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 8 created'),(9,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 9 created'),(10,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 10 created'),(11,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 11 created'),(12,'2011-06-06 10:51:51','127.0.0.1',NULL,'auth','Group 12 created'),(13,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 13 created'),(14,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 14 created'),(15,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 15 created'),(16,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 16 created'),(17,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 17 created'),(18,'2011-06-06 10:55:08','127.0.0.1',NULL,'auth','Group 18 created'),(19,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 19 created'),(20,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 20 created'),(21,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 21 created'),(22,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 22 created'),(23,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 23 created'),(24,'2011-06-06 11:00:40','127.0.0.1',NULL,'auth','Group 24 created'),(25,'2011-06-06 11:18:54','127.0.0.1',1,'auth','Usuario 1 logueado'),(26,'2011-06-06 11:23:31','127.0.0.1',1,'auth','User 1 Logged-out'),(27,'2011-06-06 11:23:38','127.0.0.1',1,'auth','Usuario 1 logueado'),(28,'2011-06-06 11:51:59','127.0.0.1',1,'auth','User 1 Logged-out'),(29,'2011-06-06 11:52:11','127.0.0.1',1,'auth','Usuario 1 logueado'),(30,'2011-06-06 12:44:04','127.0.0.1',1,'auth','User 1 Logged-out'),(31,'2011-06-06 12:44:12','127.0.0.1',1,'auth','Usuario 1 logueado'),(32,'2011-06-06 15:52:03','127.0.0.1',1,'auth','Usuario 1 logueado'),(33,'2011-06-06 15:52:56','127.0.0.1',1,'auth','User 1 Logged-out'),(34,'2011-06-06 15:54:52','127.0.0.1',1,'auth','Usuario 1 logueado'),(35,'2011-06-06 18:00:58','127.0.0.1',1,'auth','Usuario 1 logueado'),(36,'2011-06-07 13:00:35','127.0.0.1',1,'auth','Usuario 1 logueado'),(37,'2011-06-07 16:05:20','127.0.0.1',1,'auth','Usuario 1 logueado'),(38,'2011-06-07 22:03:28','127.0.0.1',1,'auth','Usuario 1 logueado'),(39,'2011-06-08 10:54:04','127.0.0.1',1,'auth','Usuario 1 logueado');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (19,'root','Administrador del  sistema'),(20,'administrador','Administrador de un punto de venta'),(21,'ventas','Encargado de ventas'),(22,'compras','Encargado de compras'),(23,'almacenes','Encargado de almacenes'),(24,'reportes','Encargado de reportes');
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
INSERT INTO `auth_membership` VALUES (1,1,19);
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
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `registration_key` varchar(255) DEFAULT NULL,
  `reset_password_key` varchar(255) DEFAULT NULL,
  `registration_id` varchar(255) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `username` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'César','Bustíos Benites','63a9f0ea7bb98050796b649e85481845','2011-06-06','','','','cesar.bustios@ictec.biz','root');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup`
--

DROP TABLE IF EXISTS `backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `log` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `tiempo` (`tiempo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `pv` smallint(3) NOT NULL DEFAULT '0',
  `fechav` date NOT NULL DEFAULT '0000-00-00',
  `fechad` date NOT NULL DEFAULT '0000-00-00',
  `banco` char(3) COLLATE latin1_bin NOT NULL DEFAULT '',
  `monto` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `cambio` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `glosa1` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `glosa2` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `agencia` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `casa` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `casa` (`casa`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `categoria` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `categoria` (`categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `catmod` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `catmod` (`catmod`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `promocion` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tarjeta` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_ing` smallint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_base` bigint(20) unsigned NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `estado` tinyint(1) unsigned NOT NULL DEFAULT '1',
  `area` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `forma_pago` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `cantidad_proveedor` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `moneda` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio_neto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `precio_imp` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `precio_bruto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `sub_total_neto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `sub_total_imp` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `sub_total_bruto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `proveedor` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `total_neto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `total_imp` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `total_bruto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `total_texto` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha_entrega` date NOT NULL DEFAULT '0000-00-00',
  `lugar_entrega` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_req` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_aut1` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_aut2` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_anul` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tiempo_anul` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `observaciones` varchar(150) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `tiempo` (`tiempo`),
  KEY `user_ing` (`user_ing`),
  KEY `user_aut2` (`user_aut2`),
  KEY `user_aut1` (`user_aut1`),
  KEY `user_anul` (`user_anul`),
  KEY `proveedor` (`proveedor`),
  KEY `area` (`area`),
  CONSTRAINT `compras_ordenes_ibfk_1` FOREIGN KEY (`user_ing`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_2` FOREIGN KEY (`user_aut2`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_3` FOREIGN KEY (`user_aut1`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_4` FOREIGN KEY (`user_anul`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_5` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`doc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_6` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `compras_ordenes_ibfk_7` FOREIGN KEY (`area`) REFERENCES `areas` (`area`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `condicion` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `descripcion` varbinary(40) NOT NULL DEFAULT '',
  `codigo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `dias` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `condicion` (`condicion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `gramos` double(10,2) NOT NULL DEFAULT '0.00',
  `adicional` double(10,2) NOT NULL DEFAULT '0.00',
  `estado` int(11) NOT NULL DEFAULT '0',
  `truco` int(11) NOT NULL DEFAULT '0',
  `orden` int(11) NOT NULL DEFAULT '0',
  `modo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `turno` varchar(5) COLLATE latin1_bin NOT NULL DEFAULT '',
  `producto` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `producto_derivado` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `porcentaje` float(20,8) NOT NULL DEFAULT '100.00000000',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `criterio2`
--

LOCK TABLES `criterio2` WRITE;
/*!40000 ALTER TABLE `criterio2` DISABLE KEYS */;
/*!40000 ALTER TABLE `criterio2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery`
--

DROP TABLE IF EXISTS `delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `delivery` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` smallint(3) unsigned NOT NULL DEFAULT '0',
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `numero` bigint(20) unsigned NOT NULL DEFAULT '0',
  `cliente` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `docnum` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `carac1` varchar(250) COLLATE latin1_bin NOT NULL DEFAULT '',
  `carac2` varchar(250) COLLATE latin1_bin NOT NULL DEFAULT '',
  `carac3` varchar(250) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `numero` (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `nombre_corto` varchar(60) COLLATE latin1_bin NOT NULL DEFAULT '',
  `razon_social` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `rubro` smallint(4) unsigned NOT NULL DEFAULT '0',
  `nombres` varchar(60) COLLATE latin1_bin NOT NULL DEFAULT '',
  `apellidos` varchar(60) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo_doc` char(3) COLLATE latin1_bin NOT NULL DEFAULT '',
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `doc_id_aux` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ubigeo` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `direccion` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codigo_postal` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pais` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `referencia` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `condicion` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tiempo_cred` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `linea_credito` double(12,4) NOT NULL DEFAULT '0.0000',
  `representante_legal` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cargo` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `sexo` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `preferente` tinyint(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `doc_id` (`doc_id`),
  KEY `condicion` (`condicion`),
  CONSTRAINT `directorio_ibfk_1` FOREIGN KEY (`condicion`) REFERENCES `condiciones_comerciales` (`condicion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `telefono` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tel_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `fax` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fax_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `email` varbinary(60) NOT NULL DEFAULT '',
  `ema_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `web` varbinary(60) NOT NULL DEFAULT '',
  `web_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `contacto` varbinary(60) NOT NULL DEFAULT '',
  `con_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `telefono_c` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tec_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `email_c` varbinary(60) NOT NULL DEFAULT '',
  `emc_prio` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `documento` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `doc_reg` char(3) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `caja` smallint(3) unsigned NOT NULL DEFAULT '0',
  `prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `correlativo` bigint(20) unsigned NOT NULL DEFAULT '0',
  `sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `copia` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `detalle` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `limite` bigint(20) unsigned NOT NULL DEFAULT '0',
  `impresion` tinyint(1) NOT NULL DEFAULT '0',
  `impuestos` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `comprobante` (`detalle`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varbinary(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos_identidad`
--

LOCK TABLES `documentos_identidad` WRITE;
/*!40000 ALTER TABLE `documentos_identidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `documentos_identidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docventa`
--

DROP TABLE IF EXISTS `docventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docventa` (
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `pv` smallint(5) unsigned NOT NULL DEFAULT '0',
  `caja` smallint(3) unsigned NOT NULL DEFAULT '0',
  `fecha_vta` date NOT NULL DEFAULT '0000-00-00',
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `n_doc_base` bigint(20) unsigned NOT NULL DEFAULT '0',
  `estado` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `comprobante` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `cliente` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cv_ing` smallint(4) unsigned NOT NULL DEFAULT '0',
  `fp` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `vales` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sello` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codigo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `detalle` varchar(250) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `cantidad` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `sub_total_bruto` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `sub_total_impto` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sub_total_neto` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `total` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `detalle_impto` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `total_neto` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `mntsol` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `mntdol` float(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `cv_anul` smallint(4) unsigned NOT NULL DEFAULT '0',
  `imod` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `data_1` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha_vto` date NOT NULL DEFAULT '0000-00-00',
  `condicion_comercial` tinyint(3) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `numdoc` (`n_doc_base`),
  KEY `codigo` (`codigo`),
  KEY `caja` (`caja`),
  KEY `tiempo` (`tiempo`),
  KEY `pv` (`pv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `empaque` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `empaque` (`empaque`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `valor` double(14,6) unsigned NOT NULL DEFAULT '0.000000',
  `modo` tinyint(2) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `forma_pago` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `forma_pago` (`forma_pago`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `genero` (`genero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(50) NOT NULL DEFAULT '',
  `prioridad` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `grupo_distribucion` (`grupo_distribucion`),
  KEY `turno` (`turno`),
  CONSTRAINT `grupo_distribucion_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`turno`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codigo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `abreviatura` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `valor` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `modo` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_venta` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `articulo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `casa` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sub_casa` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sub_genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `empaque` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sello` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sub_sello` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `catmod` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `categoria` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `status` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `moneda` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio` double(12,4) NOT NULL DEFAULT '0.0000',
  `modo_impuesto` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `impuesto` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `alias` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descuento` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `dependencia` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `unidad_medida_valor` double(20,10) NOT NULL DEFAULT '0.0000000000',
  `aux_num_data` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `stock_min` double(12,4) NOT NULL DEFAULT '0.0000',
  `stock_max` double(12,4) NOT NULL DEFAULT '0.0000',
  `reposicion` smallint(4) unsigned NOT NULL DEFAULT '0',
  `ventas_key` bigint(20) unsigned NOT NULL DEFAULT '0',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `unidad_medida` varchar(6) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `catmod` (`catmod`),
  KEY `moneda` (`moneda`),
  KEY `articulo` (`articulo`),
  KEY `unidad_medida` (`unidad_medida`),
  KEY `sello` (`sello`),
  KEY `status` (`status`),
  KEY `casa` (`casa`),
  KEY `genero` (`genero`),
  KEY `sub_genero` (`sub_genero`),
  KEY `categoria` (`categoria`),
  KEY `impuesto` (`impuesto`),
  KEY `pv` (`pv`),
  KEY `tipo` (`tipo`),
  KEY `empaque` (`empaque`),
  KEY `sub_sello` (`sub_sello`),
  KEY `sub_casa` (`sub_casa`),
  CONSTRAINT `maestro_ibfk_1` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_11` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_12` FOREIGN KEY (`tipo`) REFERENCES `tipos` (`tipo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_13` FOREIGN KEY (`empaque`) REFERENCES `empaques` (`empaque`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_14` FOREIGN KEY (`sub_sello`) REFERENCES `sub_sellos` (`sub_sello`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_15` FOREIGN KEY (`sub_casa`) REFERENCES `sub_casas` (`sub_casa`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_16` FOREIGN KEY (`catmod`) REFERENCES `catmod` (`catmod`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_2` FOREIGN KEY (`articulo`) REFERENCES `articulos` (`articulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_3` FOREIGN KEY (`unidad_medida`) REFERENCES `unidades_medida` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_4` FOREIGN KEY (`sello`) REFERENCES `sellos` (`sello`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_5` FOREIGN KEY (`status`) REFERENCES `status` (`status`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_6` FOREIGN KEY (`casa`) REFERENCES `casas` (`casa`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_7` FOREIGN KEY (`genero`) REFERENCES `generos` (`genero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_8` FOREIGN KEY (`sub_genero`) REFERENCES `sub_generos` (`sub_genero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `maestro_ibfk_9` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`categoria`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `valor` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `prioridad` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  CONSTRAINT `maestro_auxiliar_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `data` varchar(250) COLLATE latin1_bin NOT NULL DEFAULT '',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '1',
  `user_ing` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  CONSTRAINT `maestro_dependencias_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descuento` double(12,4) NOT NULL DEFAULT '0.0000',
  `monto_req` double(12,4) NOT NULL DEFAULT '0.0000',
  `user_nivel` smallint(4) unsigned NOT NULL DEFAULT '0',
  `fecha_inicio` date NOT NULL DEFAULT '0000-00-00',
  `hora_inicio` time NOT NULL DEFAULT '00:00:00',
  `fecha_fin` date NOT NULL DEFAULT '0000-00-00',
  `hora_fin` time NOT NULL DEFAULT '00:00:00',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '1',
  `user_ing` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tiempo` (`tiempo`),
  KEY `codbarras` (`codbarras`),
  CONSTRAINT `maestro_descuentos_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `posicion` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `modo` (`modo`),
  KEY `codbarras` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `proveedor` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `unidad_medida` varchar(6) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `proveedor` (`proveedor`),
  KEY `unidad_medida` (`unidad_medida`),
  CONSTRAINT `maestro_proveedores_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`),
  CONSTRAINT `maestro_proveedores_ibfk_2` FOREIGN KEY (`proveedor`) REFERENCES `directorio` (`doc_id`),
  CONSTRAINT `maestro_proveedores_ibfk_3` FOREIGN KEY (`unidad_medida`) REFERENCES `unidades_medida` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio` double(12,4) NOT NULL DEFAULT '0.0000',
  `user_ing` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `tiempo` (`tiempo`),
  CONSTRAINT `maestro_valores_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo_logistico` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tabla` varchar(60) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(4) NOT NULL DEFAULT '0',
  `descripcion` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo_tabla` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tabla` (`tabla`),
  KEY `modo` (`modo`),
  KEY `descripcion` (`descripcion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(4) NOT NULL DEFAULT '0',
  `codigo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(30) NOT NULL DEFAULT '',
  `simbolo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `orden` tinyint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `operacion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `descripcion` varbinary(60) NOT NULL DEFAULT '',
  `operacion_relac` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `almacen_relac` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `operacion` (`operacion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `area` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `user_req` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_base` bigint(20) unsigned NOT NULL DEFAULT '0',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `detalle` varchar(150) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '1',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pv` (`pv`),
  KEY `turno` (`turno`),
  KEY `area` (`area`),
  KEY `genero` (`genero`),
  KEY `codbarras` (`codbarras`),
  KEY `user_req` (`user_req`),
  KEY `user_ing` (`user_ing`),
  CONSTRAINT `pedidos_ibfk_15` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`codigo`),
  CONSTRAINT `pedidos_ibfk_16` FOREIGN KEY (`turno`) REFERENCES `turnos` (`turno`),
  CONSTRAINT `pedidos_ibfk_17` FOREIGN KEY (`area`) REFERENCES `areas` (`area`),
  CONSTRAINT `pedidos_ibfk_18` FOREIGN KEY (`genero`) REFERENCES `generos` (`genero`),
  CONSTRAINT `pedidos_ibfk_19` FOREIGN KEY (`user_req`) REFERENCES `usuarios` (`cv`),
  CONSTRAINT `pedidos_ibfk_20` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`),
  CONSTRAINT `pedidos_ibfk_21` FOREIGN KEY (`user_ing`) REFERENCES `usuarios` (`cv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) NOT NULL DEFAULT '0.0000',
  `modo` tinyint(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `peso_neto` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso_tara` double(12,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `caja` smallint(3) unsigned NOT NULL DEFAULT '0',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_out` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `apertura` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cierre` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `user_ing` (`user_ing`),
  KEY `user_out` (`user_out`),
  KEY `pv` (`pv`),
  CONSTRAINT `pos_administracion_ibfk_1` FOREIGN KEY (`user_ing`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pos_administracion_ibfk_2` FOREIGN KEY (`user_out`) REFERENCES `usuarios` (`cv`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pos_administracion_ibfk_3` FOREIGN KEY (`pv`) REFERENCES `puntos_venta` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) NOT NULL DEFAULT '0.0000',
  `modo` tinyint(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `codbarras_hijo` (`codbarras_hijo`),
  KEY `fecha` (`fecha`),
  KEY `turno` (`turno`),
  KEY `grupo_distribucion` (`grupo_distribucion`),
  KEY `pv` (`pv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `cp_base` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cp_aux` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_base` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ing_produccion` double(12,4) NOT NULL DEFAULT '0.0000',
  `ing_traslado` double(12,4) NOT NULL DEFAULT '0.0000',
  `ing_varios` double(12,4) NOT NULL DEFAULT '0.0000',
  `sal_ventas` double(12,4) NOT NULL DEFAULT '0.0000',
  `sal_merma` double(12,4) NOT NULL DEFAULT '0.0000',
  `sal_consumo_int` double(12,4) NOT NULL DEFAULT '0.0000',
  `sal_traslado` double(12,4) NOT NULL DEFAULT '0.0000',
  `sal_varios` double(12,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`),
  KEY `turno` (`turno`),
  KEY `codbarras` (`codbarras`),
  KEY `fecha` (`fecha`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_abuelo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad_abuelo` double(12,4) DEFAULT '0.0000',
  `cantidad_padre` double(12,4) DEFAULT '0.0000',
  `porcentaje_padre` double(12,4) DEFAULT '0.0000',
  `cantidad_hijo` double(12,4) DEFAULT '0.0000',
  `porcentaje_hijo` double(12,4) DEFAULT '0.0000',
  `modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `porcentaje_general` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`),
  KEY `codbarras_abuelo` (`codbarras_abuelo`),
  KEY `codbarras_padre` (`codbarras_padre`),
  KEY `codbarras_hijo` (`codbarras_hijo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad_prod` double(12,4) NOT NULL DEFAULT '0.0000',
  `condicion_pedido` char(2) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `turno` (`turno`),
  KEY `codbarras` (`codbarras`),
  KEY `grupo_distribucion` (`grupo_distribucion`),
  CONSTRAINT `produccion_planeamiento_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turnos` (`turno`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `produccion_planeamiento_ibfk_2` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `produccion_planeamiento_ibfk_3` FOREIGN KEY (`grupo_distribucion`) REFERENCES `grupo_distribucion` (`grupo_distribucion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad_prod` double(12,4) NOT NULL DEFAULT '0.0000',
  `condicion_pedido` char(2) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(4) NOT NULL DEFAULT '1',
  `tipo` tinyint(4) NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` double(12,4) NOT NULL DEFAULT '0.0000',
  `masa` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `peso` double(12,4) NOT NULL DEFAULT '0.0000',
  `temperatura` double(12,4) NOT NULL DEFAULT '0.0000',
  `hora_inicial` time NOT NULL DEFAULT '00:00:00',
  `hora_final` time NOT NULL DEFAULT '00:00:00',
  PRIMARY KEY (`id`),
  KEY `fecha` (`fecha`),
  KEY `codbarras` (`codbarras`),
  KEY `masa` (`masa`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` smallint(3) unsigned NOT NULL DEFAULT '0',
  `codigo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `porcentaje` double(12,4) NOT NULL DEFAULT '0.0000',
  `valor` double(12,4) NOT NULL DEFAULT '0.0000',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` smallint(5) unsigned NOT NULL DEFAULT '1',
  `limite` smallint(5) unsigned NOT NULL DEFAULT '0',
  `cond_modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `cond_valor` smallint(5) unsigned NOT NULL DEFAULT '0',
  `cond_fecha_inic` date NOT NULL DEFAULT '2000-01-01',
  `cond_hora_inic` time NOT NULL DEFAULT '00:00:00',
  `cond_fecha_term` date NOT NULL DEFAULT '2999-01-01',
  `cond_hora_term` time NOT NULL DEFAULT '24:00:00',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `producto` (`codbarras`),
  KEY `codigo` (`codigo`),
  CONSTRAINT `promociones_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  `distrito` varchar(25) COLLATE latin1_bin NOT NULL DEFAULT '',
  `direccion` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `posicion` tinyint(4) NOT NULL DEFAULT '0',
  `posicion2` tinyint(4) NOT NULL DEFAULT '0',
  `alias` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cab1` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cab2` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cab3` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cab4` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `impt` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modimp` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `modmon` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `moneda` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `wincha` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `money_drawer` varchar(6) COLLATE latin1_bin NOT NULL DEFAULT '',
  `area` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `replic_srv` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `replic_db` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `replic_user` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `replic_passwd` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `prodimp` varchar(255) COLLATE latin1_bin NOT NULL DEFAULT '',
  `prodkey` varchar(255) COLLATE latin1_bin NOT NULL DEFAULT '',
  `facmerma` float(4,3) NOT NULL DEFAULT '0.000',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `porcentaje` float(20,8) NOT NULL DEFAULT '100.00000000',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `pv_padre` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv_hijo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `pv_padre` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv_hijo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pv_padre` (`pv_padre`),
  KEY `pv_hijo` (`pv_hijo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cantidad` float(20,8) NOT NULL DEFAULT '0.00000000',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '1',
  `orden` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras_padre` (`codbarras_padre`),
  KEY `codbarras_hijo` (`codbarras_hijo`),
  KEY `modo` (`modo`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`codbarras_padre`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `recetas_ibfk_2` FOREIGN KEY (`codbarras_hijo`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `orden` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras_padre` (`codbarras_padre`),
  KEY `codbarras_hijo` (`codbarras_hijo`),
  KEY `modo` (`modo`),
  CONSTRAINT `relaciones_ibfk_1` FOREIGN KEY (`codbarras_padre`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `relaciones_ibfk_2` FOREIGN KEY (`codbarras_hijo`) REFERENCES `maestro` (`codbarras`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `turno` varbinary(10) NOT NULL DEFAULT '',
  `tipo` tinyint(4) NOT NULL DEFAULT '0',
  `cantidad` double(12,4) NOT NULL DEFAULT '0.0000',
  `peso` double(12,4) NOT NULL DEFAULT '0.0000',
  `merma` double(12,4) NOT NULL DEFAULT '0.0000',
  `rendimiento` double(12,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo_reporte` varbinary(30) NOT NULL DEFAULT '',
  `detalle_reporte` varbinary(255) NOT NULL DEFAULT '',
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `grupo_distribucion` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(4) NOT NULL DEFAULT '0',
  `codigo_dato` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `array` varchar(255) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_abuelo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_padre` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras_hijo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(30) NOT NULL DEFAULT '',
  `posicion` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo_reporte`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `rubro` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varbinary(20) NOT NULL DEFAULT '',
  `descripcion` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `rubro` (`rubro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sello` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sello` (`sello`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(20) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sub_casa` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sub_casa` (`sub_casa`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sub_genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sub_genero` (`sub_genero`),
  KEY `genero` (`genero`),
  CONSTRAINT `sub_generos_ibfk_1` FOREIGN KEY (`genero`) REFERENCES `generos` (`genero`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sub_sello` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sub_sello` (`sub_sello`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tabla` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` char(2) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombre` varbinary(40) NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tipo` (`tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `moneda` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `area` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `hora` time NOT NULL DEFAULT '00:00:00',
  `valor` double(12,4) NOT NULL DEFAULT '0.0000',
  `user_ing` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `moneda` (`moneda`),
  KEY `modo` (`modo`),
  KEY `fecha` (`fecha`),
  KEY `valor` (`valor`),
  KEY `area` (`area`),
  CONSTRAINT `tipos_cambio_ibfk_1` FOREIGN KEY (`moneda`) REFERENCES `monedas` (`codigo`),
  CONSTRAINT `tipos_cambio_ibfk_2` FOREIGN KEY (`area`) REFERENCES `areas` (`area`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `codbarras` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varchar(80) COLLATE latin1_bin NOT NULL DEFAULT '',
  `total` int(11) NOT NULL DEFAULT '0',
  `transferencia` int(11) NOT NULL DEFAULT '0',
  `produccion` int(11) NOT NULL DEFAULT '0',
  `turno` varchar(5) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `emp_doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombres` varbinary(60) NOT NULL DEFAULT '',
  `apellidos` varbinary(60) NOT NULL DEFAULT '',
  `ubigeo` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `direccion` varbinary(80) NOT NULL DEFAULT '',
  `posicion` tinyint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`),
  KEY `emp_doc_id` (`emp_doc_id`),
  KEY `doc_id` (`doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `turno` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `descripcion` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `hora_inicio` time NOT NULL DEFAULT '00:00:00',
  `hora_fin` time NOT NULL DEFAULT '00:00:00',
  PRIMARY KEY (`id`),
  KEY `turno` (`turno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `departamento` varchar(5) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(80) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `departamento` (`departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `departamento` varchar(5) COLLATE latin1_bin NOT NULL DEFAULT '',
  `provincia` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ubigeo` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(80) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `ubigeo` (`ubigeo`),
  KEY `departamento` (`departamento`),
  KEY `provincia` (`provincia`),
  CONSTRAINT `ubigeo_detalle_ibfk_1` FOREIGN KEY (`departamento`) REFERENCES `ubigeo_departamentos` (`departamento`),
  CONSTRAINT `ubigeo_detalle_ibfk_2` FOREIGN KEY (`provincia`) REFERENCES `ubigeo_provincias` (`provincia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `departamento` varchar(5) COLLATE latin1_bin NOT NULL DEFAULT '',
  `provincia` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(80) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `provincia` (`provincia`),
  KEY `departamento` (`departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(6) COLLATE latin1_bin NOT NULL DEFAULT '',
  `descripcion` varbinary(40) NOT NULL DEFAULT '',
  `modo` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `abreviatura_origen` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `abreviatura_destino` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `factor` double(20,8) NOT NULL DEFAULT '0.00000000',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `password` varchar(60) COLLATE latin1_bin NOT NULL DEFAULT '',
  `apellidos` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nombres` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cargo` varchar(15) COLLATE latin1_bin NOT NULL DEFAULT '',
  `nivel` smallint(5) unsigned NOT NULL DEFAULT '0',
  `autorizacion` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `almacen` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `area` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `articulo` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `backup` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `casa` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `categoria` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `comprobante` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `condicion` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `corden` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cuenta` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `delivery` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `directorio` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `docventa` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fpago` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `genero` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `gventa` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `indentificacion` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `lista` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ologistica` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pedido` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `produccion_derivados` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `pventa` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `ralmacen` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `receta` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `relacion` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `rubro` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sellos` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `status` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `subgenero` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tcambio` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `usuarios` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `valor` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `varauxiliar` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `vardependencia` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `vardescuentos` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `varvalores` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `variable` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `valores` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `iproducto` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `cliente` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `promocion` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `clientes_preferentes` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `unidadmedida` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `produccion_wong` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  `produccion_dunkin` char(1) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `cv` (`cv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variaciones_derivados`
--

DROP TABLE IF EXISTS `variaciones_derivados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variaciones_derivados` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tiempo_ini` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tiempo_fin` datetime NOT NULL DEFAULT '2999-12-30 23:59:59',
  `porcentaje` double(12,4) unsigned NOT NULL DEFAULT '0.0000',
  `cp` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `turno` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modo` char(1) COLLATE latin1_bin NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codbarras` (`codbarras`),
  KEY `cp` (`cp`),
  CONSTRAINT `variaciones_derivados_ibfk_1` FOREIGN KEY (`codbarras`) REFERENCES `maestro` (`codbarras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `doc_id` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `marca` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `modelo` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `tipo` varchar(50) COLLATE latin1_bin NOT NULL DEFAULT '',
  `caracteristicas` varchar(200) COLLATE latin1_bin NOT NULL DEFAULT '',
  `posicion` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`),
  KEY `doc_id` (`doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codigo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `entidad` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `moneda` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` smallint(3) NOT NULL DEFAULT '0',
  `fechav` date NOT NULL DEFAULT '0000-00-00',
  `fechad` date NOT NULL DEFAULT '0000-00-00',
  `banco` char(3) COLLATE latin1_bin NOT NULL DEFAULT '',
  `monto` double(12,4) NOT NULL DEFAULT '0.0000',
  `cambio` double(12,4) NOT NULL DEFAULT '0.0000',
  `glosa1` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `glosa2` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  `agencia` varchar(10) COLLATE latin1_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `fechav` (`fechav`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre` varchar(30) COLLATE latin1_bin NOT NULL DEFAULT '',
  `atajo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `articulo` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `casa` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sello` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `genero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `subgenero` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `categoria` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `aux_data` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `caja` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `tiempo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `n_doc_prefijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_base` varchar(20) COLLATE latin1_bin NOT NULL DEFAULT '',
  `n_doc_sufijo` varchar(8) COLLATE latin1_bin NOT NULL DEFAULT '',
  `estado` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `documento` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `cliente` varchar(40) COLLATE latin1_bin NOT NULL DEFAULT '',
  `user_ing` smallint(4) unsigned NOT NULL DEFAULT '0',
  `user_null` smallint(4) unsigned NOT NULL DEFAULT '0',
  `forma_pago` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `vales` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `sello` varchar(100) COLLATE latin1_bin NOT NULL DEFAULT '',
  `codbarras` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `precio` double(8,2) NOT NULL DEFAULT '0.00',
  `cantidad` smallint(4) unsigned NOT NULL DEFAULT '0',
  `total` double(12,4) NOT NULL DEFAULT '0.0000',
  `monto_local` double(12,4) NOT NULL DEFAULT '0.0000',
  `monto_dolar` double(12,4) NOT NULL DEFAULT '0.0000',
  `data_1` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `data_2` varchar(16) COLLATE latin1_bin NOT NULL DEFAULT '',
  `imod` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `numdoc` (`n_doc_base`),
  KEY `codigo` (`codbarras`),
  KEY `caja` (`caja`),
  KEY `tiempo` (`tiempo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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
  `registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pv` varchar(4) COLLATE latin1_bin NOT NULL DEFAULT '',
  `fecha` date NOT NULL DEFAULT '0000-00-00',
  `cnt_doc` int(11) unsigned NOT NULL DEFAULT '0',
  `total_neto` double(12,4) NOT NULL DEFAULT '0.0000',
  `total_igv` double(12,4) NOT NULL DEFAULT '0.0000',
  `total_srv` double(12,4) NOT NULL DEFAULT '0.0000',
  `total_bruto` double(12,4) NOT NULL DEFAULT '0.0000',
  `status` tinyint(4) unsigned NOT NULL DEFAULT '1',
  `condicion_comercial` tinyint(3) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
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

-- Dump completed on 2011-06-08 12:55:21
