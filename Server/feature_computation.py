import time
import os
import haralicklib
import cv2
import multiprocessing as mp

start_flag = '/dev/shm/breise18/flag.txt'
end_flag = '/dev/shm/breise18/end.txt'
im_path = '/dev/shm/breise18/testy.png'
feat_path = '/dev/shm/breise18/features.npy'
random_path = '/dev/shm/breise18/haralicklib.pyc'
pool = mp.Pool(mp.cpu_count())

print "calculation running..."

while True:
    while True:
        if os.path.isfile(start_flag):
            break
        time.sleep(0.01)
    if os.path.isfile(end_flag):
        os.remove(feat_path)
        os.remove(im_path)
        os.remove(start_flag)
        os.remove(end_flag)
        os.remove(random_path)
        pool.close()
        break
    image = cv2.imread(im_path)
    features = haralicklib.compute_haralick(image, pool)
    features.dump(feat_path)
    os.remove(start_flag)
