import pandas as pd
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re
import emailFunctions as emailFunc


def scanning():
    email_array = []
    email_csv = pd.read_csv('Data/EmailList.csv')  # reading csv
    email_dataframe = pd.DataFrame(email_csv, columns = ['Email','Name'])
    #print(email_dataframe)# array to iterate through names to find url
    for i in range(len(email_dataframe)):
        location = email_dataframe.loc[i]
        email_address = location['Email']
        email_name = location['Name']
        email_array.append((email_address,email_name))
    #print(email_array)
    for address, email_name in email_array:
        print(f'\t\t~~Scanning {email_name}\'s websites....')
        url_list = []
        website_l_csv = pd.read_csv(f'Data/{email_name}/WebsiteList.csv')
        website_df = pd.DataFrame(website_l_csv, columns = ['Name', 'Url'])
        website_df = website_df.set_index(['Name'], drop = False)
        url_array = pd.array(website_df['Url'])
        name_array = pd.array(website_df['Name'])

        pool = ThreadPool(5)
        results = []
        for url, url_name in zip(url_array, name_array):
            if url_name.lower() == 'example': #skip over the example
                continue
            else:
                url_list.append((url, url_name))
                results.append(pool.apply_async(website_checker, args = (url, url_name, email_name)))    #HERE YOU CHECK EACH WEBSITE..... CREATE A FUNCTION TO CALL USING THREADING
        pool.close()
        pool.join()
        results = [r.get() for r in results if r.get() != None]
        #print(results)
        if len(results) == 0:
            print(f'{email_name} Does not have any changes to their website')
            continue
        else:
            bool, message = emailFunc.report_sender(dic_list = results, email_address = address)
            print(message)
            continue
    return '\tFinished Scanning The User\'s Websites'

        #print(future.result())

    #executor.wait(futures)



def website_checker(url, url_name, file_dir):
    url_csv = pd.read_csv(f'Data/{file_dir}/{url_name}.csv')
    old_word_df = pd.DataFrame(url_csv)
    old_indexed = old_word_df.set_index(['Word'], drop=False)  # indexes the dataframe so the index is the word
    old_word_dict = defaultdict(list)
    old_word_dict = old_indexed.to_dict('index', into=old_word_dict)  # 'records',into = old_word_dict)
    email_dictionary = {}
    total_changes = 0
    #requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL' #for rasberry pi
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

        changes = {'Word': [],
                   'Count': [],
                   'New': []}
        word_changes = pd.DataFrame(changes)  # columns = ['Word', 'Count', 'New'])
        word_changes.append({'Word': 'Hello', 'Count': 2, 'New': 'Y'}, ignore_index=True)
        tracked_changes = 0
        # iterate through the new words to compare to the old. Will get you the change in words that were present in the old dictionary and whether there are any new words
        for word in new_word_dict:

            w_new_count = new_word_dict.get(word)
            w_old_count = old_word_dict.get(word)  # .get('Count')
            # print(type(w_new_count), type(w_old_count), w_old_count, w_new_count)
            if type(
                    w_old_count) == list or w_old_count == None:  # if there is a new word that was not in the last dictionary (old_dictionary)
                word_changes = word_changes.append({'Word': word, 'Count': w_new_count, 'New': 'Y'},
                                                   ignore_index=True)  # , ignore_index= True)
                tracked_changes += 1
                continue
            else:  # if there is a word that is present in both the new and old dictionary
                w_old = w_old_count.get('Count')

                if w_new_count != w_old:  # if the old dictionary count does not equal the new one (IE change in word count)
                    difference = w_new_count - w_old
                    word_changes = word_changes.append({'Word': word, 'Count': difference, 'New': 'N'},
                                                       ignore_index=True)
                    tracked_changes += 1
                    continue
                else:  # no changes for the word
                    continue
        if tracked_changes > 0:
            # print(f'There were {tracked_changes} Tracked Changes for {name}. \nSaved new word information to csv')
            new_word_df = pd.DataFrame(list(new_word_dict.items()), columns=['Word', 'Count'])
            indexed_df = new_word_df.set_index(['Word'])
            indexed_df.to_csv(f'Data/{file_dir}/{url_name}.csv', line_terminator='\n')
            print('\t\t\t - Updated the csv with new word counts')
            word_changes = word_changes.set_index(['Word'], drop=True)
            word_changes = word_changes.rename_axis(None)
            word_changes = word_changes.to_dict('index')
            title_index = f'{url_name} {url}'
            email_dictionary[title_index] = word_changes
            total_changes += tracked_changes
            return email_dictionary
        else:
            return None

    except Exception as e:  # if there is a problem with beutiful soup connection
        #raise
        statement = f'Could not parse the website: {url_name}'
        print(e, '\n', statement)
        #return (2, statement)


