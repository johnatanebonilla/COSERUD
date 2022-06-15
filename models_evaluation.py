#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import spacy
import spacy_conll
from spacy_conll import init_parser
import spacy_sentence_bert
from stanza.utils.conll import CoNLL
from sklearn.metrics import (accuracy_score, f1_score,
                             precision_score, recall_score,
                             classification_report, confusion_matrix)
import spacy_transformers
from thinc.api import Config
from spacy.language import Language
from spacy_conll.parser import ConllParser


def read_file(path):
    with open(path, encoding="utf8") as f:
        data = f.read().splitlines()

    sentences = []
    sentence = {}

    for line in data:
        if '# sent_id' in line:
            sentences.append(sentence)
            sent_id = line.strip().replace('# sent_id = ', '')
            sentence = {'id': sent_id, 'entities': []}
        elif 'text =' in line:
            text = line.strip().replace('# text = ', '')
            sentence['text'] = text

        elif line.strip() != "":
            sentence['entities'].append(line.replace('\n', '').split('\t'))      

    sentences.append(sentence)
    return sentences[1:]



def parse_file(model, gold_file, output_file):
    
    if model == 'coser_gpu':       
        nlp = spacy.load("./june2022/models/coser/model-last/")
        nlp.add_pipe('sentencizer')
        nlp.add_pipe("conll_formatter", last=True)
    elif model == 'ancora_gpu':
        nlp = spacy.load("./june2022/models/ancora/model-last/")
        nlp.add_pipe('sentencizer')
        nlp.add_pipe("conll_formatter", last=True)       
    elif model == 'gsd_gpu':
        nlp = spacy.load("./june2022/models/gsd/model-last/")
        nlp.add_pipe('sentencizer')
        nlp.add_pipe("conll_formatter", last=True)  
    elif model == 'ancoracosergsd_gpu':
        nlp = spacy.load("./june2022/models/ancoracosergsd/model-last/")
        nlp.add_pipe('sentencizer')
        nlp.add_pipe("conll_formatter", last=True)
    elif model == 'ancoracoser_gpu':
        nlp = spacy.load("./june2022/models/ancoracoser/model-last/")
        nlp.add_pipe('sentencizer')
        nlp.add_pipe("conll_formatter", last=True)           
    else:
        pass
    
    # parse/create the .conllu files with new model
    with open(output_file, 'w', encoding="utf-8") as f: 
        for sentence  in gold_file:
            tokens = [e[1:] for e in sentence['entities'] if '-' not in e[0]]
            t2s = ' '.join([t[0] for t in tokens])
            doc = nlp(t2s)

            f.write(f'# sent_id = {sentence["id"]}'  +'\n')
            f.write(f'# text =  {sentence["text"]}'  +'\n')
            c=1
            for elem in doc.sents:
                for i in range(len(elem._.conll)):
                    feats = list(elem._.conll[i].values())[5].split('__') if len(list(elem._.conll[i].values())[5].split('__')) > 1 else list(elem._.conll[i].values())[5].split('__') + ['_']
                    line = str(c)+'\t'+'\t'.join(map(str, list(elem._.conll[i].values())[1:5]))+'\t'+ '\t'.join(feats) +'\t' + '\t'.join(map(str, list(elem._.conll[i].values())[7:])) +'\n'
                    f.write(line)
                    c+=1
            f.write('\n')


def score_model(gold_file, model_output):
    pd = [[] for i in range(8)]
    gt = [[] for i in range(8)]
    c = 0
    for j in range(len(gold_file)):
        # the current sentence
        sentence = gold_file[j]['text']
        
        # gold file entities
        disk = [en[1:] for en in gold_file[j]['entities'] if '-' not in en[0]]

        # adjusted file entities
        disk1 = [en[1:] for en in model_output[j]['entities']]
        
        
        # match the words of the same sentence
        if len(disk1)!=len(disk):
            print(j)
        for i in range(len(disk)):
            # make sure the lemmes matches
            if disk[i][0] == disk1[i][0]:
                for u in range(8):                    
                    pd[u].append(disk[i][u])
                    gt[u].append(disk1[i][u])
                    
    for i in range(1, 2):
        print(classification_report(gt[i], pd[i], labels=np.unique(pd[i])))
        print(accuracy_score(gt[i], pd[i]))


# Parse and fit spanish models

gold_file = read_file('./june2022/datasets/coser/es_coser-ud-test.conllu')
parse_file('coser_gpu', gold_file, './june2022/datasets/parsed_ev/coser_coser.conllu')
parse_file('ancora_gpu', gold_file, './june2022/datasets/parsed_ev/coser_ancora.conllu')
parse_file('gsd_gpu', gold_file, './june2022/datasets/parsed_ev/coser_gsd.conllu')
parse_file('ancoracosergsd_gpu', gold_file, './june2022/datasets/parsed_ev/coser_ancoracosergsd.conllu')
parse_file('ancoracoser_gpu', gold_file, './june2022/datasets/parsed_ev/coser_ancoracoser.conllu')

# Score model 
adjusted_file = read_file('./june2022/datasets/parsed_ev/coser_cosergpu.conllu')
score_model(gold_file, adjusted_file)

