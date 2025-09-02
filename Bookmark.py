import customtkinter as ctk
import keyring
from argon2 import PasswordHasher
from time import sleep
import os
import io
import urllib.request
import threading
import shutil
import time
from PIL import Image, ImageEnhance, ImageDraw
from Book_Scouter import get_book_details
from Book_Data import longest_completed, track_book, read_data, get_total_pages, total_stats

# Ignores DPI scaling to work in Full Screen for all Systems
ctk.deactivate_automatic_dpi_awareness()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Path to Data Folder of the Application
data_loc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")

# Service Name under which User Credentials are saved
SERVICE_NAME = "Bookmark"

win = ctk.CTk(fg_color="#121212")
win.title("Login")
win.geometry("0x0")

w = win.winfo_screenwidth()
h = win.winfo_screenheight()

# Raw Data of the "No Image Available" Image by Google API
no_image_raw_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x80\x00\x00\x00\xaa\x08\x00\x00\x00\x00@b\x18G\x00\x00\x00\tpHYs\x00\x00\x00H\x00\x00\x00H\x00F\xc9k>\x00\x00\x00\tvpAg\x00\x00\x00\x80\x00\x00\x00\xaa\x00_\x8a\xfd\xb2\x00\x00\x04\x92IDATx\xda\xed\x9a;\x93\xe3 \x0c\x80\xf7\xff\xff)z:ZJ\xf5t\xf4>\xd0\x83\x87\x8d\x17c\'\x93\xcd\x8d\x98\x9b\xdb%\xf2\xc2\x87$\x83\x84\xf2\xb3}\xb8\xfd(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02(\x80\x02\xfc}\x00o\xdcg\x01\xac\x81\xcf\x02\x84\xf0\xce\xf9\xbf\xc1\x07jc]\xc4\x10\xcbG\xb1\xd3O#\xc0\xc7\xe3\x85A\xa7\x00\xde\xf84\x8f1\x11Ljq\x8b.\xfd`\xb7\x04\x9b?\xb3\xcc\xe5\xe8wcr?\xfaF\xf4\x08\x00}0M\x9e@ \x8fh,\xa4\xb1\x81\xd8\x8c\x83\x0c\x813\x1a\x92\xa4\x7f\xd4K\xcf;3w\xe0)\x00\x0e\x9fF\xb5I\x9f\xc1\xd0\x88\x16U\x00Y!\xa9\xb9\xdcK3z\xe25\x16{\xa8$@\x9aG\x00\x01\x87p4P\xe0\x159\x9c\xcc\xf3\xf2 O\xe6\xd8,\x01A|\xa6(\xf8\x8f\x00\x00\x87\xe2\x89eA\xbdf\xf3N\x15Y\x1b$\x8b\xe5\x017\xb5\xc1\x0c\xc0\x89\x0f\xd6\x95\x97n\x04\xef\x9cC\xb3\x80,y\xcb\xb2\xec,\x0e\xdb\xdc\tf\x00\xec\x83\xb6]9+\xc2\xa1\x9f;\x9f\xd5\xcchl2\x94p{\x08@\x8b\xe5\xe3@VN]\x97\xbc\xbe\x99\x12\xc4dn\xab8\x17\xda\x04\x80|\x90\x8f\x83\xc0.\x80\xdd(\xfe\x85\x0eW\xa6DY\xc1\t0\xdd\x8b&\x00\xb8 \xf1e`O\xc7\xae\xd0l\xf8\xc6\x89\x91\x805fE\x7fO\xf7\x01\\\x99\xcc\xc5\xcb\x0c\xb2\xd5\x04Z2\xeb\xc3\xd3\xfc\xa6N\x1c\xed\x85\x93|\x02`\x86>h\t\'\xeduy\x87\xc2O\xd1\xf1\x932hJ/\xb2\xe9\xfc\x13\x00\xf1\xc1\xee\xed\xe3.\xf9\xba\x97nH\xaa\xf0\xd1\x95\xcd\xe9\xca\x1bpA\x03\xbf\xe3\x1dC\x85\xba\xf3\xc5Kg\xe1\xab\xe2\x81X7\xe2\xd5?}\x15\x80x\xe4r\xf8\xf6\xa2\x88\xc8]\xf7\xba\xf7\x00l\x18\x7f,l\x80/\x07\xc8\x11\xd8\xad\xe8\xf5\xab\x82R\x05P\x80\xaf\x00\x80\xd5\xad\xf0\xc5\x00n\x1a\x86\xbf\x17\xe0c\x87\x914X?\x0cn\x02\x9cd\xc8~\xfd4X\x06\xc8q\xd11C\xf6\xb4\xfe\x1b\x07\xd22@\x9a%E\xc7\x98\x07\xd3\x9a\xa9c\x99\xc5\xb9E/\\\x06\xe0D\x99CoOq"\x87\xc17\\`\x1d\xc0qh\x8a\x93\x85.;\xb9\xe3\x02\xeb\x00bd\xcc\xcf\xca\x15\x9ed\xf1\xeb\x17j\xab\x00%\x0f\xc7\xf0\xafD\xde\x040\xbf\rx\x0e\x00\xed\xd5C\xbd\x15\xc0\x849\xaeoC\xeb\x00\xbe\r\xc0\xeb\xc6\xe7\xdb\x04\xf1\xad\x00\xb6\xa4>\xb6\x05@[\xdc\xf1\xc1e\x0013%\xaa\xf5%0\xdb=\x1f\\\x05h\x92r\xc0)-\xa9\x03{w|p\x15\x00j\xe6\xcf\x1b\x90\xf5`\xf9e\xc8\x9b\xe22\xc2"\x80\x98\xb9\x80`\x8a\xec\x8a!\xd6u\xf0\xfc8n\xf2\x91\xab\x19\xf1k\x01\x1e6\x05P\x00\x05P\x00\x05x\x00\xe0\xb9X\x15\x87\x82\x93\xde+\x0108\x1a\xa5\xa3\xfdu\xe5\xe4\xf2\xf2\x01\x00\x1e\x830X_\x7f(O\x8e\xe8\xa7>0\xa8\xce\xf4J\x99e\xecC\x80x~\xe7\xb8/\x08\xd7\xcc\xa0\x08P)e\x84\x12*\x9f\x0c:\x00h*\xc2P\xd6\x87\x8a\xa4\xf8\xa7\xa4F\xb5\xa0\xb7\x17@\xad\x16p\x0c\xd5$\xd13\x80\xb6"\x1c\xc4\xc22\x9b\xc5+i\xfc\xb0\xf1\xc1\xbd\xc0\x1a/%e\xf6\xc16\x89\x9e\x00t\x15\xe1\x8d\rH\x0b\xb5\xa5f\x14\xb7RTv\xdbQ\x80?8b\x96\xda\xf3\xd9u\xfe\x01\xa0\xab\x08o\x85\x06\xb0(\xd3\x98\xa3IG\x0f\x82P\xa1\x03\xe7lM:3\xf5\x01\x01\xa1\xead\xc0\xa5\xb5\x7fG#KQ9\x8c\x05"\xc3^\xa9e\x0f^\x89#@S\x11\x16}\x94|\x0c\x92\xc4\x1a^{ST\xee\x05\xd0\x00\xe0c9r\xc7f/\x00\xb4\x15a6\x04\x94/\x03\xd0Hlw\x90*\xf2^\x10;\xbf\xc1bzm3\x80\xae"\xcc\xca7l\x07\xe3k\r\xbd)*\x1f\x04\x1b\xdb\xdb\xb0\x13\xfd\xba\x17\xed\x00\xfa\x8a0\r\x07r\x1d\xe5D\xb5\xd0\x15\x95G\x82\xad-\xbaV\x80A\xe6\xb6\x03\xe8+\xc2\xb4\x82\xf6M\xd8\xe4=m\x8a\xca{\x81\x91\x91\xc2\xae\xf6\\\x9dq\xae\x01\xc97\xb3I\xca\x96&\x99p\xf1A\xc2\xdd\x0bPa\\Lv\xfc\xbf<1\xd5\xc0\xae"L\xb7rE96\xef\x90\x96m[\x8a\xca{Ah6=\xaeb\xf3\x13\xa3\x83y\xfc\x16\xf8&\r.\xd4\x81\x8e\x084I\xf7\xc5\x86^`\xa9\x0f\xacP\xfa\xb2\x07%\xd1\xa3\xd4u\xb0\x0f\\?\nO\x05\x83!\xceF\xfd\xe6\x98P\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\x14@\x01\xfe\x13\x80\x7f\xa7\x14\x8b\xedk\x7f(e\x00\x00\x00\x00IEND\xaeB`\x82'

