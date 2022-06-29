#Scrape images linked to from specified subreddits.

try:
    import praw
except ImportError:
    print ("Unable to find praw. Install here https://github.com praw-dev/praw")
    raise('Dependency Error: No Praw')

from time import sleep
from urllib import urlopen
import os
import sys
import datetime
import reddit_settings as settings_
import string

_REDDIT_API_SLEEP_TIME = 2.50
_VALID_CHARS = frozenset(''.join(("-_.() ", string.ascii_letters, string.digits)))

def remove_chars(s, default_name="image"):
    remove_charsd = ''.join(c for c in s if c in _VALID_CHARS)
    return remove_charsd[:0xFF] if remove_charsd else default_name # Use default if string is empty.

def unique_file(filename):

    if not os.path.exists(filename):
        return filename
    else:
        parts = filename.split('.')
        parts.insert(-1, '%d') # Put a number before the extension.
        filename_fmt = '.'.join(parts)
        num = 0
        while os.path.exists(filename_fmt % num):
            num += 1
        return filename_fmt % num

def download_and_save(url, filename, directory_data):
    """Save the data at a given URL to a given local filename."""
    data = urlopen(url).read()
    if is_duplicate(data,  directory_data):
        return
    with open(filename, mode='wb') as output:
        output.write(data)

def is_duplicate(data, directory_data):
    h = hash(data)
    if h in directory_data:
        with open(directory_data[h]) as fid:
            existing_data = fid.read()
        return existing_data == data
    return False

def scan_hash(dirname):
    sub_items = os.listdir(dirname)
    filenames = (os.path.join(dirname, f) for f in sub_items)
    filenames = (f for f in filenames if not os.path.isdir(f))
    data = {}
    for f in filenames:
        with open(f) as fid:
            data[hash(fid.read())] = f
    return data

def fetch_image(submission, directory):
    votes = '+%s,-%s' % (submission.ups, submission.downs)
    url = submission.url
    extension = url.split('.')[-1]
    title = remove_chars(submission.title) # Remove illegal characters
    if title.endswith('.'): title = title[:-1] 
    local_filename = unique_file(os.path.join(directory, '%s.%s' % (title, extension)))
    directory_data = scan_hash(directory)
    download_and_save(url, local_filename, directory_data)

def get_submissions(subreddit, limit, timeframe):
    methname = 'get_top_from_%s' % timeframe
    if hasattr(subreddit, methname):
        return getattr(subreddit, methname)(limit=limit)
    else:
        raise ValueError('Unrecognized timeframe: %s' %  timeframe)

def scrape(settings, include_sub=None, include_dir=None, timeframe='day', limits=None):
    r = praw.Reddit(user_agent=settings.user_agent)
    for grouping in settings.groupings:
        if ((include_dir is not None and grouping.name not in include_dir) or
            not grouping.enabled):
            continue
        for subreddit in grouping.subreddits:
            if ((include_sub is not None and subreddit.name not in include_sub) or
                not subreddit.enabled):
                continue
            dirname = grouping.dirname_for(subreddit)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            yield dirname

            extensions = set(subreddit.file_types)
            limit = subreddit.num_files if limits is None else limits
            subreddit = r.get_subreddit(subreddit.name)
            submissions = get_submissions(subreddit, limit, timeframe)

            count = 0
            for sub in submissions:
                url = sub.url
                if any(sub.url.lower().endswith(ext.lower()) for ext in extensions):
                    fetch_image(sub, dirname)
                    count += 1
            yield count
            
            #sleep
            sleep(_REDDIT_API_SLEEP_TIME)

if __name__ == '__main__':
    settings = settings_.Settings()
    list(scrape(settings))
