def search(pattern, text):

    M = len(pattern)                                                #1
    N = len(text)                                                   #2

    for i_txt in range(0, N - M + 1):                                #3
        j_pat=0

        for j_pat in range (0, M):                                   #4
            if text[i_txt + j_pat] != pattern[j_pat]:
               
                break
    
        if j_pat == M-1 :                                           #5
            
            print ('Pattern gefunden an Index %d\n' % i_txt)

text = '''ottos mops trotzt\n 
          ottotto: fort mops fort\n 
          ... Ernst Jandl'''

pattern = 'otto'

search(pattern, text)  #1 


# ============================================================================

def search_with_ret_list(pattern, text, bitmap):

    M = len(pattern)
    N = len(text)

    ret_list = []                                               

    for i_txt in range(0, N - M + 1):                                
        j_pat = 0

        for j_pat in range (0, M):                                   
            if text[i_txt + j_pat] != pattern[j_pat]:
                break
    
        if j_pat == M-1 :                                          
            bitmap[i_txt] = 1

