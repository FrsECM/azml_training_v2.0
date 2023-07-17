FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
###### We set all the michelin Stuffs
COPY pip.conf pip.conf
ENV PIP_CONFIG_FILE  'pip.conf'
ENV NO_PROXY='artifactory.michelin.com,gitlab.michelin.com'
ENV HTTP_PROXY="http://proxy-weu.aze.michelin.com:80"
ENV HTTPS_PROXY="http://proxy-weu.aze.michelin.com:80"

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
