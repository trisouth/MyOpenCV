import glob
import cv2
import ntpath
from queue import LifoQueue
import threading
import time
import os
import psutil
from datetime import datetime

# input video files path
videoFilesPath = "/home/utku/Desktop/100GOPRO/"
# output frames path
framePath = "/home/utku/Desktop/100GOPRO/output/"

videoFiles = LifoQueue()
frames = LifoQueue()

# number of video file reader threads
readerCount = 2
# number of frame writer threads. 
# Depending on disk performance, writer to reader ratio should be 3 : 1 or higher
writerCount = 8

frameCounts = LifoQueue()
frameCount = 0

liveReader = True

# maximum memory amount in MB which can be consumed by this app. keep this limit as high as possible.
memoryUsageLimit = 32768

# maximum counter limit for a single reader thread to hit maximum memory amount. 
# if a reader thread reaches memoryUsageLimit value for more than memoryLimitCounter times then kills itself.
memoryLimitCounter = 3

# number of seconds, a reader will sleep when application reaches memoryUsageLimit.
memoryLimitWaitSecs = 10

# Application sleeps for a maximum duration of memoryLimitCounter X memoryLimitWaitSecs seconds. if during
# sleep time, writer threads can open space in memory by writing frames to disk, then reader threads continue
# storing frames in memory. if not, then reader threads kill themselves; application stops reading videos.

def getVideoFiles():
    
    global videoFiles
    
    for videoFile in glob.glob(videoFilesPath + "*-converted.mp4"):
        
        videoFiles.put(videoFile)

class VideoFramer(threading.Thread):
    
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        #self.videoFile = videoFile
        
    def run(self):
        #print("Starting: " + self.threadName)
        frame(self.threadID, self.threadName)

def frame(threadID, threadName):
    
    global liveReader
    memoryLimit = True
    
    while not videoFiles.empty() and memoryLimit:
        
        videoFile = videoFiles.get()
        
        readFrameCount = 0 # for informational purposes on screen.
        
        video = cv2.VideoCapture(videoFile)
        _, frame = video.read()
        
        while _:
            
            readFrameCount = readFrameCount + 1
            frames.put(frame)
            
            _, frame = video.read()
            
            if frame is None:
                
                # in some cases, due to video data, the read frame can be none
                
                if _:
                    
                    pass
                
                else:
                    
                    break
        
        video.release()
        
        # after each video file, do memory and live reader threads check.
        tempMemoryLimitCounter = 1
        
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss
        
        # wait for memoryLimitCounter times, if the memory consumption is over memoryUsageLimit
        # in every wait, this thread sleeps for memoryLimitWaitSecs seconds
        while mem / (1024 * 1024) > memoryUsageLimit:
            
            print(threadName + " " + str(mem))
            tempMemoryLimitCounter = tempMemoryLimitCounter + 1
            
            if tempMemoryLimitCounter > memoryLimitCounter:
                memoryLimit = False
                print(threadName + " memory usage didnt drop after specified limits.")
                break
            else:
                print(threadName + " memory usage reached " + str(memoryUsageLimit) + " MB. waiting for " + str(memoryLimitWaitSecs) + " seconds.")
                time.sleep(memoryLimitWaitSecs)
            
            mem = process.memory_info().rss
            
        # for informational purposes. does not have any effect in functionality.
        #print(threadName + " " + videoFile + " " + str(readFrameCount))
        #frameCounts.put(readFrameCount)
    
    #print("Reader" + str(threadID) + " - finished reading video files")
    
    threads[threadID] = None
    
    tempLiveReader = False
    
    for i in range(readerCount):
        
        if threads[i] is None:
            
            #print(threadName + " " + "thread[" + str(i) + "] is none")
            tempLiveReader = False
        else:
            #print(threadName + " " + "thread[" + str(i) + "] is not none")
            tempLiveReader = True
            break
    
    #print(threadName + " is changing liveReader to " + str(tempLiveReader))
    liveReader = tempLiveReader

class FrameWriter(threading.Thread):
    
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
    
    def run(self):
        #print("Starting: " + self.threadName)
        writeDisk(self.threadID, self.threadName)

def writeDisk(threadID, threadName):
    
    #print("Writer: " + str(threadID) + " started writing to disk")
    
    global frameCount
    
    while not frames.empty():
        
        cv2.imwrite(framePath + "frameName" + str(threadID) + "-" + str(frameCount).zfill(5) + ".jpg", frames.get())

        frameCount = frameCount + 1
    
    #print("Writer: " + str(threadID) + " finished writing to disk")
    #del threads[threadID]

if __name__ == "__main__":
    
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    
    getVideoFiles()
    
    threads = {}
    
    for i in range(readerCount):
        
        t = VideoFramer(i, "reader-" + str(i))
        t.start()
        threads[i] = t
        
    print("started readers")
    
    while not frames.empty() or liveReader:
        
        #print("frames is not empty or there are liveReaders.")
        for i in range(readerCount, readerCount + writerCount):
            
            t = FrameWriter(i, "writer-" + str(i))
            t.start()
            threads[i] = t
            
        for i in range(readerCount, readerCount + writerCount):
        
            try:
                t = threads[i]
                t.join()
            except:
                pass
    
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    
    #print(liveReader)
    print("the end")
