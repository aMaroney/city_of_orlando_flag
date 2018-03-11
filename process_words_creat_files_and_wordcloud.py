from collections import Counter
import numpy
import matplotlib.pyplot
from nltk.corpus import stopwords
import pickle
import re
import wordcloud

#filtering for puncuations, letters, special characters, and stop words
def process_and_pickle(text_file, language, output_pickle):
    lines = open(text_file, 'r').readlines()
    original_input = lines[0]
    all_lowercase = original_input.lower()
    no_special_char = re.sub(r'([^\sa-z])+', '', all_lowercase)
    word_list_testing = no_special_char.split()
    filtered_words = [word for word in word_list_testing if word not in stopwords.words(language)]
    with open(output_pickle, 'wb') as handle:
        pickle.dump(filtered_words, handle, protocol=pickle.HIGHEST_PROTOCOL)

#filtering by the minimum number of times a word is used
#saving a count of of times each word is used and a raw file of all the words
def filter_words_and_output_txt(input_pickle, raw_text, words_counted_text):
    with open(input_pickle, 'rb') as handle:
        filtered_from_pickle = pickle.load(handle)
    word_list_testing_no_dups = list(set(filtered_from_pickle))
    counts = Counter(filtered_from_pickle)
    for i in range(len(word_list_testing_no_dups)):
        one_word = word_list_testing_no_dups[i]
        number_of_ocurrences = counts[one_word]
        if number_of_ocurrences < 10:
            del counts[one_word]
    keys, values = zip(*counts.items())
    indSort = numpy.argsort(values)[::-1]
    keys = numpy.array(keys)[indSort]
    values = numpy.array(values)[indSort]
    with open(raw_text, 'w') as file_handler:
        for item in filtered_from_pickle:
            file_handler.write(str(item)+' ')
    with open(words_counted_text, 'w') as file_handler:
        for i in range(len(keys)):
            file_handler.write("{}".format(keys[i])+' '+"{}".format(values[i])+'\n')

#creaitng a word cloud from the raw file of all the words
def create_wordcloud_img(raw_text_file_for_wordcloud, wordcloud_image):
    lines = (open(raw_text_file_for_wordcloud,'r').readlines())[0]
    matplotlib.pyplot.figure(figsize=(20,10))
    wc = wordcloud.WordCloud(width=2000, height=1000).generate(lines)
    wc.to_file(wordcloud_image)

process_and_pickle('corpus.txt', 'english','word_list_v1.pickle')
filter_words_and_output_txt('word_list_v1.pickle', 'new_corpus_raw.txt', 'new_corpus_count.txt')
create_wordcloud_img('new_corpus_raw.txt', "orlando_word_cloud_v1.png")