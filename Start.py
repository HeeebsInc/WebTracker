import pandas as pd
import numpy as np
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re





def start_csv(dir_name):

    website_list = pd.read_csv(f'Data/{dir_name}/WebsiteList.csv')
    website_df = pd.DataFrame(website_list)
    #name_array = pd.array(website_df['Name'])
    #url_array = pd.array(website_df['Url'])

    #print(name_array)
    #url_name_concat = np.array([[name_array],[url_array]])
    #print(url_name_concat)
    #url_name_concat = np.reshape(url_name_concat,(2,2,5))
    #name_array = np.array([])


    url_array = np.array(website_df['Url'])
    name_array = np.array(website_df['Name'])
    url_name_concat = np.array([url_array,name_array])

    pool = ThreadPool(10)
    results = []
    for url, name in zip(url_array,name_array):
        if name.lower() == 'example':
            continue
        else:
            results.append(pool.apply_async(csv_writer, args=(name,url,dir_name)))
    pool.close()
    pool.join()


    results = [r.get() for r in results]
    print('\n'.join(results))



def csv_writer(url_name, url,dir_name):
    url_dictionary = {}
    url_name = url_name.upper()
    try:  # connect to url to get current html code for comparison
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', text=True)
        # NEW WORD DICTIONARY
        new_word_dict = defaultdict(int)
        for l in links:
            for i in l:
                headline = str(i)
                # print(headline, type(headline))
                string = headline.strip()
                words = string.split(' ')
                for word in words:  # where we iterate and format each word then add it to the dictionary that is following its count
                    if '<' not in word and '>' not in word:
                        regex = re.compile('[^a-zA-Z]')
                        new_word = regex.sub('', word).lower()

                        # if regex detects a word that is just characters, will skip that word for the dictionary
                        if new_word == '\'' or new_word == '':
                            continue
                            # formatting so the apostraphe after the word gets removed with the s and counted as a normal word
                        elif len(word) > 2 and word[-2] == '\'':
                            w = word[:-2].lower()
                            if w in new_word_dict:
                                new_word_dict[w] += 1
                            else:
                                new_word_dict[w] += 1
                        # if the word does not need formatting
                        else:
                            if new_word in new_word_dict:
                                new_word_dict[new_word] += 1

                            else:
                                new_word_dict[new_word] += 1
                    else:
                        continue
        word_df = pd.DataFrame(list(new_word_dict.items()), columns = ['Word','Count'])
        word_df = word_df.set_index(['Word'])
        word_df.to_csv(f'Data/{dir_name}/{url_name.upper()}.csv', line_terminator='\n')  # ,index_label=['Word', 'Count'])

        return f'Successfully Added {url_name} {url} to csv'


    except:
        raise




start_csv('lilybarrettdc')