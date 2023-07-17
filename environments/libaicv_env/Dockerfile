FROM mcr.microsoft.com/azureml/curated/acpt-pytorch-2.0-cuda11.7
# BE CAREFUL
# This image will only work with T4 GPUs (non NCs) like explained in this page :
# https://learn.microsoft.com/en-us/azure/machine-learning/resource-azure-container-for-pytorch?view=azureml-api-2
# We add the extra requirements to the container
# We add the extra requirements to the container
COPY requirements.txt .
COPY libaicv-0.2.7+2.g6b73980-py3-none-any.whl .
RUN pip install -r requirements.txt
RUN pip install libaicv-0.2.7+2.g6b73980-py3-none-any.whl