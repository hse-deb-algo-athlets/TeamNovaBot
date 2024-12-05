from Simon import Textsuche

def test_search_with_retlist():
    text = "Das ist kein Pattern mit einer Ente"
    pattern ="ein"
    expected =[9,25]
    ret = Textsuche.search_retlist(pattern,text)
    assert expected == ret

def test_search():
    text = "Das ist kein Pattern mit einer Ente"
    pattern ="ein"
    bitmap =[0]*len(text)
    expected = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
    ret = Textsuche.search(pattern,text,bitmap)
    assert expected ==ret