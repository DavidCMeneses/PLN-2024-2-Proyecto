from datasets import load_dataset
from datasets import Dataset

def LoadDataset()->Dataset:
    ds = load_dataset("alfredplpl/artbench-pd-256x256")
    return ds