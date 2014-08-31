import csv, sys, getopt, inspect, datetime, re
from datetime import date
from datetime import tzinfo
from datetime import timedelta

THIS_WLM	= "france"
DELIMITER	= ";;;"
FILE_DB		= "files.txt"
YEAR		= 2014

START		= datetime.date(YEAR, 9, 1)
END			= datetime.date(YEAR, 10, 1)

# Dictionnary
FILENAME	= 0
COUNTRY		= 1
DATE 		= 2
USERNAME	= 3
RESOLUTION	= 4
SIZE		= 5

class WlmTZ(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=2)
    def dst(self, dt):
         return timedelta(0)
    def tzname(self,dt):
        return "Europe/Paris"

def parse_date(date, tz):
	d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
	d = d.replace(tzinfo=tz)
	return tz.fromutc(d)
