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

  #correct punctuation
  image_caption = image_caption.replace('!', '.') if image_caption.find('!') == len(image_caption)-1 else image_caption
  image_caption = image_caption.replace('?', '.') if image_caption.find('?') == len(image_caption)-1 else image_caption
  image_caption = image_caption if image_caption[-1] == '.' else '%s .' % image_caption
  
  # specific caption fixes found
  image_caption = image_caption.replace('@', '2')
  image_caption = image_caption.replace('&', 'and')
  image_caption = image_caption.replace('? ', '')
  image_caption = image_caption.replace('etc.', 'etc')
  image_caption = image_caption.replace('g ?uys', 'guys')
  image_caption = image_caption.replace(' : ', ' ; ')
  image_caption = image_caption.replace('wuth', 'with')
  image_caption = image_caption.replace(':while', 'while')
  image_caption = image_caption.replace('the name', 'a name')
  image_caption = image_caption.replace('" canal "', 'canal')
  image_caption = image_caption.replace('\' devil \'', 'devil')
  image_caption = image_caption.replace('a " bath "', 'a bath')
  image_caption = image_caption.replace('" boombox "', 'boombox')
  image_caption = image_caption.replace('" dance cage "', 'cage')
  image_caption = image_caption.replace('s gray dog', 'a gray dog')
  image_caption = image_caption.replace('" high-five "', 'high-five')
  image_caption = image_caption.replace('" farmers market "', 'market')
  image_caption = image_caption.replace('" beer gardens "', 'beer garden')
  image_caption = image_caption.replace('the " new testament "', 'a book')
  image_caption = image_caption.replace('an " angry " man " chokes "', 'a man')
  image_caption = image_caption.replace('" city picnic . "', 'city picnic')
  image_caption = image_caption.replace('professed " naked cowboy "', 'naked cowboy')
  image_caption = image_caption.replace('" moon bounce , "', 'moon bounce')
  image_caption = image_caption.replace('passed a \' model express \'', 'past a shop')
  image_caption = image_caption.replace('" hartman prehistoric garden "', 'garden')
  image_caption = image_caption.replace('hartman prehistoric garden', 'garden')
  image_caption = image_caption.replace('hartman prehistoric center', 'garden center')
  image_caption = image_caption.replace('prehistoric garden', 'garden')
  image_caption = image_caption.replace('i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture .', 'a woman holds her head as she is making a phone call .')
  image_caption = image_caption.replace('i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture .', 'three men sitting on stair steps talking to each other .')


  image_caption = image_caption.replace('a " telephone booth "', 'a telephone booth')
  image_caption = image_caption.replace('points to a " one " outside', 'points outside')
  image_caption = image_caption.replace('man with a " backyard babies " has', 'man has')
  image_caption = image_caption.replace('experiencing and exhibit', 'experiencing an exhibit')
  image_caption = image_caption.replace('two you women strolling', 'two young women strolling')
  image_caption = image_caption.replace('a " rock star " performing', 'a performer performing')
  image_caption = image_caption.replace('banner that stays , " we are demanding . " .', 'banner .')
  image_caption = image_caption.replace('republicans have a " i stole all your money hahaha " outdoor barbecue .', 'people have an outdoor barbecue .')
  image_caption = image_caption.replace('with a " do not tread on me " flag and a sign that says " Thank you U.S. Troops . "', 'with a flag and a sign .')
  image_caption = image_caption.replace('other guy the number " o " as this what they do for a living .', 'other guy .')
  
  # remove quotes 
  image_caption = re.sub(r' (after saying ,|that say ,|that says ,|which reads ,|that reads ,|that read ,|that states ,|with the phrase ,) ("(.*)"|\'(.*)\')', '', image_caption)
  image_caption = re.sub(r' (saying ,|that says|that reads|reading|marked|that states|named|called the|that is labeled|labeled a|of which say|that all say|with the phrase|entitled) ("(.*)"|\'(.*)\')', '', image_caption)
  image_caption = re.sub(r' (saying|that say|labeled|called|reads|that read|which say|titled) ("(.*)"|\'(.*)\')', '', image_caption)
  image_caption = re.sub(r' (with the text|displaying the text|that contains the text|called|reads|that read|which say|which states|which reads|that reads :|reading :) ("(.*)"|\'(.*)\')', '', image_caption)

  image_caption = re.sub(r'a ("(.*)"|\'(.*)\')', ' a', image_caption)

  image_caption = re.sub(r'the words ("(.*)"|\'(.*)\')', 'words', image_caption)
  image_caption = re.sub(r'the word ("(.*)"|\'(.*)\')', 'words', image_caption)
  image_caption = re.sub(r'(displays|says) ("(.*)"|\'(.*)\')', 'says something', image_caption)
  image_caption = re.sub(r'(a|an) "(.*)" sign', 'a sign', image_caption)
  image_caption = re.sub(r'with "(.*)" sign', 'with some sign', image_caption)
  image_caption = re.sub(r'with "(.*)"', 'with something', image_caption)
  image_caption = re.sub(r'"(.*)" written', 'something written', image_caption)
  image_caption = re.sub(r' (an ollie|an " ollie "|a ollie)', ' a trick', image_caption)
  image_caption = re.sub(r' ollies', ' does a trick', image_caption)
  image_caption = re.sub(r'prehistoric garden|hartman prehistoric garden|hartman prehistoric', 'garden', image_caption)
  image_caption = re.sub(r' (\d\d % off|\d\d %)', '', image_caption)

  image_caption = re.sub(r'" (.*) "', '', image_caption)
  image_caption = re.sub(r'\'(?![sm(re)])(.*)\'(?![sm(re)]) ', '', image_caption)
  image_caption = re.sub(r' \' |(?<=\w)\' ', ' ', image_caption)
  image_caption = re.sub(r'\((.*)\)', '', image_caption)


  # if no period at the end of the sentence, add one
  image_caption = image_caption.strip()
  image_caption = image_caption if image_caption[-1] == '.' else '%s .' % image_caption

  # remove double spaces
  image_caption = re.sub(r'  ', ' ', image_caption).strip()

  print(image_name[-8:], image_caption)


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