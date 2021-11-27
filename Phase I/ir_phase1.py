# -*- coding: utf-8 -*-
"""IR_phase1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ny8XzCifKhBgHrNn7AeL65bqeh92FaDn
"""

pip install pandas

pip install numpy

pip install hazm

from __future__ import unicode_literals
import pandas as pd
import numpy as np
from hazm import *
import collections 
import string
import operator

import datetime

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

file_id = '1jcbbbPTNnQ3NKrPJJL_oc9vrFvHH4UuR'
downloaded = drive.CreateFile({'id': file_id})

downloaded.GetContentFile('/IR1_7k_news.xlsx')

# read data
df = pd.read_excel("/IR1_7k_news.xlsx")
urls = df['url']
content = df['content']
title = df['title']
# normalize data by use hazm
normalizer = Normalizer()
print(content[11])
for i in range(len(content)):
  content[i] = normalizer.normalize(content[i])
copy_content = content
print(content[11])

punctuation  = [ '+','=', '-' , '*' , '.' ,'?', '[', ']','(',')','{','}','<','>', '«' , '»' ,':' , "؟", "؛" , "،", "،" ]
signs = [ '!' , '@' , '#' , '$' , '%' , '^' , '&' , '*', '_', '\\' , '/' , '//' , '|' , "…" , "–" ,"_"]
numbers = ['۰' , '۱', '۲','۳', '۴', '۵','۶','۷','۸','۹']
signs_ir = ['٪' , ',' , '_','–' , '٫' , '"' ]
img_src = ['UFITNPF']
end = ['انتهای پیام']
# some_unknown_char = ['\u200c' , '\u200d' , '\u200e' , '\u200f']
english = list(string.ascii_lowercase) + list(string.ascii_uppercase)
not_used = punctuation + signs + numbers + signs_ir + img_src + english + end

for i in range(len(content)):
    for l in not_used:
        content[i] = content[i].replace(l,"")

print(content[11])
print(content[9])

# make copy from the content that preprocess them (it used ^_^)
preprocess_content = content

print(content[11])
print(content[9])

# make the stem of the word
lstemmer = Stemmer()
lstemmer.stem('اعلام')

# the verb stem
lemmatizer = Lemmatizer()
verbs = lemmatizer.lemmatize('سازم')
x = verbs.split('#')
print(x)

# get tokenize by using the hazm word tokenize
normalizer = Normalizer()
dictionary_non_posting = collections.defaultdict(list)
for i in range(len(content)):
  tokenizes = []
  tokenizes = word_tokenize(content[i])
  tokenizes_count = dict(collections.Counter(tokenizes))
  for key , value in tokenizes_count.items():
    if key in dictionary_non_posting:
      value_old = dictionary_non_posting[key]
      dictionary_non_posting[key] = value + value_old
    else:
      dictionary_non_posting[key] = value

print((dictionary_non_posting['و']))

length_dict_non_posting = {k: v for k, v in sorted(dictionary_non_posting.items(), key=lambda item: item[1] , reverse=True)}
with open("mydict.txt", 'w') as f: 
    for key, value in length_dict_non_posting.items(): 
        f.write("%s:%s\n" % (key, value))

# stop_words = ['آنها' , 'پیش' ,'پس' ,'هر' ,'او' ,'یا' ,'نیز' ,'وی' ,'ما' ,'خود' ,'هم' ,'تا' ,'آن' ,'بر' ,'برای' ,'را' ,'با' ,'که' ,'این' ,'از' ,'به' ,'در' ,'و' ]

# get tokenize by using the hazm word tokenize (the postings list [docid , ferq , [position]])
normalizer = Normalizer()
dictionary_not_steam = collections.defaultdict(list)
for i in range(len(content)):
    tokenizes = []
    tokenizes = word_tokenize(content[i])
    tokenizes_count = dict(collections.Counter(tokenizes))
    for key , value in tokenizes_count.items():
        index = []
        pos_index = position_find(key , tokenizes)
        index.append(i)
        index.append(value)
        index.append(pos_index)
        dictionary_not_steam[key].append(index)

