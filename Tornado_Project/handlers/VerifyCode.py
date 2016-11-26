# coding:utf-8
import logging
import constants
import random
import re

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp


class ImageCodeHandler(BaseHandler):
	def get(self):
		code_id = self.get_argument("codeid")
		pre_code_id = self.get_argument("pcodeid")
		if pre_code_id:
			try:
				self.redis.delete("image_code %s" % pre_code_id)

			except Exception as e:
				logging.error(e)
		# 名字，文本，图片
		name, text, image = captcha.generate_captcha()
		try:
			self.redis.setex("image_code %s" % code_id, constants.IMAGE_CODE_EXPIRES_SECONDS, text,)
		except Exception as e:
			logging.error(e)
			self.write("")
		self.set_header("Content-Type", "image/jpg")
		self.write(image)
class SMSCodeHandler(BaseHandler):

	def post(self):
		mobile = self.json_args.get("mobile")
		image_code_id = self.json_args.get("image_code_id")
		image_code_text = self.json_args.get("image_code_text")

		if not all((mobile, image_code_id, image_code_text)):
			return self.write(dict(error = RET.PARAMERR, errmsg = "参数不完整"))
		if not re.match(r"1\d{10}", mobile):
			return self.write(dict(error = RET.PARAMERR, errmsg = "手机号不完整"))
		try:
			real_image_code_text = self.redis.get("image_code %s" % image_code_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(error=RET.DBERR, errmsg = "查询出错"))
		if not real_image_code_text:
			return self.write(dict(error=RET.NODATA, errmsg = "验证已过期"))

		# 作对比
		if real_image_code_text.lower() != image_code_text.lower():
			return self.write(dict(error=RET.DATAERR, errmsg = "验证码错误！"))

		# 生成随机数
		sms_code = "%04d"% random.randint(0, 9999)
		# 把验证码存起来
		try:
			self.redis.setex("sms_code %s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
		except Exception as e:
			logging.error(e)
			return self.write(dict(error=RET.DBERR, errmsg = "生成短信验证码错误！"))
		# 发送短信
		try:
			ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)

		except Exception as e:
			logging.error(e)
			return self.write(dict(error=RET.THIRDERR, errmsg = "发送失败！"))
		self.write(dict(error=RET.OK, errmsg="OK"))

	




		


