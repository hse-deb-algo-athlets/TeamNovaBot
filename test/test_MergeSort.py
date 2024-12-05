import marie.MergeSort

def test_mergeSort():

    arr=[1, 6, 4, 8 ,7 ,9 ,5 , 2, 10 ,3]
    left=0
    right= len(arr)-1

    expectedarr=[1, 2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10]
    
    marie.MergeSort.mergeSort(arr, left , right)

    assert arr==expectedarr , 'array not sorted as expected'
