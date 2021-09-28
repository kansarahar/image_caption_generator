import os
import argparse

import re
import pickle

############################## < args > ###############################

parser = argparse.ArgumentParser(description='A linear model for the MNIST dataset')

parser.add_argument('--captions_location', dest='captions_location', type=str, default='./datasets/flickr30k/results.token', help='OPTIONAL - the relative path from this folder to the dataset folder (default: ./datasets/flickr30k/results.token)')

args = parser.parse_args()

########################### < file paths > ############################

dir_name = os.path.dirname(os.path.abspath(__file__))

# directory where models will be stored
os.makedirs(os.path.join(dir_name, 'processed_caption_data'), exist_ok=True)
processed_caption_data_path = os.path.join(dir_name, 'processed_caption_data')

img2captions = pickle.load(open(os.path.join(processed_caption_data_path, 'img2captions.p'), 'rb'))
word2freq = pickle.load(open(os.path.join(processed_caption_data_path, 'word2freq.p'), 'rb'))
word2idx = pickle.load(open(os.path.join(processed_caption_data_path, 'word2idx.p'), 'rb'))
idx2word = pickle.load(open(os.path.join(processed_caption_data_path, 'idx2word.p'), 'rb'))
