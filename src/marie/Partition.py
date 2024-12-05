def partition (arr, low, high):

    pivot= arr[low]                                                     #1
    i=low
    j=high


    while i < j:
        
        while (arr[i] <= pivot  ) and (i <= high - 1) :                 #2
            i=i+1

        while (arr[j] > pivot ) and ( j >= low + 1) :                   #3
            j=j-1

        if i < j:
            arr[i],arr[j] = arr[j],arr[i]

    arr[low],arr[j] = arr[j],arr[low]                                   #4

    return j
