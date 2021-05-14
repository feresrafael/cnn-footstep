# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:14:06 2021

@author: feres
"""

import re
import librosa
import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
#%matplotlib inline
import tensorflow as tf
from sklearn.metrics import precision_recall_fscore_support

import csv
import sys
import itertools
import h5py

def load_sound_files(file_paths):
    raw_sounds = []
    for fp in file_paths:
        X,sr = librosa.load(fp)
        raw_sounds.append(X)
    return raw_sounds



# def load_audio_files():
#     project_dir = '/Sistemas de Informação/TCC/'
#     data_dir = project_dir+'data/'
#     files = librosa.util.find_files(pathAudio, ext=['wav']) 
#     files = np.asarray(files)
#     for y in files: 
#         data = librosa.load(y, sr = 16000,mono = True)   
#         data = data[0]     
#         librosa.display.waveplot(data)


def get_file_name_labels_from_audioset_csv(row_num,csv_file,audioset_indices_csv):
    str_labels = []
    int_labels = []
    # Open choosen CSV file
    with open(csv_file, 'r') as f:
        # Skip to the line we need.
        line = next(itertools.islice(csv.reader(f), int(row_num) + 3, None))
        #print("line:",line)
        # Now that we have the line we need, we need to grab the labels from it
        # This file may have multiple labels, so we need to account for that
        for element in line[3:]:
            if ((element.startswith(' "')) and (element.endswith('"'))):
                str_labels.append(element[2:-1])
            elif (element.startswith(' "')):
                str_labels.append(element[2:])
            elif (element.endswith('"')):
                str_labels.append(element[:-1])
            else:
                str_labels.append(element)

    # Now we have the string version of the labels.
    # Let's convert them to int versions
    for element in str_labels:
        with open(audioset_indices_csv, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if (row[1] == element):
                    int_labels.append(int(row[0]))

    return int_labels   

    

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def assure_path_exists(path):
    mydir = os.path.join(os.getcwd(), path)
    if not os.path.exists(mydir):
        os.makedirs(mydir)

def k_hot_encode(labels,n_unique_labels):
    n_labels = len(labels)
    k_hot_encode = np.zeros((n_labels,n_unique_labels))
    # Mark the relevant values in the area as '1'
    #  This can be multiple elements in the array as there can be
    #  multiple labels to a sample
    for index in range(n_labels):
        for element in labels[index]:
            #print(index,element)
            k_hot_encode[index, element] = 1
    return k_hot_encode


def save_files(data_dir,features,labels,save_h5 = False):
    #labels = k_hot_encode(labels,n_unique_labels = 1)

    print ("Features of = ", features.shape)
    print ("Labels of = ", labels.shape)

    if save_h5:
        feature_file = os.path.join(data_dir + '_x.hdf5')
        labels_file = os.path.join(data_dir + '_y.hdf5')
        with h5py.File(feature_file, 'w') as hf:
            hf.create_dataset("features",  data=features,compression="gzip", compression_opts=9)
        with h5py.File(labels_file, 'w') as hf:
            hf.create_dataset("labels",  data=labels,compression="gzip", compression_opts=9)
    else:
        feature_file = os.path.join(data_dir + '_x.npy')
        labels_file = os.path.join(data_dir + '_y.npy')
        np.save(feature_file, features)
        np.save(labels_file, labels)

    print ("Saved " + feature_file)
    print ("Saved " + labels_file)
    
    
    

