# This script will download mnist dataset in a filesystem...
import argparse
import torchvision
import os
import shutil
from PIL import Image as PIL_Image
import numpy as np
from tqdm import tqdm
from tempfile import TemporaryDirectory

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir',type=str,default='../data/mnist',help='directory containing datas')
parser.add_argument('--n_max',type=int,default=100,help='directory containing datas')
parser.add_argument('--seed',type=int,default=42,help='directory containing datas')

def main(data_dir:str,n_max:int,seed:int=42):
    """Will download MNIST 

    Args:
        data_dir (str): Download directory
        n_max (int): Nmax
        seed (int, optional): _description_. Defaults to 42.
    """
    with TemporaryDirectory() as tmp_dir:
        # We download MNIST in a temp directory...
        mnist = torchvision.datasets.MNIST(root=tmp_dir,train = True,download=True)
        # We'll take n_max samples per classes
        NClasses = len(mnist.classes)
        indices = np.arange(len(mnist))
        np.random.seed(seed)
        np.random.shuffle(indices)
        selection = {clsName:[] for clsName in mnist.classes}
        for i in tqdm(indices,desc="Select Datarows"):
            img_pil,clsID = mnist[i]
            clsName = mnist.classes[clsID]
            if len(selection[clsName])<n_max:
                # We convert in RGB (optionnal)
                selection[clsName].append(img_pil.convert('RGB')) 
            if sum([len(indices) for indices in selection.values()])==n_max*NClasses:
                break
        print('Selection of datarow is Completed !')
        # When selection is done, we'll download images in the destination directory...
        shutil.rmtree(data_dir,ignore_errors=True)
        os.makedirs(data_dir,exist_ok=True)
        for clsName in selection:
            dest_dir = os.path.join(data_dir,clsName)
            os.makedirs(dest_dir,exist_ok=True)
            images = selection[clsName]
            for i,img in tqdm(enumerate(images),total=len(images),desc=f"Download {clsName}"):
                im_name = f"{clsName}_{i}.jpg"
                im_path = os.path.join(dest_dir,im_name)
                img:PIL_Image
                img.save(im_path)


if __name__=='__main__':
    args = parser.parse_args()
    main(**vars(args))