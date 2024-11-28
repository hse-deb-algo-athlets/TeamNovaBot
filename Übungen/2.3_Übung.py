import time

def myFunction():
    print("Eine nützliche Aktion ... nehmen Sie sich 10 Sekunden.")
    time.sleep(10)  # Sekunden

start = time.time()

myFunction()

stop = time.time()

print('Laufzeit = ' + '{:5.3f} s'.format(stop - start))