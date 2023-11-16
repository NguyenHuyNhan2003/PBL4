# create a virtual environment (.venv)
# run virtual environment: .venv/bin/activate
# install requirement: pip install -r requirements.txt
from facebook_scraper import get_posts, get_group_info 
from datetime import datetime, timedelta 
import pandas as pd 
from pymongo import MongoClient 
import time
import os

# constants
FANPAGE_LINK ="groups/" # jobITDaNang
FOLDER_PATH = "."
PAGES_NUMBER = 5
mongoURI = 'mongodb+srv://adminPBL4:admin@pbl4.xemvqhk.mongodb.net/PBL4?retryWrites=true&w=majority'
DATABASE_NAME = "PBL4"

# read group names from file
def read_group_names():
    file_path = FOLDER_PATH + "/group_names.txt"
    
    with open(file_path, "r") as file:
        content = file.read().split(",")
        group_names = [value.strip() for value in content]
        
    return group_names

def get_time_limit():
    days_before = (datetime.now() - timedelta(days=7)).date() #date from which to scrap posts
    return days_before

# reaction counter
def reaction_counter(post):
    # define reacrions counter
    reaction_count = 0
    like_count = 0
    love_count = 0
    care_count = 0
    haha_count = 0
    wow_count = 0
    sad_count = 0
    angry_count = 0
    
    if(post['reactions'] != None): # if there is reaction
        if('like' in post['reactions']):
            like_count = post['reactions']['like'] # like count
            reaction_count += like_count
        else: like_count = 0
        if('love' in post['reactions']):
            love_count = post['reactions']['love'] # love count
            reaction_count += love_count
        else:  love_count = 0
        if('haha' in post['reactions']):
            haha_count = post['reactions']['haha'] # haha count
            reaction_count += haha_count
        else: haha_count = 0
        if('sad' in post['reactions']):
            sad_count = post['reactions']['sad'] # sad count
            reaction_count += sad_count
        else: sad_count = 0
        if('wow' in post['reactions']):
            wow_count = post['reactions']['wow'] # wow count
            reaction_count += wow_count
        else: wow_count = 0
        if('angry' in post['reactions']):
            angry_count = post['reactions']['angry'] # angry count
            reaction_count += angry_count
        else: angry_count = 0
        if('care' in post['reactions']):
            care_count = post['reactions']['care'] # care count
            reaction_count += care_count
        else: care_count = 0
        
    return reaction_count, like_count, love_count, care_count, haha_count, wow_count, sad_count, angry_count

# filter post data
def filter_post_data(post, group_name):
    (reaction_count, like_count, love_count, care_count, haha_count, wow_count, sad_count, angry_count) = reaction_counter(post)
    
    post_info = {
        "post_id": post["post_id"],
        "text": post["text"],
        "shares": post["shares"],
        "like_count": like_count,
        "love_count": love_count,
        "care_count": care_count,
        "haha_count": haha_count,
        "wow_count": wow_count,
        "sad_count": sad_count,
        "angry_count": angry_count,
        "reaction_count": reaction_count,
        "comments": post["comments"],
        "post_date": post["time"],
        "post_url": post["post_url"],
        "fetch_date": datetime.now(),
        "group_name": group_name
        }
    
    return post_info    
            
# scapre post from group
def scrape_group_post(group_link, group_name):
    post_list = []
    # scrape post
    for post in get_posts(group_link, 
                    options={"comments": True, "reactions": True, "allow_extra_requests": True}, 
                    extra_info=True, pages=PAGES_NUMBER):
       # if(post['time'].date() >= get_time_limit()): #limit the date from which to add to post_list
        if post["text"] != None: #eliminate posts that have no text
            post_info = filter_post_data(post, group_name)
            post_list.append(post_info)
            
    print("Scraped ", len(post_list), " posts from ", group_link)
    return post_list

# get group information
def scrape_group_info():
    group = get_group_info("jobITDaNang")
    
    group_info = {
        "group_id": group["id"],
        "group_name": group["name"],
        "group_description": group["about"],
        "group_members": group["members"]
    }
    
    return group_info

# scrape mutiple groups
def scrape_multiple_groups():
    for group in read_group_names():
        group_name = get_group_info(group)["name"]
        group_link = FANPAGE_LINK + group
        save_group_post(group_link, group_name)
        print("Resting...")
        time.sleep(60)

# save posts to excel file
def save_group_post(group_link, group_name):
    path=FOLDER_PATH + "/result" + "/post_result" + ".xlsx"
    # check if the file already exists
    if os.path.exists(path):
        # load the existing data from the file
        post_df_full = pd.read_excel(path)
    else:
        # create a new DataFrame if the file doesn't exist
        post_df_full = pd.DataFrame(columns=[])
        
    post_list = scrape_group_post(group_link, group_name)
        
    for post in post_list:
        post_entry = post
        fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
        fb_post_df = fb_post_df.transpose()
        post_df_full = post_df_full._append(fb_post_df)

    post_df_full.to_excel(path, index=False)    
    print("Saved ", len(post_list), " posts from ", group_name , " to ", path)
    
# save group information to excel file
def save_group_info():
    post_df_full = pd.DataFrame(columns = [])
    
    post_entry = scrape_group_info()
    
    fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
    fb_post_df = fb_post_df.transpose()
    post_df_full = post_df_full._append(fb_post_df)
    path=FOLDER_PATH + "/result" + "/group_result" + ".xlsx"
    post_df_full.to_excel(path, index=False)

# extract post text and date
def extract_post_text_and_date():
    result_list = []
    df = pd.read_excel('./result/post_result.xlsx')
    post_data = df[['text', 'post_date']]
    post_data.to_excel('./result/post_text_date.xlsx', index=False)

# save excel to mongodb
def save_excel_to_mongoDB():
    try:
        # connect to mongodb
        client = MongoClient(mongoURI)
        db = client[DATABASE_NAME]
        collection = db['Facebook_Posts']
        if client.server_info():
            print("Connected to MongoDB!")
        # read excel file
        path=FOLDER_PATH + "/result" + "/post_result" + ".xlsx"
        df = pd.read_excel(path)
        data = df.to_dict('records')
        # insert data to mongodb
        collection.delete_many({})
        collection.insert_many(data)
        print("Inserted ", len(data), " posts to MongoDB!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection closed!")

if __name__ == "__main__":
    print("Scraping...")    
    scrape_multiple_groups()
    #extract_post_text_and_date()
    save_excel_to_mongoDB()
    print("Done!")
    
# py scraper.py