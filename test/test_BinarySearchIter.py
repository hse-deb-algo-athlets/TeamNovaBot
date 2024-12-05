import marie.BinarySearchIter as lec_sort

def test_binarySearchIter ():

    arr=[3,5,9,23,45,56,77,89,104,156,178,199]
    low=0
    high= len(arr)
    x=104

    expectedindex=8

    detindex= lec_sort.binarySearchIter(arr,low,high,x)

    assert expectedindex==detindex , 'Detected Index not equal to expected one'
