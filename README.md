Chroma key by 홍성욱20221140, 안동원20221056

-- How To Use--
Run python program with the two input videos in the same directory. This program replaces green colors with the background video

-- Methods Used --
We used a simple cv2.inRange() function to create a mask for a certain range of colors. 
Then we used cv2.copyTo() to make the output video.
Finally cv2.VideoWriter() was used to save the video 
