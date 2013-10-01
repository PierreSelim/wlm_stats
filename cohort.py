#!/usr/bin/python
import csv, sys, getopt, inspect, datetime, re
from datetime import date
from datetime import tzinfo
from datetime import timedelta
from wlm_emijrp_api import *

def print_cohort(user_count):
	for k in sorted(user_count.keys()):
		print k + ",commons"

def main():
	filedb 	= open(FILE_DB, "rb")
	count 	= 0
	tz 		= WlmTZ()
	user_count	= dict() # upload count by user
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
					count = count +1
			if(count==0):
				count=1

	filedb.close()
	print_cohort(user_count)


if __name__ == "__main__":
	main()