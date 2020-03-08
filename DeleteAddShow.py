import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re
import os
#import numpy as np
import csv as csv

fieldnames = ['Name', 'Url']

def website_adder(web_name, dir_name, url):
    web_name = web_name.upper()
    website_list = pd.read_csv(f'WebsiteList.csv')
    url_array = pd.array(website_list['Url'])
    name_array = pd.array(website_list['Name'])

    if url not in url_array and web_name not in name_array:
        #grabbing html code and creating a dictionary following the word counts
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', text=True)
            word_counts = defaultdict(list)
            for l in links:
                for i in l:
                    headline = str(i)
                    string = headline.strip()
                    words = string.split(' ')
                    for word in words:
                        if '<' not in word and '>' not in word:
                            regex = re.compile('[^a-zA-Z]')
                            new_word = regex.sub('', word).lower()
                            '''if regex detects a word that is just characters, will skip that word for the dictionary'''
                            if new_word == '\'':
                                pass
                            elif len(word) > 2 and word[-2] == '\'':
                                w = word[:-2].lower()
                                if w in word_counts:
                                    word_counts[w][0] += 1
                                else:
                                    word_counts[w].append(1)
                            else:
                                if new_word in word_counts:
                                    word_counts[new_word][0] += 1
                                else:
                                    word_counts[new_word].append(1)
                        else:
                            continue
            string_df = pd.DataFrame(word_counts)
            indexed_df = string_df.transpose()

            indexed_df.to_csv(f'{web_name}.csv', index_label=['Word', 'Count'], line_terminator='\n')

            with open(f'WebsiteList.csv', 'a') as website_index:
                csv_writer = csv.DictWriter(website_index, fieldnames=fieldnames, lineterminator='\n')
                info = {
                    'Name': web_name,
                    'Url': url,
                }
                csv_writer.writerow(info)
                website_index.close()
            message = f'Added the new website to {dir}\'s file'
            return 0,message,website_list
        except:
            raise
            message = f'{dir_name}:\tMake Sure you Are Entering the Correct Url (include \'https://\') || If the problem persists, write down link and give to admin***'
            return 1,message,website_list
    #else:
        #raise
    elif url in (url_array):# and name not in name_array:
        message = f'{dir_name}:\tYou already have this url ({url}) saved to their list.  See website list and try again'
        return 2,message,website_list
    elif web_name in (name_array):# and url not in url_array:
        message = f'{dir_name}\t You already have the keyword ({web_name})saved. See website list and choose another name to save to your url'
        return 3,message,website_list



def website_deleter(name, dir_name):
    name = name.upper()

    website_list = pd.read_csv(f'Data/{dir_name}/WebsiteList.csv')
    website_df = pd.DataFrame(website_list)
    website_indexed = website_df.set_index(['Name'], drop=False)
    website_dictionary = website_indexed.to_dict('index')
    if name == 'EXAMPLE':
        message = f'{dir_name}:\tYou tried to delete the url with name Example.. Cannot Delete the example preset'
        return (3, message, website_list)
    try:
        url = website_dictionary[name].get('Url')
        del website_dictionary[name]

        website_df = pd.DataFrame(website_dictionary)
        website_indexed = website_df.transpose()

        website_indexed.to_csv(f'WebsiteList.csv', line_terminator='\n', index=False,
                               index_label=['Name', 'Url', 'Position'])
        os.remove(f'{name}.csv')
        message = f'Successfully deleted\t{name}\t{url}'
        return (0, message, website_indexed)
    except:
        #raise
        message = f'{dir_name}:\tYou have entered an incorrect name to delete... Check the list and try again'
        return (2, message, website_list)


def website_shower(dir_name):
    website_list = pd.read_csv(f'Data/{dir_name}/WebsiteList.csv')
    website_df = pd.DataFrame(website_list)
    website_indexed = website_df.set_index(['Name'], drop=True)
    message = f'{dir_name}\'s current website list'
    return (-1,message,website_indexed)



