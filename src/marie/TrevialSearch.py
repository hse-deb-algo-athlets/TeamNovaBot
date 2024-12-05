def trivialsearch(array,x):

    for i in range(0,len(array)):
      
        if array[i] == x:
            return i
        
    return -1