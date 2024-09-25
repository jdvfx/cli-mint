import glob
import re
from webbrowser import get
from operator import itemgetter

d={

r"*instacart*":"grocery",
r"paypal*uber*":"grocery",
r"h-mart*":"grocery",
r"save on foods":"grocery",
r"brandon*":"grocery",
r"*kin*farm*":"grocery",
r"safeway*":"grocery",
r"iga *":"grocery",
r"aria markey":"grocery",
r"*celtic*":"grocery",
r"davie*yig":"grocery",

r"old navy*":"clothes",
r"*sketchers*":"clothes",

r"payment *you":"cc",

r"*sonnet*":"house",
r"davie flowers":"house",

r"*stepho*":"takeout",
r"anh and chi":"takeout",
r"rollzzy":"takeout",
r"happy lemon":"takeout",
r"kitanoya guu*":"takeout",
r"romilano pizza":"takeout",
r"babylon cafe":"takeout",
r"tom*sushi":"takeout",

r"ferryhopper*":"holidays",
r"aegeanair*":"holidays",
r"*airbnb*":"holidays",
r"ragoussi*":"holidays",
r"glafkos":"holidays",
r"anemos":"holidays",
r"trip.com":"holidays",
r"sncf*":"holidays",

r"playstation*":"entertain",
r"*nintendo*":"entertain",
r"steam*":"entertain",
r"*pools*":"entertain",
r"catfe":"entertain",

r"compass*":"travel",
r"paypal*uber":"travel",

r"london drugs":"health",
r"dr. caroline*":"health",

r"balance*":"bills",

r"bc liquor*":"booze",
r"sutton place wine*":"booze",

r"*google*":"subscription",
r"*spotify*":"subscription",
r"*chatr*":"subscription",
r"*apple*":"subscription",
r"*ymca*":"subscription",
r"alivecor*":"subscription",


r"b.c hydro*":"bills",
r"shaw cable*":"bills",
r"questrade*":"savings",
r"mortgage*":"mort",
r"tribe*":"house",
r"vancou tax*":"house",
r"*tfr-to*":"cc",

}


k ={}
for key,value in d.items():

    escaped_pattern = re.escape(key).replace(r'\*', '.*')
    escaped_pattern = escaped_pattern.upper()
    regex_pattern = re.compile(escaped_pattern)
    k[regex_pattern]=value

def find_category(item:str) -> str:

    for key,val in k.items():
        m = key.match(item)
        if m:
            return val
    return ">other"


matches=[]

for file in glob.glob("*.csv"):
    print(file)

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

            # if "MORTGAGE" in item:
            #     print(item , e[2])

            # ignore credit card payments
            ignore_list = ["TFR-TO"]
            for i in ignore_list:
                if i in item:
                    debit=""

            if len(debit)>0:
                d["debit"]=f"{e[2]}"
                matches.append(d)


# sort list by dict key "month"
matches = sorted(matches, key=itemgetter("month"))

months = []
for m in matches:
    months.append(m.get("month"))
months = list(set(months))
months.sort()

for month in months:
    print(f">>> month:{month}")
    # create a list for the items of this month
    month_list = []
    for match in matches:
        m = match.get("month")
        if m==month:
            month_list.append(match)

    cat_found={}
    for key,val in k.items():
        cat_found[val]=0
    cat_found[">other"]=0

    for transaction in month_list:
        cat = transaction["cat"]
        cat_occurences =  cat_found.get(cat)
        if cat_occurences is not None:
            cat_found[cat]=cat_occurences+1

    total=0
    # -- display percentages 
    for key,val in cat_found.items():
        total+=val

    for key,val in cat_found.items():
        percentage = (val*100.0)/total

        print(f"{key} {percentage:.2f}%")
        for transaction in month_list:
            cat = transaction["cat"]
            if cat==key:
                print(f"    - {transaction}")

    print("----------------")



