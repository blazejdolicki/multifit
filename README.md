# Multifit for Dutch
This is a fork of the original Multifit [repository](https://github.com/n-waves/multifit) used for my [bachelor thesis](https://github.com/blazejdolicki/multilingual-analysis). We add scripts to use the 110k DBRD dataset, merge it with CLS into CLS+ and evaluate the supervised and zero-shot learning performance in Dutch. We additionally pretrain a Dutch language model from scratch.

## Reproducing the results
### Initial steps
1. Clone the repository.

`>> git clone https://github.com/blazejdolicki/multifit`

2. Create a new conda environment and activate it after creation.
```
>> conda create -n multifit_env python=3.6
>> conda activate multifit_env
```
(sometimes conda is set up differently and instead of `conda activate multifit_env` you should use `source activate multifit_env`).

3. Install dependencies.
```
>> pip install -r requirements.txt
>> pip install ninja==1.9.0.post1
```
### Train and make predictions on CLS+
Download the data by running

`>> python prepare_cls.py https://storage.googleapis.com/ulmfit/cls-full`

Optionally, if you want to download only 30k of unsupervised data you can run this instead: 

`>> python prepare_cls.py https://storage.googleapis.com/ulmfit/cls`

#### Supervised learning
Finetune LM on CLS and train a classifier (replace "fr" with your desired language for which have a pretrained LM):

`>>python -m ulmfit eval --glob="wiki/fr-100/models/sp15k/qrnn_nl4.m" --name nl4 --dataset-template='../cls/fr-books' --num-lm-epochs=20  --num-cls-epochs=8  --bs=18 --lr_sched=1cycle --label-smoothing-eps=0.1`

If you already trained a classifier before and want to overwrite the results/train it again, add `overwrite_clas=True` at the end of the command.

#### Zero-shot learning
To run zero-shot learning, at first setup LASER and get pseudolabels according to these [instructions](https://github.com/blazejdolicki/LASER/blob/master/README.md).  
Finally, use a similar command as for supervised learning, the only difference is the dataset path:

`>>python -m ulmfit eval --glob="wiki/fr-100/models/sp15k/qrnn_nl4.m" --name nl4 --dataset-template='../cls/fr-books-laser' --num-lm-epochs=20  --num-cls-epochs=8  --bs=18 --lr_sched=1cycle --label-smoothing-eps=0.1`

### Pretrain a language model from scratch
Download wikipedia data ("de" means that we are downloading German wikipedia, for other languages, you should use their appropriate abbreviations) - beware that this command will take a few hours to run.

`>> bash prepare_wiki.sh de`

After running this command you will be asked about max token number. Just click Enter to use the default number (100).

Finally pretrain the language model with wikipedia data using QRNNs:

`>>python -m ulmfit lm2 --dataset-path data/wiki/de-100 --tokenizer='sp' --nl 4 --name 'nl4' --max-vocab 15000 --lang de --qrnn=True - train_lm 10 --bs=50 --drop_mult=0`


