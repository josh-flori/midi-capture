########   SETTING UP RASPBERRY PI  #########
########   SETTING UP RASPBERRY PI  #########
########   SETTING UP RASPBERRY PI  #########
########   SETTING UP RASPBERRY PI  #########
########   SETTING UP RASPBERRY PI  #########
########   SETTING UP RASPBERRY PI  #########

#For the raspberry pi camera array you will need:
#5 raspberry pi zero's, 5 micro usbs, 5 micro sd cards (16 gigs are fine) with at least 1 micro sd to regular sd card adapter and then a way to get the regular sd card into your computer, 5 mounting plates, 5 camera modules and 5 standard pi zero cases.

#This video will walk you through setting up the system. I think the video is out of date, jessie seems to have been replaced by Stretch when you go to download the operating system.
https://www.youtube.com/watch?v=upY4Fusi4zI&t=720s


sudo dd bs=1m if=/users/josh.flori/desktop/2017-11-29-raspbian-stretch-lite.img of=/dev/rdisk2

open up boot drive. if you dont see it in finder, to navigate to the "go" menu at top of screen from 
within finder, then click on computer. you will see it there.

config.txt > dtoverlay=dwc2
cmdline.txt > modules-load=dwc2,g_ether
create empty text file named "ssh" and drag it into the boot drive


#At 8:53 in the vieo when he adds a folder, I don't know what program he is using that allows him to createa file, but I had to open a text editor, save a file as "ssh" and just drag it into the boot drive. That works.
#And just like the video, my diskutil would not let me eject the boot drive, I just had to take it out.




#To share internet with pi on mac do: system preferences > sharing > and enabled "internet sharing". You will probably need to be on your home network for internet sharing to work.



#Be aware that the camera can be damaged by static electricity. Before removing the camera from its grey anti-static bag, make sure you have discharged yourself by touching an earthed object (e.g. a radiator or PC Chassis). I did break one of my camera modules by either dropping it or getting static on it, not sure which. So just be careful


# tpye sudo raspi-config to enure camera is installed and working

########   PRE-GAME PARTY   #########
########   PRE-GAME PARTY   #########
########   PRE-GAME PARTY   #########
########   PRE-GAME PARTY   #########
########   PRE-GAME PARTY   #########
########   PRE-GAME PARTY   #########

## PURPOSE: take a simple video with the raspberry pie of the inside of the piano. video will be used for image recognition and fed into our algorithm for note detection.

# 1) after configuring raspberry pie, make sure it's plugged in, the green power light is on and then type this into the command line
ssh pi@raspberrypi.local
#when prompted for a password, type this:
raspberry

# 2) in the command line, type this to install the canera library:
sudo apt-get install python-picamera
sudo raspi-config

# 3) enter python by typing 
python


print_time()
threading.Timer(60-float(str(datetime.datetime.today().second) +'.'+ str(datetime.datetime.today().microsecond)), print_time).start()

time.sleep(60-float(str(datetime.datetime.today().second) +'.'+ str(datetime.datetime.today().microsecond)))
print(datetime.datetime.today().microsecond)

### NOTE THAT TIME.SLEEP WILL NOT WORK AS IT IS WILDLY INACCURATE

# 4) set the camera up where you want, then record video with the folloing:
import picamera
import datetime
import threading
camera = picamera.PiCamera()
camera.framerate = 120  ## 120 is the highest possible framerate and will not work beyond a certain resolution
camera.iso = 1600
camera.resolution = (900, 300)  ## please note 900x200 refers to the number of columns (width) and then the height (rows) in pixels. all other references to matrices and arrays in python and excel will be the exact opposite which means that as an array, a 900x200 image is actually 200x900 (rows by columns) as opposed to columns by rows. 
camera.start_preview()
camera.start_recording('second_test.h264')

camera.stop_recording()


MP4Box -add test.h264 first.mp4
MP4Box -add test.h264 second.mp4
MP4Box -add test.h264 third.mp4
MP4Box -add test.h264 fourth.mp4
MP4Box -add test.h264 fifth.mp4

    
exit() #this takes you out of python
ls #this will show you the file to ensure it was captured correctly. If you see nothing, the file was not captured

scp pi@192.168.2.9:first.mp4 /users/josh.flori/desktop
scp pi@192.168.2.8:second.mp4 /users/josh.flori/desktop
scp pi@192.168.2.7:third.mp4 /users/josh.flori/desktop
scp pi@192.168.2.6:fourth.mp4 /users/josh.flori/desktop
scp pi@192.168.2.5:fifth.mp4 /users/josh.flori/desktop

#### GENERAL NOTES:::::
#### to exit python type: "exit()"
#### to see what files exist on the pi, type: "ls" in the home directory (home directory looks like this: pi@raspberrypi:~ $)
#### to clear ALL files from home directory, type: "rm -r *"




#In the event that you dont have a monitor to view footage coming from pi and follow the code above, create a video and try to view in vlc and it says the length is 0 seconds and are unable to view it, enter python again on the raspberry pi and enter the following code:

