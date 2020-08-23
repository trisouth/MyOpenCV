"""

  @author: Utku Guney (trisouth@github)

  @development environment:
  
    Windows 10
    Python 3.7.6
    OpenCV 4.2.0

  @version history:
      1. 20.08.2020 - v1.0 - initial release
        
  @description:
      
      This Python code reads the video files located in videoFilesPath and
      stores each frame in the video files as an image into the framePath.
      
      Those stored frames are to be used in AI model training.
      
      Note: This code crashed with videos captured with GoPro Hero 4.
      Code started running but in the 52nd frame crashed.
      
      Researches in the web resulted in that, OpenCV is not happy with audio 
      tracks in videos. I removed the audio with VLC from all input videos,
      and worked fine.
      
"""

import glob
import cv2
import ntpath
from queue import LifoQueue

import threading
import time

videoFilesPath = "C:\\Users\\Utku.GUNEY\\Desktop\\100GOPRO\\"
framePath = "C:\\Users\\Utku.GUNEY\\Desktop\\100GOPRO\\output\\"

videoFiles = LifoQueue()
frames = LifoQueue()

"""
def captureFrames(videoFile):
    
    video = cv2.VideoCapture(videoFile)
    print("Video Details")
    print("File name   : " + videoFile)
    print("FPS         : " + str(video.get(cv2.CAP_PROP_FPS)))
    print("Frame Width : " + str(video.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("Frame Height: " + str(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    frameCount = 0
    windowName = "Open CV Video Player"
    
    # -14 is based on yourfile name preference
    frameName = getVideoFileName(videoFile)[:-14] + "_"
    
    # Start reading the video file
    _, frame = video.read()
    
    # Print a sample output frame name
    print(framePath + frameName + str(frameCount).zfill(5) + ".jpg")
    
    while _:
        
        # Count the frames
        frameCount = frameCount + 1
        
        # Save the frame to an image file
        cv2.imwrite(framePath + frameName + str(frameCount).zfill(5) + ".jpg", frame)        
        
        # Read the next frame from video file
        _, frame = video.read()
        
        #if frame is None:
        #    print("Frame is none")
        
        if _:
            
            # Delete comments if you want to watch videos during processing
            #cv2.imshow(windowName, frame)
            
            #if cv2.waitKey(1) == 27:
            #    break
            
            pass
            
        else:
            
            break
        
            
    print("Frame Count: " + str(frameCount))
    cv2.destroyAllWindows()
    video.release()
"""    

def getVideoFiles():
    
    global videoFiles
    
    # Use your own pattern for your input video files
    #videoFiles = glob.glob(videoFilesPath + "*-converted.MP4")
    
    for videoFile in glob.glob(videoFilesPath + "*-converted.MP4"):
        
        #captureFrames(videoFile)
        videoFiles.put(videoFile)
        

def getVideoFileName(videoFilePath):
    
    head, tail = ntpath.split(videoFilePath)
    return tail or ntpath.basename(head)
    
#   >>> paths = ['a/b/c/', 'a/b/c', '\\a\\b\\c', '\\a\\b\\c\\', 'a\\b\\c', 
#   ...     'a/b/../../a/b/c/', 'a/b/../../a/b/c']
#   >>> [path_leaf(path) for path in paths]
#   ['c', 'c', 'c', 'c', 'c', 'c', 'c']
#
#   ntpath module works in both windows and linux. above are possible videoFilePath samples
#   and this function returns always the right file name



exitFlag = 0
frameCount = 0

class  FrameWriter(threading.Thread):
    
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
    
    def run(self):
        #print("Starting: " + self.threadName)
        writeDisk(self.threadID, self.threadName)

        
def writeDisk(threadID, threadName):
    
    print("Writer: " + str(threadID) + " started writing to disk")
    
    global frameCount
    
    while ((not threads[0] is None) or (not threads[1] is None)):
        
        if not frames.empty():
        
            cv2.imwrite(framePath + "frameName" + str(threadID) + "-" + str(frameCount).zfill(5) + ".jpg", frames.get())
            frame = frames.get()
            #print(framePath + "frameName" + str(frameCount).zfill(5) + ".jpg")
            
            frameCount = frameCount + 1
    
    print("Writer: " + str(threadID) + " finished writing to disk")
    #del threads[threadID]
    
    
class VideoFramer(threading.Thread):
    
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        #self.videoFile = videoFile
        
    def run(self):
        print("Starting: " + self.threadName)
        frame(self.threadID, self.threadName)

        
def frame(threadID, threadName):
    
    while not videoFiles.empty():
        
        videoFile = videoFiles.get()
        
        readFrameCount = 0
        
        video = cv2.VideoCapture(videoFile)
        _, frame = video.read()
        
        while _:
            
            readFrameCount = readFrameCount + 1
            frames.put(frame)
            
            _, frame = video.read()
            
            if frame is None:
                
                #    print("Frame is none")
                
                if _:
                    
                    pass
                
                else:
                    
                    break
        
        video.release()
            
        print(threadName + " " + videoFile + " " + str(readFrameCount))
    
    print("Reader" + str(threadID) + " - finished reading video files")
    
    #del threads[threadID]
    threads[threadID] = None
    
    #t = FrameWriter(threadID, "writer-" + str(threadID))
    #t.start()
    #threads[threadID] = t


class myThread(threading.Thread):
    
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Existing " + self.name)
        
def print_time(threadName, delay, counter):
    
    while(counter):
        if exitFlag:
            threadName.exit()
            
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1



if __name__ == "__main__":
    
    getVideoFiles()
    
    threads = {}
    
    for i in range(2):
        
        t = VideoFramer(i, "reader-" + str(i))
        t.start()
        threads[i] = t
    
    print("started readers")
    
    #time.sleep(2)
    
    while frames.empty():
        print("waiting")
        pass
    
    print("starting writers")
        
    for i in range(2, 6):
            
        t = FrameWriter(i, "writer-" + str(i))
        t.start()
        threads[i] = t
    
    print("started writers")
    
    print("joining")
    for i in range(7):
        #print(str(i) + " is joining")
        try:
            t = threads[i]
            t.join()
        except:
            pass
    
    print("len(threads)=" + str(len(threads)))
    

    
    """
    thread1 = VideoFramer(1, "Thread-1")
    thread2 = VideoFramer(2, "Thread-2")
    
    threads[1] = thread1
    threads[2] = thread2
    
    # Start new Threads
    thread1.start()
    thread2.start()
    
    print("1 joining")
    thread1.join()
    print("2 joining")
    thread2.join()
    """
    
    print ("Exiting Main Thread")
    
    print("ok")