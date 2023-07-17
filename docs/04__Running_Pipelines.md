# Running Pipeline

## Introduction
In this part you'll learn how to run pipeline chaining different jobs.<br>
In order to do this, you'll need to have two existing and working jobs.<br>

Note :<br>
Sometimes, it is interesting to do pipelines even with a single job.
It's because pipelines are publishable and can be re-runned easily with different parameters.


## Create the YmlLaunch
In order to launch the job as a pipeline we'll have to create a yamlLaunch similar to the one we created for jobs.<br>
Differences are :<br>
- There is a **default compute**, but each job can override this compute
- Their is a new **jobs** entry
- There are global input / outputs

For example, in order to chain the two jobs we've created before, we can do :
<div style="background-color:#0000EE22">
IN AZUREML WORKSPACE<br>
>> pipelines/00_train_MNIST/scripts/train_mnist.py
</div>

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

experiment_name: MNIST_Training_Pipeline
display_name: Train Mnist Model Pipeline
settings:
    default_compute: azureml:devtracpucluster
 
# Global Input and Outputs
inputs:
  n_max: 1000
  epochs: 5
  batch_size: 4
  learning_rate: 1e-4
  scheduler_step: 2
  scheduler_gamma: 0.5
  data_dir: # As an input for training job, it's read_only.
    type: uri_folder
    path: azureml://datastores/mnist_data_f296849/paths/
    mode: ro_mount

outputs:
  data_dir: # As an output for download job
    type: uri_folder
    path: azureml://datastores/mnist_data_f296849/paths/
    mode: rw_mount
  output_dir:
    type: uri_folder
    path: azureml://datastores/workspaceblobstore/paths/mnist_training
    mode: rw_mount

jobs:
  download_mnist: # We have here our first job
    code: ./download_mnist
    environment: azureml:torch_cpu@latest
    command: >-
      python download_mnist.py
      --data_dir ${{outputs.data_dir}} 
      --n_max ${{inputs.n_max}}
    # it reuses parent parameters
    inputs:
      n_max: ${{parent.inputs.n_max}}
    outputs:
      data_dir: ${{parent.outputs.data_dir}}

  train_mnist:     # We have here the second job
    code: ./train_mnist
    environment: azureml:libaicv_env@latest
    compute: azureml:devtragpucluster # We override the default compute
    command: >-
      python train_mnist.py
      --data_dir ${{inputs.data_dir}} 
      --output_dir ${{outputs.output_dir}} 
      --epochs ${{inputs.epochs}} 
      --batch_size ${{inputs.batch_size}} 
      --learning_rate ${{inputs.learning_rate}} 
      --scheduler_step ${{inputs.scheduler_step}}
      --scheduler_gamma ${{inputs.scheduler_gamma}} 
    inputs:
      epochs: ${{parent.inputs.epochs}}
      batch_size: ${{parent.inputs.batch_size}}
      learning_rate: ${{parent.inputs.learning_rate}}
      scheduler_step: ${{parent.inputs.scheduler_step}}
      scheduler_gamma: ${{parent.inputs.scheduler_gamma}}
      data_dir: ${{parent.inputs.data_dir}}
  
    outputs:
      output_dir: ${{parent.outputs.output_dir}}
```

If you launch this pipeline, exactly like you launched your jobs :<br>
```bash
az ml job create \
    --file jobs/mnist_pipeline.yaml \
    --subscription $AZUREML_SUBSCRIPTION \
    --resource-group $AZUREML_RESSOURCE_GROUP \
    -w $AZUREML_WORKSPACE_NAME --verbose
```

It will create a new pipeline in AzureML :<br>

<img src="../assets/img/00056 - Pipeline Global View.png" alt="drawing" width="800"/>

If you click on the pipeline, you'll see that it contains different jobs chained together :<br>

<img src="../assets/img/00057 - Pipeline Local View.png" alt="drawing" width="800"/>

In the main screen, you can see the child jobs if you select **include child jobs**.

<img src="../assets/img/00058 - Pipeline Child View.png" alt="drawing" width="800"/>


But why is it interesting to define pipelines ?<br>
It's because we can re-run it with different inputs by the UI !<br>

<img src="../assets/img/00059 - Resubmit.png" alt="drawing" width="800"/>


---
[<< Back](../README.md)