import picamera
from time import sleep
camera = picamera.PiCamera()
camera.capture('image1.jpg')

#if you get a bunch of error messages with this at the bottom: "No data recevied from sensor. Check all connections, including the SUNNY chip on the camera board" then fiddle around with the physical connection between the raspberry pi and the camera module until you get a secure connection.

#if you get an error message like :"Camera is not enabled. Try running 'sudo raspi-config' and interfacing options to enable the camera. picamera.exc.PiCameraError: Camera is not enabled. Try running 'sudo raspi-config' and ensure that the camera has been enabled." then 



import picamera
import datetime
import threading
camera = picamera.PiCamera()
camera.framerate = 120 
camera.iso = 1600
camera.resolution = (900, 300) 
camera.start_preview()
camera.start_recording('test.h264')
camera.wait_recording(2)
camera.stop_recording()

MP4Box -add test.h264 test.mp4


scp pi@192.168.2.9:test.h264 /users/josh.flori/desktop





########      STEP 1      ###########
######## VIDEO CONVERSION ###########
######## VIDEO CONVERSION ###########
######## VIDEO CONVERSION ###########
######## VIDEO CONVERSION ###########
######## VIDEO CONVERSION ###########
########      STEP 1      ###########

### PURPOSE: we have taken a video of the inside of the piano. in this step we will convert the file type from the default .h264 to .mp4 because .h264 will not be recognized by our code in the next step, so we must convert it to get it to work.

sudo apt-get update
sudo apt-get install gpac

MP4Box -add test.h264 test.mp4   ## you will type this command into the command line on the raspberry pi after installing the proper libraries (MP4Box). change the filenames as needed and it should work properly. this needs to be done so that in the next step, where we convert the video to single image jpegs, actually works. cv2 won't read the video if it remains h264 so we must convert.

## now we must get file on to main computer
# in the command line (on main computer, not raspberry pie), use this to get file from pie to computer:
scp pi@192.168.2.9:test.mp4 /users/josh.flori/desktop #"filename.mp4" will be whatever filename you set in the previous line. then change the "josh.flori" to your user folder. THE VIDEO WILL NOT BE VIEWABLE IN QUICKTIME. USE VLC OR YOUR VIDEO VIEWER OF CHOICE
 
 
 
 ####IN ORDER TO RE-CONNECT A SINGLE PI TO THE INTERNETS
 SSH into the desired pi
 
 enter the command "sudo su -" to change to the "superuser" known as root (this gives us rights to change network settings)

 change to the folder "etc" by entering: "cd /etc"

 edit the file dhcpcd.conf using nano:
 "nano dhcpcd.conf"

 COMMENT OUT the following lines of code:
 interface usb0
 static ip_address=192.168.2.8/24
 static router=192.168.2.1/24
 static domain_name_servers=192.168.2.1
 
 save and exit the file in nano (ctrl o + enter, ctrl x)
 
 still as the super user, enter the command reboot to apply the change
 
 On your PC, remove the network bridge then unplug the other pis 
 
 enable internet connection sharing from Wifi to the remaining plugged in RNDIS 
 (or virtual raspberry pi) network adapter)
 
 Clear the ssh known hosts files with this:
 > ~/.ssh/known_hosts
 
 ssh back into the rapsberry pi using pi@raspberrypi.local (it may take two tries)
 
 Test connectivity by running "ping google.com"
 if it doesnt work, go into network settings (mac), click on the rndis device, click advanced, then renew 
 dhcp lisense, reboot the pi, and repeat if it doesnt work on first try.
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
########     STEP 2     ###########
######## VIDEO TO IMAGE ###########
######## VIDEO TO IMAGE ###########
######## VIDEO TO IMAGE ###########
######## VIDEO TO IMAGE ###########
######## VIDEO TO IMAGE ###########
########     STEP 2     ###########

### PURPOSE: so far, we have captured a video, converted it to .mp4 so that we can actually use it, and transfered it to our main computer where we will be working. now, our algorithm cannot work directly with a video, it can only work with images - one at a time. so we must take the video and extract each frame as a jpg image.

## we must enter a virutal environment because i have two versions of pandas (i think it was pandas) and cv2 references the old one and says "sorry, this version is too old, i can't help you" so we intsalled new pandas in virtual environment to get around having to point to the new one in regular environment
source ENV/bin/activate

## enter python, then do this stuff
import cv2 
import os
os.chdir('/Users/josh.flori/project') ## navigate to wherever you put your video. i can't remember, but i think i changed directory because i was unable to pass the path in the file name in the next line. 
vidcap = cv2.VideoCapture('test.mp4')  ## this reads video file taken from inside of piano
count = 0
success = True
while success: #count < 2:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imwrite("frame%d.jpg" % count, image)    # this saves frame as JPEG file
  count += 1
  





