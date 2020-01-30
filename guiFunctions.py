import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re
import emailFunctions as sender
import os
import numpy as np
import csv as csv

fieldnames = ['Name', 'Url', 'Position']

def csv_list(name, url):
    name = name.upper()
    website_list = pd.read_csv('Websites/WebsiteList.csv')

    url_array = pd.array(website_list['Url'])
    name_array = pd.array(website_list['Name'])
    position = (len(website_list))

    if url not in url_array and name not in name_array:
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
            indexed_df.to_csv(f'Websites/{name}.csv', index_label=['Word', 'Count'], line_terminator='\n')

            with open('Websites/WebsiteList.csv', 'a') as website_index:
                csv_writer = csv.DictWriter(website_index, fieldnames=fieldnames, lineterminator='\n')
                info = {
                    'Name': name,
                    'Url': url,
                    'Position': position
                }
                csv_writer.writerow(info)
                print('Added the New URL to your file')
                website_index.close()
            message = 'Added the new website to your file'
            return (1,message)
        except:
            #raise
            message = 'Make Sure you Are Entering the Correct Url (include \'https://\') || If the problem persists, write down link and give to admin***'
            return (0,message)
    #else:
        #raise
    elif url in (url_array):# and name not in name_array:
        message = 'You already have this url saved to the list'
        return 2,message
    elif name in (name_array):# and url not in url_array:
        message = 'You already have the keyword saved.  Choose another name to save to your url'
        return 3,message
    '''else:
        message = 'Make Sure you Are Entering the Correct Code (include \'https://\') || If the problem persists, write down link and give to admin***'
        return 0, message'''



def number_of_items():
    website_list = pd.read_csv('Websites/WebsiteList.csv')
    array = pd.array(website_list['Url'])
    count = len(array)
    return count

def list_of_items():
    website_list = pd.read_csv('Websites/WebsiteList.csv')
    websites = pd.DataFrame(website_list)
    websites = websites[['Name', 'Url']]
    websites.index = np.arange(1, len(websites)+1)
    if len(websites) == 0: #empty dataframe
        statement = 'You do not have any websites saved.  You must add a website to see the list'
        return (2, statement)
    else:
        return (1,websites)



