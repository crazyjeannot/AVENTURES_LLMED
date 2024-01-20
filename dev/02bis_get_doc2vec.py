import pandas as pd
import numpy as np
import argparse
import os
import csv
from glob import glob
from tqdm import tqdm
from collections import Counter
from operator import add
import pickle
import nltk

def get_vec(list_token, doc2vec_model):
    return doc2vec_model.infer_vector(list_token)

def get_embeddings(path_name, model):
    columns_df = ['doc']+[i for i in range(0,300)]
    df_main = pd.DataFrame(columns=columns_df)

    for doc in tqdm(glob(path_name)):
        doc_name = path.splitext(path.basename(doc))[0]
        with open(doc, encoding="utf8") as file:
            text = file.readlines()
            text_cleaned = str(text).lower().replace('\xa0', ' ')
            tokens = nltk.tokenize.word_tokenize(text_cleaned, language='french')
            embedding = get_vec(tokens, model)

            new_row_data = [doc_name] + list(embedding)
            new_row_df = pd.DataFrame([new_row_data], columns=columns_df)

            df_main = pd.concat([df_main, new_row_df], ignore_index=True)
                
    df_main.set_index('doc', inplace=True)
    
    return df_main

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help='input directory containing txt files', required=True
    )
    parser.add_argument(
        '-o', '--output', help='output file to write final Dataframe', required=True
    )
    parser.add_argument(
        '-d', '--doc2vec_model', help='path to doc2vec model', required=True
    )

    args = vars(parser.parse_args())
    inputDir = args["input"]
    outputfile = args["output"]
    doc2vec_path = args["doc2vec_model"]

    model = pickle.load(open(doc2vec_path,'rb'))
    
    df_FINAL = get_embeddings(doc_name, model)
    df_FINAL.to_csv('DOC2VEC_EMBEDDINGS_OUTPUT_MAIN.csv')
