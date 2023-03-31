/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - performance_evaluation
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`performance_evaluation` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `performance_evaluation`;

/*Table structure for table `assign_tl` */

DROP TABLE IF EXISTS `assign_tl`;

CREATE TABLE `assign_tl` (
  `a_tl_id` int(50) NOT NULL AUTO_INCREMENT,
  `wid` int(50) DEFAULT NULL,
  `tl_id` int(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`a_tl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `assign_tl` */

insert  into `assign_tl`(`a_tl_id`,`wid`,`tl_id`,`date`,`status`) values 
(1,1,4,'2023-03-26','pending'),
(2,1,4,'2023-03-26','pending'),
(3,2,1,'2023-03-26','pending');

/*Table structure for table `assign_tm` */

DROP TABLE IF EXISTS `assign_tm`;

CREATE TABLE `assign_tm` (
  `a_tm_id` int(50) NOT NULL AUTO_INCREMENT,
  `wid` int(50) DEFAULT NULL,
  `tm_id` int(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`a_tm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `assign_tm` */

insert  into `assign_tm`(`a_tm_id`,`wid`,`tm_id`,`date`,`status`) values 
(1,2,3,'2023-03-27','partially');

/*Table structure for table `attendance` */

DROP TABLE IF EXISTS `attendance`;

CREATE TABLE `attendance` (
  `aid` int(50) NOT NULL AUTO_INCREMENT,
  `attendance` varchar(100) DEFAULT NULL,
  `lid` int(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `intime` time DEFAULT NULL,
  `outtime` time DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `attendance` */

insert  into `attendance`(`aid`,`attendance`,`lid`,`date`,`intime`,`outtime`) values 
(1,'present',4,'2023-03-24','09:30:00','04:30:00');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `cid` int(50) NOT NULL AUTO_INCREMENT,
  `lid` int(50) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`cid`,`lid`,`complaint`,`date`,`reply`) values 
(1,3,'dgfgfg','2023-03-24','fdghfjh'),
(2,3,'dfsgfdc','2023-03-27','pending'),
(3,3,'dfsgfdc','2023-03-27','pending');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `fid` int(50) NOT NULL AUTO_INCREMENT,
  `rid` int(50) DEFAULT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  `score` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`fid`,`rid`,`feedback`,`score`,`date`) values 
(1,4,'nice','0','2023-03-27');

/*Table structure for table `hr` */

DROP TABLE IF EXISTS `hr`;

CREATE TABLE `hr` (
  `hid` int(50) NOT NULL AUTO_INCREMENT,
  `lid` int(50) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` int(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` bigint(50) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `hr` */

insert  into `hr`(`hid`,`lid`,`first_name`,`last_name`,`place`,`post`,`pin`,`email`,`phone`,`gender`) values 
(1,2,'sabira','seheer','ponnani','ponnani',14234,'dfsdaf@gmail.com',134567888,'female');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `l_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`l_id`)
) ENGINE=InnoDB AUTO_INCREMENT=452 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`l_id`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'sabi','sabi','hr'),
(3,'tm','tm','team_member'),
(4,'tl','tl','team_leader'),
(445,'ssss','ssss','hr'),
(448,'ssss','ssss','team_leader'),
(449,'tftgh','hgfjh','team_member'),
(451,'as','as','team_leader');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `nid` int(50) NOT NULL AUTO_INCREMENT,
  `notification` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`nid`,`notification`,`date`) values 
(1,'dfssgf','2023-03-24');

/*Table structure for table `report` */

DROP TABLE IF EXISTS `report`;

CREATE TABLE `report` (
  `rid` int(50) NOT NULL AUTO_INCREMENT,
  `wid` int(50) DEFAULT NULL,
  `report` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `report` */

insert  into `report`(`rid`,`wid`,`report`,`date`,`status`) values 
(1,1,'ggf','2023-03-28','partially completed'),
(2,2,'fgdgh','2023-03-26','not completed'),
(3,2,'<FileStorage: \'Diagram4.PNG\' (\'image/png\')>','2023-03-27','ok'),
(4,1,'<FileStorage: \'Diagram4.PNG\' (\'image/png\')>','2023-03-27','fgd');

/*Table structure for table `tl` */

DROP TABLE IF EXISTS `tl`;

CREATE TABLE `tl` (
  `tl_id` int(50) NOT NULL AUTO_INCREMENT,
  `lid` int(50) DEFAULT NULL,
  `hid` int(50) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` int(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `tl` */

insert  into `tl`(`tl_id`,`lid`,`hid`,`first_name`,`last_name`,`place`,`post`,`pin`,`email`,`phone`,`gender`) values 
(1,4,2,'santhosh','sai','fhghg','fhf',4656,'fgfggh',4656565,'female'),
(5,448,2,'fdgfd','fdgf','gnfg','ghg',0,'hgjhgj',5646576,'male'),
(6,449,4,'gffhjhf','fdsgfd','htfj','gfg',0,'hfgfh',0,'radiobutton'),
(7,451,2,'tfgh','jghg','jhjkjk','yjjku',0,'ghjgjgjk',0,'male');

/*Table structure for table `tm` */

DROP TABLE IF EXISTS `tm`;

CREATE TABLE `tm` (
  `tm_id` int(50) NOT NULL AUTO_INCREMENT,
  `lid` int(50) DEFAULT NULL,
  `tl_id` int(50) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` int(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `tm` */

insert  into `tm`(`tm_id`,`lid`,`tl_id`,`first_name`,`last_name`,`place`,`post`,`pin`,`email`,`phone`,`gender`) values 
(1,3,4,'Rahul','ravi','malappuram','panakkad',34455667,'ghghgh@gmail.com',344,'male');

/*Table structure for table `work` */

DROP TABLE IF EXISTS `work`;

CREATE TABLE `work` (
  `wid` int(50) NOT NULL AUTO_INCREMENT,
  `work` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hid` int(50) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `submission_date` date DEFAULT NULL,
  PRIMARY KEY (`wid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `work` */

insert  into `work`(`wid`,`work`,`date`,`hid`,`status`,`submission_date`) values 
(1,'evaluation','2023-03-24',1,'pending','2023-03-31'),
(2,'software ','2023-03-26',2,'pending','2023-03-26'),
(3,'software ','2023-03-26',2,'pending','2023-03-26');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
