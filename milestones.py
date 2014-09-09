#!/usr/bin/python
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

def get_milestone_from_arg():
    return int(sys.argv[1])

def main():
	filedb 	= open(FILE_DB, "rb")
	count 	= 0
	previous_count = 0
	tz 		= WlmTZ()
	milestone = get_milestone_from_arg()
	db = dict()
	for line in filedb:
		words = line.split(DELIMITER)
		if(words[COUNTRY].strip() == THIS_WLM):
			user = words[USERNAME].strip()
			if count > 0:
				datetime_image = parse_date(words[DATE].strip(), tz)
				date_image = datetime.datetime.strftime(datetime_image, "%Y-%m-%d")
				if(datetime_image.date()>=START and datetime_image.date()<END):
					#user
					key = words[DATE] + " " + words[FILENAME]
					db[key] = datetime.datetime.strftime(datetime_image, "%Y-%m-%dT%H:%M:%SZ") + " > " + words[FILENAME] + " > " + words[USERNAME]
					count = count +1

			if(count==0):
				count=1
	count = 1
	for k in sorted(db.keys()):
		if(count==milestone):
			print db[k]
		count = count +1
	filedb.close()
	#print "total: " + str(count)


if __name__ == "__main__":
	main()
