#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib2
import lxml.html
from lxml import etree
from urllib import urlencode
class SubwayClubCardAPI:

	CHARGE_PAGE_AUTH_URL = "https://rapico.jp/R03F764SUBWAY/PcCard/login"

	def __init__(self):
		pass

	# 残高を返します
	def get_balance(self, card_id, pin_id):
		raw_html = self.get_raw_html_after_login(
				self.CHARGE_PAGE_AUTH_URL,
				card_id,
				pin_id
				)
		html_root = etree.fromstring(raw_html, etree.HTMLParser())
		data_table = html_root.xpath('//tr[@class="odd"]')
		if not len(data_table) > 1:
			raise Exception("invalid response")
		if not len(data_table[1]) > 1:
			raise Exception("invalid response")
		balance_str = data_table[1][1]
		if not type(balance_str) == lxml.etree._Element:
			raise Exception("invalid response")

		return balance_str.text.replace(u"￥", "").replace(u",","")


	# 残高照会ページにログイン後のページ内容を返します
	def get_raw_html_after_login(self, login_url, card_id, pin_id):
		params = {
				"card_id" : card_id,
				"pin_id" : pin_id,
				"flg_post" : "1",
				"sabe_card_id" : "1"
				}
		cj = cookielib.MozillaCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = opener.open(login_url, urlencode(params))
		return response.read()



if __name__=="__main__":
	card_id = "123" # your id
	pin_id = "456"  # your id
	api = SubwayClubCardAPI()
	print api.get_balance(card_id, pin_id).encode("cp932")
