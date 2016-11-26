#coding:utf-8

import os

#Application配置参数

settings = {
	"static_path":os.path.join(os.path.dirname(__file__), "static",),
	"cookie_secret":"+Xq/sB8hQvqjyyVWKTf0S2j/0YuQ/0z8j3wiSL/u2jM=",
	"xsrf_cookies":True,
	"debug":True,
}


# mysql
mysql_options = dict(
	host = "127.0.0.1",
	database = "ihome",
	user = "root",
	password = "mysql",
)
# redis
redis_options = dict(
	host = "127.0.0.1",
	port = 6379
)
# logging
log_file = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"


session_expires = 86400 #session数据有效期 

passwd_hash_key = "ihome@^*" #密码加密 

image_url_prefix = "http://oh6y237ob.bkt.clouddn.com/" #七牛图片的域名



