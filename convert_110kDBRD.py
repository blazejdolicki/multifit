import os, pandas as pd 

DATA_DIR='data/cls/110kDBRD'
NEW_DIR = 'data/cls/nl-books'
for part in ['unsup','test','train']:
    revs_dict = {"labels":[],"text":[]}
    # unsup doesn't have labels
    if part=="unsup":
        TEXT_DIR = f"{DATA_DIR}/{part}"
        for txt in os.listdir(TEXT_DIR)[:1000]:
            with open(f"{TEXT_DIR}/{txt}","r") as f:
                text = f.read()
                # use -1 to indicate no label
                revs_dict["labels"].append(-1)
                revs_dict["text"].append(text)
    else:
        for i, label in enumerate(['neg','pos']):
            TEXT_DIR = f"{DATA_DIR}/{part}/{label}"
            for txt in os.listdir(TEXT_DIR)[:1000]:
                with open(f"{TEXT_DIR}/{txt}","r") as f:
                    text = f.read()
                    revs_dict["labels"].append(i)
                    revs_dict["text"].append(text)

    revs_df = pd.DataFrame.from_dict(revs_dict)
    # shuffle the data
    revs_df = revs_df.sample(frac=1,random_state=7).reset_index(drop=True)   
    # save to csv 
    revs_df.to_csv(f"{NEW_DIR}/nl.{part}.csv", header=None,index=False)