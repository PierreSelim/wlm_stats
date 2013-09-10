#!/usr/bin/python
import csv, sys, getopt, inspect, datetime, re
from datetime import date
from datetime import tzinfo
from datetime import timedelta

THIS_WLM	= "france"
DELIMITER	= ";;;"
FILE_DB		= "files.txt"
YEAR		= 2013

START		= datetime.date(YEAR, 9, 1)
END			= datetime.date(YEAR, 10, 1)

# Dictionnary
FILENAME	= 0
COUNTRY		= 1
DATE 		= 2
USERNAME	= 3
RESOLUTION	= 4
SIZE		= 5

class Aggregate:
	def __init__(self, date):
		self.date 		= date
		self.day_count 	= 0;

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

def print_agg(daily,total, uploaders, new_uploaders):
	print "date;daily up;total up;new uploaders"
	for k in sorted(daily.keys()):
		print k + ";" + str(daily[k]) + ";" + str(total[k]) + ";"  + str(len(new_uploaders[k]))

def print_cohort(user_count):
	for k in sorted(user_count.keys()):
		print k + ",commons"
		
def main():
	filedb 	= open(FILE_DB, "rb")
	count 	= 0
	previous_count = 0
	tz 		= WlmTZ()
	daily_count = dict() # upload count by day
	total_count	= dict() # cumulative upload count by day
	user_count	= dict() # upload count by user
	userd_count = dict() # user count by day
	usernd_count= dict() # new user count by day
	for line in filedb:
		words = line.split(DELIMITER)
		if(words[COUNTRY].strip() == THIS_WLM):
			user = words[USERNAME].strip()
			if count > 0:
				datetime_image = parse_date(words[DATE].strip(), tz)
				date_image = datetime.datetime.strftime(datetime_image, "%Y-%m-%d")
				if(datetime_image.date()>=START and datetime_image.date()<END):
					#user
					if user in user_count:
						user_count[user] = user_count[user]+1
					else:
						user_count[user] = 1
					if date_image in daily_count:
						daily_count[date_image] = daily_count[date_image] +1
						total_count[date_image] = total_count[date_image] + 1
						if(not (user in userd_count[date_image])):
							userd_count[date_image].append(user)
					else:
						previous_count = count -1
						daily_count[date_image] = 1
						total_count[date_image] = previous_count +1
						userd_count[date_image]	= []
						usernd_count[date_image] = []
						userd_count[date_image].append(user)
					if(user_count[user] <= 1):
						usernd_count[date_image].append(user)
					count = count +1
			if(count==0):
				count=1

	filedb.close()
	print "total: " + str(count)
	print "total up: " + str(len(user_count.keys()))
	print_agg(daily_count, total_count, userd_count, usernd_count)
	#print_cohort(user_count)


if __name__ == "__main__":
	main()