def email_scanner(email):                #error codes used, 1,2, 3, 4, 5
    verify, statement = sender.email_verifer(email)
    if verify == False:
        return 1,statement #error for if email is not valid
    website_l_csv = pd.read_csv('Websites/WebsiteList.csv') #reading csv
    name_array = pd.array(website_l_csv['Name'])     # array to iterate through names to find url
    website_list = pd.DataFrame(website_l_csv)      # a data frame and set index to name to find the direct url
    name_indexed = website_list.set_index('Name')
    email_dictionary = {}
    total_changes = 0
    for name in name_array: #iterate through name_array to see if the name entered matches one that is previously entered

        if name == 'EXAMPLE': #SKIPS OVER THE EXAMPLE IN THE DATAFRAME-- need it because of the delete function
            continue
        name_loc = name_indexed.loc[f'{name}']
        url = str(name_loc['Url'])
        try:            #connect to url to get current html code for comparison
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', text=True)
            #NEW WORD DICTIONARY
            new_word_dict = defaultdict(int)
            for l in links:
                for i in l:
                    headline = str(i)
                    # print(headline, type(headline))
                    string = headline.strip()
                    words = string.split(' ')
                    for word in words: #where we iterate and format each word then add it to the dictionary that is following its count
                        if '<' not in word and '>' not in word:
                            regex = re.compile('[^a-zA-Z]')
                            new_word = regex.sub('', word).lower()

                            #if regex detects a word that is just characters, will skip that word for the dictionary
                            if new_word == '\'' or new_word == '':
                                continue
                                #formatting so the apostraphe after the word gets removed with the s and counted as a normal word
                            elif len(word) > 2 and word[-2] == '\'':
                                w = word[:-2].lower()
                                if w in new_word_dict:
                                    new_word_dict[w] += 1

                                else:
                                    new_word_dict[w] += 1

                            #if the word does not need formatting
                            else:
                                if new_word in new_word_dict:
                                    new_word_dict[new_word] += 1

                                else:
                                    new_word_dict[new_word] += 1
                        else:
                            continue

            #OLD WORD DICTIONARY: opening csv to compare current with old word count
            name_csv = pd.read_csv(f'Websites/{name}.csv')
            old_word_df = pd.DataFrame(name_csv)
            old_indexed = old_word_df.set_index(['Word'], drop = False)   #indexes the dataframe so the index is the word
            old_word_dict = defaultdict(list)
            old_word_dict = old_indexed.to_dict('index',into = old_word_dict)#'records',into = old_word_dict)




            changes = {'Word': [],
                 'Count': [],
                 'New': []}
            word_changes = pd.DataFrame(changes)#columns = ['Word', 'Count', 'New'])
            word_changes.append({'Word': 'Hello', 'Count': 2, 'New': 'Y'}, ignore_index= True)
            tracked_changes = 0
            #iterate through the new words to compare to the old. Will get you the change in words that were present in the old dictionary and whether there are any new words
            for word in new_word_dict:

                w_new_count = new_word_dict.get(word)
                w_old_count = old_word_dict.get(word)#.get('Count')
                #print(type(w_new_count), type(w_old_count), w_old_count, w_new_count)
                if type(w_old_count) == list or w_old_count == None: #if there is a new word that was not in the last dictionary (old_dictionary)
                    word_changes= word_changes.append({'Word': word, 'Count': w_new_count, 'New': 'Y'}, ignore_index= True)#, ignore_index= True)
                    tracked_changes +=1
                    continue
                else:  #if there is a word that is present in both the new and old dictionary
                    w_old = w_old_count.get('Count')

                    if w_new_count != w_old: #if the old dictionary count does not equal the new one (IE change in word count)
                        difference = w_new_count - w_old
                        word_changes = word_changes.append({'Word': word, 'Count': difference, 'New': 'N'}, ignore_index = True)
                        tracked_changes +=1
                        continue
                    else: #no changes for the word
                        continue
            if tracked_changes > 0:
                #print(f'There were {tracked_changes} Tracked Changes for {name}. \nSaved new word information to csv')
                new_word_df = pd.DataFrame(list(new_word_dict.items()), columns = ['Word', 'Count'])
                indexed_df = new_word_df.set_index(['Word'])
                indexed_df.to_csv(f'Websites/{name}.csv', line_terminator='\n')#,index_label=['Word', 'Count'])
                word_changes = word_changes.set_index(['Word'], drop=True)
                word_changes = word_changes.rename_axis(None)
                word_changes = word_changes.to_dict('index')
                title_index = f'{name} {url}'
                email_dictionary[title_index] = word_changes
                total_changes += tracked_changes

        except: #if there is a problem with beutiful soup connection
            #raise
            statement = 'Could not parse the website'
            return (2,statement)

    #print('These are all the changes for each website', email_dictionary)  # this is what will be used to send the report6 to the user
    if total_changes > 0:
        bool_var, statement = sender.email_sender(dictionary=email_dictionary, email=email, total_changes = total_changes)
        if bool_var == False:
            return (3, statement)
        if bool_var == True:
            return (4, statement)

    else:
        statement = 'There were no tracked changes across any of the websites'
        return (5, statement)

#scanning('samuel.mohebban@gmail.com')


def deleter(name):
    name = name.upper()
    if name == 'EXAMPLE':
        statement = 'Cannot Delete the example preset'
        return (3,statement)
    website_list = pd.read_csv('Websites/WebsiteList.csv')
    website_df = pd.DataFrame(website_list)
    website_indexed = website_df.set_index(['Name'], drop = False)
    website_dictionary = website_indexed.to_dict('index')
    try:
        url = website_dictionary[name].get('Url')
        del website_dictionary[name]

        website_df = pd.DataFrame(website_dictionary)
        website_indexed = website_df.transpose()

        website_indexed.to_csv(f'Websites/WebsiteList.csv', line_terminator='\n', index=False,
                               index_label=['Name', 'Url', 'Position'])
        os.remove(f'Websites/{name}.csv')
        statement = f'Successfully deleted\t{name}\t{url}'
        return (1, statement)
    except:
        #raise
        statement = 'You have entered an incorrect name... Check the list and try again'
        return (2, statement)

