# Create the job from yaml file.
az ml job create \
    --file jobs/train_mnist/train_mnist.yaml \
    --subscription $AZUREML_SUBSCRIPTION \
    --resource-group $AZUREML_RESSOURCE_GROUP \
    -w $AZUREML_WORKSPACE_NAME --verbose