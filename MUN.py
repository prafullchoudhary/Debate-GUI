import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
from tkinter import PhotoImage
import awoc
win = tk.Tk()
win.geometry("350x280")
win.title("MUN Debate Facilitator")

win1 = tk.Frame(win)
win2 = tk.Frame(win)
win3 = tk.Frame(win)
win4 = tk.Frame(win)
win5 = tk.Frame(win)
win6 = tk.Frame(win)
win7 = tk.Frame(win)
win8 = tk.Frame(win)
win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)
win1.pack(fill='x')
for frame in (win1, win2, win3, win4, win5, win6, win7, win8):
    frame.grid(row=0, column=0, sticky='nsew')

my_world=None
countries=None
countries_vars=None

def show_frame(frame):
    frame.tkraise()

def starting_screen():
    show_frame(win1)
def choose_country():
    show_frame(win2)
def debate_type():
    show_frame(win3)
def general_speakers_list():
    show_frame(win4)
def moderated_caucus():
    show_frame(win5)
def unmoderated_caucus():
    show_frame(win6)
def general_debate_screen():
    show_frame(win7)
def moderated_debate_screen():
    show_frame(win8)
style = ttk.Style()
style.configure("B.TButton", font=('Goudy old style', 13, 'bold'))

import os,sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Screens:
    def __init__(self):
        self.win1 = win1
        self.win2 = win2
        self.win3 = win3
        self.hidden_rows = []
        self.selected_countries = []
    
    def First_screen(self):
        welcome_label = ttk.Label(win1, text="Welcome to the MUN app", font=('Goudy old style bold', 15))
        welcome_label.place(relx=0.5, rely=0.2, anchor='center')

        start_debating_button = ttk.Button(win1, text="Start Debating", command=choose_country, style="B.TButton")
        start_debating_button.place(relx=0.5, rely=0.5, anchor='center')

        instructions_button = ttk.Button(win1, text="How This Works", command=show_instructions, style="B.TButton")
        instructions_button.place(relx=0.5, rely=0.8, anchor='center')

    def Second_screen(self):
        global check_buttons
        canvas = tk.Canvas(win2)
        canvas.place(relx=0.07, rely=0.27, height=140, width=180)
        scrollbar = tk.Scrollbar(win2, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        Choose_Countries = ttk.Label(win2, text="Choose Countries", font=("Helvetica", 14), foreground="grey")
        Choose_Countries.place(relx=0.05, rely=0.1, anchor='w')
        self.my_entry = ttk.Entry(win2, font=("Helvetica", 12))
        self.my_entry.place(relx=0.05, rely=0.20, anchor='w', width=250, height=25)

        country_var = {}
        check_buttons = {}
        global my_world
        global countries
        global countries_vars
        my_world = awoc.AWOC()
        countries = my_world.get_countries()
        countries_vars = {country['Country Name']: tk.IntVar() for country in countries}

        i = 0
        for i, country in enumerate(countries):
            check_button = ttk.Checkbutton(frame, text=country['Country Name'], variable=countries_vars[country['Country Name']], onvalue=1, offvalue=0)
            check_button.grid(row=i, column=0, sticky="w")
            check_buttons[country['Country Name']] = check_button
            i += 1

        def update_label():
            self.selected_countries = [country for country in countries if countries_vars[country['Country Name']].get() == 1]
            

        for country in countries:
            check_buttons[country['Country Name']].config(command=update_label)

        self.my_entry.bind("<KeyRelease>", lambda e: check(self, e))
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

        Back_Button = ttk.Button(win2, text="Back", command=starting_screen, style="B.TButton")
        Back_Button.place(relx=0.07, rely=0.8)

        def check_contry(countries_vars):
            filtered_coun = {k: v for k, v in countries_vars.items() if v.get()==1}
            if len(filtered_coun) == 0:
                m_box.showwarning("Error", "Please choose at least one country")
            elif len(filtered_coun) > 30:        
                m_box.showwarning("Error", "Please select less than 30 countries")
            else:
                debate_type()
                
        self.Continue_Button = ttk.Button(win2, text="Continue", command=lambda: [check_contry(countries_vars)], style="B.TButton")
        self.Continue_Button.place(relx=0.5, rely=0.8)

        def check(self, e):
            typed = self.my_entry.get()
            for i, row in enumerate(frame.winfo_children()):
                cb_text = row.cget('text')
                if cb_text != '' and (typed.lower() not in cb_text.lower()):
                    row.grid_forget()
                    self.hidden_rows.append(row)
                else:
                    if row in self.hidden_rows:
                        self.hidden_rows.remove(row)
                        row.grid(row=i, column=0, sticky="w")
            
            for item in countries:
                if typed.lower() in item['Country Name'].lower():
                    if check_buttons[item['Country Name']].winfo_manager() == 0:
                        check_buttons[item['Country Name']] = ttk.Checkbutton(frame, text=item['Country Name'], variable=countries_vars[item['Country Name']], onvalue=1, offvalue=0)
                        check_buttons[item['Country Name']].grid(row=countries.index(item), column=0, sticky="w")


    def Third_screen(self):
        Debate_Type = ttk.Label(win3, text="Pick Debate Type", font=('Goudy old style bold', 15))
        Debate_Type.place(relx=0.5, rely=0.1, anchor='center')

        General_Speakers_List = ttk.Button(win3, text="General Speakers List",command=general_speakers_list, style="B.TButton")
        General_Speakers_List.place(relx=0.5, rely=0.3,anchor='center')

        Moderated_Caucus = ttk.Button(win3, text="Moderated Caucus",command=moderated_caucus, style="B.TButton")
        Moderated_Caucus.place(relx=0.5, rely=0.5,anchor='center')

        UnModerated_Caucus = ttk.Button(win3, text="UnModerated Caucus",command=unmoderated_caucus, style="B.TButton")
        UnModerated_Caucus.place(relx=0.5, rely=0.7,anchor='center')

        back_button_icon = tk.PhotoImage(file=resource_path("Back.png"))
        Back_Button = tk.Button(win3, image=back_button_icon, command=choose_country,width=25,height=25)
        Back_Button.image = back_button_icon 
        Back_Button.place(relx=0.02, rely=0.02)

class Debateing:
    global my_world
    global countries
    global countries_vars
    
    def __init__(self):
        self.win4 = win4
        self.win5 = win5
        self.win6 = win6
        self.from_win=False
        self.items=[]
        self.second1=None
        self.minute1=None

    def general(self):
        self.filtered_coun = None
        self.abc_iter = None
        self.current_country = None
        self.pre_country=None
        
        self.selected_countries = []
        def is_valid_integervalue(value1,value2):
            if value1 == "" and value2 == "":
                m_box.showwarning("Error", "Please enter a valid Time")
                return
            else:
                general_debate_screen()
                if value2 == "":
                    self.second1 = 0
                else:
                    self.second1 = int(value2)
                if value1 == "":
                    self.minute1 = 0
                else:
                    self.minute1 = int(value1)
                if self.current_country!=self.pre_country:
                    lable.config(text=self.current_country[0])
                    self.pre_country=self.current_country
                    self.current_country=next(self.abc_iter,self.current_country)
                    if self.current_country!=self.pre_country:
                        next_speaker_lable.config(text=f"Next Speaker: {self.current_country[0]}")
                    else:
                        next_speaker_lable.config(text="")
                    update_time()
                else:
                    m_box.showinfo("Time's Up!","Debate has Stoped")
                    self.from_win=False
                    return debate_type()

        def update_time():
            time_l = "{:02d}:{:02d}".format(self.minute1, self.second1)
            timer_label.config(text=time_l)
            timer_label.update_idletasks()
            if self.second1 == 0:
                if self.minute1 == 0:
                    ok=m_box.showinfo("Time's Up!",f"Time's Up! {self.pre_country[0]}")
                    if ok=="ok":
                        is_valid_integervalue(minute_spinbox.get(),second_spinbox.get())
                    return
                else:
                    self.minute1 -= 1
                    self.second1 = 59
            else:
                self.second1 -= 1
            if self.second1 < 0:
                self.second1 = 59
            win4.after(1000, update_time)

        def for_each_country():
            if self.from_win==True:
                self.filtered_coun = {k: 1 for k in self.items}
            else: 
                self.filtered_coun = {k: v for k, v in countries_vars.items() if v.get()==1}
            self.abc_iter = iter(self.filtered_coun.items())
            self.current_country = next(self.abc_iter)
            self.pre_country=(0)
            is_valid_integervalue(minute_spinbox.get(),second_spinbox.get())


        label_per_speaker = ttk.Label(win4, text="Set a Time Per Speaker", font=("Helvetica", 18))
        label_per_speaker.place(relx=0.49, rely=0.3, anchor='center')

        minute_spinbox_label = ttk.Label(win4, text="Minutes")
        minute_spinbox_label.place(relx=0.33, rely=0.53)
        minute_spinbox = ttk.Spinbox(win4, from_=0, to=59, width=5)
        minute_spinbox.place(relx=0.33, rely=0.46)

        minute_label = ttk.Label(win4, text=":")
        minute_label.place(relx=0.50, rely=0.46)

        second_spinbox_label = ttk.Label(win4, text="Seconds")
        second_spinbox_label.place(relx=0.53, rely=0.53)
        second_spinbox = ttk.Spinbox(win4, from_=0, to=59, width=5)
        second_spinbox.place(relx=0.53, rely=0.46)

        set_time_button = ttk.Button(win4, text="Continue", command=lambda: [for_each_country()])
        set_time_button.place(relx=0.50, rely=0.7, anchor='center')

        back_button_icon = tk.PhotoImage(file=resource_path("Back.png"))
        Back_Button = tk.Button(win4, image=back_button_icon, command=debate_type,width=25,height=25)
        Back_Button.image = back_button_icon 
        Back_Button.place(relx=0.02, rely=0.02)

        lable = ttk.Label(win7, text="Speaker Name", font=("Helvetica", 17))
        lable.place(relx=0.48, rely=0.3,anchor='center')
        timelable = ttk.Label(win7, text="Time Left ", font=("Helvetica", 12))
        timelable.place(relx=0.23, rely=0.43)
        timer_label = ttk.Label(win7, text="00:00", font=("Helvetica", 24))
        timer_label.place(relx=0.48, rely=0.4)
        next_speaker_lable = ttk.Label(win7, text="Next Speaker: ABC", font=("Helvetica", 12))
        next_speaker_lable.place(relx=0.48, rely=0.65,anchor='center')

    def unmoderated(self):
        selected_countries_label = tk.Listbox(win5,height=130)
        selected_countries_label.place(relx=0.18, rely=0.18, width=150, height=200)

        def on_click():
            self.items = [selected_countries_label.get(i) for i in range(selected_countries_label.size())]
            self.from_win=True
            general_speakers_list()
            # minute_spinbox.get()

        def update_label():
            self.selected_countries = [country for country in countries if countries_vars[country['Country Name']].get() == 1]
            selected_countries_label.delete(0, tk.END)
            for country in self.selected_countries:
                selected_countries_label.insert(tk.END, country['Country Name'])

        for country in countries:
            check_buttons[country['Country Name']].config(command=update_label)

        def move_up():
            try:
                selected_index = selected_countries_label.curselection()[0]
                if selected_index > 0:
                    selected_item = selected_countries_label.get(selected_index)
                    selected_countries_label.delete(selected_index)
                    selected_countries_label.insert(selected_index - 1, selected_item)
                    selected_countries_label.see(selected_index - 1)
                    selected_countries_label.select_set(selected_index - 1)
            except:
                m_box.showinfo("Info",f"Please select a country")
        
        def move_down():
            try:
                selected_index = selected_countries_label.curselection()[0]
                if selected_index < selected_countries_label.size() - 1:
                    selected_item = selected_countries_label.get(selected_index)
                    selected_countries_label.delete(selected_index)
                    selected_countries_label.insert(selected_index + 1, selected_item)
                    selected_countries_label.see(selected_index + 1)
                    selected_countries_label.select_set(selected_index + 1)
            except:
                m_box.showinfo("Info",f"Please select a country")

        Choose_Countries = ttk.Label(win5, text="Choose Speaker Order", font=("Helvetica", 14), foreground="grey")
        Choose_Countries.place(relx=0.12, rely=0.1, anchor='w')
        up_button = ttk.Button(win5, text="Order Up", command=move_up)
        up_button.place(relx=0.68, rely=0.3)
        down_button = ttk.Button(win5, text="Order Down", command=move_down)
        down_button.place(relx=0.68, rely=0.45)

        selected_countries_label.bind("<<ListboxSelect>>")
        back_button_icon = tk.PhotoImage(file=resource_path("Back.png"))
        Back_Button = tk.Button(win5, image=back_button_icon, command=debate_type, width=25, height=25)
        Back_Button.image = back_button_icon 
        Back_Button.place(relx=0.02, rely=0.04)

        Continue_Button = ttk.Button(win5, text="Continue", command= on_click)
        Continue_Button.place(relx=0.68, rely=0.7)

    def moderated(self):
        def is_valid_integervalue(value1,value2):
            if value1 == "" and value2 == "":
                m_box.showwarning("Error", "Please enter a valid Time")
                return
            else:
                if value2 == "":
                    self.second1 = 0
                else:
                    self.second1 = int(value2)
                if value1 == "":
                    self.minute1 = 0
                else:
                    self.minute1 = int(value1)
                moderated_debate_screen()
                update_time()

        def update_time():
            time_l = "{:02d}:{:02d}".format(self.minute1, self.second1)
            timer_label.config(text=time_l)
            timer_label.update_idletasks()
            if self.second1 == 0:
                if self.minute1 == 0:
                    m_box.showinfo("Time's Up!","Debate has Stoped")
                    return debate_type()
                else:
                    self.minute1 -= 1
                    self.second1 = 59
            else:
                self.second1 -= 1
            if self.second1 < 0:
                self.second1 = 59
            win4.after(1000, update_time)

        label_per_speaker = ttk.Label(win6, text="Set Total Time", font=("Helvetica", 18))
        label_per_speaker.place(relx=0.49, rely=0.3, anchor='center')

        minute_spinbox_label = ttk.Label(win6, text="Minutes")
        minute_spinbox_label.place(relx=0.33, rely=0.53)
        minute_spinbox = ttk.Spinbox(win6, from_=0, to=59, width=5)
        minute_spinbox.place(relx=0.33, rely=0.46)

        minute_label = ttk.Label(win6, text=":")
        minute_label.place(relx=0.50, rely=0.46)

        second_spinbox_label = ttk.Label(win6, text="Seconds")
        second_spinbox_label.place(relx=0.53, rely=0.53)
        second_spinbox = ttk.Spinbox(win6, from_=0, to=59, width=5)
        second_spinbox.place(relx=0.53, rely=0.46)

        set_time_button = ttk.Button(win6, text="Continue", command=lambda: [is_valid_integervalue(minute_spinbox.get(),second_spinbox.get())])
        set_time_button.place(relx=0.50, rely=0.7, anchor='center')

        label_per_speaker = ttk.Label(win6, text="Set Total Time", font=("Helvetica", 18))
        label_per_speaker.place(relx=0.49, rely=0.3, anchor='center')

        minute_spinbox_label = ttk.Label(win6, text="Minutes")
        minute_spinbox_label.place(relx=0.33, rely=0.53)
        minute_spinbox = ttk.Spinbox(win6, from_=0, to=59, width=5)
        minute_spinbox.place(relx=0.33, rely=0.46)
        minute_label = ttk.Label(win6, text=":")
        minute_label.place(relx=0.50, rely=0.46)
        second_spinbox_label = ttk.Label(win6, text="Seconds")
        second_spinbox_label.place(relx=0.53, rely=0.53)
        second_spinbox = ttk.Spinbox(win6, from_=0, to=59, width=5)
        second_spinbox.place(relx=0.53, rely=0.46)

        set_time_button = ttk.Button(win6, text="Continue", command=lambda: [is_valid_integervalue(minute_spinbox.get(),second_spinbox.get())])
        set_time_button.place(relx=0.50, rely=0.7, anchor='center')

        back_button_icon = tk.PhotoImage(file=resource_path("Back.png"))
        Back_Button = tk.Button(win6, image=back_button_icon, command=debate_type,width=25,height=25)
        Back_Button.image = back_button_icon 
        Back_Button.place(relx=0.02, rely=0.02)


        lable = ttk.Label(win8, text="Time Left", font=("Helvetica", 24))
        lable.place(relx=0.5, rely=0.35, anchor='center')
        timer_label = ttk.Label(win8, text="00:00", font=("Helvetica", 24))
        timer_label.place(relx=0.5, rely=0.55, anchor='center')
  
def show_instructions():
    m_box.showinfo("Instructions", "This app is used to facilitate MUN debates. Before beginning establish what countries are taking part in your debates and what committee and topic you will be debating. Then, you will be able to begin debating.\n\nThe recommended structure for MUN debates is as follows:\n\n1. General Speakers List - all countries should have enough time to state their opinion on the topic. Around 2 minutes per speaker is recommended.\n\n 2. Moderated Caucus - here countries will formally debate. This is recommended for further discussions on the topic after the General Speakers List debates.\n\n3. Unmoderated Caucus - here countries will debate informally. Delegates can freely move around and talk to others. This form of debates is recommended by the end of your discussions.")


show_frame(win1)

my_screens = Screens()
my_screens.First_screen()
my_screens.Second_screen()
my_screens.Third_screen()

Debate=Debateing()
Debate.general()
Debate.unmoderated()
Debate.moderated()

win.mainloop()