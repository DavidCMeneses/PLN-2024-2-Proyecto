from datasets import load_dataset
from datasets import Dataset

def LoadDataset()->Dataset:
    '''
    Carga el dataset alfredplpl/artbench-pd-256x256
    '''
    ds = load_dataset("alfredplpl/artbench-pd-256x256")
    return ds