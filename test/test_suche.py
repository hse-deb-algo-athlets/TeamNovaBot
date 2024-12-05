#from src.Marie import Text_suche

import marie.Text_suche as mt

def test_search_with_ret_list():

    text = 'Das ist kein pattern mit einer Ente'

    pattern = 'ein'

    bitmap = [0] * len(text)

    expBitmap = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    mt.search_with_ret_list(pattern, text, bitmap)

    assert bitmap == expBitmap , 'Result is not equal to expected Bitmap'

    for i in range(len(bitmap)):
        if bitmap[i] == 1:
            print ("Pattern found at index: %i\n" %i)               #3
