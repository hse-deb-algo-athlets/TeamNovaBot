import lec_sort.binarySearchRecu

def test_binarySearchRecu():

    arr= [1, 3, 5, 7, 9, 12, 15, 21, 23, 29 ]
    low= 0
    high= len(arr)
    x= 21

    expextedindex= 7

    detindex= lec_sort.binarySearchRecu.binarySearchRecu(arr, low, high, x)

    assert expextedindex==detindex , 'Detected Index not equal to expected one'
