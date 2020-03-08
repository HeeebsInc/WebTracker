This web scraper works by continuously tracking websites across multiple users.  

So, it works by housing a list of saved urls per user based on their email address, then sends them an email if there is a change to any of their saved websites

In order to use the webscraper you must first do the following:
  1. Create a new email account with gmail 
  2. create a directory named 'Data' in the location where the .py files are
  3. Add the emails and name of each user to the csv file called EmailList.csv seperates by a comma
    - email is the email address of the user
    - name is the email address without the @...com So, for hello@gmail.com, the name would be just hello
  3. For each user you want to track, you must also set up a directory within the Data directory that is called the name of the user 
    - so, for hello@gmail.com (name = hello), you would have to set up a directory in data called 'hello'
 
  
