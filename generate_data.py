#!/usr/bin/python

FILE_11="wlmfr11.csv"
FILE_12="wlmfr12.csv"
FILE_13="wlmfr13.csv"

def save_cumul(name, cumul):
	file	= name + ".js"
	f		= open(file, "w")
	f.write("var " + name + " = google.visualization.arrayToDataTable([\n['Jour', '2011', '2012', '2013'],\n")
	for k in sorted(cumul.keys()):
		data = cumul[k].split(";")
		output = ""
		if len(data) == 3:
			output = "[" + k + "," + data[0] + "," + data[1] + "," + data[2] + "]"
		else:
			output = "[" + k + "," + data[0] + "," + data[1] + ",null]"
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
	file_11	= open(FILE_11, "rb")
	lc = 1
	previous = 0
	for line in file_11:
		if lc>=4:
			words = line.split(";")
			key =  parse_key(words)
			cumul[key] = str(int(words[2]))
			upload[key] = str(int(words[1]))
			previous = previous + int(words[3])
			user[key] = str(previous)
		lc = lc + 1
	file_11.close()
	file_12	= open(FILE_12, "rb")
	lc = 1
	previous = 0
	for line in file_12:
		if lc>=4:
			words = line.split(";")
			key =  parse_key(words)
			cumul[key] = cumul[key] + ";" + str(int(words[2]))
			upload[key] = upload[key] + ";" + str(int(words[1]))
			previous = previous + int(words[3])
			user[key] = user[key] + ";" + str(previous)
		lc = lc +1
	file_12.close()
	file_13	= open(FILE_13, "rb")
	lc = 1
	previous = 0
	for line in file_13:
		if lc>=4:
			words = line.split(";")
			key =  parse_key(words)
			cumul[key] = cumul[key] + ";" + str(int(words[2]))
			upload[key] = upload[key] + ";" + str(int(words[1]))
			previous = previous + int(words[3])
			user[key] = user[key] + ";" + str(previous)
		lc = lc +1
	file_13.close()
	save_cumul("data1", cumul)
	save_cumul("data2", user)
	save_cumul("data3", upload)

if __name__ == "__main__":
	main()