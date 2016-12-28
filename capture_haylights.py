'''
Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham
'''

import cv2
import sys
import glob
import os
import time
import datetime
import argparse

inputDir = 'input'
outputDir = 'output'
cascadesDir = 'cascades'
dataDir = 'data'


###############################  START parseCommandLineArguments #########################################


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument('--useInputFiles', dest='inputFilesFromDir', action='store_true', help="Use files from directory, rather than webcam?")
ap.add_argument('--dontUseInputFiles', dest='inputFilesFromDir', action='store_false', help="Use files from directory, rather than webcam?")
ap.set_defaults(inputFilesFromDir=False)

ap.add_argument('--showVideo', dest='show', action='store_true', help="Is video displayed? For unattended file processing etc.")
ap.add_argument('--dontShowVideo', dest='show', action='store_false', help="Is video displayed? For unattended file processing etc.")
ap.set_defaults(show=True)

ap.add_argument("--doFlipFrame", dest='horizontalFlipEachFrameForAsymetricalDetector', action='store_true', help="In addition to initial frame orientation, flip frame around the Y axis and also test this against the current detector?")
ap.add_argument("--dontFlipFrame", dest='horizontalFlipEachFrameForAsymetricalDetector', action='store_false', help="In addition to applying the detector to the initial frame orientation, flip frame horizontally (reflected around the Y axis) and also test this against the current detector?")
ap.set_defaults(horizontalFlipEachFrameForAsymetricalDetector=True)

ap.add_argument("--doPromptCodec", dest='promptCodec', action='store_true', help="Prompt user to select output file codec from those installed.")
ap.add_argument("--dontPromptCodec", dest='promptCodec', action='store_false', help="Prompt user to select output file codec from those installed.")
ap.set_defaults(promptCodec=False)

ap.add_argument("--outFileExt", default="avi", help="Output video file extension.")
ap.add_argument("--outFileCodec", default="XVID", help="Output video file codec.")
ap.add_argument("--outFileFPS", default=10, type=int, help="Output video file FPS.") # Warning: if the frame rate is higher than the hardware can handle, then the video clip appears speeded up.
ap.add_argument("--maxNumberOfConsecNonDectectFramesBeforeStopRecording", type=int, default=64, help="When recording, the maximum number of consecutive frames without object detection, before recording stops.")
ap.add_argument("--maxNumberOfConsecDectectFramesBeforeStartRecording", type=int, default=32, help="The maximum number of consecutive frames where the target object is detected, before recording is started.")

args = vars(ap.parse_args())

# reference as: args["inputFilesFromDir"] etc.



###############################  END parseCommandLineArguments #########################################

'''
None of the these codecs worked for MP4 output
fourcc = cv2.cv.CV_FOURCC(*'H264')
fourcc = cv2.cv.CV_FOURCC(*'X264')
fourcc = cv2.cv.CV_FOURCC(*'mp4v')
fourcc = cv2.cv.CV_FOURCC(*'MJPG')
fourcc = cv2.cv.CV_FOURCC(*'avc1')
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # this breaks it!

"mp4" # can't get this to work with any of the above codecs

'''

logTimeStamp = datetime.datetime.now()
logTimeStamp = logTimeStamp.strftime("%Y%m%d-%H%M%S")

if (args["inputFilesFromDir"]==True):
	text_file = open(dataDir + "\\file_" + logTimeStamp + ".txt", "w")
else:
	text_file = open(dataDir + "\\webcam_" + logTimeStamp + ".txt", "w")



###############################  START using Haar Cascade detectors #########################################

