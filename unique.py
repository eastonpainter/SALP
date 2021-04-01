# List all unique elements in an array print amount
import re

arr = ['a', 'b', 'b', 'c', 'c', 'c', 'd', 'd', 'd', 'd']
elems = {}
arr.append('e')
arr.append('a')
arr.append('b')

# elems['a'] = 1

print(elems)

for i in range(len(arr)):
    if (arr[i] in elems) != True:
        elems[arr[i]] = 1

    else: 
        elems[arr[i]] += 1

print(elems)
