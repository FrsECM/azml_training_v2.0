# Running Jobs

## Introduction
In this part, we'll learn how to create jobs in AzureML.
For that, we'll need environment to be already created.
Especially **torch_cpu**.

## Create your developpment tree
First of all, we'll have to structure our code.
It is important in order to be able to relaunch it 6 month after for example....

Create a new folder **jobs** in your repository containing a "download_mnist" directory.
In this folder we'll create :
- A EntryScript - **download_mnist.py**
- A YmlLaunch - **download_mnist.yaml**
- [Optional] A ShellLaunch - **download_mnist.sh**

<img src="../assets/img/00053 - Jobs - Structure.png" alt="drawing" width="300"/>

Now, we are ready to start dev, but first, we'll do a short introduction about **WSL**, **Compute Instance** vs **Compute Clusters**.

## WSL / Computer Instance / Compute Cluster
**WSL** is a VM that is running a linux kernel in your windows Machine.<br>
A **compute instance** is a machine that can be use only by one user, it is schedulable in order to start and stop automatically and you can developp directly on it.<br>
A **compute cluster**, is a machine that can be use by all users, it is automatically scalable and you pay only the time of computation.<br>

Bellow a short summary of their capabilities :
|                      | WSL   |Compute Instance | Compute Cluster |
|----------------------|-------|-----------------|-----------------|
|MultiNode             |       |                 | &check;         |
|MultiUser             |       |                 | &check;         |
|AutoScale             |       |                 | &check;         |
|RealTime Debug        |&check;| &check;         |                 |
|Pipeline Compatibility|       | &check;         | &check;         |
|Launch & Forget       |       |                 | &check;         |

What you can see from this table, is that it is very convenient to :
- Use **WSL** for debug and dev
- Use **Compute Instance** for debug and dev **if you need specific hardware (GPU).**
- Use **Compute Cluster** for Execution

We'll start by creating our script on our machine with wsl.

# Download MNIST - **Local**

First, we have to make sure we have locally all the libraries we'll use in our job...

<div style="background-color:#0000EE22">
IN WSL<br>
</div>

```bash
# We install Pytorch CPU Version first...
(azureml_training) >> pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
```

## Create the EntryScript
<div style="background-color:#0000EE22">
IN WSL<br>
>> jobs/download_mnist/download_mnist.py
</div>

```python
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
```

In order to check that everything is working well, we can put a debugpoint on the line 48 **images = selection[clsName]**<br>
<img src="../assets/img/00054 - Download_Labels_debug.png" alt="drawing" width="800"/>

If you let the script running, you'll see that it created a directory **data** containing images of mnist digits as RGB images.

## Create the YmlLaunch
Now we have a running script locally, we'll have to explain azureML how to run it. For that, we'll have to say him :<br>
- The **compute** machine where to run
- The **environment** to use
- Where is the **code**
- What are **inputs** and **outputs** of your script
- What is the **command** to start your script.

This is the rôle of the YmlLaunch file.

<div style="background-color:#0000EE22">
IN WSL<br>
>> jobs/download_mnist/download_mnist.yaml
</div>

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json

# The name that will be displayed in your azureml workspace
experiment_name: MNIST_Download
display_name: Download MNIST Dataset

# Where is your code base
code: ../../ # Relative from yaml file in order to get the root directory.
# The command to launch with your job
command: >-
  python jobs/download_mnist/download_mnist.py
  --data_dir ${{outputs.data_dir}} 
  --n_max ${{inputs.n_max}} 

# Inputs and Outputs
inputs:
  n_max: 1000

# IMPORTANT
# Here you see that the path is azureml://datastores/<datastore_name>/paths/<path>
# <path> can be empty and it will mount a folder at the root of the datastore.
outputs:
  data_dir:
    type: uri_folder
    path: azureml://datastores/mnist_data_f296849/paths/
    mode: rw_mount

# Environment and Compute
environment: azureml:torch_cpu@latest
compute: azureml:devtracpucluster
```

## Run Job
Now, you can run your job this way :
```bash
# Create the job from yaml file.
az ml job create \
    --file jobs/download_mnist/download_mnist.yaml \
    --subscription $AZUREML_SUBSCRIPTION \
    --resource-group $AZUREML_RESSOURCE_GROUP \
    -w $AZUREML_WORKSPACE_NAME --verbose
```

When it will be run, you'll be able to see it in AzureML Workspace...

<img src="../assets/img/00055 - Download_Labels_job.png" alt="drawing" width="800"/>


## Train MNIST
Once done, you can do the same in order to train MNIST.<br>
In order to do it, you'll need to install libaicv.
```bash
# We install Pytorch CPU Version first...
(azureml_training) >> pip install environments/libaicv_env/libaicv-0.2.7+2.g6b73980-py3-none-any.whl
```

The entrypoint will be a little different :
<div style="background-color:#0000EE22">
IN WSL<br>
>> jobs/train_mnist/train_mnist.py
</div>

```python
from libaicv.classification import ClassificationDataset,ResNetClassifier,ClassificationTrainer
from libaicv.core import ACCELERATOR
import os,argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir',default=None)
parser.add_argument('--output_dir',default="results")
parser.add_argument('--epochs',type=int,default=5)
parser.add_argument('--batch_size',type=int,default=4)
parser.add_argument('--learning_rate',type=float,default=1e-4)
parser.add_argument('--scheduler_step',type=int,default=2)
parser.add_argument('--scheduler_gamma',type=float,default=0.5)

def main(data_dir:str,output_dir:str,epochs:int=5,batch_size:int=3,learning_rate:float=1e-4,scheduler_step:int=2,scheduler_gamma:float=0.5):
    #######################################
    # We Create training...
    #######################################    
    dataset = ClassificationDataset.fromFolder(rootFolder=data_dir,size=(28,28))
    dataset.split()
    model = ResNetClassifier(nChannels=3,clsCount=dataset.clsCount)
    # We set the trainer and all it's dependancies...
    trainer = ClassificationTrainer(model,root_logdir=output_dir)
    trainer.attr_hparams.Lr0 = learning_rate
    trainer.attr_logging.logger_azureml = True
    trainer.set_StepScheduler(scheduler_step,scheduler_gamma)
    # We launch training job
    trainer.fit(dataset,batch_size=batch_size,epochs=epochs,accelerator=ACCELERATOR.CUDA_AMP)



if __name__=='__main__':
    # We parse our Arguments
    args = parser.parse_args()
    #######################################
    main(**vars(args))  
    print('Terminé !')

```

As an exercise, you can adapt the yaml file in order to fit with this python file and run your job.
Be carefull, for this job you'll need to change **compute** and **environment**.


---
[<< Back](../README.md)