# Check for removing Folders for which a User doesn't exist or remove Users for which Folders don't exist and removing Auto-Logins and Saved Passwords if necessary
Users = keyring.get_password(SERVICE_NAME, "Users")
if Users: Users = Users.split("\n")
else: Users = []

for user in Users:

    # Removing User if User Folder or Database doesn't exist
    if not os.path.exists(os.path.join(data_loc, "Accounts", user, "User.db")):
        Users.remove(user)
        keyring.delete_password(SERVICE_NAME, user)
        if keyring.get_password(SERVICE_NAME, "Auto-Login") == user:
            keyring.delete_password(SERVICE_NAME, "Auto-Login")

# Removing Folders for which a User doesn't exist
for dir in os.listdir(os.path.join(data_loc, "Accounts")):
    if dir not in Users:
        shutil.rmtree(os.path.join(data_loc, "Accounts", dir))

keyring.set_password(SERVICE_NAME, "Users", "\n".join(Users))

# Center Window on the Screen
def center(win, screen_resolution, animation_time):

    x1, y1 = 0, 0

    while (x1 < screen_resolution[0]) or (y1 < screen_resolution[1]):

        if x1 != screen_resolution[0]: x1 += screen_resolution[0]/(animation_time*10)
        if y1 != screen_resolution[1]: y1 += screen_resolution[1]/(animation_time*10)

        win.geometry(f"{int(x1)}x{int(y1)}")

        x2 = w//2 - win.winfo_width()//2
        y2 = h//2 - win.winfo_height()//2

        win.geometry(f"+{x2}+{y2}")

        sleep(0.008)
        win.update()

    x1, y1 = screen_resolution

    win.geometry(f"{int(x1)}x{int(y1)}")

    x2 = w//2 - win.winfo_width()//2
    y2 = h//2 - win.winfo_height()//2

    win.geometry(f"+{x2}+{y2}")

    win.update()

# Marquee Text Functions to Describe the Max Roll Over Length
home_page_cap = 70
search_page_cap = 20

# Start Marquee Animation
def start_marquee(home, btn, text, speed=200):
    def scroll():
        nonlocal text
        text = text[1:] + text[0]  # shift text left
        btn.configure(text=text[:home_page_cap if home else search_page_cap])
        btn._marquee_job = btn.after(speed, scroll)

    btn._marquee_job = btn.after(speed, scroll)

# Stop Marquee Animation
def stop_marquee(home, btn, original_text):
    if hasattr(btn, "_marquee_job"):
        btn.after_cancel(btn._marquee_job)
        btn.configure(text=original_text[:home_page_cap if home else search_page_cap])

# -------------- Login and Sign Up Functions -------------- #

# Switch Between Login and Sign Up Windows
def switch_method(button):

    # Underline Animation for Selected Window
    def make_selector(x, length):
        for i in range(1, length):

            text = "_"*i

            selector.configure(text=text)
            selector.place(x=x)

            sleep(0.04)

            win.update()

    if username.get() != "":
        username.delete(0, ctk.END)
    if password.get() != "":
        password.delete(0, ctk.END)

    try:
        pass_notification.destroy()
    except:
        pass
    
    check_var.set("")
    show_pass([password])

    if button == "login":

        login_page(False)
        make_selector(133, 6)

    else:

        signup_page()
        make_selector(267, 7)

# Show Password
def show_pass(inputs):

    show = check_var.get()

    if show == "*":
        check_var.set("")
        show_password.configure(image=ctk.CTkImage(dark_image=Image.open(os.path.join(data_loc, "Images", "Eye Show.png")), size=(30,30)))
    else:
        check_var.set("*")
        show_password.configure(image=ctk.CTkImage(dark_image=Image.open(os.path.join(data_loc, "Images", "Eye Hide.png")), size=(30,30)))

    for input in inputs:
        input.configure(show=check_var.get())

