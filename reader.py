from threading import Thread
import sys
from unicodedata import name
import cv2
from time import sleep

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


class UMatFileVideoStream:

    def __init__(self, path, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.count = 0

        # initialize the queue used to store frames read from
        # the video stream
        self.Q = Queue(maxsize=queueSize)

        # We need some info from the file first. See more at:
        # https://docs.opencv.org/4.1.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        self.width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # since this version uses UMat to store the images to
        # we need to initialize them beforehand
        self.frames = [0] * queueSize
        for ii in range(queueSize):
            self.frames[ii] = cv2.UMat(self.height, self.width, cv2.CV_8UC3)

    def __del__(self):
        self.stream.release()

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the stream
                # (grabbed, frame) = self.stream.read()
                self.count += 1
                target = (self.count-1) % self.Q.maxsize
                grabbed = self.stream.grab()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return

                self.stream.retrieve(self.frames[target])

                # add the frame to the queue
                self.Q.put(target)

    def read(self):
        while (not self.more() and self.stopped):
            sleep(0.1)
        # return next frame in the queue
        return self.frames[self.Q.get()]

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
