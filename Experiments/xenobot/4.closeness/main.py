import os, shutil, re
import numpy as np
np.random.seed(1)
import lxml.etree as etree
child = etree.SubElement
import utilities

def safe_mkdir(dir_name):
    try:
        shutil.rmtree(dir_name, ignore_errors=True)
        os.mkdir(dir_name)
    except Exception:
        pass

safe_mkdir("data")
x = 100; y = 10; z = 10
world = np.zeros([z,y,x], dtype=int)
world[0,9,12] = 5
world[0,9,14] = 5
world[0,9,99] = 5

body = np.load("assets/handes.npy")
body = np.swapaxes(body, 0,2)
world[:,:,:10] = body[::-1,:,:]

safe_mkdir(f"data")
shutil.copy("base.vxa", f"data/base.vxa")

body_flatten = world.reshape([z,-1])

root = etree.Element("VXD")

# Main Structure and PhaseOffset
structure = child(root, "Structure")
structure.set('replace', 'VXA.VXC.Structure')
structure.set('Compression', 'ASCII_READABLE')
child(structure, "X_Voxels").text = str(x)
child(structure, "Y_Voxels").text = str(y)
child(structure, "Z_Voxels").text = str(z)
data = child(structure, "Data")
print(body_flatten)
for i in range(body_flatten.shape[0]):
    layer = child(data, "Layer")
    str_layer = "".join([str(c) for c in body_flatten[i]])
    layer.text = etree.CDATA(str_layer)

with open(f"data/robot.vxd", 'wb') as file:
    file.write(etree.tostring(root))
