import json
f = open('security_intelligence.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

i=0
for labels in data.values():
    if len(labels)>1:
        i+=1
print(i)

print(len(data))