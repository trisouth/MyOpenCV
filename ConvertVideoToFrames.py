"""
  
  ConvertVideoToFrames.py
  
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

# Set your paths accordingly
videoFilesPath = "C:\\Users\\Utku.GUNEY\\Desktop\\100GOPRO\\"
framePath = "C:\\Users\\Utku.GUNEY\\Desktop\\100GOPRO\\output\\"

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
    

def getVideoFiles():
    
    # Use your own pattern for your input video files
    videoFiles = glob.glob(videoFilesPath + "*-converted.MP4")
    
    for videoFile in videoFiles:
        
        captureFrames(videoFile)
        

def getVideoFileName(videoFilePath):
    
    head, tail = ntpath.split(videoFilePath)
    return tail or ntpath.basename(head)


if __name__ == "__main__":
    
    getVideoFiles()
