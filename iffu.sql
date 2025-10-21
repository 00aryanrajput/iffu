-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: iffu
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gallery`
--

DROP TABLE IF EXISTS `gallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text_content` text,
  `file_path` varchar(255) DEFAULT NULL,
  `file_type` enum('image','video') DEFAULT NULL,
  `upload_data` datetime DEFAULT CURRENT_TIMESTAMP,
  `upload_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery`
--

LOCK TABLES `gallery` WRITE;
/*!40000 ALTER TABLE `gallery` DISABLE KEYS */;
INSERT INTO `gallery` VALUES (50,'Queen...🫶🏻🥹❤️‍🩹','IMG-20241231-WA0022.jpg','image','2025-10-21 15:34:47','2025-10-21 15:34:48'),(51,'First_pic_❤️‍🩹','WhatsApp_Image_2025-10-21_at_3.13.11_PM.jpeg','image','2025-10-21 15:35:55','2025-10-21 15:35:55'),(52,'Pagli>>>3','IMG-20240917-WA0094.jpg','image','2025-10-21 15:36:45','2025-10-21 15:36:45'),(53,'tera diya hua 1st_gift..🎀','WhatsApp_Image_2025-10-21_at_3.13.11_PM_1.jpeg','image','2025-10-21 15:37:50','2025-10-21 15:37:50'),(54,'Diwali_random_pic...🎀','IMG_20241030_120933.jpg','image','2025-10-21 15:39:07','2025-10-21 15:39:07'),(55,'cutest_one..🫶🏻','WhatsApp_Video_2025-10-21_at_3.18.32_PM.mp4','video','2025-10-21 15:40:49','2025-10-21 15:40:50'),(56,'samosa_paglu..🫶🏻','WhatsApp_Video_2025-10-21_at_3.18.32_PM_2.mp4','video','2025-10-21 15:42:23','2025-10-21 15:42:24'),(57,'','WhatsApp_Image_2025-10-21_at_3.13.07_PM.jpeg','image','2025-10-21 15:43:35','2025-10-21 15:43:35'),(58,'no one can replace you..🦋🧿','WhatsApp_Image_2025-10-21_at_3.13.10_PM.jpeg','image','2025-10-21 15:44:51','2025-10-21 15:44:52'),(60,'','WhatsApp_Image_2025-10-21_at_3.13.09_PM.jpeg','image','2025-10-21 15:47:24','2025-10-21 15:47:25'),(61,'helmet..🦋🧿','WhatsApp_Video_2025-10-21_at_3.13.05_PM.mp4','video','2025-10-21 15:47:55','2025-10-21 15:47:56'),(62,'madam jii ka gulam..','WhatsApp_Image_2025-10-21_at_3.12.48_PM.jpeg','image','2025-10-21 15:48:57','2025-10-21 15:48:57'),(63,'cutie>>>>>infinite..','WhatsApp_Image_2025-10-21_at_3.12.49_PM.jpeg','image','2025-10-21 15:50:03','2025-10-21 15:50:03'),(64,'🫶🏻🥹❤️‍🩹','WhatsApp_Image_2025-10-21_at_3.12.49_PM_1.jpeg','image','2025-10-21 15:50:49','2025-10-21 15:50:50'),(65,'🫶🏻🥹❤️‍🩹','WhatsApp_Image_2025-10-21_at_3.12.50_PM.jpeg','image','2025-10-21 15:52:12','2025-10-21 15:52:13'),(66,'🫶🏻🥹','WhatsApp_Video_2025-10-21_at_3.13.07_PM.mp4','video','2025-10-21 15:52:42','2025-10-21 15:52:42'),(67,'🫶🏻','WhatsApp_Video_2025-10-21_at_3.13.04_PM.mp4','video','2025-10-21 15:53:36','2025-10-21 15:53:37'),(68,'','WhatsApp_Video_2025-10-21_at_3.18.33_PM.mp4','video','2025-10-21 15:54:13','2025-10-21 15:54:13'),(69,'','WhatsApp_Video_2025-10-21_at_3.18.32_PM_1.mp4','video','2025-10-21 15:54:38','2025-10-21 15:54:39'),(70,'dekh ke dil mai ding ding hone lgta h  “🌕✨💗᪲᪲᪲”','WhatsApp_Image_2025-10-21_at_3.12.48_PM_1.jpeg','image','2025-10-21 15:56:09','2025-10-21 15:56:09'),(71,'','WhatsApp_Image_2025-10-21_at_3.13.07_PM_1.jpeg','image','2025-10-21 15:57:01','2025-10-21 15:57:02'),(72,'uffff','WhatsApp_Image_2025-10-21_at_3.12.47_PM_1.jpeg','image','2025-10-21 15:57:42','2025-10-21 15:57:42'),(73,'🫰❤️✨','WhatsApp_Image_2025-10-21_at_3.12.47_PM.jpeg','image','2025-10-21 15:58:41','2025-10-21 15:58:42'),(75,'SUKOON💕🤞🏻','IMG-20241204-WA0010.jpg','image','2025-10-21 16:01:16','2025-10-21 16:01:17');
/*!40000 ALTER TABLE `gallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'iffu','138');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-21 16:29:08
