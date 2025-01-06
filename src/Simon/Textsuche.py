
def search_retlist(pattern, text):                                      #1

    M = len(pattern)                                               
    N = len(text)                                                   
    retlist = []
    for i_txt in range(0, N - M + 1):                                
        j_pat=0

        for j_pat in range (0, M):                                   
            if text[i_txt + j_pat] != pattern[j_pat]:
                break
    
        if j_pat == M-1 :                                           #2
            retlist.append(i_txt)
            pass

    
    return  retlist


def search(pattern, text, bitmap):                                      #1

    M = len(pattern)                                               
    N = len(text)                                                   

    for i_txt in range(0, N - M + 1):                                
        j_pat=0

        for j_pat in range (0, M):                                   
            if text[i_txt + j_pat] != pattern[j_pat]:
                break
    
        if j_pat == M-1 :                                           #2
            bitmap[i_txt] = 1
    return bitmap
