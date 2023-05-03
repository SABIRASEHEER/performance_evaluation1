positive = open("vader_lexicon.txt", "r+", encoding="UTF-8")
file = positive.read()

positive_list = file.split("\n")
ps=[]
nl=[]
for i in positive_list:
    print(i)
    ii=i.split("\t")
    if float(ii[1])>=0:
        ps.append(ii[0])
    else:
        nl.append(ii[0])
    print(ii)

print(len(ps))
print(len(nl))



# Program to show various ways to read and
# write data in a file.
file1 = open("positive.txt","w")
L = '\n'.join(ps)

# \n is placed to indicate EOL (End of Line)

file1.writelines(L)
file1.close() #to change file access modes


# Program to show various ways to read and
# write data in a file.
file1 = open("negative.txt","w")
L = '\n'.join(nl)

# \n is placed to indicate EOL (End of Line)

file1.writelines(L)
file1.close() #to change file access modes