import numpy as np
import time
import haralicklib
import cv2
import multiprocessing as mp

test_nbr = 100

pool = mp.Pool(mp.cpu_count())
haralick_times = np.array([])

i = 0
while i < test_nbr:
    t1 = time.time()
    image = cv2.imread("testy.png")
    features = haralicklib.compute_haralick(image, pool)
    t2 = time.time()
    haralick_times = np.append(haralick_times, t2 - t1)
    print i, "  time: ", t2-t1
    i = i + 1

np.save("haralick_times.npy", haralick_times)
print "AVG of Haralick computation: ", np.average(haralick_times), "\n\n"

