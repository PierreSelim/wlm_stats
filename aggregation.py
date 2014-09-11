#!/usr/bin/python
import csv, sys, getopt, inspect, datetime, re
from datetime import date
from datetime import tzinfo
from datetime import timedelta
from wlm_emijrp_api import *
import json

def print_agg(daily,total, uploaders, new_uploaders):
    print "date;daily up;total up;new uploaders"
    for k in sorted(daily.keys()):
        print k + ";" + str(daily[k]) + ";" + str(total[k]) + ";"  + str(len(new_uploaders[k]))

def read_emijrp_csv(csv_file):
    """ Read the files.txt provided by emijrp. 

        Args:
            csv_file (str): name of the csv file

        Returns:
            a dictionnary containing
                - upload count by day
                - upload count by day
                - upload count by user
                - user count by day
                - new user count by day
    """
    filedb  = open(csv_file, "rb")
    count   = 0
    previous_count = 0
    tz      = WlmTZ()
    daily_count = dict() # upload count by day
    total_count = dict() # cumulative upload count by day
    user_count  = dict() # upload count by user
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
                        userd_count[date_image] = []
                        usernd_count[date_image] = []
                        userd_count[date_image].append(user)
                    if(user_count[user] <= 1):
                        usernd_count[date_image].append(user)
                    count = count +1
            if(count==0):
                count=1
    filedb.close()
    return {
        'count': count,
        'daily count': daily_count,
        'total count': total_count,
        'user count': user_count,
        'user count by day': userd_count,
        'new user count by day': usernd_count
    }

def read_emijrp_json(json_file):
    """ Read the files.json provided by emijrp. 

        Args:
            json_file (str): name of the csv file

        Returns:
            a dictionnary containing
                - upload count by day
                - upload count by day
                - upload count by user
                - user count by day
                - new user count by day
    """
    with open(json_file, "rb") as f:
        data = json.load(f)
        f.close()
        count   = 0
        previous_count = 0
        tz      = WlmTZ()
        daily_count = dict() # upload count by day
        total_count = dict() # cumulative upload count by day
        user_count  = dict() # upload count by user
        userd_count = dict() # user count by day
        usernd_count= dict() # new user count by day
        for k in data:
            image_info = data[k]
            user = image_info[u'username']
            datetime_image = parse_date(image_info[u'date'].strip(), tz)
            date_image = datetime.datetime.strftime(datetime_image, "%Y-%m-%d")

            if(datetime_image.date()>=START and datetime_image.date()<END) and (image_info['country']==THIS_WLM):
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
                    userd_count[date_image] = []
                    usernd_count[date_image] = []
                    userd_count[date_image].append(user)
                if(user_count[user] <= 1):
                    usernd_count[date_image].append(user)
                count = count +1
    return {
        'count': count,
        'daily count': daily_count,
        'total count': total_count,
        'user count': user_count,
        'user count by day': userd_count,
        'new user count by day': usernd_count
    }
 
def main():
    # data = read_emijrp_csv(FILE_DB)

    # Using JSON
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Aggregation of WLM magic files data")
    parser.add_argument("-c", "--csv",
        type=str,
        dest="csv",
        metavar="CSV",
        required=False,
        default=None,
        help="emijrp magic file (CSV format)")
    
    parser.add_argument("-j", "--json",
        type=str,
        dest="json",
        metavar="JSON",
        required=False,
        default=None,
        help="emijrp magic file (JSON format)")
    args = parser.parse_args()

    data = None
    print args
    if (args.json is None) and (args.csv is None):
        raise ValueError("Needs either CSV entry (--csv) or JSON (--json)")

    if args.json is not None:
        data = read_emijrp_json(args.json)

    if args.csv is not None:
        data = read_emijrp_csv(args.csv)

    daily_count = data['daily count'] # upload count by day
    total_count = data['total count'] # cumulative upload count by day
    user_count  = data['user count'] # upload count by user
    userd_count = data['user count by day'] # user count by day
    usernd_count= data['new user count by day'] # new user count by day

    total = 0
    for k in sorted(daily_count.keys()):
        total += daily_count[k]
        total_count[k]=total
    print "total: " + str(data['count'])
    print "total up: " + str(len(user_count.keys()))
    print_agg(daily_count, total_count, userd_count, usernd_count)



    #print_cohort(user_count)


if __name__ == "__main__":
    main()
