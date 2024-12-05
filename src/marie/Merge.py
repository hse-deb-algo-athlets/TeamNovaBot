def merge(arr, left, m ,right):

    i = 0                                                         #1
    j = 0
    k = 0                                                         #2                                                  
    n1= int (m - left + 1  )                                         #3
    n2= int (right - m )                                              #4

    L=[0] * n1
    R=[0] * n2

    for i in range(0,n1):                                         #5
        L[i]=arr[left + i]
       

    for j in range(0,n2):

        R[j]=arr[ int (m + 1 + j) ]
       

    i=0
    j=0
    k = left

    while i < n1 and j < n2:    
                                                                     #6
        if L[i] <= R[j]:
            arr[k]=L[i]
            i=i+1

        else :
           arr[k]=R[j]
           j=j+1

        k= k + 1

    while i < n1:                                                   #7
        arr[k] = L[i]
        k= k + 1
        i=i+1

    while j < n2:
        arr[k] = R[j]
        k= k + 1
        j=j+1