# Login Page
def login_page(first_time):

    global frame, selector, username, password, check_var, show_password, login_button

    win.title("Login")

    try:
        confirm_password.destroy()
        signup_button.destroy()
        login_button.destroy()
    except:
        try:
            login_button.destroy()
        except:
            pass

    if first_time:

        center(win, (600, 400), 1.5)

        frame = ctk.CTkFrame(win, fg_color="#1f1f1f")
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="BOOKMARK", text_color="#9a4cfa", font=("Helvetica", 24, "bold"))
        label.pack(pady=12, padx=10)
    
    if first_time:

        selector = ctk.CTkLabel(frame, text="_____", text_color="#9a4cfa", font=("Helvetica", 24, "bold"))
        selector.place(x=133, y=55)

    login_switch_method = ctk.CTkButton(frame, text="LOGIN", text_color="#9a4cfa", font=("Helvetica", 16, "bold"), fg_color="#1f1f1f", hover_color="#1f1f1f", cursor="hand2", height=0, width=0, command=lambda: switch_method("login"))
    login_switch_method.place(x=136, y=50)

    sign_up_switch_method = ctk.CTkButton(frame, text="SIGN UP", text_color="#9a4cfa", font=("Helvetica", 16, "bold"), fg_color="#1f1f1f", hover_color="#1f1f1f", cursor="hand2", height=0, width=0, command=lambda: switch_method("sign_up"))
    sign_up_switch_method.place(x=270, y=50)

    if first_time:    
        
        username = ctk.CTkEntry(frame, placeholder_text="Username", fg_color="#1f1f1f", show="", font=("Helvetica", h/90, "bold"), height=40, width=200)
        username.pack(pady=(50, 12), padx=10)

        check_var = ctk.StringVar()
        check_var.set("*")

        password = ctk.CTkEntry(frame, placeholder_text="Password", fg_color="#1f1f1f", show="*", font=("Helvetica", h/90, "bold"), height=40, width=200)
        password.pack(pady=12, padx=10)

        show_password = ctk.CTkButton(frame, text="", fg_color="#1f1f1f", hover_color="#191919", image=ctk.CTkImage(dark_image=Image.open(os.path.join(data_loc, "Images", "Eye Hide.png")), size=(30,30)), width=30, height=30, command=lambda: show_pass([password]))
        show_password.place(x=345, y=168)

    else:

        show_password.configure(command=lambda: show_pass([password]))

    login_button = ctk.CTkButton(frame, text="Login", text_color="#121212", fg_color="#9a4cfa", hover_color="#b87bff", font=("Helvetica", 13, "bold"), cursor="hand2", command=login)
    login_button.pack(pady=12, padx=10)

    win.bind("<Return>", lambda event: login())

# Sign Up Page
def signup_page():

    global confirm_password, signup_button, return_key_bind

    win.title("Sign Up")

    try:
        login_button.destroy()
        confirm_password.destroy()
        signup_button.destroy()
    except:
        try:
            confirm_password.destroy()
            signup_button.destroy()
        except:
            pass

    confirm_password = ctk.CTkEntry(frame, placeholder_text="Confirm Password", fg_color="#1f1f1f", show="*", font=("Helvetica", h/90, "bold"), height=40, width=200)
    confirm_password.pack(pady=12, padx=10)

    show_password.configure(command=lambda: show_pass([password, confirm_password]))

    signup_button = ctk.CTkButton(frame, text="Sign Up", text_color="#121212", fg_color="#9a4cfa", hover_color="#b87bff", font=("Helvetica", 13, "bold"), cursor="hand2", command=sign_up)
    signup_button.pack(pady=12, padx=10)

    return_key_bind = win.bind("<Return>", lambda event: sign_up())

# Login Button Function
def login():

    global pass_notification, account_loc

    if (username.get() != "") and (password.get() != ""):

        user = username.get()
        passw = password.get()

        # Kind of useless (basically useless) since App opens immediately after Login, so "Login Successful" Text isn't visible
        try:
            # Match Entered Password to Stored Password
            if PasswordHasher().verify(keyring.get_password(SERVICE_NAME, user), passw): text = "Login Successful!"; color = "#21c065"; x = 90
        except:
            text = "Username or Password is Incorrect."; color = "red"; x = 92

        pass_notification = ctk.CTkLabel(frame, text=text, font=("Helvetica", 10, "bold"), text_color=color, height=0, width=300)
        pass_notification.place(x=x, y=212)

        frame.after(5000, pass_notification.destroy)

        if text == "Login Successful!":
            account_loc = os.path.join(data_loc, "Accounts", user)

            # Make Account Folder if it doesn't exist
            os.makedirs(account_loc, exist_ok=True)

            # Start Main Application
            book_collection(user)

    else:

        if username.get() == "": text = "You have a Username right?"; x = 92
        else: text = "I believe you forgot the Password"; x = 91

        pass_notification = ctk.CTkLabel(frame, text=text, font=("Helvetica", 10, "bold"), text_color="red", height=0, width=300)
        pass_notification.place(x=x, y=212)

        frame.after(5000, pass_notification.destroy)

# Signup Button Function
def sign_up(username_taken = False):
    
    global pass_notification
    
    if (password.get() == confirm_password.get()) and (password.get() != "" and confirm_password.get() != "" and username.get() != "") and (not username_taken):

        user = username.get()
        passw = PasswordHasher().hash(password.get())

        # Use Keyring to use OS Token Authentication and store passwords securely if Username is not taken
        if not keyring.get_password(SERVICE_NAME, user):

            keyring.set_password(SERVICE_NAME, user, passw)

            Users = keyring.get_password(SERVICE_NAME, "Users")
            if Users:
                Users = Users.split("\n")
            else:
                Users = []
            keyring.set_password(SERVICE_NAME, "Users", "\n".join(Users + [user]))

            pass_notification = ctk.CTkLabel(frame, text="Registered Successfully", font=("Helvetica", 10, "bold"), text_color="#21c065", height=0, width=300)
            pass_notification.place(x=89, y=276)

            frame.after(5000, pass_notification.destroy)

        else:

            # Recurse to the Signup Function if Username Taken as "Username Taken" case is last case in 'else' block
            username_taken = True
            sign_up(username_taken)

        if not username_taken:
            os.makedirs(os.path.join(data_loc, "Accounts", user), exist_ok=True)

    else:

        if username.get() == "": text = "Don't you need a Username?"; x = 140
        elif (password.get() == "") and (confirm_password.get() == ""): text = "Trust Me. You need a Password"; x = 140
        elif password.get() != confirm_password.get(): text = "The Passwords do not Match"; x = 140
        else: text = "Username is already taken"; x = 140

        pass_notification = ctk.CTkLabel(frame, text=text, font=("Helvetica", 10, "bold"), text_color="red", height=0, width=200)
        pass_notification.place(x=x, y=276)

        frame.after(5000, pass_notification.destroy)


