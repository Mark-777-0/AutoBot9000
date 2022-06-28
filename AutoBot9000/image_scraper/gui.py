# gui.py
import tk
from tk import *
from tk import Tkinter 
from tk import tkFileDialog 

from tk import tkSimpleDialog 
from tk import tkMessageBox 
import requests
import subprocess
import os

import functools
wraps = functools.wraps

import reddit_settings
import scraper
import itertools

SELECTION_COLOR = '#000'
BLANK_COLOR = '#ddd'

def gui(fn):
    @wraps(fn)
    def updater(self, *args, **kwargs):
        val = fn(self, *args, **kwargs)
        self.update_gui()
        return val
    return updater

class ScraperWindow(object):
    def __init__(self):
        self.root = self.get_root()
        self.state = GUIState()
        self.filetype = None
        self.settings = reddit_settings.Settings()
        self.add_elements()
        self.update_gui()
        self.root.after(100, self.center_window)
        self.start_timer()
        self.root.mainloop()

    def start_timer(self):
        self.prev_state = self.state.tuple()
        self.prev_entry = ''
        self.root.after(100, self.timer)

    def timer(self):
        if self.number_of_files_entry.get() != self.prev_entry:
            num = self._int_in_entry(self.number_of_files_entry)
            if num is not None:
                self.subreddit.num_files = num
        self._entry_update(self.number_of_files_entry, self.subreddit.num_files if
                           self.subreddit else '')

        self.prev_entry = self.number_of_files_entry.get()

        
        self.grouping_listbox.selection_clear(0, Tkinter.END)
        self.subreddit_listbox.selection_clear(0, Tkinter.END)
        self.file_types_listbox.selection_clear(0, Tkinter.END)
        if not self.prev_state == self.state.tuple():
            self.update_gui()
        self.prev_state = self.state.tuple()
        self.root.after(100, self.timer)

    def get_root(self):
        """Create a new window."""
        root = Tkinter.Tk()
        root.title("Reddit Scraper")
        return root

    def center_window(self):
        w = float(self.root.winfo_screenwidth())
        h = float(self.root.winfo_screenheight())
        rootsize = tuple(int(i) for i in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - rootsize[0]/2
        y = h/2 - rootsize[1]/2
        self.root.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))

    def scrape_all(self, timeframe='day', limits=None):
        self._scrapes(None, None, timeframe=timeframe, limits=limits)

    def scrape_current_sub(self, timeframe='day', limits=None):
        if self.subreddit:
            self._scrapes([self.subreddit.name], None, timeframe=timeframe,
                          limits=limits)
        else:
            tkMessageBox.askokcancel("", "Please select a subreddit to scrape.")

    def scrape_current_dir(self, timeframe='day', limits=None):
        if self.grouping:
            self._scrapes(None, [self.grouping.name], timeframe=timeframe,
                          limits=limits)
        else:
            tkMessageBox.askokcancel("", "Please select a directory to scrape.")
            
    def _scrapes(self, include_sub, include_dir, expose=True, alert_when_done=True,
                 timeframe='day', limits=None):
        try:
            count = 0
            for x in scrape.scrape(self.settings, include_sub=include_sub, include_dir=include_dir,
                                   timeframe=timeframe, limits=limits):
                if isinstance(x, int):
                    count += x
                    continue
                if expose:
                    reveal(x)
        except requests.ConnectionError:
            tkMessageBox.askokcancel("Connection Error",
                                     "Could not connect to Reddit. Check your internet settings, "
                                     "and make sure Reddit isn't down.")
        else:
            tkMessageBox.askokcancel("", "Scrape Complete! %d files downloaded." % count)

    def add_elements(self):
        root = self.root
        self.add_groupings_pane(root)
        self.add_subreddits_pane(root)
        self.add_details_pane(root)

    def add_groupings_pane(self, root):
        pane = Tkinter.Frame(root)
        # List of directories,
        self.grouping_listbox = Tkinter.Listbox(pane)
        self.grouping_listbox.grid(row=0, column=0, sticky=Tkinter.N)
        self.grouping_listbox.bind('<Button-1>', self.grouping_listbox_click)

        row_1_frame = Tkinter.Frame(pane)

        # Add directory button,        
        add_dir_button = Tkinter.Button(row_1_frame, text=" + ", command=self.add_directory)
        add_dir_button.pack(side=Tkinter.LEFT)

        # Reomve directory button,
        del_dir_button = Tkinter.Button(row_1_frame, text=" - ", command=self.del_directory)
        del_dir_button.pack(side=Tkinter.LEFT)
        
        # Enable/Disable button
        self.enable_button = Tkinter.Button(row_1_frame, text="Disable", command=self.enable)
        self.enable_button.pack(side=Tkinter.LEFT)

        row_1_frame.grid(row=1, column=0)
        
        # Scrape all button
        scrape_all_button = Tkinter.Button(pane, text="Scrape All", command=self.scrape_all)
        scrape_all_button.grid(row=2, column=0)

        row_3_frame = Tkinter.Frame(pane)
        
        # Load/Save
        load_button = Tkinter.Button(row_3_frame, text="Load", command=self.load)
        load_button.pack(side = Tkinter.LEFT)

        save_button = Tkinter.Button(row_3_frame, text="Save", command=self.save)
        save_button.pack(side=Tkinter.LEFT)

        row_3_frame.grid(row=3, column=0)
        
        pane.grid(row=0, column=0)


    def add_subreddits_pane(self, root):
        pane = Tkinter.Frame(root)

        # List of subreddits,
        self.subreddit_listbox = Tkinter.Listbox(pane)
        self.subreddit_listbox.grid(row=0, column=0, sticky=Tkinter.N)
        self.subreddit_listbox.bind('<Button-1>', self.subreddit_listbox_click)

        row_1_frame = Tkinter.Frame(pane)

        # Add subreddit button
        add_sub_button = Tkinter.Button(row_1_frame, text=" + ", command=self.add_subreddit)
        add_sub_button.pack(side=Tkinter.LEFT)

        # Remove subreddit button
        del_sub_button = Tkinter.Button(row_1_frame, text=" - ", command=self.del_subreddit)
        del_sub_button.pack(side=Tkinter.LEFT)

        # Enable/Disable button
        self.enable_sub_button = Tkinter.Button(row_1_frame, text="Disable", command=self.enable_sub)
        self.enable_sub_button.pack(side=Tkinter.LEFT)

        row_1_frame.grid(row=1, column=0)

        self.scrape_dir_button = Tkinter.Button(pane, text="Scrape Directory", command=self.scrape_current_dir)
        self.scrape_dir_button.grid(row=2, column=0)
        
        # Create folder for each subreddit (checkbox)

        row_3_frame = Tkinter.Frame(pane)
        
        self.persubvar = Tkinter.BooleanVar(row_3_frame)
        self.persubbutton  = Tkinter.Checkbutton(row_3_frame, command=self.persub, var=self.persubvar)
        self.persubbutton.pack(side=Tkinter.LEFT)
        self.persublabel = Tkinter.Label(row_3_frame, text='Create a directory for each subreddit',
                                         wraplength=130)
        self.persublabel.pack(side=Tkinter.LEFT)

        row_3_frame.grid(row=3, column=0)

        pane.grid(row=0, column=1)

    def add_details_pane(self, root):
        pane = Tkinter.Frame(root, width=500)
        # Subreddit name
        self.subreddit_name_label = Tkinter.Label(pane, text='', anchor=Tkinter.N)
        self.subreddit_name_label.grid(row=0, column=0)

        # Number of files to download (INC/DEC)
        row_1_frame = Tkinter.Frame(pane)
        
        self.number_of_files_label = Tkinter.Label(row_1_frame, text='Files to Download:')
        self.number_of_files_label.pack(side=Tkinter.LEFT)

        self.number_of_files_entry = Tkinter.Entry(row_1_frame, width=3)
        self.number_of_files_entry.pack(side=Tkinter.LEFT)

        row_1_frame.grid(row=1, column=0)

        # File types to include (list box?) (ADD/REM)
        self.file_types_label = Tkinter.Label(pane, text="Include these extensions:")
        self.file_types_label.grid(row=2, column=0)
        
        self.file_types_listbox = Tkinter.Listbox(pane, height=5)
        self.file_types_listbox.grid(row=3, column=0)
        self.file_types_listbox.bind('<Button-1>', self.file_types_listbox_click)

        row_4_frame = Tkinter.Frame(pane)
        add_ext_button = Tkinter.Button(row_4_frame, text=' + ', command=self.add_ext)
        add_ext_button.pack(side=Tkinter.LEFT)

        del_ext_button = Tkinter.Button(row_4_frame, text=' - ', command=self.del_ext)
        del_ext_button.pack(side=Tkinter.LEFT)

        row_4_frame.grid(row=4, column=0)
        
        # Last scraped (LABEL)
        # Open folder in finder/explorer (BUTTON)
        
        # Scrape now button
        self.scrape_now_button = Tkinter.Button(pane, text="Scrape Subreddit", command=self.scrape_current_sub)
        self.scrape_now_button.grid(row=5, column=0)

        pane.grid(row=0, column=2)

    @gui
    def grouping_listbox_click(self, event):
        index = self.grouping_listbox.nearest(event.y)
        self.state.grouping = self.grouping_listbox.get(index)
        self.state.subreddit = None

    @gui
    def subreddit_listbox_click(self, event):
        if self.grouping is None:
            return
        index = self.subreddit_listbox.nearest(event.y)
        self.state.subreddit = self.subreddit_listbox.get(index)

    @gui
    def file_types_listbox_click(self, event):
        if self.subreddit is None:
            return
        index = self.file_types_listbox.nearest(event.y)
        self.filetype = self.file_types_listbox.get(index)
        if self.filetype == '<Extensions>':
            self.filetype = None

    def persub(self):
        if self.grouping:
            self.grouping.subdir_per_subreddit = self.persubvar.get()

    @property
    def grouping(self):
        if self.state.grouping is None: return None
        return self.settings[self.state.grouping]

    @property
    def subreddit(self):
        if self.state.subreddit is None: return None
        return self.grouping[self.state.subreddit]

    def update_gui(self):
        ## Grouping listbox
        desired_grouping_listbox = [group.shortname for group in self.settings.groupings]
        if not desired_grouping_listbox:
            desired_grouping_listbox = ['<Directories>']
        self._listbox_update(self.grouping_listbox, desired_grouping_listbox)

        # Color
        for i in xrange(self.grouping_listbox.size()):
            grp = self.settings[self.grouping_listbox.get(i)]
            if grp is None or grp.enabled:
                fg_color = 'black'
            else:
                fg_color = 'gray'
            self.grouping_listbox.itemconfig(i, bg=BLANK_COLOR, fg=fg_color)
        if self.state.grouping:
            index = self.grouping_listbox.get(0, Tkinter.END).index(self.state.grouping)
            self.grouping_listbox.itemconfig(index, bg=SELECTION_COLOR)
            self.grouping_listbox.selection_clear(0, Tkinter.END)

        ## Enable buttons
        self.enable_button.config(text='      ' if not self.grouping else
                                  'Disable' if self.grouping.enabled else 'Enable')
        self.enable_sub_button.config(text='      ' if not self.subreddit else
                                      'Disable' if self.subreddit.enabled else 'Enable')


        ## Subreddit listbox
        if self.grouping is None:
            desired_subreddit_listbox = ['<Subreddits>']
        else:
            desired_subreddit_listbox = [sub.name for sub in self.grouping.subreddits]
        if not desired_subreddit_listbox:
            desired_subreddit_listbox = ['<Subreddits>']
        self._listbox_update(self.subreddit_listbox, desired_subreddit_listbox)

        # Color
        for i in xrange(self.subreddit_listbox.size()):
            sub = None if not self.grouping else self.grouping[self.state.subreddit]
            if sub is None or sub.enabled:
                fg_color = 'black'
            else:
                fg_color = 'gray'
            self.subreddit_listbox.itemconfig(i, bg=BLANK_COLOR, fg=fg_color)
        if self.state.subreddit:
            index = self.subreddit_listbox.get(0, Tkinter.END).index(self.state.subreddit)
            self.subreddit_listbox.itemconfig(index, bg=SELECTION_COLOR)
            self.subreddit_listbox.selection_clear(0, Tkinter.END)

        # Checkbox
        if self.grouping:
            self.persubvar.set(self.grouping.subdir_per_subreddit)

        ## Details Frame
        if self.subreddit is not None:
            self.subreddit_name_label.config(text='/r/'+self.state.subreddit)
            #self._entry_update(self.number_of_files_entry, self.ubreddit.num_files)
            desired_filetypes = self.subreddit.file_types
            self._listbox_update(self.file_types_listbox, desired_filetypes)
        else:
            self.subreddit_name_label.config(text='')
            self.filetype = None
            #self._entry_update(self.number_of_files_entry, '')
            self._listbox_update(self.file_types_listbox, ['<Extensions>'])

        ## Color
        for i in xrange(self.file_types_listbox.size()):
            self.file_types_listbox.itemconfig(i, bg=BLANK_COLOR)
        if self.filetype:
            index = self.file_types_listbox.get(0, Tkinter.END).index(self.filetype)
            self.file_types_listbox.itemconfig(index, bg=SELECTION_COLOR)

    def _listbox_update(self, listbox, desired_values):
        current_values = listbox.get(0, Tkinter.END)
        to_remove = set(current_values) - set(desired_values)
        to_add = set(desired_values) - set(current_values)
        for item in to_remove:
            idx = listbox.get(0, Tkinter.END).index(item)
            listbox.delete(idx)
        for item in to_add:
            listbox.insert(Tkinter.END, item)

    def _entry_update(self, entry, desired_text):
        desired_text = str(desired_text)
        if entry.get() != desired_text:
            entry.delete(0, Tkinter.END)
            entry.insert(0, desired_text)

    def _int_in_entry(self, entry):
        contents = entry.get()
        if contents == '': return 0
        contents = ''.join(c for c in contents if c in '0123456789.')
        if contents == '': return None
        return int(float(contents))

    @gui
    def add_subreddit(self):
        if self.grouping is None:
            tkMessageBox.askokcancel("", "Please select a directory first.")
        else:
            s = tkSimpleDialog.askstring("Add a Subreddit", "Enter the name of the subreddit: /r/")
            if not s:
                return
            if s.startswith('/r/'):
                s = s[len('/r/'):]
            self.grouping.add_subreddit(s)
            self.state.subreddit = s
            self.ask_for_all_time()

    def ask_for_all_time(self):
        if tkMessageBox.askokcancel("Added Subreddit", "Successfully added /r/%s!"% self.subreddit.name +
                                    " Scrape this subreddit's history now?"):
            
            self.scrape_current_sub(timeframe='all', limits=20)
            
    @gui
    def del_subreddit(self):
        if self.subreddit:
            current_items = list(self.subreddit_listbox.get(0, Tkinter.END))
            current_idx = current_items.index(self.subreddit.name)
            del self.grouping[self.subreddit.name]
            del current_items[current_idx]
            if current_items:
                new_idx = max(0, min(len(current_items)-1, current_idx))
                self.state.subreddit = current_items[new_idx]
            else:
                self.state.subreddit = None
        else:
            tkMessageBox.askokcancel("", "Please select a subreddit to remove.")

    @gui
    def add_ext(self):
        if self.subreddit is None:
            tkMessageBox.askokcancel("", "Please select a subreddit first.")
        else:
            s = tkSimpleDialog.askstring("Add an extension", "Enter the extension:")
            if not s:
                return
            s = s.upper().strip('.')
            self.subreddit.add_file_type(s)

    @gui
    def del_ext(self):
        if self.filetype:
            current_items = list(self.file_types_listbox.get(0, Tkinter.END))
            current_idx = current_items.index(self.filetype)
            self.subreddit.rm_filetype(self.filetype)
            del current_items[current_idx]
            if current_items:
                new_idx = max(0, min(len(current_items)-1, current_idx))
                self.filetype = current_items[new_idx]
            else:
                self.filetype = None
        else:
            tkMessageBox.askokcancel("", "Please select an extension to remove.")

    @gui
    def save(self):
        self.settings.save()

    @gui
    def load(self, explicit=True):
        try:
            self.settings.load(explicit)
        except ValueError:
            reset = tkMessageBox.askokcancel("", "Cannot read your config file. Reset?")
            if reset:
                self.settings.reset()
        except NameError:
            reset = tkMessageBox.askokcancel("", "No config file found. Create a new one?")
            if reset:
                self.settings.reset()
        self.state = GUIState()

    @gui
    def add_directory(self):
        dirname = tkFileDialog.askdirectory()
        if dirname:
            self.settings.add_grouping(dirname)
            self.state.grouping = self.settings[dirname].shortname
            self.state.subreddit = None

    @gui
    def del_directory(self):
        if self.grouping:
            current_items = list(self.grouping_listbox.get(0, Tkinter.END))
            current_idx = current_items.index(self.grouping.shortname)
            del self.settings[self.state.grouping]
            del current_items[current_idx]
            if current_items:
                new_idx = max(0, min(len(current_items)-1, current_idx))
                self.state.grouping = current_items[new_idx]
                self.state.subreddit = None
            else:
                self.state.grouping = None
            
        else:
            tkMessageBox.askokcancel("", "Please select a directory to remove.")

    @gui
    def enable(self):
        if self.grouping:
            self.grouping.enable()

    @gui
    def enable_sub(self):
        if self.subreddit:
            self.subreddit.enable()
            

class GUIState(object):
    def __init__(self, grouping=None, subreddit=None):
        self.grouping = grouping
        self.subreddit = subreddit
    def tuple(self):
        return (self.grouping, self.subreddit)

def reveal(direc, raised=[False]):
    if raised[0]:
        # No need to try again - we already know an exception will
        # be raised.
        return
    if not os.path.exists(direc):
        raise ValueError("Could not find %s" % direc)
    try:
        if os.path.isdir(direc):
            subprocess.call(['open', direc])
        else:
            subprocess.call(['open', '-R', direc])
    except:
        # Non-unixy
        raised[0] = True
