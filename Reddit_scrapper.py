import praw
import pandas as pd
import config
from datetime import datetime, timedelta
from time import sleep
from Logger import configure_logging, log_message
import os
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
    return scrp_reddit_pf


def scraper_function_with_shifting_time(scrp_n):
    search_query = "immigrants OR immigration OR Asylum OR Refugee OR Border Control OR Deportation in:uk"
    subreddit = reddit_pf.subreddit('all').search(query=search_query, time_filter='all', sort='new', limit=50000)

    for submission in subreddit:
        # Reset topics_comments for each new submission to maintain consistent list lengths
        topics_comments = {"date_start": [], "cmt_id": [], "cmt_body": [], "cmt_author": []}

        # Append submission data to topics_dict
        topics_dict['date_start'].append(datetime.utcfromtimestamp(submission.created).strftime('%Y-%m-%d %H:%M:%S'))
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext if submission.selftext else None)  # Handle empty body

        submission.comments.replace_more(limit=None)  # Ensure all comments are retrieved

        if submission.comments.list():
            for comment in submission.comments.list():
                topics_comments["date_start"].append(datetime.utcfromtimestamp(comment.created).strftime('%Y-%m-%d %H:%M:%S'))
                topics_comments["cmt_id"].append(comment.id)
                topics_comments["cmt_body"].append(comment.body if comment.body else None)  # Handle empty comment body
                topics_comments["cmt_author"].append(comment.author if comment.author else None)  # Handle deleted users

        print(topics_dict)
        print(topics_comments)
        for v in topics_comments.values():
            print(v, " ", len(v))
        if (len(v) > 0 for v in topics_dict.values()):
            df = pd.DataFrame(topics_dict)
            append_to_csv(df,
                'C:/Users/Krishan/PycharmProjects/The_millenium_falcon_project/The_millenium_falcon_project/static'
                '/reddit_immigration_uk.csv')
        if (len(v) > 0 for v in topics_comments.values()):
            df2 = pd.DataFrame(topics_comments)
            append_to_csv(df2,
                'C:/Users/Krishan/PycharmProjects/The_millenium_falcon_project/The_millenium_falcon_project/static'
                '/reddit_immigration_comments_uk.csv')

    log_message(f"Iteration number: Success {scrp_n}")
    sleep(2)


try:
    reddit_pf = account_login()
    configure_logging(filename='error.log')
    topics_dict = {"date_start": [], "title": [], "score": [], "id": [], "url": [], "comms_num": [],
                   "created": [], "body": []}

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    n = 1
    scraper_function_with_shifting_time(n)
    # while end_date - start_date <= timedelta(days=365 * 2):
    #     scraper_function_with_shifting_time(n)
    #     # Update time range for the next iteration
    #     end_date = start_date - timedelta(days=1)  # Move back by 1 day
    #     start_date = end_date - timedelta(days=30)
    #     n = n + 1

except FileNotFoundError as e:
    print(f"Environmental variables not setup correctly, check for files: {e}")
except (ValueError, TypeError) as e:
    print(f"Error execution: {e}")
except (IOError, PermissionError) as e:
    print(f"Error system: {e}")
