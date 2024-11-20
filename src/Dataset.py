from datasets import load_dataset
from datasets import Dataset

def Dataset()->Dataset:
    ds = load_dataset("alfredplpl/artbench-pd-256x256")
    return ds