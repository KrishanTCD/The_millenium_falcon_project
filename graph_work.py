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


def scraper_function_with_shifting_time(node_dict2, edge_dict2, scrp_n):
    search_query = "immigrants OR immigration OR Asylum OR Refugee OR Border Control OR Deportation in:uk"
    subreddit = reddit_pf.subreddit('all').search(query=search_query, time_filter='all', sort='new', limit=50000)

    for submission in subreddit:
        # Reset topics_comments for each new submission to maintain consistent list lengths
        # topics_comments = {"date_start": [], "cmt_id": [], "cmt_body": [], "cmt_author": []}

        # Append submission data to topics_dict
        node_dict2["Id"].append(submission.id)
        node_dict2["Label"].append(submission.id)
        node_dict2["Role"].append("Initiator")

        submission.comments.replace_more(limit=None)  # Ensure all comments are retrieved

        if submission.comments.list():
            for comment in submission.comments.list():
                node_dict2["Id"].append(comment.id)
                node_dict2["Label"].append(comment.id)
                node_dict2["Role"].append("Commentor")
                edge_dict2["Source"].append(submission.id)
                edge_dict2["Target"].append(comment.id)
                edge_dict2["Type"].append(comment.body if comment.body else None)

        print(node_dict2)
        print(edge_dict2)
        if (len(v) > 0 for v in node_dict2.values()):
            df = pd.DataFrame(node_dict2)
            append_to_csv(df,
                          'C:/Users/Krishan/PycharmProjects/The_millenium_falcon_project/The_millenium_falcon_project/static'
                          '/reddit_immigration_uk_node.csv')
        if (len(v) > 0 for v in edge_dict2.values()):
            df2 = pd.DataFrame(edge_dict2)
            append_to_csv(df2,
                          'C:/Users/Krishan/PycharmProjects/The_millenium_falcon_project/The_millenium_falcon_project/static'
                          '/reddit_immigration_comments_uk_edge.csv')

    log_message(f"Iteration number: Success {scrp_n}")
    sleep(2)


try:
    reddit_pf = account_login()
    configure_logging(filename='error.log')
    topics_dict = {"date_start": [], "title": [], "score": [], "id": [], "url": [], "comms_num": [],
                   "created": [], "body": []}
    node_dict = {"Id": [], "Label": [], "Role": []}
    edge_dict = {"Source": [], "Target": [], "Type": []}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    n = 1
    scraper_function_with_shifting_time(node_dict, edge_dict, n)


except FileNotFoundError as e:
    print(f"Environmental variables not setup correctly, check for files: {e}")
except (ValueError, TypeError) as e:
    print(f"Error execution: {e}")
except (IOError, PermissionError) as e:
    print(f"Error system: {e}")
