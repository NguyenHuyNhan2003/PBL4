from facebook_scraper import get_posts, get_group_info
from datetime import datetime, timedelta
import pandas as pd

FANPAGE_LINK ="groups/jobITDaNang"
FOLDER_PATH = "./"
PAGES_NUMBER = 2

def get_time_limit():
    days_before = (datetime.now() - timedelta(days=7)).date() #date from which to scrap posts
    #print(days_before)
    return days_before

#scapre post from group
def scrape_group_post():
    post_list = []
    #define reacrions counter
    reaction_count = 0
    like_count = 0
    love_count = 0
    care_count = 0
    haha_count = 0
    wow_count = 0
    sad_count = 0
    angry_count = 0
    #scrape post
    for post in get_posts(FANPAGE_LINK, 
                    options={"comments": True, "reactions": True, "allow_extra_requests": True}, 
                    extra_info=True, pages=PAGES_NUMBER):
        if(post['time'].date() >= get_time_limit()): #limit the date from which to add to post_list
            if(post['reactions'] != None): #if there is reaction
                if('like' in post['reactions']):
                    like_count = post['reactions']['like'] #like count
                    reaction_count += like_count
                else: like_count = 0
                if('love' in post['reactions']):
                    love_count = post['reactions']['love'] #love count
                    reaction_count += love_count
                else:  love_count = 0
                if('haha' in post['reactions']):
                    haha_count = post['reactions']['haha'] #haha count
                    reaction_count += haha_count
                else: haha_count = 0
                if('sad' in post['reactions']):
                    sad_count = post['reactions']['sad'] #sad count
                    reaction_count += sad_count
                else: sad_count = 0
                if('wow' in post['reactions']):
                    wow_count = post['reactions']['wow'] #wow count
                    reaction_count += wow_count
                else: wow_count = 0
                if('angry' in post['reactions']):
                    angry_count = post['reactions']['angry'] #angry count
                    reaction_count += angry_count
                else: angry_count = 0
                if('care' in post['reactions']):
                    care_count = post['reactions']['care'] #care count
                    reaction_count += care_count
                else: care_count = 0
            post_info = {
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
                "post_date": post["time"]
                }
            post_list.append(post_info)
    
    print(len(post_list))
    return post_list

#get group information
def scrape_group_info():
    group = get_group_info("jobITDaNang")
    group_info = {
        "group_id": group["id"],
        "group_name": group["name"],
        "group_description": group["about"],
        "group_members": group["members"]
    }
    return group_info

#save post to excel file
def save_group_post():
    post_df_full = pd.DataFrame(columns = [])
    for post in scrape_group_post():
        post_entry = post
        fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
        fb_post_df = fb_post_df.transpose()
        post_df_full = post_df_full._append(fb_post_df)
        path=FOLDER_PATH + "/result" + "/post_result" + ".xlsx"
        post_df_full.to_excel(path, index=False)
    
#save group information to excel file
def save_group_info():
    post_df_full = pd.DataFrame(columns = [])
    post_entry = scrape_group_info()
    fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
    fb_post_df = fb_post_df.transpose()
    post_df_full = post_df_full._append(fb_post_df)
    path=FOLDER_PATH + "/result" + "/group_result" + ".xlsx"
    post_df_full.to_excel(path, index=False)
    

if __name__ == "__main__":
    save_group_post()
    #save_group_info()