stopwords = list(stopwords_list())
lstemmer = Stemmer()
lemmatizer = Lemmatizer()
def stem_stop(words_content):
  for j in range(len(words_content)):
    for l in stopwords:
      if l == words_content[j]:
        words_content[j] = ""
      else:
        words_content[j] = lstemmer.stem(words_content[j])
  return words_content

# to find position of each word in contents
def position_find(word_to_find , lists):
  # words = contents.split()
  return  [pos for pos, word in enumerate(lists, start=0) if word == word_to_find]

# get tokenize by using the hazm word tokenize (the postings list [docid , ferq , [position]])
normalizer = Normalizer()
dictionary = collections.defaultdict(list)
for i in range(len(content)):
    tokenizes = []
    tokenizes = word_tokenize(content[i])
    tokenizes = stem_stop(tokenizes)
    tokenizes_count = dict(collections.Counter(tokenizes))
    for key , value in tokenizes_count.items():
        index = []
        pos_index = position_find(key , tokenizes)
        index.append(i)
        index.append(value)
        index.append(pos_index)
        dictionary[key].append(index)

# with open("posting-list.json", "w") as outfile:
#     json.dump(dictionary, outfile)
with open("posting-list.txt", 'w') as f: 
    for key, value in dictionary.items(): 
        f.write('%s:%s\n' % (key, value))

print(len(dictionary[lstemmer.stem('صنعتی')]))
print((dictionary[lstemmer.stem('صنعتی')]))
print(dictionary_not_steam[('بین‌الملل')])
print(len(dictionary_not_steam[('بین‌الملل')]))

# the more priority
def sort_dict(dictionary):
   dicts = dictionary
   sorted_dicts = sorted(dicts, key = operator.itemgetter(0, 1) , reverse=False)
   all = 0
   
   for i in range(len(sorted_dicts)):
     all = all + sorted_dicts[i][1]
   return all , sorted_dicts

# one word query 
# this sorted query question by frequency
def query_one_word():
  query = input("enter a word for checking: ")
  time_start = datetime.datetime.now()
  normal_query = lstemmer.stem(query)
  print("Normal word to search {}".format(normal_query))
  # all ,sorted_dict = sort_dict(dictionary[normal_query])
  dicts = dictionary[normal_query]
  sorted_dict = sorted(dicts, key = operator.itemgetter(1, 2) , reverse=True)
  print(sorted_dict)
  time_finish = datetime.datetime.now()
  print("{} results in {} ms".format(len(sorted_dict), ((time_finish - time_start).total_seconds())*1000))
  print("id -> title\n")
  for i in sorted_dict:
    print("{} -> {}".format(i[0] , title[i[0]]))
  print(sorted_dict)
query_one_word()

# the dictionary values is the posting lists
# post_list = dictionary[key][i] 
# the i is iteated 
# return docID
def docID(post_list):
        return post_list[0]

# the dictionary values is the posting lists
# post_list = dictionary[key][i] 
# the i is iteated 
# return list of position
def position(plist):
        return plist[2]

