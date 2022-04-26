import torch
import numpy as np
from matplotlib import pyplot as plt
import copy
from skimage.transform import resize

import h5py
import numpy as np
from PIL import Image
import shutil
from scipy.io import loadmat
import glob
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from typing import List, Tuple

import h5py
import scipy.io as io
import PIL.Image as Image
import numpy as np
import os
import glob
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter 
import scipy
import json
from matplotlib import cm as CM
# from model import CSRNet
import torch
import scipy.spatial

img_path = '/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/NWPU-Crowd-Sample-Code/NWPU-Crowd/images/*.jpg'
mat_path = 'NWPU/mats/*.mat'
images = {}
mats = {}

for name in glob.glob(img_path):
    key = int(name.replace('/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/NWPU-Crowd-Sample-Code/NWPU-Crowd/images/','').replace('.jpg',''))
    images[key] = name

for name in glob.glob(mat_path):
    key = int(name.replace('NWPU/mats/','').replace('.mat',''))
    mats[key] = name

images = dict(sorted(images.items()))
mats = dict(sorted(mats.items()))

def _resize(image, matrix):

    im = Image.open(image)
    w, h = im.size
    im = im.resize((224,224))
    new_pts = np.zeros(matrix.shape)
    for i, pt in enumerate(matrix):
        new_pts[i][0] = pt[0]*(224/w)
        new_pts[i][1] = pt[1]*(224/h)
    
    return im , new_pts

#this is borrowed from https://github.com/davideverona/deep-crowd-counting_crowdnet
def gaussian_filter_density(gt):
    # print(gt.shape)
    density = np.zeros(gt.shape, dtype=np.float32)
    gt_count = np.count_nonzero(gt)
    if gt_count == 0:
        return density

    pts = np.array(list(zip(np.nonzero(gt)[1], np.nonzero(gt)[0])))
    # print('ponts shape is',pts.shape)
    leafsize = 2048
    # build kdtree
    tree = scipy.spatial.KDTree(pts.copy(), leafsize=leafsize)
    # query kdtree
    distances, locations = tree.query(pts, k=4)

    print('generate density...')
    for i, pt in enumerate(pts):
        pt2d = np.zeros(gt.shape, dtype=np.float32)
        pt2d[pt[1],pt[0]] = 1.
        if gt_count > 1:
            sigma = (distances[i][1]+distances[i][2]+distances[i][3])*0.1
        else:
            sigma = np.average(np.array(gt.shape))/2./2. #case: 1 point
        density += scipy.ndimage.filters.gaussian_filter(pt2d, sigma, mode='constant')
    print('done.')
    return density

im = []
mat = []
for i in range(1425, 3610):
    im.append(images[i])
    mat.append(mats[i])

for imm, ma in zip(im, mat):
    print(imm, ma)
    m = io.loadmat(ma)['annPoints']
    img = plt.imread(imm)
    
    imag, gt = _resize(imm, m)
    k = np.zeros((imag.size[1],imag.size[0]))
    # print(len(gt))
    for i in range(0,len(gt)):
        # print(i)
        if int(gt[i][1])<imag.size[1] and int(gt[i][0])<imag.size[0]:
            k[int(gt[i][1]),int(gt[i][0])] = 1
    try:
        k = gaussian_filter_density(k)
    except:
        continue
    with h5py.File('NWPU_density/'+imm.replace('/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/NWPU-Crowd-Sample-Code/NWPU-Crowd/images/','').replace('.jpg','')+'.h5', 'w') as hf:
            hf['density'] = k

img = plt.imread(im[0])

new_pts = np.zeros(io.loadmat(mat[0])['annPoints'].shape)
w, h = Image.open(im[0]).size
print(w,h)
for i, pt in enumerate(io.loadmat(mat[0])['annPoints']):
    new_pts[i][0] = pt[0]*(224/w)
    new_pts[i][1] = pt[1]*(224/h)
plt.imshow(resize(img, (224, 224)))
plt.plot(224, 224, "og", markersize=2)  # og:shorthand for green circle
plt.scatter(new_pts[:,0], new_pts[:,1], marker="x", color="red", s=20)
plt.show()

groundtruth = np.asarray(k)
print(groundtruth.shape)
plt.imshow(groundtruth,cmap=CM.jet)

path = '/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/objects_counting_dmap/NWPU_density/*h5'
h5s = []
not_in = [1424, 1557, 1558, 1920, 1926, 2981, 3584]
for i in range(1001,3603):
    path = f"/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/objects_counting_dmap/NWPU_density/{str(i)}.h5"
    if i in not_in:
        continue
    else:
        pass
    print(path)
    with h5py.File(path,'r') as f:
        x = np.asarray(f['density'])
        h5s.append(x)