def detect(frame, frame_orientation, logTimeStamp):
    
    targetDetected = False
	
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
    count = 0;
	
    for cascade in glob.glob(cascadesDir + "\\*.xml"):
	
      #print ( glob.glob(cascadesDir + "\\*.xml") ) # list all found cascades
      #print(cascade)
      cascadename = cascade[cascade.rfind("\\") + 1:]
      cascadenameWithoutPath = os.path.splitext(cascadename)[0]
      
      #print("Trying :" + cascadenameWithoutPath + " " + str(count))
      count += 1
		
      # load the Haar cascade detector, then detect target object in the input image
      detector = cv2.CascadeClassifier(cascade)

      targetObjects = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
      )

	   # Draw a rectangle around the target objects... if any detected
      for (x, y, w, h) in targetObjects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		
      if len(targetObjects) != 0:
        print(logTimeStamp + ' - ' + cascadenameWithoutPath + ': target detected (' + frame_orientation + ')!')
        text_file.write(logTimeStamp + ' - ' + cascadenameWithoutPath + ': target detected (' + frame_orientation + ')!\n')
        targetDetected = True;
		
    #if len(targetObjects) != 0:
    if targetDetected == True:
     return True
    else:
      #print('nothing in frame')
     return False

###############################  End using Haar Cascade detectors #########################################



###############################  Start using example detector #############################################

def exampleDetector(frame):

      '''
      if <detection is positive>:
       return True
      else:
       return False
      '''

###############################  End using example detector #############################################


def processVideoFrameByFrame(video_capture, filename):

    recording = False
	
    frameWidth = int( video_capture.get(3) )
    frameHeight = int ( video_capture.get(4) )
	
    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*args["outFileCodec"])
	
    timestamp = datetime.datetime.now()
	
    # consecutive number of frames that have *not* contained any action
    currentNumberOfConsecNonDectectFrames = 0

    # loop through video frame by frame
    #while True:
    while(video_capture.isOpened()):
    #while ret != False:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
		
        if (args["inputFilesFromDir"]==True):
          millisecsSinceVideoStart = int ( video_capture.get(0) )
          hours = int( (millisecsSinceVideoStart/(1000*60*60))%24 )
          minutes = int( (millisecsSinceVideoStart/(1000*60))%60 )
          seconds = int( (millisecsSinceVideoStart/1000)%60 )
          #print (str(hours) + ":" + str(minutes) + ":" + str(seconds) ) 
          logTimeStamp = str(hours).rjust(2, '0') + ":" + str(minutes).rjust(2, '0') + ":" + str(seconds).rjust(2, '0')
		  
        else:
          logTimeStamp = datetime.datetime.now()
          logTimeStamp = logTimeStamp.strftime("%Y%m%d-%H%M%S")
        
		#print (logTimeStamp)		

        if ret:
            #print ("Valid Frame!")

		###############################  Start detecting... #############################################	
			# only proceed if target object detected
            frameDectionStatus = False
            frame_flippedDectionStatus = False
            if args["horizontalFlipEachFrameForAsymetricalDetector"] == True:
              frame_flipped = cv2.flip(frame,0) # flip frame
              frame_flippedDectionStatus = detect(frame_flipped, "flipped", logTimeStamp) # run detector on flipped frame
            frameDectionStatus = detect(frame, "unflipped", logTimeStamp) # run detector on un-flipped frame
			
            '''
			Note: although, the detect() function takes the variable 'frame' (which is a local, not global variable), the changes made to it around line 108 (cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) ) will be reflected in the outer version of 'frame' in this While loop. So, the detected object green boxes are on this version of the frame. 
			I think that this is because the OpenCV rectangle function appends to the variable, rather than reassigning it. Probably works like this:
			If B is assigned to "cat" in the outer code (B="cat"), and then it (B) is reassigned (B = "dog") in the inner function, then the outer variable (B) remains unchanged ("cat"). 
			When the inner variable is appended to (B.append (" has run away"), then the outer variable also changes to "cat has run away".
            '''
            
            if frameDectionStatus == False or frame_flippedDectionStatus == False:
			# if exampleDetector(frame, "unflipped", logTimeStamp): # how to add a different detector, instead of Haar Cascades
		###############################  End detecting... ###############################################	


			    #print('target detected!')
				# reset the number of consecutive frames with *no* action to zero 
				currentNumberOfConsecNonDectectFrames = 0
				# if we are not already recording, start recording
				if recording == False:
						timestamp = datetime.datetime.now()
						#p = "{}/{}.avi".format(args["output"],timestamp.strftime("%Y%m%d-%H%M%S"))
						# start recording...
						recording = True
						
						print ("Recording...")
						text_file.write("Recording...\n")
					
						outPutVideoPathAndFileName = "{}/{}{}.{}".format(outputDir, filename, timestamp.strftime("%Y%m%d-%H%M%S"),args["outFileExt"])
						
						if (args["promptCodec"] == True):
						  # Note: next line shows using -1 instead of fourcc. This will prompt for required codec.
						  out = cv2.VideoWriter(outPutVideoPathAndFileName,-1, args["outFileFPS"], (frameWidth,frameHeight))
						else:
						  out = cv2.VideoWriter(outPutVideoPathAndFileName,fourcc, args["outFileFPS"], (frameWidth,frameHeight))

						
			# otherwise, no action has taken place in this frame, so
			# increment the number of consecutive frames that contain
			# no action
            else:
				currentNumberOfConsecNonDectectFrames = currentNumberOfConsecNonDectectFrames + 1
				#print('nothing in frame')
				
			#print (currentNumberOfConsecNonDectectFrames)

			# if we are recording and reached a threshold on consecutive
			# number of frames with no action, stop recording the clip
            if recording == True and currentNumberOfConsecNonDectectFrames >= args["maxNumberOfConsecNonDectectFramesBeforeStopRecording"]:
				# stop recording...
				print ("Stop Recording...")
				#log += "Stop Recording...\n"
				text_file.write("Stop Recording...\n")
				recording = False
				out.release()
			
            # if we are flipping frames for detection (in addition to regular detection) AND a target object has been detected in the flipped frame...			
            if args["horizontalFlipEachFrameForAsymetricalDetector"] == True and frame_flippedDectionStatus == True:
              frame = cv2.flip(frame_flipped,0) # flip frame (with marked up detected targets) back to correct orientation

            if recording == True:	
			 # write the frame
			 out.write(frame)
			
            if args["show"] == True:
			 # Display the resulting frame
			 cv2.imshow('Video', frame)
		 
            if cv2.waitKey(1) & 0xFF == ord('q'):
				break
				
        else:
            print ("Invalid Frame!")
            #log += "Invalid Frame!\n"
            text_file.write("Invalid Frame!\n")
            print "Stop recording..."
            #log += "Stop recording...\n\n"
            text_file.write("Stop recording...\n\n")
            break # end of the video detected, break out of the while loop

    # print ("And done...")
	# When everything is done, release the capture
    #video_capture.release()
    #out.release()
    cv2.destroyAllWindows()
	