# position intersection algorithm
# get the to word position list and start find k position for p1 , p2
def position_intersect(p1,p2,k):
        answer = []                                                                     # answer <- ()
        len1 = len(p1)
        len2 = len(p2)
        i = j = 0 
        while i != len1 and j != len2:                                                  # while (p1 != nil and p2 != nil)
                if docID(p1[i]) == docID(p2[j]):
                        l = []                                                          # l <- ()
                        pp1 = position(p1[i])                                           # pp1 <- positions(p1)
                        pp2 = position(p2[j])                                           # pp2 <- positions(p2)
    
                        plen1 = len(pp1)
                        plen2 = len(pp2)
                        ii = jj = 0 
                        while ii != plen1:                                              # while (pp1 != nil)
                                while jj != plen2:                                      # while (pp2 != nil)
                                        if abs(pp1[ii] - pp2[jj]) <= k:                 # if (|pos(pp1) - pos(pp2)| <= k)
                                                l.append(pp2[jj])                       # l.add(pos(pp2))
                                        elif pp2[jj] > pp1[ii]:                         # else if (pos(pp2) > pos(pp1))
                                                break    
                                        jj+=1                                           # pp2 <- next(pp2)      
                                while l != [] and abs(l[0] - pp1[ii]) > k :             # while (l != () and |l(0) - pos(pp1)| > k)
                                        l.remove(l[0])                                  # delete(l[0])
                                for ps in l:                                            # for each ps in l
                                        answer.append([ docID(p1[i]), pp1[ii], ps ])    # add answer(docID(p1), pos(pp1), ps)
                                ii+=1                                                   # pp1 <- next(pp1)
                        i+=1                                                            # p1 <- next(p1)
                        j+=1                                                            # p2 <- next(p2)
                elif docID(p1[i]) < docID(p2[j]):                                       # else if (docID(p1) < docID(p2))
                        i+=1                                                            # p1 <- next(p1)                                                        
                else:
                        j+=1                                                            # p2 <- next(p2)
        return answer

# multi word query 
# this sorted query question by frequency
def query_multi():
  sorted_dicts = []
  query = input("enter words for checking: ")
  time_start = datetime.datetime.now()
  query_split = query.split(" ")
  k = 1
  if len(query_split) < 2:
    print("not enough word:(")
    return 
  for i in range(len(query_split)):
    normal_query = lstemmer.stem(query_split[i])
    print("Normal word to search {}".format(normal_query))
    all , diction =  sort_dict(dictionary[normal_query])
    print(all)
    print(diction)
    sorted_dicts.append((all , diction))
  print(sorted_dicts)
  sorted_dicts = sorted(sorted_dicts, key = lambda x: x[1])
  
  for x in range(len(sorted_dicts)-1):
    if(sorted_dicts[x][0] == 0):
      sorted_dicts.pop(x)
  print(len(sorted_dicts))
  if len(sorted_dicts) > 2:
    sorted_dicts1 = position_intersect(sorted_dicts[0][1] ,sorted_dicts[1][1] , k)
    sorted_dicts1 = sorted(sorted_dicts1, key = lambda x: x[1])
    sorted_dicts2 = position_intersect(sorted_dicts[1][1] ,sorted_dicts[2][1] , k)
    sorted_dicts2 = sorted(sorted_dicts2, key = lambda x: x[1])
    print("sorted_dicts1: ", sorted_dicts1)
    print("sorted_dicts2: ",sorted_dicts2)
  #   arr3 = []
  #   while(len(sorted_dicts) > 2):
  #     arr1 = sorted_dicts[0][1]
  #     arr2 = sorted_dicts[1][1]
  #     print(sorted_dicts[0])
  #     print(sorted_dicts[1])
  #     sorted_dicts.pop(0)
  #     sorted_dicts.pop(1)
  #     arr3 = position_intersect(arr1 ,arr2 , k)
  #     sorted_dicts.append((len(arr3), arr3))
  #     sorted_dicts = sorted(sorted_dicts, key = lambda x: x[1])
    # print(arr3)
  elif (len(sorted_dicts) == 2):
    sorted_dicts = position_intersect(sorted_dicts[0][1] ,sorted_dicts[1][1] , k)
    sorted_dicts = sorted(sorted_dicts, key = lambda x: x[1])
    print(sorted_dicts)
    res = collections.defaultdict(list)
    for x in range(len(sorted_dicts)):
      res[sorted_dicts[x][0]].append([sorted_dicts[x][1] , sorted_dicts[x][2]])
    print(res)
    res = sorted(res, key=lambda k: len(res[k]), reverse=True)
    print(res)
  time_finish = datetime.datetime.now()
  print("{} results in {} ms".format(len(res), ((time_finish - time_start).total_seconds())*1000))
  print("id -> title\n")
  for i in range(len(res)):
    print("{} -> {}".format(res[i] , title[res[i]]))
query_multi()