import lec_sort.partition 


def quickSort(arr, low, high):
    
   if low < high:                                                          #1

        partitionIndex= lec_sort.partition.partition(arr, low , high)       #2 

        quickSort(arr, low , partitionIndex - 1)                             #3

        quickSort(arr, partitionIndex + 1, high)                               #4
