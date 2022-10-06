import time 
import multiprocessing
import numpy as np
import astropy.io.fits as fits
import scipy.ndimage as ndimage


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



start = time.time()

# an example of running this on one image
with fits.open(fileformat.format(ny, nx, 0)) as hdulist:
    data = hdulist[0].data

    filt_data = process_image(data)

single_time = time.time() - start
print('1 image/1 process: {:.2f} seconds'.format(single_time))



#### Activity:
# write and time some code that does this in parallel. How does the performance increase as you increase the number of processes you use?
# we recommend you use multiprocessing pool for this task

if __name__ == "__main__":
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)


    start = time.time()


    # start the jobs running in parallel
    pool_jobs = []
    for i in np.arange(25):
        img_indices = [i] # only do one image per job
        job = pool.apply_async(process_image_loop, args=(img_indices,))
        pool_jobs.append(job)

    for job in pool_jobs:
        result = job.get() 

    # save the 
    parallelized_time = time.time() - start


    print('25 images/{} processes: {:.2f} seconds'.format(num_processes, parallelized_time))

"""
For me, 1 image took 12.65 seconds. 25 images (using 8 processes) took 89.66 seconds. Extrapolating for 1 image, we would expect this to take 316 seconds on 1 core. 
This is a 3.5x speedup. We don't get the full 8x speedup due to many reasons (overheads, Intel CPU architecture, etc..)
"""