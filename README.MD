Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham

Highligher and Summariser

This app takes either a webcam video stream or multiple (unspecified) video files (currently AVI/XVID) and applies multiple (unspecified) Haar Cascade detectors (including optional rotation of frames for asymmetrical detectors). The output from this are video 'highlight' files, including each of the detection instances, where lack for detection for a prescribed period ends a highlight.
The intention is that, using this app, Haar Cascades can be tested and combined to find optimal detection configurations.
Also, video files (for example captured animal behaviour video from 'the field') can be bulk processed, so that researchers can rapidly get to the action.

USAGE

Command Line Options:

Switches: 

capture_haylights.py --useInputFiles [DEFAULT]
capture_haylights.py --dontUseInputFiles

capture_haylights.py --showVideo [DEFAULT]
capture_haylights.py --dontShowVideo

capture_haylights.py --doFlipFrame [DEFAULT]
capture_haylights.py --dontFlipFrame

capture_haylights.py --doPromptCodec
capture_haylights.py --dontPromptCodec [DEFAULT]

Parameters: 

capture_haylights.py --outFileExt [DEFAULT = avi]
capture_haylights.py --outFileCodec [DEFAULT = XVID]
capture_haylights.py --outFileFPS [DEFAULT = 10]
capture_haylights.py --maxNumberOfConsecNonDectectFramesBeforeStopRecording [DEFAULT = 64]
capture_haylights.py --maxNumberOfConsecDectectFramesBeforeStartRecording [DEFAULT = 32]

Therefore...
Running: capture_haylights.py
is the same as running: 
capture_haylights.py --useInputFiles --showVideo --doFlipFrame --dontPromptCodec --outFileExt avi --outFileCodec XVID --outFileFPS 10 --maxNumberOfConsecNonDectectFramesBeforeStopRecording 64 --maxNumberOfConsecDectectFramesBeforeStartRecording 32

TO DO:

1. Fix for input / output MP4 files. Currently, this only works to input / output .AVI / XVID format videos. This is probably because the correct codecs need installing (?). For MP4 files, I tried codec (fourcc) settings: 'H264', 'X264', 'mp4v', 'MJPG' and 'avc1'. None of these works. Note: run with --doPromptCodec switch (default = False) to see installed codecs.

2. Longer term - add an 'activity' parameter? So, that only clips are saved that exceed a specified level of movement within a sequential series of frames. This is intended to filter out active behaviours from long videos, where horses are consistently on screen, but are inactive.

3. Consider using threads when running multiple Haar Cascades, to speed things up a bit.

