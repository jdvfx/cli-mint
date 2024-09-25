import glob
import re
from webbrowser import get

d={
r"*instacart*":"food",
r"paypal*uber*":"food",
r"steam*":"entertain",
r"old navy*":"clothes",
r"h-mart*":"food",
r"payment *you":"cc",
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

# -----------------------------
# categories occurences
cat_found={}
for key,val in k.items():
    cat_found[val]=0
cat_found[">other"]=0
# -----------------------------
matches={}
# for key,val in k.items():
#     matches[]=0
# cat_found["other"]=0

tokens = []
for file in glob.glob("*.csv"):

    with open(file,"r") as f:
        lines = f.read().splitlines()
        for line in lines:

            e = line.split(",")
            item = e[1]
            cat = find_category(item)

            matches[item] = cat

            cat_occurences =  cat_found.get(cat)
            if cat_occurences is not None:
                cat_found[cat]=cat_occurences+1

# -- display matches 
for key,val in matches.items():
    print(f"{val} : {key}")

# -- display percentages 
total=0
for key,val in cat_found.items():
    total+=val

for key,val in cat_found.items():
    percentage = (val*100.0)/total
    print(f"{key} {percentage:.2f}%")



