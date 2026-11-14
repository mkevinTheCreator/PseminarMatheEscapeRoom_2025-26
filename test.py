import time

lastSolvedTime = 0
while True:
    if int( time.time() - lastSolvedTime ) > 5:
        print(f"lst {lastSolvedTime} time {time.time()}")
        lastSolvedTime = time.time()
    