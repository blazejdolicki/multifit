import pandas as pd
import os
from shutil import copyfile

SOURCE_DIR = "../LASER/tasks/cls"

# CLS languages
langs = ["de","fr","ja","nl"]
# langs = ["de"]
for lang in langs:
    DATA_DIR = f"data/cls/{lang}-books"
    TARGET_DIR = f"{DATA_DIR}-laser"

    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        for part in ["test","unsup"]:
            copyfile(f"{DATA_DIR}/{lang}.{part}.csv", f"{TARGET_DIR}/{lang}.{part}.csv")

    

    train = pd.read_csv(f"{SOURCE_DIR}/preds-train-{lang}.csv", header=None,dtype={0:int,1:int})
    train.columns = ["actuals","pseudolabels"]
    # read
    dev = pd.read_csv(f"{SOURCE_DIR}/preds-dev-{lang}.csv", header=None,dtype={0:int,1:int})
    dev.columns = ["actuals","pseudolabels"]

    merged = pd.concat([train,dev], axis=0,ignore_index=True)

    # read ground truth, skip the summary column
    ground_truth = pd.read_csv(f"{DATA_DIR}/{lang}.train.csv",header=None,usecols=[0,2])
    print(lang)
    ground_truth.columns = ["actuals","text"]
    assert (ground_truth["actuals"]==merged["actuals"]).all(), "Ground truth is not the same, probably order of predictions is different"
    
    merged["text"] = ground_truth["text"]
    merged[["pseudolabels","text"]].to_csv(f"{TARGET_DIR}/{lang}.train.csv", index=False, header=False)