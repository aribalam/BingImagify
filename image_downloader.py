import os
import shelve
import urllib.request as urlutil
import json
from urllib.error import URLError

# The URL from which the image gets extracted
base_url = 'https://www.bing.com'
url_feed = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'

# The destination directory where the images gets saved
image_dest_dir = os.path.expanduser('~/Pictures/BingWallpapers')

# The shelve data for keeping track of images getting displayed
shelve_filename = 'info'
image_basename = 'IMG_'
shelve_dir_path = os.path.join(image_dest_dir, 'Info')
shelve_file_path = os.path.join(shelve_dir_path, shelve_filename)


# Extracts the image url from the bing json feed
def get_image_url(url):
    try:
        jsondata = urlutil.urlopen(url)
        handler = json.loads(jsondata.read().decode())
        image_base_address = handler['images'][0]['url']
        image_full_address = base_url + image_base_address
    except URLError as e:
        print(e.reason)
        print(e.args)
        return None

    return image_full_address


# Continue only when the info file exist
if os.path.exists(shelve_file_path):

    # Opens the shelve file and get the previously downloaded image url
    info_file = shelve.open(shelve_file_path)
    previous_url = info_file['previous_url']
    # image_index gives the index to be given to the image
    image_index = info_file['image_index']

    image_url = get_image_url(url_feed)

    # proceed only when the image url found is not the same as the previous one
    # to avoid downloading of duplicate images
    if image_url is not None and not previous_url == image_url:
        # Create the filename for the new image
        image_name = image_basename + str(image_index) + ".jpg"
        image_full_address = os.path.join(image_dest_dir, image_name)
        urlutil.urlretrieve(image_url, image_full_address)

        # update the parameters in the info file
        info_file['previous_url'] = image_url
        info_file['image_index'] = image_index + 1
        
    info_file.close()