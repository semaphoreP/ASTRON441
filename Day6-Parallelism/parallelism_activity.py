"""
Parallelism activity. After generating the images in the notebook, this script will process each image.
The code below shows how to run it on a single image.
"""

import time 
import multiprocessing
import numpy as np
import astropy.io.fits as fits
import scipy.ndimage as ndimage

# some bookkeeping information on the files
fileformat = "fake_{0}x{1}_{2}.fits"
ny = 1000
nx = 1000

def process_image(frame, filtersize=50):
    """
    Run a high-pass filter on the data. 
    Remove the low spatial frequency (i.e., smooth features) in the image

    Args:
        frame (np.array): a 2-D image to be processed
        fitersize (int): the size of the filter. Features smaller than the filtersize will be preserved

    Returns:
        processed_frame (np.array): a 2-D image after processing
    """
    # run a median filter to smooth the image
    frame_smooth = ndimage.median_filter(frame, filtersize)

    processed_frame = frame - frame_smooth

    return processed_frame

###########################################
# an example of running this on one image #
###########################################

start = time.time()

with fits.open(fileformat.format(ny, nx, 0)) as hdulist:
    data = hdulist[0].data

    filt_data = process_image(data)

single_time = time.time() - start
print('1 image/1 process: {:.2f} seconds'.format(single_time))



#### Activity #########################################
# write and time some code that does this in parallel. 
# How does the performance increase as you increase the number of processes you use?
# we recommend you use multiprocessing pool for this task

if __name__ == "__main__":
    # may need to put code in here (Especially Mac OS users)