import cv2
import numpy
from reader import UMatFileVideoStream
from random import seed, randint

stream = UMatFileVideoStream(0).start()

def main():
    with open("seed","r") as f:
        seed(f.readline())
    while not stream.stopped:
        frame = stream.read()
        matrix = frame.get()
        #Example encode-decode
        perms = 100
        ts = [0]*perms*4
        for i in range(1, perms):
            ts[i*4] = randint(1, matrix.shape[0]-1)
            ts[i*4+1] = randint(1, matrix.shape[0]-1)
            matrix[[ts[i*4], ts[i*4+1]],:] = matrix[[ts[i*4+1], ts[i*4]],:]
            ts[i*4+2] = randint(1, matrix.shape[1]-1)
            ts[i*4+3] = randint(1, matrix.shape[1]-1)
            matrix[:,[ts[i*4+2], ts[i*4+3]]] = matrix[:,[ts[i*4+3], ts[i*4+2]]]
            cv2.imshow('encoded', matrix)
        for i in range(perms-1, 0, -1):
            matrix[:,[ts[i*4+2], ts[i*4+3]]] = matrix[:,[ts[i*4+3], ts[i*4+2]]]
            matrix[[ts[i*4], ts[i*4+1]],:] = matrix[[ts[i*4+1], ts[i*4]],:]

        cv2.imshow('decoded', matrix)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()