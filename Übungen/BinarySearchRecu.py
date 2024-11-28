def binarySearchRecu(arr, low, high, x):

    if high >= low:
        
        mid=int (low +(high-low)/2)
      
        if arr[mid] == x:
            return mid
        
        if arr[mid] > x:
            return  binarySearchRecu(arr, low, mid-1, x)
        
        return  binarySearchRecu(arr, mid+1, high, x)
    
    return -1