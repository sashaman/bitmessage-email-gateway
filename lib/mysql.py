#!/usr/bin/python2.7

from lib.config import BMConfig
import lib.singleton
import os
import sys
import MySQLdb
import MySQLdb.converters
from MySQLdb.constants import FIELD_TYPE
from warnings import filterwarnings

class BaseBMMySQL(object):
	db = None

	def __init__(self):
		self.db = self.connect()

	def connect(self):
		orig_conv = MySQLdb.converters.conversions
		#Adding support for bit data type
		orig_conv[FIELD_TYPE.BIT] = bool

		for mysql in BMConfig().get("mysql"):
			if BMConfig().get("mysql", mysql, "unix_socket"):
				try:
					self.db =  MySQLdb.connect(unix_socket = BMConfig().get("mysql", mysql, "unix_socket"),
						user = BMConfig().get("mysql", mysql, "user"),
						passwd = BMConfig().get("mysql", mysql, "passwd"),
						db = BMConfig().get("mysql", mysql, "db"), conv = orig_conv)
					return self.db
				except MySQLdb.Error, e:
					print "MySQLdb.Error is %d: %s" % (e.args[0], e.args[1])
					continue
				except:
					print "Error connecting to " + mysql
					continue
			elif BMConfig().get("mysql", mysql, "host"):
				try:
					self.db =  MySQLdb.connect(host = BMConfig().get("mysql", mysql, "host"),
						user = BMConfig().get("mysql", mysql, "user"),
						passwd = BMConfig().get("mysql", mysql, "passwd"),
						db = BMConfig().get("mysql", mysql, "db"))
					return self.db
				except MySQLdb.Error, e:
					print "MySQLdb.Error is %d: %s" % (e.args[0], e.args[1])
					continue
				except:
					print "Error connecting to " + mysql
					continue
			else:
				self.db = None
				print "No host or unix socket in mysql definition for " + mysql
		return False

class BMMySQL(BaseBMMySQL):
	__metaclass__ = lib.singleton.Singleton