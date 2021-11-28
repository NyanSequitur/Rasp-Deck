file=open('key1.csv','r')
keyOneCommand=[]
for line in file:
    keyOneCommand.append(list(filter(None,line.strip('\n').split(','))))
print(keyOneCommand)