import os
from dateutil.parser import parse
from collections import defaultdict
import csv

PATH = "."

filenames = os.listdir(PATH)
hours = defaultdict(int)
for fname in filenames:
    with open(PATH+"/"+fname) as icsfile:
        if fname[-3:] != "ics":
            continue
        print(fname)
        line = icsfile.readline()
        while line:
            if line[0:8] == "DTSTART:":
                start = parse(line[8:])
                line = icsfile.readline()
                if line[0:6] == "DTEND:":
                    end = parse(line[6:])
                    delta = end-start
                    hours[start.strftime("%Y-%m")] += delta.seconds / 3600
            line = icsfile.readline()

with open('ical_counter.csv', 'w') as outfile:    
    w = csv.DictWriter(outfile, ["month","hours"])
    w.writeheader()
    for month in sorted(list(hours.keys())):
        w.writerow({'month':month,'hours':round(hours[month],2)})
    
