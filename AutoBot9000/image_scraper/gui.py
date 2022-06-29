import tkinter as tk

window = tk.Tk()

color='#34fgh4'
background_color='#ddd'


#welcome screen
greeting = tk.Label(text="Welcome to AutoBot9000",
width=90,
height=10,
bg='#ffa500')

greeting.pack()



#cross posting button
run_cross_poster = tk.Button(
    text="Start Cross Posting",
    width=25,
    height=5,
    bg="green",
    fg="black",
)
run_cross_poster.pack(side=tk.BOTTOM,padx=10, ipadx=10,)

#scraper settings button
set_scraper_settings = tk.Button(
    text="Settings",
    width=25,
    height=5,
    bg="black",
    fg="black",
)
set_scraper_settings.pack(side=tk.LEFT, padx=10, ipadx=10)

#run scraper
button = tk.Button(
    text="Run Scraper",
    width=25,
    height=5,
    bg="#ffa500",
    fg="black",
)
button.pack(side=tk.RIGHT, padx=10, ipadx=10,)



#listen for events
window.mainloop()