from PIL import Image
import cv2 
import os
import numpy as np
os.chdir('/Users/josh.flori/project') ## navigate to wherever you put your video. i can't remember, but i think i changed directory because i was unable to pass the path in the file name in the next line. 
vidcap = cv2.VideoCapture('/Users/josh.flori/project/goodtest.mp4')  ## this reads video file taken from inside of piano
count = 0
success = True
while success:
  success,color_img = vidcap.read()
  blkwht_img = np.asarray(Image.fromarray(color_img).convert('L'))
  retval, final_img = cv2.threshold(blkwht_img, 30, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
  print('Read a new frame: ', success)
  cv2.imwrite("frame%d.jpg" % count, final_img)    # this saves frame as JPEG file
  count += 1






blkwht_img = np.asarray(Image.open('frame2200.jpg').convert('L'))
retval, final_img = cv2.threshold(blkwht_img, 100, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
display_cropped_image = Image.fromarray(final_img)  ## convert array back into an image with this line
display_cropped_image.show()  






import cv2 
import os
os.chdir('/Users/josh.flori/desktop') ## navigate to wherever you put your video. i can't remember, but i think i changed directory because i was unable to pass the path in the file name in the next line. 
vidcap = cv2.VideoCapture('test.mp4')  ## this reads video file taken from inside of piano
count = 0
success = True
while success and count < 200: #count < 2:
        success,color_img = vidcap.read()
        #blkwht_img = np.asarray(Image.fromarray(color_img).convert('L'))
        retval, final_img = cv2.threshold(color_img, 50, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        poop = np.asarray(final_img)
        cv2.imwrite("final.jpg", final_img)   
        count += 1





  
  
########         STEP 3           #########
######## CROP IMAGES FOR LABELING #########
######## CROP IMAGES FOR LABELING #########
######## CROP IMAGES FOR LABELING ######### 
######## CROP IMAGES FOR LABELING #########
######## CROP IMAGES FOR LABELING #########   
########         STEP 3           #########

### PURPOSE: not only can the algorithm not work with a video, it also cannot work with the entire image. we must crop down to a single note at a time in order to train the algorithm because after all, note detection only works for just that - a single note at a time. so we must work note by note. when we have cropped down all of the frames to represent just a single note, we will do two things: 1) pass the pixel values of each image into a dictionary which we will feed to our algorithm as raw data a well as... 2) look at the images and by hand, label them as being of class 1 (at rest), 2 (in motion) or 3 (fully activated). we will pass this class information along with the raw data information into the algorithm and it will then figure out what class an image is without being told. that way, we can play the piano and it knows what's happening! but first, step 3:
  
  
# in case you left the directory, make sure you are still there:
import os
from PIL import Image
import numpy as np
os.chdir('/Users/josh.flori/project/')


# now, we ask ourselves, "in what pixel range does our note reside?" we can test that here.
crop_image = np.asarray(Image.open('frame200.jpg').convert('L'))[160:300:,850:870] ## "Image.open" simply opens the image in question, in this case we have picked a single frame in which the note was activated so that it would be easy to identify in the image. ".convert('L')" converts the image to black and white (greyscale), the L stands for "luminance" I believe, in other words, brightness only, no color. so with those lines we load the image and convert to greyscale. "np.asarray" takes the greyscale image and converts it to an array of pixel values ranging from 0 to 255 to represent the brightness of the image at that pixel. the dimensions of the array will be 200x900 (rows by columns) because the image was 200pixels high (rows) and 900pixels wide (columns). the next part is the "[:,451:506]". when you see anything in [] in python it means "get these range of values". specifically, it means "give me "all rows for columns 451 to 506".

## .... technically this section is used for discovering the note's placement in the image and so converting to greyscale is not necessary yet but oh well.


display_cropped_image = Image.fromarray(crop_image)  ## convert array back into an image with this line
display_cropped_image.show()         ## you can view the image like this
display_cropped_image.save('/users/josh.flori/desktop/cropped_image.jpg')   ## and use this to save the image, if you want   
  
  
## in the above, mess with the 451:506 numbers until you find the exact dimensions of the note you are looking for. we are going to use that section to train our algorithm on that note.
  

## now below we are basically just taking what we learned above and looping through all the images, cropping them down, then saving new cropped files, one image, or frame of the video, at a time
for i in range(0,1189):  ## this sectiond the number of images
    temp_array= np.asarray(Image.open(str('frame')+str(i)+str('.jpg')).convert('L'))[160:300:,855:870]  ## our code in step 2 named the images with the word "frame" so we use that in our construction of the image name, then we just pass i and add the final .jpg to create the file name. we open the image with "Image.open", then convert to greyscale with ".convert('L')", then get the range of pixels that we discovered above and convert to array of pixel values
    retval, threshold = cv2.threshold(temp_array, 40, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C) # crushes the image to reduce information down to only what's necessary. I chose a value of 200 instead of 255 just because grey is easier on the eyes than white.
    temp_image = Image.fromarray(threshold)  ## convert back to an image
    temp_image.save(str('/users/josh.flori/project/C8/')+str(i)+str('.jpg'))  ## save the image to whatever directory you want. we are just saving them with the number of the frame, no name.
    
## why why can't just crop the image without converting to an array, im not sure, it's probably possible but this is just kind of what i found first and it works.
    




