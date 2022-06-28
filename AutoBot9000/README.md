<h1>Reddit AutoBot9000 </h1>

![reddit]('./img/example.gif')

There are two parts to this bot, the auto_poster and the image_scraper. 

<h2> Selenium Poster</h2>
=======
Head to the env.py and fill in your Data, reddit username, password, title, and subreddit

next run the reddit_auto_post.py and it should begin to cross post your subreddit to a list of 


<h2> Reddit Scraper</h2>
=======

<h2> Install Dependencies and Check Environment </h2>

```
python --version
```

-Updated your OS to the latest system, and make sure you are running a version of python that works with Tkinter

```
 Pip install Tk
```
```
 Pip install tkinter
```
```
 Pip install python-tk
```

```
 Pip install python3-tk
```

```
 Pip install tk-dev
```

```
 Pip install tcl
```
=======

<h2> Start up the GUI </h2>


Run 
```gui.py```
to configure your settings. Afterwards when you run `python scraper.py` it will
use your saved settings. Feel free to schedule it to run dailt.


Reddit Scraper allows you to scrape the top images (or other file formats) 
from selected subreddits into selected directories on your machine.
You may configure how many files to scrape, what extensions to include,
which subreddits to scrape from, and which directories to write to.

Uses Python Reddit API Wrapper: https://github.com/praw-dev/praw
```
pip install praw
```

