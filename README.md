<h1>Reddit AutoBot9000 </h1>

![reddit](https://github.com/Mark-777-0/AutoBot9000/blob/main/AutoBot9000/img/example.gif)

There are two parts to this bot, the auto_poster and the image_scraper. 

<h2> Selenium Poster</h2>

Head to the env.py and fill in your Data, reddit username, password, title, and subreddit

next run the reddit_auto_post.py and it should begin to cross post your subreddit to a list of  


<h2> Reddit Scraper</h2>


<h2> Install Dependencies and Check Environment </h2>

```
python --version
```

-Updated your OS to the latest system, and make sure you are running a version of python that works with PRAW
```
pip install praw
```

```
 Pip install tcl
```
=======

<h2> Fill in Settings</h2>


Alter
```reddit_settings.py```
to configure your settings. Afterwards when you run `python scraper.py` it will
use your saved settings. Feel free to schedule it to run daily.


The AutoBot9000 will allow you to download the top images from any subreddit. Specifying file formats and directories.

Uses Python Reddit API Wrapper: https://github.com/praw-dev/praw

Credit to chloe-47/reddit_scraper for help with the scraper section of this bot

Uses Selenium: https://www.selenium.dev/documentation/
