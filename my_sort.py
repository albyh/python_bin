def mySort(coll):
    s = []
    while len(coll) > 0:
        s.append(min(coll))
        coll.remove(min(coll))
    return s   

#********TESTS***********
 
test1 = [67, 45, 2, 13, 1, 998]
expected1 = [1, 2, 13, 45, 67, 998]

print( 'test1 = [67, 45, 2, 13, 1, 998]' )
print( 'expected1 = [1, 2, 13, 45, 67, 998]' )
print( 'mySort(test1) == expected1'+str(mySort(test1) == expected1) )

test2 = [89, 23, 33, 45, 10, 12, 45, 45, 45]
expected2 = [10, 12, 23, 33, 45, 45, 45, 45, 89]

print( 'test2 = [89, 23, 33, 45, 10, 12, 45, 45, 45]' )
print( 'expected2 = [10, 12, 23, 33, 45, 45, 45, 45, 89]' )
print( 'mySort(test2) == expected2'+str(mySort(test2) == expected2) )

