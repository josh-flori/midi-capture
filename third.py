#source ENV/bin/activate

###### IMPORT
#sudo apt-get install python-pip
import os
#sudo apt-get install libjpeg-dev
#sudo pip install pillow
from PIL import Image
#pip install numpy
import numpy as np
#sudo apt-get install python-opencv
import cv2
import logging
##############  sudo apt-get install python-pandas <-- not needed, only for debugging
###############  import pandas as pd  <-- not needed, only for debugging
#sudo apt-get install scipy
from scipy import stats 

 
def find_note_positions(video_file):
    vidcap = cv2.VideoCapture(video_file) 
    #number_of_frames = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) ## gets total number of frames
    #syntax must be: int(vidcap.get(cv2.cv.CAP_PROP_FRAME_COUNT)) for computer, i guess it's running a different version
    number_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success = True
    count=0
    while success and count < number_of_frames:
        #this process is reading the LAST frame of the video and using that to construct a list of index ranges of where the notes are. so.... you need to be sure that all of the notes are at rest for the final frame when you stop recording. the reason we take the final frame is because the camera starts the first second or two dark and adjusts the iso upward, so the first frames won't be good... so taking the last is the easiest way to ensure we get a good image every time.
        success, color_img = vidcap.read()
        count+=1
        retval, final_img = cv2.threshold(color_img, 50, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        #cv2.imwrite("/users/josh.flori/project/debug/0/frame{}.jpg".format(count), final_img)
    start_list = [] ##these hold the column indeces of the notes - found by the method below. these will need to be passed 
    end_list = []
    row_list = [] ### DELETE THIS, FOR DEBUGGING ONLY
    sos=[] ## same with this one
    bottom_of_note = []
    have_we_reached_the_notes = 'no'
    are_we_past_the_notes = 'no'
    for row in range(len(final_img)-1,-1,-1): # len(blkwht_image) return the number of rows in the image. the range argument returns the rows, from bottom up, of final_img. for instance, if the image has 300 rows, then range(len(blkwht_img)-1,-1,-1) will return numbers 299,298,297..... 2,1,0, in that order. When we iterate over this, it lets us search the image from the bottom row to the top
        potential_note_count = 0 #when a white value is found in the loop, this begins to accumulate all continuous white values
        # and resets to 0 when a non-white value is found, the theory being that when you have like 10 or more of these, you have found a note.
        potential_start_position = 0 #gets set to the iteration number (column number) when a white value is first found. 
        #this will stay fixed until the next note is found.. i think
        iteration_number = 0 # counts the pixel iteration - will be used to set column index value for notes
        potential_end_position = 0
        if np.sum(final_img[row,:]) < 200*3*(final_img.shape[1]*.9): ##this section is just checking the basic color of # the row...final_img.shape[1] is the number of columns (number of pixels in the row), 200 is the grey value we set things to when we process the image, 3 is the number of values for each pixel (rgb). so if this evaluates to true, which means the sum is really big, that means we are still in the grey section and have not yet reached the notes
            have_we_reached_the_notes = 'yes' ##not sure if continue will do what you want here, be sure to check on it
            for pixel in final_img[row,:]:
                if np.sum(pixel) == 0 and potential_note_count == 0:
                    ##if potential_note_count=0 this means that it is the first #white pixel that has been detected in foward motion since the previous black space, or the beginning of the frame if the note is immediately in view. np.sum(pixel) is necessary because we have 3 values for each pixel (rgb) and = 0 is when all of them are 0, which means they are black, which in our image will be the note in question
                    potential_start_position = iteration_number
                    iteration_number += 1
                    potential_note_count += 1
                elif np.sum(pixel) == 0: ## if potential_note_count > 0
                    iteration_number += 1
                    potential_note_count += 1
                else: #if not a note (black space, <30 brightness)
                    if potential_note_count > 22: #this will effectively be triggered as soon as a grey (or other color) (non-note) pixel is found. 
                    # it is looking at the previous continous range of black pixels (note) and 10 is an arbitrary minimum distance that represents the width of a note, so if the count > 10 then we can pretty much confirm that it was a note. once we have figured this out, we will finalize the index range for that note and add our knowledge of it's placement into the overall logic so that we do not reindex it on our next row iteration
                        if len([i for i in range(potential_start_position-30,potential_start_position+30) if i in start_list]) > 0:
                            #ok so the above line just checks to see if the note in question has already been found or not. it does
                            # this by taking the potential_start_position, creating a wider window (-10,+11), and seeing if one of the notes in that window are in the logged list of start_index numbers (start_list). we create a wider window because row for row, the starting position of a note is almost definitely going to be in a different position on each row. this window is appropriately sized to account for a wide variance while still not encroaching on another, entirely seperate start position. FUCK that's intense. > 0 just checks to see if the start position has already been recorded. if it has, we just continue onward
                            potential_note_count = 0
                            iteration_number += 1
                            continue
                        else:
                            start_list.append(potential_start_position)
                            end_list.append(iteration_number)
                            row_list.append(row)
                            bottom_of_note.append(row) #we will also need a function that looks at this value for each
                            # note, then goes upward until it finds the first black pixel and then defines that as a global value to be used 
                            potential_note_count = 0 #start this back at the beginning, ready for another note
                            iteration_number += 1
                    else: # this will be triggered if the previous white pixel was either an artifact or just the edge of a note, which we don't really care about because that doesn't give us enough information about the note really
                        iteration_number += 1
                        potential_note_count = 0
        elif have_we_reached_the_notes == 'no':
            continue
        elif have_we_reached_the_notes == 'yes': ##........... i don't think this is necessary, you could just say "else, break"
            break          
    return start_list, end_list, bottom_of_note, final_img         
                    
               
 
         
                        
    


def get_slice_values(start_list, end_list, bottom_of_note):
    bottom_of_note = [i for _,i in sorted(zip(start_list,bottom_of_note))]
    start_list = sorted(start_list)
    end_list = sorted(end_list)
    index_list =[]
    window_height = 75  #this gets used in get_parameters so it knows how many rows to loop over. must be identical to the range listed below
    for i in range(0,len(start_list)): #start_list is arbitrary; all lists have the same length so we could have used any of them
        index_list.append((slice(bottom_of_note[i]-65, bottom_of_note[i]+10), slice(start_list[i], end_list[i])))
    return index_list, window_height
          
     
     
def get_parameters2(video_file, index_value, window_height):
    vidcap = cv2.VideoCapture(video_file) #read the vidya file
    success = True  ## VideoCapture outputs "success" for each frame it finds. on the last frame, it outputs "false". and in this way, iterating "while success" allows us to process all of the frames nicely. 
    count = 0  ## increases every frame and is used in calculate the average note height over all frames
    row_count_for_calculation = 0  ## in each video frame, this counts the number of row of black pixels, or in other words, how tall the note was in that particular frame. this is counted and average out over all frames to get the average height.
    local_row_count = 0 ## COMMENT IN LATER
    local_log = [] ## COMMENT IN LATER
    error_log = [] ## COMMENT IN LATER
    upper_lower_accumulation =[] ## this will be used to find the lowest and highest rows in which the note exists in each frame, or in other words, where the note is in each frame (the lower_end and upper_end will populate this list) and then from this list we will find the median values of the two ends (silenced and destination ends, excluding the middle stroke of motion) to get our actual positions for silenced and destination
    while success:
        try:
            lower_end = 0  ## for each frame, logs the lowest row in which the note was found, or the bottom of the note in each frame, if you will. this will be use to find the median lowest note, therefore the bottom.
            upper_end = 100  ## just some arbitrarily high value that will never be exceeded, same purpose as the above line.
            count += 1
            success, color_img = vidcap.read()
            retval, final_img = cv2.threshold(color_img, 35, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
            final_img = final_img[index_value]  ## we have to crop down to the window size we want but can't do it on the previous line because idk 
            #cv2.imwrite("/users/josh.flori/project/debug/0/frame{}.jpg".format(count), final_img)
            if np.sum(final_img) < final_img.size * 200: #this will make sure the code only triggers once the lights turn on since a black image, once converted, == 1530000. i've set the value a little lower just to allow for some error
                for pixel_row in range(0,window_height):  ## loop over all of the rows in the image, or window, for the note
                    if np.sum(final_img[pixel_row,:]) < 1201:
                        row_count_for_calculation += 1   ## accumulate height values to be calculated in the average
                        local_row_count += 1  ## COMMENT IN LATER
                        local_log.append('y')  ## COMMENT IN LATER
                        if pixel_row > lower_end:
                            lower_end = pixel_row
                        if pixel_row < upper_end:
                            upper_end = pixel_row
                    else: #if sum of row is NOT <12001, which means the row is white and note is NOT present
                        local_log.append('n')
                if lower_end > 0 and upper_end < 100:  ## lower and upper end will remain 0 and 100 (unchanged from defaults) if the first few frames of video for that note did not actually contain the note. that happens when the camera is initially adjusting it's iso or whatever.
                    upper_lower_accumulation.append(lower_end)
                    upper_lower_accumulation.append(upper_end)
                if local_log[0] == 'y' and 'y' in local_log[local_row_count+5:]:
                    error_log.append('1')
        except:  ## when last frame was reached it errors out
            continue
    note_height = int(row_count_for_calculation / count) +2
    lowest_row = np.max(upper_lower_accumulation)  ## this will find the lowest value, on which we add the note height and then find the median of the range, which will serve as the silenced location.
    silenced_contenders = [i for i in upper_lower_accumulation if i > lowest_row - note_height+2]  ## gets all the lowest rows from each frame where the row was lower than the lowest overall row + noteheight, which is basically just gonna give you all the bottom notes. the logic here is that almost all of these notes will be at rest, very few will be in motion, so we can just use median or mode to get the "average" silenced location. i don't think this logic is necessary to find the silenced location but who knows, lets give it a whirl. The PLUS+2 makes it so that you EXCLUDE the actual top of the note from the calculation because otherwise it may be included lol.
    silenced = int(stats.mode(silenced_contenders)[0]) -2  ##int(...[0] is required because scipy.stats.mode outputs some bullshit like this:         ModeResult(mode=array([1]), count=array([2])) so getting the int of the first part is what gets you the actual mode
    highest_row = min(upper_lower_accumulation)  ## this will find the highest value, on which we subtract the note height and then find the median of the range, which will serve as the destination location.
    destination_contenders = [i for i in upper_lower_accumulation if i < highest_row + note_height-2]  ## blablabla same logic as above no explanation needed. just doing it for destination. 
    ####### WARING!!!!!!!!!!!! THE ABOVE ASSUMES THAT A NOTE WILL BE HELD FOR A LONGER PERIOD OF TIME OVERALL THAN IT WILL BE IN MOTION THROUGH THE SPECIFIED RANGE. THAT'S THE ONLY WAY THAT GETTING THE MODE WORKS!!! 
    destination = int(stats.mode(destination_contenders)[0]) + 2
    upmotion = silenced - note_height
    downmotion = destination + note_height
    if silenced - destination < 30: # this just checks to see if the note was not actually played
         destination = 1 ## this sets the destination to some arbitrarily high, unreachable value such that it will thus never be triggered
    return silenced, destination, upmotion, downmotion, error_log, silenced_contenders, destination_contenders, upper_lower_accumulation, note_height
                 
           
        
            
###### COMPUTE VELOCITY
def compute_velocity(max_possible_inmotion_frames, velocity_count):
    resolution = 127/max_possible_inmotion_frames
    return 127 - (resolution * velocity_count) + 1



###### READ IMAGES
def get_midi_information(video_file, index_value, 
                         max_possible_inmotion_frames, silenced, 
                         upmotion, destination, downmotion, note_number,
                         iteration_number):
    temp_string='['
    tick=0
    velocity_count = 0  # +1 for each frame of inmotion footage
    current_position = 'silenced'
    vidcap = cv2.VideoCapture(video_file)
    success='true'
    debug_list =[] ##this holds evaluation (silenced,upmotion,etc) which will be manually compared against frames of video to see what the fuck is going wrong
    count=0 ##this counts the frames and returns it in the image name output for debugging
    while success:  ## vidcap.read outputs a success indicator (true/false) for whether it found a frame of video or not as well as a numpy array of RGB pixel values. Since we need black and white instead of RGB, in the line below we must first read the array back into an image by using "Image.fromarray" at which point we can then convert to black and white, then we convert back into an array and take the cropped values to get just the note we want
        try: ## the reason we need this is because for whatever reason "vidcap.read" which output a false signal at the very end of the video once it fails to find a new frame, so we just need to avoid that error.
    	    success, color_img = vidcap.read()
    	    retval, final_img = cv2.threshold(color_img, 35, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
            final_img = final_img[index_value]  
            #cv2.imwrite("/users/josh.flori/project/debug/"+str(iteration_number)+"/frame{}.jpg".format(count), final_img) ## this prints out images to folder for debugging
            #print(np.sum(final_img))
            if np.sum(final_img) < final_img.size * 200: #this will make sure the code only triggers once the lights turn on since a black image, once converted, == 1530000. i've set the value a little lower just to allow for some error
                if current_position == 'silenced':
                    if np.sum(final_img[upmotion,:]) < 1201: ## "if note has started moving upward".... 77 marks the first movement row from bottom, grey background = 200, black note = 0 with some error, so <10 means the note has reached that position in space and therefore is in motion.
                        velocity_count = velocity_count + 1  # add 1 frame of velocity
                        tick=tick+3  # add 1 tick
                        current_position = 'upmotion' 
                        debug_list.append('{}_upmotion'.format(count))
                    else:
                        tick=tick+3
                        debug_list.append('{}_silenced'.format(count))
                elif current_position == 'upmotion':
                    if np.sum(final_img[destination,:]) < 1201: ## "if note has reached destination".... 42 marks the first row needed to be reached for the note to be activated, or reach it's "destination" 
                        velocity_count = velocity_count+1
                        velocity = compute_velocity(max_possible_inmotion_frames, velocity_count)
                        tick=tick+3
                        current_position = 'destination'  ## it has reached the destination, resolve the motion
                        temp_string = temp_string + ('midi.NoteOnEvent(tick='+str(int(round(tick)))+
        	                                          ', channel=0, data=['+str(note_number)+', '+str(velocity)+']),')
                        velocity_count = 0 ## reset to 0
                        tick = 0  ## we have logged the midi information for the note activation and now the tick information must be reset so that we can track how many ticks it is until the next event, which will be the release of this note which has just been activated
                        debug_list.append('{}_destination'.format(count))
                    elif np.sum(final_img[silenced,:]) < 1201:  ## "if note went back down"
                        current_position = 'silenced'
                        velocity_count=0
                        tick = tick+3
                        debug_list.append('{}_silenced'.format(count))
                    else: # if note is still in motion
                        velocity_count = velocity_count+1 ## if note still in motion upward
                        tick = tick+3
                        debug_list.append('{}_upmotion'.format(count))
                elif current_position == 'destination':
                    if np.sum(final_img[downmotion,:]) < 1201:  ## if note has started moving downward
                        tick = tick+3
                        current_position = 'downmotion'
                        debug_list.append('{}_downmotion'.format(count))
                    else: # if note is still sitting at it's destination
                        tick = tick+3
                        debug_list.append('{}_destination'.format(count))
                elif current_position == 'downmotion':
                    if np.sum(final_img[silenced,:]) < 1201:  ## "if note has reached the bottom and is now silenced" where row 83 = the bottom
                        tick = tick+3
                        current_position = 'silenced'
                        temp_string = temp_string + ('midi.NoteOnEvent(tick='+str(int(round(tick)))+', channel=0, data=['+str(note_number)+', 0]),') ## 0 velocity means the note is silenced
                        debug_list.append('{}_silenced'.format(count))
                        tick = 0
                    else: # if note is still in motion downward
                        tick = tick+3
                        debug_list.append('{}_downmotion'.format(count))
                count +=1
        except: ## when you finish processing the final frame of the video it errors out
            if len(temp_string) == 1: ## if not never moved (wasn't played) and nothing was appended
                temp_string = ''
            else:
                temp_string = temp_string[:len(temp_string)-1] #gets rid of trailing comma
                temp_string = temp_string + '],' # close out the midi requirements for that track
            break
    return temp_string, debug_list
            



##### change directory
os.chdir('/users/josh.flori/project')
### the following is used for midi string concatenation. 
temp_string=''
debug_dict={}
midi_string = ''
### get the note positions
start_list, end_list, bottom_of_note, final_img = find_note_positions('third.mp4')
### now get the indexlist
index_list, window_height = get_slice_values(start_list, end_list, bottom_of_note) 
### so now we loop over all of the notes in the video in question...
for note in range(0,18): ## loops from 0-19
    note_number = note+53
    silenced, destination, upmotion, downmotion, error_log, silenced_contenders, destination_contenders, upper_lower_accumulation, note_height  = get_parameters2('third.mp4', index_list[note], window_height)
    if len(error_log) > 10:
        print('POTENTIAL ERROR FOUND')
    print(silenced, upmotion, destination, downmotion)
    print(index_list[note])
    temp_string,debug_list = get_midi_information('third.mp4', index_list[note], 33, silenced, upmotion, destination, downmotion, note_number, note)
    debug_dict[note]=debug_list
    midi_string = midi_string + temp_string

    
os.chdir('/Users/josh.flori')
file = open('third.txt','w') 
file.write(str(midi_string)) 
file.close()


