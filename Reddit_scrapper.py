import praw
import pandas as pd
import config
from datetime import datetime, timedelta
from time import sleep
from Logger import configure_logging, log_message


def account_login():
    scrp_reddit_pf = praw.Reddit(username=config.username,
                                 password=config.password,
                                 client_id=config.client_id,
                                 client_secret=config.client_secret,
                                 user_agent='Xero_Sam Scrapper_test')
    return scrp_reddit_pf


def scraper_function_with_shifting_time(scrp_start_date, scrp_end_date, scrp_n):
    search_query = "immigrants in:usa"
    subreddit = reddit_pf.subreddit('all').search(query=search_query, time_filter='all', sort='new', limit=10)
    for submission in subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)

        submission.comments.replace_more(limit=None)  # making sure to retrieve all comments
        for comment in submission.comments.list():
            topics_comments["cmt_id"].append(comment.id)
            topics_comments["cmt_body"].append(comment.body)
            topics_comments["cmt_author"].append(comment.author)
        df = pd.DataFrame(topics_dict)
        print(df)
        df2 = pd.DataFrame(topics_comments)
        print(df2)
        df.to_csv('static/reddit_immigration.csv', index=False)
        df2.to_csv('static/reddit_immigration_comments.csv', index=False)

    log_message(f"Iteration number:Success {scrp_n}")
    sleep(120)
    return


try:
    reddit_pf = account_login()
    configure_logging(filename='error.log')
    topics_dict = {"date_start": [], "date_end": [], "title": [], "score": [], "id": [], "url": [], "comms_num": [],
                   "created": [], "body": []}
    topics_comments = {"date_start": [], "date_end": [], "cmt_id": [], "cmt_body": [], "cmt_author": []}

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    n = 1
    while end_date - start_date <= timedelta(days=365 * 2):
        scraper_function_with_shifting_time(start_date, end_date, n)
        # Update time range for the next iteration
        end_date = start_date - timedelta(days=1)  # Move back by 1 day
        start_date = end_date - timedelta(days=30)
        n = n + 1

except FileNotFoundError as e:
    print(f"Environmental variables not setup correctly, check for files: {e}")
except (ValueError, TypeError) as e:
    print(f"Error execution: {e}")
except (IOError, PermissionError) as e:
    print(f"Error system: {e}")
