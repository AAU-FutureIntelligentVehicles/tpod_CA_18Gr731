import numpy as np
import mahotas


def slide_window_helper(img, window_size=[64, 64]):
    window_size_x = window_size[0]
    window_size_y = window_size[1]
    x_windows = img.shape[0]//window_size_x
    y_windows = img.shape[1]//window_size_y

    window_list = []
    for j in range(x_windows):
        for i in range(y_windows):
            window = [i*window_size_x, j*window_size_y, (i+1)*window_size_x, (j+1)*window_size_y, j, i]
            window_list.append(window)

    return window_list


def _ch(roi):
    return mahotas.features.haralick(roi).mean(0)[:5]


def compute_haralick(crop_img, pool, windows=None):
    window_size = 64
    crop_img = np.array(crop_img)
    if (windows == None):
        windows = slide_window_helper(crop_img)
    rois = []
    for window in windows:
        roi = crop_img[window[1]:window[3], window[0]:window[2], :3]
        rois.append(roi)
    haralick_features = pool.map(_ch, rois)
    dims = crop_img.shape
    scaling_factor = [0.05423693486427112, 2258.078377174232,0.986424403324001,9114.763475900238,0.42569913950248545]

    window_countx = dims[0]//window_size
    window_county = dims[1]//window_size
    haralick_arr = np.zeros((window_countx, window_county, 5))
    for window, result in zip(windows, haralick_features):
        haralick_arr[window[4], window[5]] = result
    array = haralick_arr / scaling_factor
    # print(array)
    return array.astype(np.float32)
