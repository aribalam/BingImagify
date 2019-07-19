import os
import shelve
import random
import pickle

# The destination directory where the images gets saved
image_dest_dir = os.path.expanduser('~/Pictures/BingWallpapers')

# The shelve for keeping track of images getting displayed
shelve_filename = 'info'
terminal_command = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri '

file_formats = ['.jpg', '.JPG', '.jpeg']

def initInfo():
    # Creating a new info file if it doesnt exist
    if not os.path.exists(os.path.join('Info', shelve_filename)):
        info_file = open(os.path.join('Info', shelve_filename), 'wb')
        info = {
            'image_index': 0,
            'previous_url': '',
            'curr_image': '',
        }
        pickle.dump(info, info_file)   
        info_file.close()


def getInfo():
    # getting the filename of the current wallpaper
    info_file = open(os.path.join('Info', shelve_filename), 'rb')
    info = pickle.load(info_file)
    info_file.close()
    return info


def writeInfo(info):
    info_file = open(os.path.join('Info', shelve_filename), 'wb')
    pickle.dump(info, info_file)
    info_file.close()

# Checking or requireed directories and creating if not present
if not os.path.exists(image_dest_dir):
    os.makedirs(image_dest_dir)

os.chdir(image_dest_dir)

if not os.path.exists(os.path.join(image_dest_dir, 'Info')):
    os.makedirs('Info')

initInfo();

info = getInfo()
curr_image = info['curr_image']

# retrieving list of images from the destination directory
images_list = [file for file in os.listdir(image_dest_dir) if os.path.splitext(file)[1] in file_formats]
images_list.sort()

next_image = ''
if not curr_image == '':    # making sure that the name of the current image exists in the shelve file
    next_image = images_list[(images_list.index(curr_image) + 1) % len(images_list)]
elif len(images_list) > 0:      # if there is no current image saved, take the first image from the image list
    next_image = images_list[0]

# updating the data in the info file
if not next_image == '':
    info['curr_image'] = next_image
    writeInfo(info)

# change the wallpaper using the terminal command
os.system(terminal_command + os.path.join(image_dest_dir, next_image))
