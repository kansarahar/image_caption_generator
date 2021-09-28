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

# dataset paths
captions_file_location = os.path.join(dir_name, args.captions_location)

####################### < parse captions file > #######################

captions_file = open(captions_file_location, 'r', encoding='utf-8')
captions_content = captions_file.readlines()

img2captions = {}
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
  image_caption = image_caption.replace('.` ', '')
  image_caption = image_caption.replace('` ', ' \'')
  image_caption = image_caption.replace('etc.', 'etc')
  image_caption = image_caption.replace(' ans ', ' and ')
  image_caption = image_caption.replace('g ?uys', 'guys')
  image_caption = image_caption.replace(' : ', ' ; ')
  image_caption = image_caption.replace(' st .', ' st')
  image_caption = image_caption.replace(' st. ', ' st ')
  image_caption = image_caption.replace('wuth', 'with')
  image_caption = image_caption.replace('uh oh . ', '')
  image_caption = image_caption.replace('da fun', 'day fun')
  image_caption = image_caption.replace('man \'s i.v.', 'man')
  image_caption = image_caption.replace('mr. potao', 'mr. potato')
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
  image_caption = image_caption.replace('that advertises easy bus.co.uk ', '')
  image_caption = image_caption.replace('the " new testament "', 'a book')
  image_caption = image_caption.replace('2.5 stories high ', '')
  image_caption = image_caption.replace('bronco.', 'bronco')
  image_caption = image_caption.replace('r.v.', 'rv')
  image_caption = image_caption.replace('r.c. boat', 'remote control boat')
  image_caption = image_caption.replace('in charlotte , nc.', '')
  image_caption = image_caption.replace('hi , which are you using l\'oreal nail polish on your fingers .', 'a woman in a green dress looking at the hands of a woman in a black dress')
  image_caption = image_caption.replace('of bagpipe.co.uk nifty nosh ', 'a')
  image_caption = image_caption.replace('an " angry " man " chokes "', 'a man')
  image_caption = image_caption.replace('" city picnic . "', 'city picnic')
  image_caption = image_caption.replace('professed " naked cowboy "', 'naked cowboy')
  image_caption = image_caption.replace('" moon bounce , "', 'moon bounce')
  image_caption = image_caption.replace('passed a \' model express \'', 'past a shop')
  image_caption = image_caption.replace('" hartman prehistoric garden "', 'garden')
  image_caption = image_caption.replace('hartman prehistoric garden', 'garden')
  image_caption = image_caption.replace('hartman prehistoric center', 'garden center')
  image_caption = image_caption.replace('prehistoric garden', 'garden')
  image_caption = image_caption.replace('psychic readings by mrs. lillian ', '')
  image_caption = image_caption.replace('weas the number 28 and black', 'wears black')
  image_caption = image_caption.replace('number 28 slides', 'a player slides')
  image_caption = image_caption.replace('jersey number 28', 'jersey')
  image_caption = image_caption.replace('cross west 23rd street', 'cross the street')


  image_caption = image_caption.replace('i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture .', 'a woman holds her head as she is making a phone call .')
  image_caption = image_caption.replace('i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture i do n\'t see a picture .', 'three men sitting on stair steps talking to each other .')

  image_caption = image_caption.replace('a " telephone booth "', 'a telephone booth')
  image_caption = image_caption.replace('points to a " one " outside', 'points outside')
  image_caption = image_caption.replace('man with a " backyard babies " has', 'man has')
  image_caption = image_caption.replace('experiencing and exhibit', 'experiencing an exhibit')
  image_caption = image_caption.replace('two you women strolling', 'two young women strolling')
  image_caption = image_caption.replace('a " rock star " performing', 'a performer performing')
  image_caption = image_caption.replace('banner that stays , " we are demanding . " .', 'banner .')
  image_caption = image_caption.replace('1.20 euro', 'money')
  image_caption = image_caption.replace('selling chestnuts for 2.00 euros', 'money')
  image_caption = image_caption.replace('buttocks', 'butt')
  image_caption = image_caption.replace('green 5.00 sticker', 'green sticker')
  image_caption = image_caption.replace('republicans have a " i stole all your money hahaha " outdoor barbecue .', 'people have an outdoor barbecue .')
  image_caption = image_caption.replace('the player from the miami dolphins tries to tackle the l.a. raider .', 'the player tries to tackle the opponent .')
  image_caption = image_caption.replace('with a " do not tread on me " flag and a sign that says " Thank you U.S. Troops . "', 'with a flag and a sign .')
  image_caption = image_caption.replace('other guy the number " o " as this what they do for a living .', 'other guy .')
  image_caption = image_caption.replace('and appears to be speaking about nursing idol steven dr robert harry taylor who is sitting next to her ', '')
  image_caption = image_caption.replace('s.c.u.b.a.', 'scuba')

  image_caption = image_caption.replace('it seems there dr pepper soda', 'it seems there is soda')
  image_caption = image_caption.replace('seems to me', 'it')
  image_caption = image_caption.replace('man in dr pepper logo shirt laying', 'Man laying')
  image_caption = image_caption.replace('in a dr. pepper t-shirt', 'in a t-shirt')
  image_caption = image_caption.replace('building called mr bagel \'s that', 'building that')
  image_caption = image_caption.replace('building named mr bagel \'s', 'building')
  image_caption = image_caption.replace('wow ! this book is good , have get comfortable to read it .', 'a young girl reading a book on the couch')
  image_caption = image_caption.replace('whoa ! the cowboy is underneath', 'the cowboy is underneath')
  image_caption = image_caption.replace('on that says frog ! stands', 'on stands')
  image_caption = image_caption.replace('backseat that says jouez la carta de frete ! on', 'backseat on')
  image_caption = image_caption.replace('a pop ! tech event', 'an event')
  image_caption = image_caption.replace('you , too,can achieve financial freedom after listening carefully to this presentation', 'a woman is giving a presentation')
  image_caption = image_caption.replace('at a berlin,germany train', 'at a train')
  image_caption = image_caption.replace('two men,one', 'two men , one')
  image_caption = image_caption.replace('this man is a union employee making 95,000 a year mopping floors for the government .', 'this man is mopping the floors of the building .')
  image_caption = image_caption.replace('in long coat,grey slacks', 'in a long coat , grey slacks ,')
  image_caption = image_caption.replace('plastic bib,girl', 'plastic bib ; girl')
  image_caption = image_caption.replace('check for 10,000 dollars .', 'check .')
  image_caption = image_caption.replace('t.v.', 'tv')
  image_caption = image_caption.replace('over # 5 \'s head ', 'over another player \'s head ')
  image_caption = image_caption.replace('a uh football player , # 15 , stands', 'a football player stands')
  image_caption = image_caption.replace('market shortly before 2 o\'clock in the afternoon ,', 'market ,')
  image_caption = image_caption.replace('hair and a five o\'clock shadow is', 'hair is')
  image_caption = image_caption.replace('watch that appears to be about 7 o\'clock is', 'watch is')

  image_caption = image_caption.replace('in washington d.c.', '')
  image_caption = image_caption.replace('in washington dc', '')
  image_caption = image_caption.replace('mr. t ', '')
  image_caption = image_caption.replace('base .a group', 'base')
  image_caption = image_caption.replace('a .group of', 'a group of')
  image_caption = image_caption.replace('john a. noble', 'a')
  image_caption = image_caption.replace('joseph a. bank', 'a')
  image_caption = image_caption.replace('..asian food court', '; asian food court')
  image_caption = image_caption.replace('dr. nava', 'a man')
  image_caption = image_caption.replace('road.an o', 'road')
  image_caption = image_caption.replace('hand . is jumping into', 'hand , is jumping into')
  image_caption = image_caption.replace('for craftzine .com ', '')
  image_caption = image_caption.replace('george w. bush ', '')
  image_caption = image_caption.replace('dale earnhardt , jr. , ', '')
  image_caption = image_caption.replace('dale jr. ', '')
  image_caption = image_caption.replace('that reads Happy Birthday Quinn ', '')
  image_caption = image_caption.replace('3 ft . deep ', '')
  image_caption = image_caption.replace('at a depth of 3.5 feet ', '')
  image_caption = image_caption.replace('... and no , this is n\'t the beginning of a joke ', '')
  image_caption = image_caption.replace('...', '')
  image_caption = image_caption.replace('u.s.m.c. ', '')
  image_caption = image_caption.replace('u.s. ', '')
  image_caption = image_caption.replace('n.y . ', '')
  image_caption = image_caption.replace('rees.com ', '')
  image_caption = image_caption.replace('3.5 ft . ', '')
  image_caption = image_caption.replace('prince st. ', '')
  image_caption = image_caption.replace('prince st ', '')
  image_caption = image_caption.replace('that says e.s.e. electronics ', '')
  image_caption = image_caption.replace('e.s.e. electronics ', '')
  image_caption = image_caption.replace('india inc. ', '')
  image_caption = image_caption.replace('for l. vaggi ', '')
  image_caption = image_caption.replace('promoting dr. faustus ', '')
  image_caption = image_caption.replace(', by laura a. large ', '')
  image_caption = image_caption.replace('l.e.d. ', '')
  image_caption = image_caption.replace('john . f hunt owned genpac ', '')
  image_caption = image_caption.replace('in c.d\'s ', '')
  image_caption = image_caption.replace('of kebap haus.', '')
  image_caption = image_caption.replace('outside bua.', '')
  image_caption = image_caption.replace('fire dept . ', '')
  image_caption = image_caption.replace('for miami u. ', '')
  image_caption = image_caption.replace('u. miami ', '')
  image_caption = image_caption.replace('el pub restaurant.com ', '')
  image_caption = image_caption.replace('j.p. morgan corporate ', '')
  image_caption = image_caption.replace('by j.p. morgan chase with security ', '')
  image_caption = image_caption.replace(', named victoria l. leak , ', '')
  image_caption = image_caption.replace('victoria l. leak , ', '')
  image_caption = image_caption.replace('s.w.a.t. ', '')
  image_caption = image_caption.replace('laura a. large ', '')  
  image_caption = image_caption.replace('dr. seuss ', '')
  image_caption = image_caption.replace(' . a g', '')
  image_caption = image_caption.replace('that says rocks.', '')
  image_caption = image_caption.replace('a woman with .', '')
  image_caption = image_caption.replace(' for sudan.', '')
  image_caption = image_caption.replace('courtesy of shell corporation of america ', '')
  image_caption = image_caption.replace('red khera transport corp. truck', 'red truck')
  image_caption = image_caption.replace('driver for khera transport corp. makes', 'driver makes')
  image_caption = image_caption.replace('red semi-truck of khera transport corp', 'red semi-truck')
  image_caption = image_caption.replace('semi truck', 'truck')
  image_caption = image_caption.replace('semi-truck', 'truck')
  image_caption = image_caption.replace('drums from america \'s corp fort lewis , washington while', 'drums while')
  image_caption = image_caption.replace('drums labeled fort lewis , washington', 'drums')
  image_caption = image_caption.replace('us army', 'army')
  image_caption = image_caption.replace('grass-covered', 'grass covered')
  image_caption = image_caption.replace('a blue-colored racing sailboat sporting the number 5 and oracle corporate logos is sailing', 'a blue colored sailboat is sailing')
  image_caption = image_caption.replace('men recreating an ancient fife and drum corps from the american revolutionary war are marching in a modern parade while wearing white wigs , black tricorn hats , white waistcoats , and white knickers or knee breeches .', 'men are marching in a parade while wearing white wigs , black hats , and white pants .')
  image_caption = image_caption.replace('at the atms', 'at the atm')
  image_caption = image_caption.replace('money our of an atm', 'money out of an atm')
  image_caption = image_caption.replace('washington mutual atms', 'the atm')
  image_caption = image_caption.replace('using washington mutual atm machines', 'using the atm')
  image_caption = image_caption.replace('atm machines', 'atm')
  image_caption = image_caption.replace('atm machine', 'atm')
  image_caption = image_caption.replace('ba tangles', 'be tangled')
  image_caption = image_caption.replace('cheer at the 2007 uefa under-21 football championship in the netherlands', 'cheer')
  image_caption = image_caption.replace('marathon , runner 721 and 5132 are the leaders', 'marathon')
  image_caption = image_caption.replace('yellow , number 21 jersey', 'yellow jersey')
  image_caption = image_caption.replace('Number 21 slides into second base as number 4 runs', 'one player slides into second base as another runs')
  image_caption = image_caption.replace('two forever 21 bags', 'two bags')
  image_caption = image_caption.replace('wearing a shirt with number 32', 'wearing a shirt')
  image_caption = image_caption.replace('wearing a shirt with number 96', 'wearing a shirt')
  image_caption = image_caption.replace('showing lafayette player number 32 and penn state player number 23', 'showing two players')
  image_caption = image_caption.replace('number 32 , on the burgundy team is', 'a player on one team is')
  image_caption = image_caption.replace('player wearing the number 32 and', 'player and')
  image_caption = image_caption.replace('pillow-fight', 'pillow fight')

  # pattern substitution using regex
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
  image_caption = re.sub(r'for \$.*\d ', '', image_caption)

  image_caption = re.sub(r'" (.*) "', '', image_caption)
  image_caption = re.sub(r'\'(?![sm(re)])(.*)\'(?![sm(re)]) ', '', image_caption)
  image_caption = re.sub(r' \' |(?<=\w)\' ', ' ', image_caption)
  image_caption = re.sub(r'\((.*)\)', '', image_caption)
  image_caption = re.sub(r'\.([a-z]+) \.', '.', image_caption)
  image_caption = re.sub(r' \$.*\d ', ' money ', image_caption)
  image_caption = re.sub(r'\w*\.com ', '', image_caption)
  image_caption = re.sub(r'\. (?!claus)([a-z]*) \.', '.', image_caption)
  image_caption = re.sub(r'#(| )\d+', '', image_caption)

  image_caption = re.sub(r' (that says|that say|that reads) \w* \.', ' .', image_caption)
  image_caption = re.sub(r' (that says|that say|that reads) \w* \w* \.', ' .', image_caption)

  image_caption = image_caption.replace(' . ', ' ; ')

  # if no period at the end of the sentence, add one
  image_caption = image_caption.strip()
  image_caption = image_caption if image_caption[-2:] == ' .' else '%s .' % image_caption

  # remove double spaces
  image_caption = re.sub(r'  ', ' ', image_caption).strip()

  image_caption = '%s%s' % (image_caption[:-1], '--end--')

  if image_name in img2captions:
    img2captions[image_name].append(image_caption.split(' '))
  else:
    img2captions[image_name] = [image_caption.split(' ')]

######################## < build vocabulary > #########################

word2freq = {}
for image_name, image_captions in img2captions.items():
  for caption in image_captions:
    for word in caption:
      if word in word2freq:
        word2freq[word] += 1
      else:
        word2freq[word] = 1

word2idx = { item[0]:idx for idx,item in enumerate(word2freq.items()) }
idx2word = { value:key for key,value in word2idx.items() }

pickle.dump(img2captions, open(os.path.join(processed_caption_data_path, 'img2captions.p'), 'wb'))
pickle.dump(word2freq, open(os.path.join(processed_caption_data_path, 'word2freq.p'), 'wb'))
pickle.dump(word2idx, open(os.path.join(processed_caption_data_path, 'word2idx.p'), 'wb'))
pickle.dump(idx2word, open(os.path.join(processed_caption_data_path, 'idx2word.p'), 'wb'))
