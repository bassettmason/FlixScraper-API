import os
import re
import json
import logging
from typing import List, Dict
import requests
import openai
import praw
from praw.models import MoreComments

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
log_file = "scraper.log"
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)


def is_valid_reddit_url(url: str) -> bool:
    """
    Check if a given URL is a valid subreddit URL.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200 and "reddit.com/r/MovieSuggestions" in response.url:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {e}")
        return False


def get_comments(url: str) -> str:
    """
    Get the comments from a given Reddit URL.
    """
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENTID"),
        client_secret=os.getenv("REDDIT_SECRET"),
        user_agent="prawtutorial",
    )

    submission = reddit.submission(url=url)

    raw_comment_list = []

    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        else:
            if top_level_comment.score > 5:
                raw_comment_list.append(top_level_comment.body)

    united_string = ""

    for comment in raw_comment_list:
        united_string += comment + "\n"

    united_string = united_string.replace("\n\n\n", "\n\n")
    united_string = united_string.replace("\n\n", "\n")
    united_string = united_string.replace("-", "")
    united_string = united_string.replace("**", "")
    united_string = united_string.replace("*", "")

    logger.debug(f"get_comments united string: {united_string}")
    return united_string


def extract_titles(comments: str) -> List[Dict[str, str]]:
    """
    Extract movie titles from the comments using OpenAI's GPT-3 API.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'''Identify all entities of type 'MOVIE' in this text: Here are some comments that mention movies: {comments}
        JSON format example: [{{"title": "Movie Title", "year": Year}}, {{"title": "Movie Title","year": "null"}}, {{'title': "Movie Title","year": Year}}]''',
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0,
        )

        # Extract the recognized entities from the API response
        result = response["choices"][0]["text"].strip().replace("Answer: ", "")
        logger.debug(f"extract_titles result: {result}")
        result_dictified = json.loads(result)
        logger.debug(f"extract_titles result_dictified: {result_dictified}")
        return result_dictified
    except openai.Error as e:
        logger.error(f"OpenAI Error: {e}")
        return []


def extract_title(url: str) -> str:
    """
    Extract the submission title from a given Reddit URL.
    """
    match = re.search("/r/(.*)/comments/([^/]+)/(.*)/?$", url)
    if match:
        return match.group(3).rstrip("/")
    else:
        return ""



