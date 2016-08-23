my_list = ['apple','banana','grapes','pear']

for c,value in enumerate(my_list,1):
    print (c,value)

for c,value in enumerate(my_list):
    print (c,value)

counter_list = list(enumerate(my_list,2))
print(counter_list)