def loadAndLoopMultipleVideoFiles():

	
    for videoPath in glob.glob(inputDir + "\*.avi"):
      # extract the video filename (assumed to be unique)
      filename = videoPath[videoPath.rfind("\\") + 1:]
      print ("processing..." + filename)
      text_file.write("processing..." + filename + "\n\n")
      # print (glob.glob(inputDir + "\*.avi")) # check that all expected vid files are listed
      video_capture = cv2.VideoCapture(videoPath)
      processVideoFrameByFrame(video_capture,filename + "_")

	  
	  

if (args["inputFilesFromDir"]==True):
  loadAndLoopMultipleVideoFiles()
  
else:
  video_capture = cv2.VideoCapture(0)
  print ("processing...from webcam")
  text_file.write("processing...from webcam\n\n")
  processVideoFrameByFrame(video_capture, "webcam_")

print ("Finished processing...")

text_file.write("Finished processing...\n")



'''

Following properties can be accessed via video_capture.get(n), where n = their number (starting at 0) in the list that follows.
So, video_capture.get(3) gives the width 

CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds or video capture timestamp.
CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file: 0 - start of the film, 1 - end of the film.
CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
CV_CAP_PROP_FPS Frame rate.
CV_CAP_PROP_FOURCC 4-character code of codec.
CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
CV_CAP_PROP_HUE Hue of the image (only for cameras).
CV_CAP_PROP_GAIN Gain of the image (only for cameras).
CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
CV_CAP_PROP_WHITE_BALANCE_U The U value of the whitebalance setting (note: only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_WHITE_BALANCE_V The V value of the whitebalance setting (note: only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_ISO_SPEED The ISO speed of the camera (note: only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_BUFFERSIZE Amount of frames stored in internal buffer memory (note: only supported by DC1394 v 2.x backend currently)

'''