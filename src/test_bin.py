import marie.Text_suche as mt

text = 'Das ist kein pattern mit einer Ente'

pattern = 'ein'

bitmap = [0] * len(text)

expBitmap = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

mt.search_with_ret_list(pattern, text, bitmap)

for i in range(len(bitmap)):
    if bitmap[i] == 1:
        print ("Pattern found at index: %i\n" %i)               #3
