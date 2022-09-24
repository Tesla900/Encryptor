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
        #Example shuffle
        for i in range(1, 200):
            a1 = randint(1, matrix.shape[0]-1)
            b1 = randint(1, matrix.shape[0]-1)
            matrix[[a1, b1],:] = matrix[[b1, a1],:]
            a2 = randint(1, matrix.shape[1]-1)
            b2 = randint(1, matrix.shape[1]-1)
            matrix[:,[a2, b2]] = matrix[:,[b2, a2]]
        cv2.imshow('frame', matrix)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()