
import matplotlib.pyplot as plt
import json
import glob
import re
from webbrowser import get
from operator import itemgetter

# load categories filters
categories = "categories.json"
with open(categories,'r') as file:
    cat_dict = json.load(file)


k ={}
for key,value in cat_dict.items():

    escaped_pattern = re.escape(key).replace(r'\*', '.*')
    escaped_pattern = escaped_pattern.upper()
    regex_pattern = re.compile(escaped_pattern)
    k[regex_pattern]=value

def find_category(item:str) -> str:

    for key,val in k.items():
        item = item.upper()
        m = key.match(item)
        if m:
            return val
    return "other"


matches=[]

for file in glob.glob("*.csv"):

    with open(file,"r") as f:
        lines = f.read().splitlines()
        for line in lines:

            e = line.split(",")
            item = e[1]

            m=e[0].split("/")

            d = {}
            month= f"{m[2]}_{m[0]}"
            cat = find_category(item)
            d["month"]=month
            d["item"]=item
            d["cat"]=cat

            debit = e[2]

            # ignore credit card payments
            ignore_list = ["TFR-TO","MONTHLY ACCOUNT FEE"]
            for i in ignore_list:
                if i in item:
                    debit=""

            if len(debit)>0:
                d["debit"]=f"{e[2]}"
                if d not in matches: #???
                	matches.append(d)
                	
                	
  	



months = []
for m in matches:
    months.append(m.get("month"))
months = list(set(months))
months.sort()


log = []

for month in months:

    l = f"-- {month} --------------------------"
    log.append(l)
    
    # create a list for the items of this month
    month_list = []
    for match in matches:
        m = match.get("month")
        if m==month:
            month_list.append(match)

    # sort by item name
    month_list = sorted(month_list,key=itemgetter("item"))
            
    cat_val={}
    for key,val in k.items():
        cat_val[val]=0.0
    cat_val["other"]=0.0

    for transaction in month_list:
        cat = transaction["cat"]
        debit = transaction["debit"]
        cat_val[cat]=cat_val[cat] + float(debit)



    # -- display percentages
    total=0
    
    for key,val in cat_val.items():
        total+=val
        
    for key,val in cat_val.items():
        percentage = (val*100.0)/total

        if val>0:
            l = f"[{key.upper()}] {percentage:.2f}% ${val:.2f}"
            log.append(l)
            for transaction in month_list:
                cat = transaction["cat"]
                d = transaction
                if cat==key:
                    l=f"    {d['debit']:>8} {d['item']}"
                    log.append(l)
                    
            l=""
            log.append(l)

# for line in log:
#     print(line)

with open("log.txt","w") as file:    
    for line in log:
        file.write(line+"\n")
        print(line)

# ////////////////////////////////////////

month = months[-2]

# create a list for the items of this month
month_list = []
pie={}
for match in matches:
    m = match.get("month")
    if m==month:
        month_list.append(match)

cat_val={}
for key,val in k.items():
    cat_val[val]=0.0
cat_val["other"]=0.0

for transaction in month_list:
    cat = transaction["cat"]
    debit = transaction["debit"]
    cat_val[cat]=cat_val[cat] + float(debit)

# -- display percentages
total=0
for key,val in cat_val.items():
    total+=val

for key,val in cat_val.items():
    percentage = (val*100.0)/total
    if percentage>0:
        pie[key] = percentage
#

pie = dict(sorted(pie.items(),key=itemgetter(1)))

labels = list(pie.keys())
sizes = list(pie.values())

colors_ = [\
 "#ffaa00",\
 "#2279ff",\
 "#2bc395",\
 "#2c9440",\
 "#c866ff",\
 "#d3302e",\
 "#e6ecec",\
 "#fc552e",\
 "#ff77bb",\
 "#212c3e",\
 "#4088cc",\
 "#2bc395",\
 "#32a448",\
 "#c866ff",\
 "#aa2255",\
 "#afb6b9",\
 "#bb33bb"\
]


dict_colors={}
d = list(set(cat_dict.values()))
d.sort()
for idx,i in enumerate(d):
    dict_colors[i] = colors_[idx]

dict_colors["other"] = "#888888"

colors = []
for idx,i in enumerate(labels):
    col = dict_colors.get(i)
    colors.append(col)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
                    


