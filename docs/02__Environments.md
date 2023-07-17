# Environment

## Introduction
When we will work with AzureML, the computation will not be done on our local machine.
We'll need to send the job to a compute cluster.

<img src="../assets/img/00051 - AzureML Pipeline Execution Schema.png" alt="drawing" width="400"/>

**But how is this job aware of the libraries you'll use when running your code ?**

It is not, for that, we need to declare a **fresh** environment.

## Create the Environment
The environement is the image of what will be the environment when we'll run our pipeline. There we'll declare our libraries and dependancies.<br>

The easiest way to create an environment is to use a **DockerFile**.<br>
For example, our base Dockerfile with GPU support will look like that :<br>

<div style="background-color:#0000EE22">
IN WSL<br>
>> environments/torch_cpu/Dockerfile
</div>

```docker
FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
###### We set all the michelin Stuffs
# In Michelin, we have a custom artifactory
COPY pip.conf pip.conf
ENV PIP_CONFIG_FILE  'pip.conf'
# In Michelin, we have a proxy
ENV NO_PROXY='artifactory.michelin.com,gitlab.michelin.com'
ENV HTTP_PROXY="http://proxy-weu.aze.michelin.com:80"
ENV HTTPS_PROXY="http://proxy-weu.aze.michelin.com:80"

# We install our dependancies (force CPU for pytorch)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
```

In order to declare the environment, We'll run this script with the right parameters : **environments/create_environment.py**<br>

<div style="background-color:#0000EE22">
IN AZUREML WORKSPACE<br>
>> environments/create_environment.py
</div>

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
#import required libraries for environments examples
from azure.ai.ml.entities import Environment, BuildContext
import argparse
import os

SUBSCRIPTION = os.getenv('AZUREML_SUBSCRIPTION')
RESSOURCE_GROUP = os.getenv('AZUREML_RESSOURCE_GROUP')
WORKSPACE = os.getenv('AZUREML_WORKSPACE_NAME')

parser = argparse.ArgumentParser()
parser.add_argument('--environment',help='name of the environment to build...',choices=['torch_cpu','libaicv_env'],default="libaicv_env")

if __name__=='__main__':
    args = parser.parse_args()
    #################################
    ### Connect to the workspace
    #################################
    credential = DefaultAzureCredential()
    ml_client = MLClient(credential=credential,subscription_id=SUBSCRIPTION,resource_group_name=RESSOURCE_GROUP,workspace_name=WORKSPACE)
    #################################
    ### Create the docker Context
    #################################
    # We copy sources to env rootdir
    env_root_dir = f"environments/{args.environment}"
    # We create the env    
    env_docker_context = Environment(
        build=BuildContext(path=env_root_dir,dockerfile_path="Dockerfile"),
        name=f"{args.environment}",
        description="Environment created from a Docker context.",
    )
    ml_client.environments.create_or_update(env_docker_context)
```

The advantage of this method is that you can include whatever you want in your Dockerfile.

## Exercises

As an exercise, we'll create our two first environment :<br>
- torch_cpu
- libaicv_env

When the environments will be created, we'll normally see it :

<img src="../assets/img/00052 - Environment Created.png" alt="drawing" width="400"/>

As an exercise, you can add a third environment : 
- torch_gpu_your_id


---
[<< Back](../README.md)