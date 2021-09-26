import os
import argparse

import re

############################## < args > ###############################

parser = argparse.ArgumentParser(description='A linear model for the MNIST dataset')

parser.add_argument('--captions_location', dest='captions_location', type=str, default='./datasets/flickr30k/results.token', help='OPTIONAL - the relative path from this folder to the dataset folder (default: ./datasets/flickr30k/results.token)')

args = parser.parse_args()

############################## </ args > ##############################

########################### < file paths > ############################

dir_name = os.path.dirname(os.path.abspath(__file__))

# directory where models will be stored
os.makedirs(os.path.join(dir_name, 'preprocessed_data'), exist_ok=True)
preprocessed_data_path = os.path.join(dir_name, 'preprocessed_data')

# dataset paths
captions_file_location = os.path.join(dir_name, args.captions_location)

########################### </ file paths > ###########################


####################### < parse captions file > #######################
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
captions_file = open(captions_file_location, 'r', encoding='utf-8')
captions_content = captions_file.readlines()

bad_captions = []
for num,row in enumerate(captions_content):
  image_name = row[:row.find('#')].strip().lower()
  image_caption = row[row.find('#')+2:].strip().lower()
  # if no period at the end of the sentence, add one
  image_caption = image_caption if image_caption[-1] == '.' else '%s .' % image_caption
  # all @'s are just mistyped 2's
  image_caption = image_caption.replace('@', '2')
  # replace any unnecessary '!' with '.'
  image_caption = image_caption.replace('!', '.') if image_caption.find('!') == len(image_caption)-1 else image_caption
  # remove quotes 
  image_caption = re.sub(r' (saying|that says|that says ,|that reads|that reads ,|reading|named|labeled|called|called the|marked|that states|that states ,) ("(.*)"|\'(.*)\')', '', image_caption)
  image_caption = re.sub(r' (a|reads|that read) ("(.*)"|\'(.*)\')', '', image_caption)

  image_caption = re.sub(r'(a|an) "(.*)" sign', 'a sign', image_caption)
  image_caption = re.sub(r'with "(.*)" sign', 'with some sign', image_caption)
  image_caption = re.sub(r'the words "(.*)"', 'words', image_caption)

  #remove double spaces
  image_caption = re.sub(r'  ', ' ', image_caption)

  print(image_name[-8:], image_caption)
  bad_condition = '.' in image_caption and image_caption.find('.') < len(image_caption)-1
  bad_condition = bad_condition or '"' in image_caption
  bad_condition = bad_condition or ('\'' in image_caption and not '\'s' in image_caption)
  if bad_condition:
    bad_captions.append(image_caption)

    r"'(?![sm(re)])(.*)'(?![sm(re)])"
  # if ('!' in image_caption and '"' not in image_caption):
  #   print(image_caption)
  # naughty_chars = '~`!@$%^*()'
  # if any([char in image_caption for char in naughty_chars]) and not bad_condition:

  #   print(image_caption)

# print(len(bad_captions))

###################### </ parse captions file > #######################

######################### < parse csv file > ##########################
# captions_dict = {}
# with open(captions_file_location, encoding='utf8', newline='') as csvfile:
#   reader = csv.reader(csvfile, delimiter='|')
#   for index,row in enumerate(reader):
#     if (index > 0):
#       image_name = row[0].strip()
#       image_caption = row[-1].strip().lower()
#       if not ('.' in image_caption and image_caption.find('.') < len(image_caption)-1):
#         if ('"' in image_caption):
#           print(image_caption)
#         if image_name in captions_dict:
#           captions_dict[image_name].append(image_caption)
#         else:
#           captions_dict[image_name] = [image_caption]

# vocabulary = {}
# for image_name, captions in captions_dict.items():
#   for caption_idx, caption in enumerate(captions):
#     captions_dict[image_name][caption_idx] = '__start__ %s' % caption.replace('.', '__end__')
#     words = captions_dict[image_name][caption_idx].split(' ')
#     for word in words:
#       if word not in vocabulary:
#         vocabulary[word] = 0

# for word in vocabulary:
#   print(word)

######################### </ parse csv file > #########################