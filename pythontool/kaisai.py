import base64
import string
s = raw_input("input the string:")
base = raw_input("base64_choice:\n0.no\n1.decode\n2.encode\n")
table1 = string.lowercase
table2 = string.uppercase
print table1
for f in range(len(table1)):
    flag = ""
    for i in s:
        if i in table1:
            it = table1.find(i)
            lens = it + f            
            if lens >= len(table1):
                flag = flag + table1[it+f-len(table1)]
            else:
                flag = flag + table1[it+f]
        elif i in table2:
            it = table2.find(i)
            lens = it + f            
            if lens >= len(table1):
                flag = flag + table2[it+f-len(table2)]
            else:
                flag = flag + table2[it+f] 
        else:
            flag = flag + i
    if base == '1':
        print str(f)+" : "+str(base64.b64decode(flag))
    elif base== '2':
        print str(f)+" : "+str(base64.b64encode(flag))
    else:
        print str(f)+" : "+flag
    
    
    