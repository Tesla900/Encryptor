import cv2
from reader import UMatFileVideoStream

stream = UMatFileVideoStream(0).start()

def main():
    while not stream.stopped:
        frame = stream.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()