# -------------- Main App Functions -------------- #

# --> Quit Functions

# Quit Application
def quit_application(event):
    win.destroy()

# Quit Add Book Section
def quit_add_books(frame, widgets):

    # In case there are no Saved Widgets; In the case User is accessing a Saved Book
    if saved_widgets:
        saved_widgets[0].configure(state="disabled")

    win.unbind("<Motion>")
    for widget in frame.winfo_children():
        widget.destroy()

    # Frame Close Animation
    size = 0.8
    while size >= 0:
        frame.place_configure(relwidth=size, relheight=size)
        
        win.update()
        sleep(0.001)

        size -= 0.04

    size=0
    frame.place_configure(relwidth=size, relheight=size)

    frame.destroy()
    win.unbind("<Escape>")

    # Enabling Widgets on closing Search Window
    widgets[0].configure(state="normal")
    widgets[1].configure(state="normal", fg_color="#9a4cfa")
    widgets[2].configure(state="normal")
    for widget in widgets[0].tab(widgets[0].get()).winfo_children():
        try:
            if ("label" not in str(widget)) and (widget.cget("text") in ["◀", "▶"]):
                widget.configure(state="normal", fg_color="#9a4cfa")
            else:
                widget.configure(state="normal")
        except:
            pass
    win.bind("<Escape>", quit_application)

# Quit Logout Confirmation
def quit_logout_confirmation(logout_confirmation, widgets):

    logout_confirmation.destroy()
    win.unbind("<Escape>")

    # Enabling Widgets on closing Search Window
    widgets[0].configure(state="normal")
    widgets[1].configure(state="normal", fg_color="#9a4cfa")
    widgets[2].configure(state="normal")
    for widget in widgets[0].tab(widgets[0].get()).winfo_children():
        if ("label" not in str(widget)) and (widget.cget("text") in ["◀", "▶"]):
            widget.configure(state="normal", fg_color="#9a4cfa")
        else:
            widget.configure(state="normal")
    win.bind("<Escape>", quit_application)

# --> Other Functions

# Create Rounded Corners for a given Image
def create_rounded_image(image_path, radius):
    img = Image.open(image_path).convert("RGBA")
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', img.size, 255)
    w, h = img.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    img.putalpha(alpha)
    return img

# Open Saved Book Details
def open_book_details(widgets, search_term, books, book_num):

    # Get the specified Book and make a separate Dictionary for the Book Details
    book = {}
    for content_title in books.keys():
        book[content_title] = books[content_title][book_num]

    # Use 'add_book' function to Lazily recreate Book Info Window
    add_book(widgets, book_collection_search_term=search_term, book=book, search=False)

