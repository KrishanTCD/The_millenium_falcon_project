from datetime import datetime, timedelta
import praw
import pandas as pd
import config
import os
from time import sleep
from Logger import configure_logging  # Assuming this is a custom logger

def append_to_csv(df, filename):
    # Check if the file exists
    file_exists = os.path.isfile(filename)
    df.to_csv(filename, mode='a', index=False, header=not file_exists)

def account_login():
    scrp_reddit_pf = praw.Reddit(username=config.username,
                                 password=config.password,
                                 client_id=config.client_id,
                                 client_secret=config.client_secret,
                                 user_agent='Xero_Sam Scrapper_test')
    print("Logged IN")
    return scrp_reddit_pf

def scraper_function_with_shifting_time(start_date_fn, end_date_fn, scrp_n):
    search_query = "immigrants OR immigration OR Asylum OR Refugee OR Border Control OR Deportation in:uk"
    subreddit = reddit_pf.subreddit('all').search(query=search_query, time_filter='all', sort='new', limit=100)
    max_start_date = datetime.strptime('2012-12-12', '%Y-%m-%d')
    min_start_date = datetime.strptime('2012-12-12', '%Y-%m-%d')

    for submission in subreddit:
        if (datetime.utcfromtimestamp(submission.created_utc).replace(hour=0, minute=0, second=0,
                                                                      microsecond=0) > start_date_fn) and (
                datetime.utcfromtimestamp(submission.created_utc).replace(hour=0, minute=0, second=0,
                                                                          microsecond=0) <= end_date_fn):
            topics_dict['date_start'].append(
                datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created_utc)
            topics_dict["body"].append(submission.selftext if submission.selftext else None)


    df = pd.DataFrame(topics_dict)
    print(df)
    append_to_csv(df, 'reddit_immigration1_uk.csv')

    print(f"Iteration completed: {scrp_n}, entries added: {len(topics_dict)}")
    start_dates_list = topics_dict.get('date_start', [])
    if start_dates_list:
        # Converting date strings to datetime objects
        start_dates = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in start_dates_list]
        # Finding the maximum and minimum dates
        max_start_date = max(start_dates)
        min_start_date = min(start_dates)
    print(f"Time period of {scrp_n}th iteration: {max_start_date} : {min_start_date} ")
    sleep(120)


try:
    global reddit_pf, topics_dict
    reddit_pf = account_login()
    configure_logging(filename='error.log')
    topics_dict = {"date_start": [], "title": [], "score": [], "id": [], "url": [], "comms_num": [],
                   "created": [], "body": []}
    # Initialise the dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    n = 1
    while end_date - start_date <= timedelta(days=60):
        # Update time range for the next iteration
        scraper_function_with_shifting_time(start_date, end_date, n)
        end_date = start_date - timedelta(days=1)  # Move back by 1 day
        start_date = start_date - timedelta(days=30)
        print(n)
        n += 1
        if n == 5:
            sleep(240)

except FileNotFoundError as e:
    print(f"Environmental variables not setup correctly, check for files: {e}")
except Exception as e:
    print(f"Error: {e}")
