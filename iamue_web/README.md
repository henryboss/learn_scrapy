# iamue爬取文章内容
配置可看settings.py。设置0.5秒爬取一篇文章，跳过错误页面，总共爬取10000个页面，有效页面为777个。  
保存的格式有：json，mysql，image。  
图片保存在当前目录的iamue目录，json保存在当前目录的data.json文件。
数据库表如下：
```mysql
CREATE DATABASE `iamue`;
use `iamue`;
CREATE TABLE `iamue_article` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
	`content` TEXT NOT NULL COLLATE 'utf8_unicode_ci',
	`spider_url` VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
	PRIMARY KEY (`id`)
)
COLLATE='utf8_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=778;
CREATE TABLE `iamue_images` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`article_id` INT(11) NOT NULL,
	`images` VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
	`image_urls` VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
	PRIMARY KEY (`id`),
	INDEX `article_id` (`article_id`)
)
COLLATE='utf8_unicode_ci'
ENGINE=InnoDB;
```