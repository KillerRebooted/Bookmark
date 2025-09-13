
# Bookmark

Bookmark is a Python Desktop Application based on `customtkinter` to Search, View & Store the info of Books locally, with option to have multiple Profiles/Accounts for multiple Users on the same device.
This Application is to help keep track of your Reading History.
## Features

- Works on Mac/Windows/Linux
- Search Books by ISBN Number or Name
- Save Books and their Reading Status Locally
- Make Multiple Profiles
- Display Overall Reading Stats

## Usage/Examples

Use the `Bookmark.py` to Run the Application

### Sign Up

![Sign Up Demo](https://github.com/KillerRebooted/Bookmark/blob/main/README%20Images/Sign%20Up%20Demo.png)

After the App opens, click on `SIGN UP`, enter `Username` and `Password` and click `Sign Up` Button.

### Login

After Registering, go back to `LOGIN` and use the Registered Credentials and click `Login`

### Add Book

![Add Book Demo](https://github.com/KillerRebooted/Bookmark/blob/main/README%20Images/Add%20Book%20Demo.png)

Click on `+` Icon and Search the Book by using it's Name or ISBN-10/13 Number and wait for a few seconds. Here the Search Term being used is `One Punch Man` and upto 10 results are displayed.

![Book Actions Demo](https://github.com/KillerRebooted/Bookmark/blob/main/README%20Images/Book%20Actions%20Demo.png)

Choose a Book and Click on it. Hover over the Image to display various actions and choose the desired one.

Press `Escape` to close the Menu

### Moving/Removing a Book

Click on the Tab to which the Book was added (here, `Completed`) and the Book will be visible.

Click on the Book to View the Book Info. Click on any other action to move it to another Tab. Click on `Remove From List` from the actions to Remove it from Saved Books.

### Filtering Saved Books

Click on the Arrow Keys at the bottom of the yab to switch between pages and use the Search Bar at the top to look for a specific Book within the tab.

### Stats Tab

![Stats Tab Demo](https://github.com/KillerRebooted/Bookmark/blob/main/README%20Images/Stats%20Tab%20Demo.png)

Check out Reading Stats in the Stats Tab such as Books Read/Completed, Pages Read etc. along with the Longest Book Read.

### Quitting the Application

Pressing `Escape` while not Viewing Book Info or in the Add Book Menu exits the Application

### Auto-Login

Once Logged In, whenever the Application is opened, it will open the last closed Profile unless logged out.

![Logout Demo](https://github.com/KillerRebooted/Bookmark/blob/main/README%20Images/Logout%20Demo.png)

To Logout, instead of pressing `Escape`, press the `Power Off` Icon in the top left and Press `Yes`. It will go back to the Login Page which can be closed using the `Escape` or the `Close` Button.

## Book API

This project utilizes the free-to-use Google Books API. If an ISBN Number doesn't get a result, it's either not in the Google Database or the Internet Connection is unstable.

## Authors

- [@Shreyas Nair](https://www.github.com/KillerRebooted)

## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
