# import the necessary packages
import numpy as np
import base64
import sys
from scipy.ndimage import zoom
from skimage.transform import resize

def resize_image(im, new_dims, interp_order=1):
    """
    Resize an image array with interpolation.

    Parameters
    ----------
    im : (H x W x K) ndarray
    new_dims : (height, width) tuple of new dimensions.
    interp_order : interpolation order, default is linear.

    Returns
    -------
    im : resized ndarray with shape (new_dims[0], new_dims[1], K)
    """
    if im.shape[-1] == 1 or im.shape[-1] == 3:
        im_min, im_max = im.min(), im.max()
        if im_max > im_min:
            # skimage is fast but only understands {1,3} channel images
            # in [0, 1].
            im_std = (im - im_min) / (im_max - im_min)
            resized_std = resize(im_std, new_dims, order=interp_order, mode='constant')
            resized_im = resized_std * (im_max - im_min) + im_min
        else:
            # the image is a constant -- avoid divide by 0
            ret = np.empty((new_dims[0], new_dims[1], im.shape[-1]),
                           dtype=np.float32)
            ret.fill(im_min)
            return ret
    else:
        # ndimage interpolates anything but more slowly.
        scale = tuple(np.array(new_dims, dtype=float) / np.array(im.shape[:2]))
        resized_im = zoom(im, scale + (1,), order=interp_order)
    return resized_im.astype(np.float32)

def base64_encode_image(ary):
    # base64 encode the input NumPy array
    return base64.b64encode(ary).decode("utf-8")

def base64_decode_image(ary, dtype, shape):
    # if this is Python 3, we need the extra step of encoding the serialized NumPy string as a byte object
    if sys.version_info.major == 3:
        ary = bytes(ary, encoding="utf-8")

    # convert the string to a NumPy array using the supplied data type and target shape
    ary = np.frombuffer(base64.decodebytes(ary), dtype=dtype)
    ary = ary.reshape(shape)

    # return the decoded image
    return ary