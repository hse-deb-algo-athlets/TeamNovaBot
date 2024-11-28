def binarySearchIter(arr, low, high, x) :

    while low <= high :

        mid= int (low + (high-low) / 2) 

        if arr[mid] == x:
            return mid
        
        if arr[mid] < x:
            low= mid + 1
        
        else : 
            high = mid -1

    return -1