import lec_sort.merge

def mergeSort(arr, left , right):

    if left > right-1:
        return
    
    m= int (left + right-1 / 2)

    mergeSort(arr, left , m)
    mergeSort(arr, m + 1 , right)

    lec_sort.merge.merge(arr, left, m, right)
