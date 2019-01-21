import os
import shelve
import random

# The destination directory where the images gets saved
image_dest_dir = os.path.expanduser('~/Pictures/BingWallpapers')

# The shelve for keeping track of images getting displayed
shelve_filename = 'info'
terminal_command = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri '

file_formats = ['.jpg', '.JPG', '.jpeg']

os.chdir(image_dest_dir)

# Creating a new info file if it doesnt exist
if not os.path.exists(os.path.join('Info', shelve_filename)):
    os.makedirs('Info')
    info_file = shelve.open(os.path.join('Info', shelve_filename))
    info_file['image_index'] = 0
    info_file['previous_url'] = 'null'
    info_file['curr_image'] = 'null'
    info_file.close()

# getting the filename of the current wallpaper
info_file = shelve.open(os.path.join('Info', shelve_filename))
curr_image = info_file['curr_image']

# retrieving list of images from the destination directory
images_list = [file for file in os.listdir(image_dest_dir) if os.path.splitext(file)[1] in file_formats]
images_list.sort()

next_image = 'null'
if not curr_image == 'null':    # making sure that the name of the current image exists in the shelve file
    next_image = images_list[(images_list.index(curr_image) + 1) % len(images_list)]
elif len(images_list) > 0:      # if there is no current image saved, take the first image from the image list
    next_image = images_list[0]

# updating the data in the info file
if not next_image == 'null':
    info_file['curr_image'] = next_image
    info_file.close()

# change the wallpaper using the terminal command
os.system(terminal_command + os.path.join(image_dest_dir, next_image))
