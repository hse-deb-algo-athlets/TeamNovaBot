import time

def myFunction():
    print("some usefull actions ... taking 10 sec")
    time.sleep(10) #sec
    

start= time.time()

myFunction() 

stop = time.time()

print ('Laufzeit = ' +'{:5.3f} s'.format (stop-start))
