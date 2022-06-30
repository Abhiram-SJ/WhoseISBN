"""A simple Book detail fetcher using the 10 digit isbn number"""

import PySimpleGUI as sg
import webbrowser
import json
from urllib.request import urlopen

def fetch(ISBN):
    # function to fetch details of the book via isbn
    isbn = ISBN.strip()
    if len(isbn) == 10:
        url =  "https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn
        resp = urlopen(url)
        book_data = json.load(resp)
        try:
            book_info = book_data['items'][0]['volumeInfo']
        except:
            return False
        keys = ['title','authors','publisher','publishedDate','pageCount','description','categories','language','averageRating','imageLink','previewLink']
        keys_book_data = book_info.keys()
        book_details = {}
        for key in keys:
            if key in keys_book_data:
                book_details[key] = book_info[key]
            else:
                book_details[key] = None
        for key , value in book_details.items():
            print(key+" : ",value)
        return book_details
    else:
        print("Please enter a 10 digit isbn number...")
        return False
def GUI():
    # GUI window
    Data = None
    book_detail_layout = [
        [sg.Text("Name :", size = (15,1)),sg.Text("",key = "-BOOKNAME-"),sg.Text("Language :"),sg.Text("",key = "-LANG-")],
        [sg.Text("Author/s :", size = (15,1)), sg.Listbox(values = [],size = (15,2),key = "-AUTHORS-")],
        [sg.Text("Category :",size=(15,1)),sg.Listbox(values = [],size = (15,2),key="-CATEGORY-")],
        [sg.Text("Publisher :", size = (15,1)),sg.Text("",key="-PUBLISHER-")],
        [sg.Text("Published :",size=(15,1)),sg.Text("",key="-DATE-")],
        [sg.Text("About")],
        [sg.Multiline("",size = (100,8),disabled=True,key = "-ABOUT-")],
        [sg.Button("preview Link >>",key ="-LINK-",visible=False)]
    ]
    layout = [
        [sg.Text("ISBN no :", size = (7,1)),sg.Input(size = (25,1),key = "-ISBN-"),sg.Button("Get Details",key = "-FETCH-")],
        [sg.Frame(title="Book Detail",layout=book_detail_layout,tooltip="Book Detail")]
    ]
    window = sg.Window(title="whoseISBN",layout=layout, size = (720,420))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-FETCH-":
            Data = fetch(ISBN = values["-ISBN-"])
            if Data:
                window["-BOOKNAME-"].update(Data["title"])
                window["-LANG-"].update(Data["language"])
                window["-AUTHORS-"].update(values=Data["authors"])
                window["-CATEGORY-"].update(values = Data["categories"])
                window["-PUBLISHER-"].update(Data["publisher"])
                window["-DATE-"].update(Data["publishedDate"])
                window["-ABOUT-"].update(Data["description"])
                if Data["previewLink"]:
                    window["-LINK-"].update(visible=True)
            else:
                sg.popup("ISBN not found!!!")
                window["-ISBN-"].update("")
        elif event == "-LINK-":
            if Data and Data["previewLink"]:
                webbrowser.open(Data["previewLink"])
            else:
                pass

    window.close()

if __name__ == "__main__":
    GUI()