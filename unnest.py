# function used for removing nested  
# lists in python.  
def reemovNestings(l, output): 
    for i in l: 
        if type(i) == list: 
            reemovNestings(i, output) 
        else: 
            output.append(i) 
            
def unnest( l ):
    # output list 
    output = [] 
    reemovNestings(l, output)
    return output 
            
# l = [[[1], 2], [3, 4, [5, 6]], 7, 8, [9, [10]]] 

# print ('The original list: ', l) 
# l = unnest(l) 
# print ('The list after removing nesting: ', l) 