# User Book Collection
def book_collection(user):
    global update_tab

    # Execute Frame Destroy only if it isn't an Auto-Login
    if not keyring.get_password(SERVICE_NAME, "Auto-Login"):
        # Set up Default Auto-Login
        keyring.set_password(SERVICE_NAME, f"Auto-Login", user)
        frame.destroy()
    
    win.unbind("<Return>")

    center(win, (w, h), 2)
    win.title("Application")
    win.attributes("-fullscreen", True)
    win.geometry(f"{w}x{h}+0+0")

    # Main App Frame
    main_frame = ctk.CTkFrame(win, fg_color="#121212")
    main_frame.pack(fill="both", expand=True)

    # Add/Remove/Update Buttons in Tab
    def update_tab(widgets, search_term=None):

        category = tabs.get()

        if category != "Stats":

            filter_search.place(relx=0.5, rely=0.11, relwidth=0.45, relheight=0.06, anchor=ctk.CENTER)

            for widget in tabs.tab(category).winfo_children():
                if ("button" in str(widget)) and (widget.cget("text") not in ["◀", "▶"]):
                    widget.destroy()

            if (search_term) and (search_term.get() != "Enter Name or ISBN No. of the Book..."):
                books = read_data(account_loc, category, int(page_counters[category].get()), search_term.get())
            else:
                books = read_data(account_loc, category, int(page_counters[category].get()))

            for book_num in range(len(books.get("id", ""))):
                
                # Replace Default "No Image Found" with provided one
                raw_data = books["thumbnail"][book_num]
                if raw_data == no_image_raw_data:
                    image = create_rounded_image(os.path.join(data_loc, "Images", "No Image Found.png"), 35)
                else:
                    image = create_rounded_image(io.BytesIO(raw_data), 35)

                btn = ctk.CTkButton(tabs.tab(category), text=books["title"][book_num][:home_page_cap], fg_color="#1f1f1f", hover_color="#9a4cfa", border_color="#9a4cfa", border_width=h/320, image=ctk.CTkImage(dark_image=image, size=(150, 115)), compound=ctk.LEFT, anchor="w", corner_radius=15, command=lambda search_term=search_term, book_num=book_num: open_book_details(widgets, search_term, books, book_num))
                btn.configure(font=("Helvetica", h/32, "bold"))
                btn._text_label.configure(padx=20)
                btn.bind("<Enter>", lambda event, btn=btn, book_num=book_num: start_marquee(True, btn, books["title"][book_num]+"      ", speed=150))
                btn.bind("<Leave>", lambda event, btn=btn, book_num=book_num: stop_marquee(True, btn, books["title"][book_num]))
                
                if book_num == 0:
                    btn.place(relx=0.02, rely=0.1, relwidth=0.958, relheight=0.145)
                else:
                    btn.place(in_=prev_widget, relx=0, rely=1.1, relwidth=1, relheight=1)

                if (search_term) and (search_term.get() != "Enter Name or ISBN No. of the Book..."):
                    total_pages[category].set(str(get_total_pages(account_loc, category, search_term.get())))
                else:
                    total_pages[category].set(str(get_total_pages(account_loc, category, None)))

                prev_widget = btn

            win.update()

        else:

            filter_search.place_forget()

            for widget in tabs.tab(category).winfo_children():
                widget.destroy()

            # Stats to Display
            reading_stat = total_stats(account_loc, "Reading")
            completed_stat = total_stats(account_loc, "Completed")
            planned_stat = total_stats(account_loc, "Plan To Read")

            # Creating individual Frames for the Stats

            reading_frame = ctk.CTkFrame(tabs.tab(category), fg_color="#1f1f1f", corner_radius=h/108, border_width=h/280, border_color="#9a4cfa")
            reading_frame.place(relx=0.024, rely=0.07, relwidth=0.3, relheight=0.55)

            completed_frame = ctk.CTkFrame(tabs.tab(category), fg_color="#1f1f1f", corner_radius=h/108, border_width=h/280, border_color="#9a4cfa")
            completed_frame.place(in_=reading_frame, relx=1.09, rely=0, relwidth=1, relheight=1)

            planned_frame = ctk.CTkFrame(tabs.tab(category), fg_color="#1f1f1f", corner_radius=h/108, border_width=h/280, border_color="#9a4cfa")
            planned_frame.place(in_=completed_frame, relx=1.09, rely=0, relwidth=1, relheight=1)

            # Frame Titles and Images
            reading_image = Image.open(os.path.join(data_loc, "Images", "Reading.png"))
            reading_title = ctk.CTkLabel(reading_frame, text="Reading", font=("Helvetica", h/24, "bold"), text_color="#FFFFFF", image=ctk.CTkImage(dark_image=reading_image, size=(h/10, h/10)), compound=ctk.TOP, pady=10)
            reading_title.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            completed_image = Image.open(os.path.join(data_loc, "Images", "Completed.png"))
            completed_title = ctk.CTkLabel(completed_frame, text="Completed", font=("Helvetica", h/24, "bold"), text_color="#FFFFFF", image=ctk.CTkImage(dark_image=completed_image, size=(h/12, h/12)), compound=ctk.TOP, pady=12)
            completed_title.place(relx=0.5, rely=0.22, anchor=ctk.CENTER)

            planned_image = Image.open(os.path.join(data_loc, "Images", "Planned.png"))
            planned_title = ctk.CTkLabel(planned_frame, text="Plan To Read", font=("Helvetica", h/24, "bold"), text_color="#FFFFFF", image=ctk.CTkImage(dark_image=planned_image, size=(h/14, h/14)), compound=ctk.TOP, pady=18)
            planned_title.place(relx=0.5, rely=0.22, anchor=ctk.CENTER)

            # Frame Stats
            reading_books = ctk.CTkLabel(reading_frame, text=f"Books Left: {reading_stat['books']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            reading_books.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

            reading_pages = ctk.CTkLabel(reading_frame, text=f"Pages Left: {reading_stat['pages']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            reading_pages.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

            completed_books = ctk.CTkLabel(completed_frame, text=f"Books Read: {completed_stat['books']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            completed_books.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

            completed_pages = ctk.CTkLabel(completed_frame, text=f"Pages Read: {completed_stat['pages']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            completed_pages.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

            planned_books = ctk.CTkLabel(planned_frame, text=f"Books Left: {planned_stat['books']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            planned_books.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

            planned_pages = ctk.CTkLabel(planned_frame, text=f"Pages Left: {planned_stat['pages']}", font=("Helvetica", h/28, "bold"), text_color="#9a4cfa")
            planned_pages.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

            longest_completed_book = longest_completed(account_loc)
            if longest_completed_book:

                info = ctk.CTkLabel(tabs.tab(category), text="Longest Completed Book", font=("Helvetica", h/36, "bold"), text_color="#FFFFFF")
                info.place(relx=0.5, rely=0.69, anchor=ctk.CENTER)

                image = create_rounded_image(io.BytesIO(longest_completed_book["thumbnail"][0]), 35)

                btn = ctk.CTkButton(tabs.tab(category), text=longest_completed_book["title"][0][:home_page_cap], fg_color="#1f1f1f", hover_color="#9a4cfa", border_color="#9a4cfa", border_width=h/280, image=ctk.CTkImage(dark_image=image, size=(150, 115)), compound=ctk.LEFT, anchor="w", corner_radius=h/108, command=lambda search_term=search_term: open_book_details(widgets, search_term, longest_completed_book, 0))
                btn.configure(font=("Helvetica", h/32, "bold"))
                btn._text_label.configure(padx=20)
                btn.bind("<Enter>", lambda event, btn=btn: start_marquee(True, btn, longest_completed_book["title"][0]+"      ", speed=150))
                btn.bind("<Leave>", lambda event, btn=btn: stop_marquee(True, btn, longest_completed_book["title"][0]))

                btn.place(relx=0.5, rely=0.8, relwidth=0.958, relheight=0.145, anchor=ctk.CENTER)

            else:

                info = ctk.CTkLabel(tabs.tab(category), text="No Completed Books Yet", font=("Helvetica", h/18, "bold"), text_color="#818181")
                info.place(relx=0.5, rely=0.77, relwidth=0.958, relheight=0.145, anchor=ctk.CENTER)

    # Change Page
    def page_change(change_qty):
        category = tabs.get()

        page_var = page_counters[category]
        new_page_count = int(page_var.get()) + change_qty

        if not ((new_page_count == 0) or (new_page_count > int(total_pages[category].get()))):
            page_var.set(new_page_count)

        update_tab([tabs, add_btn, logout_btn])

    # Create Tabular View
    tabs = ctk.CTkTabview(main_frame,
                        corner_radius=h/108,
                        border_width=h/540,
                        fg_color="#1f1f1f",
                        border_color="#9a4cfa",
                        segmented_button_fg_color="#1f1f1f",
                        segmented_button_selected_color="#9a4cfa",
                        segmented_button_unselected_color="#2a2a2a",
                        segmented_button_selected_hover_color="#b87bff",
                        segmented_button_unselected_hover_color="#393939",
                        command=lambda: update_tab([tabs, add_btn, logout_btn], search_term))
    tabs._segmented_button.configure(font=("Helvetica", h/45, "bold"))
    tabs.pack(padx=w/32, pady=h/54, fill="both", expand=True)

    # Create Tabs
    tabs.add("Plan To Read")
    tabs.add("Reading")
    tabs.add("Completed")
    tabs.add("On Hold")
    tabs.add("Dropped")
    tabs.add("Stats")

    all_tabs = ["Plan To Read", "Reading", "Completed", "On Hold", "Dropped"]

    # Setting Up default Page Count and Total Pages for each tab
    page_counters = {tab_name:ctk.StringVar(value="1") for tab_name in all_tabs}
    total_pages = {tab_name:ctk.StringVar(value="1") for tab_name in all_tabs}

    # Add Previous/Next Buttons and Page Counter
    for tab in all_tabs:
        previous_button = ctk.CTkButton(tabs.tab(tab), text="◀", fg_color="#9a4cfa", bg_color="#1f1f1f", hover_color="#b87bff", font=("Helvetica", h/36, "bold"), text_color="#121212", command=lambda: page_change(-1))
        previous_button.place(relx=0.424, rely=0.942, relwidth=0.02)

        page_text_info = ctk.CTkLabel(tabs.tab(tab), text="Page          of ", font=("Helvetica", h/50), text_color="#9a4cfa")
        page_text_info.place(in_=previous_button, relx=1.4, rely=0.1)

        page_counter = ctk.CTkLabel(tabs.tab(tab), textvariable=page_counters[tab], font=("Helvetica", h/50), text_color="#9a4cfa")
        page_counter.place(in_=page_text_info, relx=0.38, rely=0, relwidth=0.4, relheight=1)

        total_pages_counter = ctk.CTkLabel(tabs.tab(tab), textvariable=total_pages[tab], font=("Helvetica", h/50), text_color="#9a4cfa")
        total_pages_counter.place(in_=page_text_info, relx=1, rely=0, relwidth=0.4, relheight=1)

        next_button = ctk.CTkButton(tabs.tab(tab), text="▶", fg_color="#9a4cfa", bg_color="#1f1f1f", hover_color="#b87bff", font=("Helvetica", h/36, "bold"), text_color="#121212", command=lambda: page_change(1))
        next_button.place(in_=previous_button, relx=7.65, rely=0, relwidth=1, relheight=1)

    # Set Default Tab to Reading
    tabs.set("Reading")

    # String Variable that keeps track of the Text in the Search Bar
    search_term = ctk.StringVar()
    search_term.trace_add('write', lambda var, index, mode: update_tab([tabs, add_btn, logout_btn], search_term=search_term))

    # Search Bar to Filter Books through Keywords
    filter_search = ctk.CTkEntry(main_frame, text_color="#818181", fg_color="#1f1f1f", font=("Helvetica", h/42, "bold"), textvariable=search_term)
    filter_search.place(relx=0.5, rely=0.11, relwidth=0.45, relheight=0.06, anchor=ctk.CENTER)

    # Reset Search Bar and open Search Menu
    def add_book_initiator():
        # Open Add Book Menu
        add_book([tabs, add_btn, logout_btn], book_collection_search_term=search_term)

    # Log Out Confirmation and Execution
    def logout(widgets):
        
        win.unbind("<Escape>")

        # Disabling Widgets to avoid complications
        widgets[0].configure(state="disabled")
        widgets[1].configure(state="disabled", fg_color="#3a3a3a", text_color_disabled="#777777")
        widgets[2].configure(state="disabled")
        for widget in widgets[0].tab(widgets[0].get()).winfo_children():
            if ("label" not in str(widget)) and (widget.cget("text") in ["◀", "▶"]):
                widget.configure(state="disabled", fg_color="#3a3a3a", text_color_disabled="#777777")
            else:
                widget.configure(state="disabled")

        logout_confirmation = ctk.CTkFrame(win, bg_color="#1f1f1f", fg_color="#0f0f0f", corner_radius=h/45)
        logout_confirmation.place(relx=0.5, rely=0.49, relheight=0.15, relwidth=0.25, anchor=ctk.CENTER)

        # Exit Logout Confirmation Pop-up
        def escape_function(logout_confirmation):
            quit_logout_confirmation(logout_confirmation, widgets)
            update_tab(widgets)

        # Return to Login Page on Log Out
        def return_to_login():
            quit_logout_confirmation(logout_confirmation, widgets)
            main_frame.destroy()
            win.attributes("-fullscreen", False)

            # Remove Auto-Login
            keyring.delete_password(SERVICE_NAME, "Auto-Login")
            login_page(True)

        win.bind("<Escape>", lambda event, logout_confirmation=logout_confirmation: escape_function(logout_confirmation))

        prompt_question = ctk.CTkLabel(logout_confirmation, text="Are you sure you want to Log Out?", font=("Helvetica", h/54, "bold"), fg_color="#0f0f0f")
        prompt_question.pack(pady=(30, 0))

        prompt_yes = ctk.CTkButton(logout_confirmation, text="Yes", text_color="#121212", fg_color="#9a4cfa", hover_color="#b87bff", font=("Helvetica", h/67.5, "bold"), command=return_to_login)
        prompt_yes.pack(side="left", padx=(50,0), pady=(5, 0))

        prompt_no = ctk.CTkButton(logout_confirmation, text="No", text_color="#121212", fg_color="#9a4cfa", hover_color="#b87bff", font=("Helvetica", h/67.5, "bold"), command=lambda logout_confirmation=logout_confirmation: escape_function(logout_confirmation))
        prompt_no.pack(side="right", padx=(0,50), pady=(5, 0))

    # Button to open Search for Adding or Removing Books
    add_btn = ctk.CTkButton(main_frame, text="+", text_color="#121212", fg_color="#9a4cfa", bg_color="#1f1f1f", hover_color="#b87bff", font=("Helvetica", h/24, "bold"), width=w/24, height=h/13.5, corner_radius=h/36, command=add_book_initiator)
    add_btn.place(relx=0.91, rely=0.895)

    # Log Out Button
    logout_btn = ctk.CTkButton(main_frame, text="", text_color="#121212", fg_color="#1f1f1f", bg_color="#1f1f1f", hover_color="#2f2f2f", font=("Helvetica", h/24, "bold"), image=ctk.CTkImage(dark_image=Image.open(os.path.join(data_loc, "Images", "Log Out.png")), size=(30,30)), width=0, height=15, command=lambda: logout([tabs, add_btn, logout_btn]))
    logout_btn.place(relx=0.933, rely=0.045)

    # Custom Placeholder Text Method as in-built doesn't work
    search_term.set("Enter Name or ISBN No. of the Book...")
    filter_search.bind("<FocusIn>", lambda event: [filter_search.configure(text_color="#FFFFFF"), search_term.set("")])

    win.update()

    update_tab([tabs, add_btn, logout_btn])

# Add/Remove Books
def add_book(widgets, book_collection_search_term=None, book=None, search=True):
    global saved_widgets, search_bar

    win.unbind("<Escape>")

    # Disabling Widgets to avoid complications
    widgets[0].configure(state="disabled")
    widgets[1].configure(state="disabled", fg_color="#3a3a3a", text_color_disabled="#777777")
    widgets[2].configure(state="disabled")
    for widget in widgets[0].tab(widgets[0].get()).winfo_children():
        try: 
            if ("label" not in str(widget)) and (widget.cget("text") in ["◀", "▶"]):
                widget.configure(state="disabled", fg_color="#3a3a3a", text_color_disabled="#777777")
            else:
                widget.configure(state="disabled")
        except:
            pass

    search_frame = ctk.CTkFrame(win, bg_color="#1f1f1f", fg_color="#0f0f0f", corner_radius=h/27)
    search_frame.place(relx=0.5, rely=0.5, relheight=0.1, relwidth=0.1, anchor=ctk.CENTER)

    # Frame Grow Animation
    size = 0
    while size <= 0.8:
        search_frame.place_configure(relwidth=size, relheight=size)
        
        win.update()
        sleep(0.008)

        size += 0.06

    size=0.8
    search_frame.place_configure(relwidth=size, relheight=size)

    # Close Add Book Menu
    def escape_function(search_frame, book_collection_search_term):
        quit_add_books(search_frame, widgets)
        update_tab(widgets, book_collection_search_term)

    win.bind("<Escape>", lambda event, search_frame=search_frame, book_collection_search_term=book_collection_search_term: escape_function(search_frame, book_collection_search_term))

    if search:
        # String Variable that keeps track of the Text in the search_bar
        search_term = ctk.StringVar()
        search_term.trace_add('write', lambda var, index, mode: run_thread(search_frame, search_term))

        # Search Bar has no Placeholder Text since Textvariable used, a bug in CustomTkinter
        search_bar = ctk.CTkEntry(search_frame, text_color="#818181", fg_color="#1f1f1f", textvariable=search_term)
        search_bar.place(relx=0.48, rely=0.1, relwidth=0.45, relheight=0.06, anchor=ctk.CENTER)

        # Custom Placeholder Text Method as in-built doesn't work
        search_term.set("Enter Name or ISBN No. of the Book...")
        search_bar.bind("<FocusIn>", lambda event: [search_bar.configure(text_color="#FFFFFF"), search_term.set("")])

        saved_widgets = [search_bar]

    else:
        
        saved_widgets = None
        win.after(100, lambda: get_book(search_frame, book))

# Run threads to Run simultaneous Searches
def run_thread(search_frame, search_term):

    if search_term.get() != "Enter Name or ISBN No. of the Book...":
        thread = threading.Thread(target=lambda: update_search(search_frame, search_term))
        thread.start()

# Remove Old Recommendations or Recommendations from Half Completed Search from Screen
def kill_recommendation(recommendation, search_term, search_text):

    # Function to Check whether Recommendation is old or not
    def check_and_destroy():
        if search_text != search_term.get():
            recommendation.destroy()
            return

        # Recurse until Recommendation is destroyed
        win.after(100, check_and_destroy)

    check_and_destroy()

# Fetch Book Recommendations based on Search Term
def update_search(search_frame, search_term):

    search_text = search_term.get()

    # Wait for 0.5 seconds of user inactivity
    time.sleep(0.5)

    if (search_term.get() != search_text) or (len(search_term.get()) == 0):
        return

    # Get Recommendations based on Search Term
    recommendations = get_book_details(search_text)

    list_of_recommendations = []
    def load_recommendation(book):

        with urllib.request.urlopen(book["thumbnail"]) as u:
            raw_data = u.read()

        # Replace Default "No Image Found" with provided one
        if raw_data == no_image_raw_data:
            image = create_rounded_image(os.path.join(data_loc, "Images", "No Image Found.png"), 35)
        else:
            image = create_rounded_image(io.BytesIO(raw_data), 35)

        recommendation = ctk.CTkButton(search_frame, text=book["title"][:search_page_cap], font=("Helvetica", h/65, "bold"), image=ctk.CTkImage(dark_image=image, size=(w/8.53, h/4.32)), fg_color="#0f0f0f", hover_color="#1f1f1f", compound=ctk.TOP, anchor="w", width=w/8.53 + 25, height=h/4.32 + 65, command=lambda book=book: get_book(search_frame, book, search_term))
        recommendation.bind("<Enter>", lambda event, recommendation=recommendation: start_marquee(False, recommendation, book["title"]+"      ", speed=150))
        recommendation.bind("<Leave>", lambda event, recommendation=recommendation: stop_marquee(False, recommendation, book["title"]))
        try:
            thread = threading.Thread(target=lambda search_text=search_text: kill_recommendation(recommendation, search_term, search_text))
            thread.start()

            list_of_recommendations.append(recommendation)

        except:
            pass

    # Use Threading to Load Recommendations Simultaneously

    threads = []
    for book in recommendations:
        thread = threading.Thread(target=lambda book=book: load_recommendation(book))
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    win.unbind("<Motion>")

    for widget in search_frame.winfo_children():
        if "ctklabel" in str(widget):
            widget.destroy()

    # Place Recommendations in Grid

    iteration = 0
    relative_y = 0.2

    try:
        for recommendation in list_of_recommendations:

            if iteration % 5 == 0:
                recommendation.place(in_=search_frame, relx=0.03, rely=relative_y, relwidth=0.16, relheight=0.35)
                relative_y = 0.6
            else:
                recommendation.place(in_=prev_recommendation, relx=1.2, rely=0, relwidth=1, relheight=1)

            prev_recommendation = recommendation
            iteration += 1
    
    except:
        pass

# Fetch Book Details
def get_book(search_frame, book, search_term=None):

    # To check whether this function is being used by the Search Method or just to see a Saved Book
    if search_term:
        search_term.set("")

        with urllib.request.urlopen(book["thumbnail"]) as u:
            raw_data = u.read()
    else:
        raw_data = book["thumbnail"]

    # Replace Default "No Image Found" with provided one
    if raw_data == no_image_raw_data:
        image = Image.open(os.path.join(data_loc, "Images", "No Image Found.png"))
    else:
        image = Image.open(io.BytesIO(raw_data)).convert('RGB')

    image_enhancer = ImageEnhance.Brightness(image)
    enhanced_image = image_enhancer.enhance(1)

    for widget in search_frame.winfo_children():
        if widget not in saved_widgets:
            widget.destroy()
    
    # Placeholder for the Image of the Book
    bg = ctk.CTkLabel(search_frame, text="", fg_color="#0f0f0f")
    
    # To check whether this function is being used by the Search Method or just to see a Saved Book. Place everything slightly higher in absence of the Search Bar
    if search_term:
        bg.place(relx=0.05, rely=0.25, relwidth=0.22, relheight=0.5)
    else:
        bg.place(relx=0.05, rely=0.2, relwidth=0.22, relheight=0.5)

    image = ctk.CTkLabel(search_frame, text="", image=ctk.CTkImage(dark_image=enhanced_image, size=(search_frame.winfo_width()/100 * 25, search_frame.winfo_height()/100 * 50)))
    image.place(in_=bg, relx=0, rely=0, relwidth=1, relheight=1)

    details_order = {"title":"Title", "authors":"Author(s)", "language":"Language", "isbn10":"ISBN-10", "isbn13":"ISBN-13", "publisher":"Publisher", "publish_date":"Publish Date", "categories": "Categories", "page_count":"Pages", "description":"Description", "maturity_rating":"Maturity Rating"}

    # Filling Book Details
    text = ""

    for heading in details_order.keys():
        heading_content = book[heading]
        if heading_content != "":
            text += f"{details_order[heading]}: {heading_content}\n\n"

    # Text Widget to display Textual Data of the Book
    text_widget = ctk.CTkTextbox(search_frame, font=("Helvetica", h/67.5, "bold"), fg_color="#0f0f0f", wrap=ctk.WORD)
    text_widget.insert(ctk.END, text)
    text_widget.configure(state=ctk.DISABLED)
    text_widget.place(in_=bg, relx=1.2, rely=0, relheight=1.4, relwidth=3)

    # Display Buttons if hovering over the Image
    def check_hover(event):
        if (win.winfo_pointerx() > bg.winfo_rootx()) and (win.winfo_pointerx() < bg.winfo_rootx()+bg.winfo_width()) and (win.winfo_pointery() > bg.winfo_rooty()) and (win.winfo_pointery() < bg.winfo_rooty()+bg.winfo_height()):
            enhanced_image = image_enhancer.enhance(0.5)
            image.configure(image=ctk.CTkImage(dark_image=enhanced_image, size=(search_frame.winfo_width()/100 * 25, search_frame.winfo_height()/100 * 50)))

            new_properties = False

            prev_widget = bg
            for widget in place_order:
                if not new_properties: widget.place(in_=prev_widget, relx=0.2, rely=0.12, relheight=0.1, relwidth=0.65)
                else: widget.place(in_=prev_widget, relx=0, rely=1.35, relheight=1, relwidth=1)
                prev_widget = widget
                new_properties = True
        
        else:
            
            for widget in place_order:
                widget.place_forget()
            
            enhanced_image = image_enhancer.enhance(1)
            image.configure(image=ctk.CTkImage(dark_image=enhanced_image, size=(search_frame.winfo_width()/100 * 25, search_frame.winfo_height()/100 * 50)))

    # Perform Actions based on Button Pressed
    def button_action(btn, var):
        
        btn.configure(state="disabled")

        book["thumbnail"] = raw_data
        
        btn_text = var.get()
        track_book(account_loc, book, btn_text)

        var.set("✔")
        win.after(500, lambda: var.set(btn_text))

        win.after(500, lambda: btn.configure(state="normal"))

    # Buttons Displayed on Hovering and Add Book to SQL Database
    book_plan_var = ctk.StringVar(value="Plan To Read")
    book_reading_var = ctk.StringVar(value="Reading")
    book_completed_var = ctk.StringVar(value="Completed")
    book_hold_var = ctk.StringVar(value="On Hold")
    book_dropped_var = ctk.StringVar(value="Dropped")
    book_remove_var = ctk.StringVar(value="Remove From List")

    book_plan_btn = ctk.CTkButton(search_frame, textvariable=book_plan_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_plan_btn, book_plan_var))
    book_reading_btn = ctk.CTkButton(search_frame, textvariable=book_reading_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_reading_btn, book_reading_var))
    book_completed_btn = ctk.CTkButton(search_frame, textvariable=book_completed_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_completed_btn, book_completed_var))
    book_hold_btn = ctk.CTkButton(search_frame, textvariable=book_hold_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_hold_btn, book_hold_var))
    book_dropped_btn = ctk.CTkButton(search_frame, textvariable=book_dropped_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_dropped_btn, book_dropped_var))
    book_remove_btn = ctk.CTkButton(search_frame, textvariable=book_remove_var, font=("Helvetica", h/60, "bold"), fg_color="#1f1f1f", hover_color="#3f3f3f", corner_radius=0, command=lambda: button_action(book_remove_btn, book_remove_var))

    place_order = [book_plan_btn, book_reading_btn, book_completed_btn, book_hold_btn, book_dropped_btn, book_remove_btn]

    win.bind("<Motion>", check_hover)

def main():
    global account_loc

    win.resizable(False, False)
    
    # Open Main Application Directly if Auto-Login Exists
    if not keyring.get_password(SERVICE_NAME, "Auto-Login"):
        login_page(True)
    else:
        user = keyring.get_password(SERVICE_NAME, "Auto-Login")
        account_loc = os.path.join(data_loc, "Accounts", user)
        book_collection(user)

    win.bind("<Escape>", quit_application)

    win.mainloop()

if __name__ == "__main__":
    
    main()