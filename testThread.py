import threading

def create():
    sa = threading.Thread(target=callingFunction)
    sa.start()
    sa.join()
