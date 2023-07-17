# AzureML Training - Repository

This repo contains ressources that are necessary for AzureML SDK v2.0 Training.

<img src="assets/img/00060 - Global Schema AzureML.png" alt="drawing" width="800"/>

**Why this migration to version 2.0 ?**<br>
With version 2, it's easier to developp without compute instance.
It can be very interesting because compute instances are sometimes unstable.

## PreRequirements
It is necessary to have a working WSL environment in order to use this repository.<br>
For that you can :
- Use Michelin [Documentation](https://michelingroup.sharepoint.com/sites/ExplorationManufacturing/SitePages/WSL---Installation.aspx) (Michelin Computer)
- Use Microsoft [Documentation](https://learn.microsoft.com/fr-fr/windows/wsl/install) (Other)

The experience will be better if you have :<br>
- VSCode installed and setup with WSL  - [Documentation](https://code.visualstudio.com/docs/remote/wsl)
- Miniconda installed and setup in wsl

## Installation
Create an environment and install dependancies
```bash
conda create -n azml_training python=3.8 openssl=1.1.1n
conda activate azml_training
pip install -r requirements.txt
```

Add env variable to conda env :
```bash
conda env config vars set AZUREML_SUBSCRIPTION='<TENANT-ID>'
conda env config vars set AZUREML_RESSOURCE_GROUP='<RESSOURCE-GROUP>'
conda env config vars set AZUREML_WORKSPACE_NAME='<AML-WORKSPACE>'
conda env config vars list
```
The aim of all theses env variable is to target the right azureml workspace during your training session.<br>
All theses information are available in your AML workspace url.

## Data and Storages
In this part we'll talk about how to use Data in AzureML.

---
[==> Continue](docs/01__Data_and_Storage.md)

## Environments
In this part, we'll talk about how to create environment in AzureML.

---
[==> Continue](docs/02__Environments.md)

## Jobs
In this part, we'll talk about jobs in AzureML.

---
[==> Continue](docs/03__Running_Jobs.md)

## Pipelines
In this part, we'll talk about chaining jobs in AzureML Pipelines.

---
[==> Continue](docs/04__Running_Pipelines.md)