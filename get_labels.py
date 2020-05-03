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

    # get ground truth dev set
    train_actuals = pd.read_csv(f"{DATA_DIR}/{lang}.train.csv")

    file_size = train_actuals.shape[0]
    print("Use last 10% of training set with ground truth as dev set")
    train_dev_split = int(file_size*0.9)  
    train_actuals.iloc[train_dev_split:,:].to_csv(f"{TARGET_DIR}/{lang}.dev.csv", index=False, header=False)


    # get pseudo-labeled train set
    train = pd.read_csv(f"{SOURCE_DIR}/preds-train-{lang}.csv", header=None,dtype={0:int,1:int})
    train.columns = ["actuals","pseudolabels"]
    # read
    # dev = pd.read_csv(f"{SOURCE_DIR}/preds-dev-{lang}.csv", header=None,dtype={0:int,1:int})
    # dev.columns = ["actuals","pseudolabels"]

    # merged = pd.concat([train,dev], axis=0,ignore_index=True)

    # read ground truth, including the summary column
    ground_truth = pd.read_csv(f"{DATA_DIR}/{lang}.train.csv",header=None,nrows=train_dev_split+1)
    print(lang)
    print(ground_truth.shape,train.shape)
    # NL doesn't have summaries
    if lang=="nl":
        ground_truth.columns = ["actuals","text"]
        assert (ground_truth["actuals"]==train["actuals"]).all(), "Ground truth is not the same, probably order of predictions is different"
    
        train["text"] = ground_truth["text"]
        train[["pseudolabels","text"]].to_csv(f"{TARGET_DIR}/{lang}.train.csv", index=False, header=False)
    else:
        ground_truth.columns = ["actuals","summary","text"]
        assert (ground_truth["actuals"]==train["actuals"]).all(), "Ground truth is not the same, probably order of predictions is different"
        
        train["summary"] = ground_truth["summary"]
        train["text"] = ground_truth["text"]
        train[["pseudolabels","summary","text"]].to_csv(f"{TARGET_DIR}/{lang}.train.csv", index=False, header=False)