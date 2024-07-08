from csv import*

f = open("F:\Python project\Train_details.csv","r")
c = reader(f)
for i in c:
    for j in i:
        print(j,end="\t")
    print()

