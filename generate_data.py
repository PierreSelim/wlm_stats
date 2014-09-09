#!/usr/bin/python

FILE_11="wlmfr11.csv"
FILE_12="wlmfr12.csv"
FILE_13="wlmfr13.csv"

FILES = [ "wlmfr11.csv", "wlmfr12.csv", "wlmfr13.csv", "wlmfr14.csv"]

def save_cumul(name, cumul):
	file	= name + ".js"
	f		= open(file, "w")
	f.write("var " + name + " = google.visualization.arrayToDataTable([\n['Jour', '2011', '2012', '2013', '2014'],\n")
	print name
	print cumul
	for k in sorted(cumul.keys()):
		data = cumul[k].split(";")
		output = ""
		print data
		if len(data) == 4:
			output = "[" + k + "," + data[0] + "," + data[1] + "," + data[2] + "," + data[3] + "]"
		else:
			output = "[" + k + "," + data[0] + "," + data[1] + "," + data[2] + ",null]"
		if k != "'30'":
			output = output + ","
		f.write(output+"\n")
	f.write("]);")
	f.close()

def parse_key(words):
	return "'" + words[0][8:] + "'"

def main():
	cumul = dict() # total upload
	user = dict() # total user
	upload = dict() # upload by day
	for file_i in FILES:
		f = open(file_i, "rb")
		lc = 1
		previous=0
		for line in f:
			if lc>=4:
				words = line.split(";")
				key =  parse_key(words)
				if key in cumul:
					cumul[key] += ";" + str(int(words[2]))
				else:
					cumul[key] = str(int(words[2]))
				if key in upload:
					upload[key] += ";" + str(int(words[1]))
				else:
					upload[key] = str(int(words[1]))
				previous = previous + int(words[3])
				if key in user:
					user[key] += ";" + str(previous)
				else:
					user[key] = str(previous)
			lc = lc + 1
		f.close()
	# Q&D hack (if magic files is here we will read more than 4 lines.)
	if lc>4:
		save_cumul("data1", cumul)
		save_cumul("data2", user)
		save_cumul("data3", upload)
	else:
		print "Not saving anything magic files is not available"

if __name__ == "__main__":
	main()