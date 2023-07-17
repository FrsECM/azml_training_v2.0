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
