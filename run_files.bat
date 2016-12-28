goto comment

Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham



Command Line Arguments - none of them are required and there are default values set, if they are not specified

--useInputFiles Use files from directory, rather than webcam

--dontUseInputFiles Use webcam rather than files from directory - DEFAULT

--showVideo Dispay video - DEFAULT

--dontShowVideoIs Don't display video 

--doFlipFrame In addition to initial frame orientation, flip frame around the Y axis and also test this against the current detector? - DEFAULT

--dontFlipFrame In addition to applying the detector to the initial frame orientation, flip frame horizontally (reflected around the Y axis) and also test this against the current detector?

--doPromptCodec Prompt user to select output file codec from those installed

--dontPromptCodec Prompt user to select output file codec from those installed - DEFAULT

--outFileExt Output video file extension - default="avi"

--outFileCodec Output video file codec - default="XVID"

--outFileFPS Output video file FPS. Warning: if the frame rate is higher than the hardware can handle, then the video clip appears speeded up - default=10

--maxNumberOfConsecNonDectectFramesBeforeStopRecording When recording, the maximum number of consecutive frames without object detection, before recording stops - default=64

--maxNumberOfConsecDectectFramesBeforeStartRecording The maximum number of consecutive frames where the target object is detected, before recording is started - default=32 

:comment

capture_haylights.py --useInputFiles