def console_scanner():                #1,2,3
    website_l_csv = pd.read_csv('Websites/WebsiteList.csv') #reading csv
    name_array = pd.array(website_l_csv['Name'])     #create array to iterate through names to find url
    website_list = pd.DataFrame(website_l_csv)      #create a data frame and set index to name to find the direct url
    name_indexed = website_list.set_index('Name')
    email_dictionary = {}
    total_changes = 0
    for name in name_array:     #iterate through name_array to see if the name entered matches one that is previously entered
        if name == 'EXAMPLE':
            continue
        name_loc = name_indexed.loc[f'{name}']
        url = str(name_loc['Url'])

        #connect to url to get current html code for comparison
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', text=True)  # attrs= {'href': re.compile("http://")}) #find all links href
            new_word_dict = defaultdict(int)
            for l in links:
                for i in l:
                    headline = str(i)
                    string = headline.strip()
                    words = string.split(' ')
                    for word in words:
                        if '<' not in word and '>' not in word:
                            regex = re.compile('[^a-zA-Z]')
                            new_word = regex.sub('', word).lower()
                            #if regex detects a word that is just characters, will skip that word for the dictionary
                            if new_word == '\'' or new_word == '':
                                continue
                                #formatting so the apostraphe after the word gets removed with the s and counted as a normal word
                            elif len(word) > 2 and word[-2] == '\'':
                                w = word[:-2].lower()
                                if w in new_word_dict:
                                    new_word_dict[w] += 1

                                else:
                                    new_word_dict[w] += 1

                            #if the word does not need formatting
                            else:
                                if new_word in new_word_dict:
                                    new_word_dict[new_word] += 1

                                else:
                                    new_word_dict[new_word] += 1 #.append(1)
                        else:
                            continue

            #OLD WEBSITE: opening csv to compare current with old word count
            name_csv = pd.read_csv(f'Websites/{name}.csv')
            old_word_df = pd.DataFrame(name_csv)
            old_indexed = old_word_df.set_index(['Word'], drop = False)   #indexes the dataframe so the index is the word
            old_word_dict = defaultdict(list)
            old_word_dict = old_indexed.to_dict('index',into = old_word_dict)#'records',into = old_word_dict)


            changes = {'Word': [],
                 'Count': [],
                 'New': []}
            word_changes = pd.DataFrame(changes)#columns = ['Word', 'Count', 'New'])
            word_changes.append({'Word': 'Hello', 'Count': 2, 'New': 'Y'}, ignore_index= True)
            tracked_changes = 0
            #iterate through the new words to compare to the old. Will get you the change in words that were present in the old dictionary and whether there are any new words
            for word in new_word_dict:

                w_new_count = new_word_dict.get(word)
                w_old_count = old_word_dict.get(word)#.get('Count')
                if type(w_old_count) == list or w_old_count == None: #if there is a new word that was not in the last dictionary (old_dictionary)
                    word_changes= word_changes.append({'Word': word, 'Count': w_new_count, 'New': 'Y'}, ignore_index= True)
                    tracked_changes +=1
                    continue
                else:  #if there is a word that is present in both the new and old dictionary
                    w_old = w_old_count.get('Count')

                    if w_new_count != w_old: #if the old dictionary count does not equal the new one (IE change in word count)
                        difference = w_new_count - w_old
                        word_changes = word_changes.append({'Word': word, 'Count': difference, 'New': 'N'}, ignore_index = True)
                        tracked_changes +=1
                        continue
                    else: #no changes for the word
                        continue
            if tracked_changes > 0:
                #print(f'There were {tracked_changes} Tracked Changes for {name}. \nSaved new word information to csv')
                new_word_df = pd.DataFrame(list(new_word_dict.items()), columns = ['Word', 'Count'])
                indexed_df = new_word_df.set_index(['Word'])
                indexed_df.to_csv(f'Websites/{name}.csv', line_terminator='\n')#,index_label=['Word', 'Count'])
                word_changes = word_changes.set_index(['Word'], drop=True)
                word_changes = word_changes.rename_axis(None)
                word_changes = word_changes.to_dict('index')
                title_index = f'{name} {url}'
                email_dictionary[title_index] = word_changes
                total_changes += tracked_changes

        except:
            statement = 'Could not parse the website'
            return (-1,statement)

      # this is what will be used to send the report6 to the user
    if total_changes > 0:
        bool_var, statement = sender.email_sender(dictionary=email_dictionary, total_changes = total_changes)
        return total_changes,statement

    else:
        statement = 'There were no tracked changes across any of your websites'
        return (0, statement)

