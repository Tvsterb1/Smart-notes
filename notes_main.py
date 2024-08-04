#start to create smart notes app
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
app=QApplication([])
window=QWidget()
window.setWindowTitle("Smart Note")
window.resize(800,650)

textEdit=QTextEdit()
lb_listnote=QLabel("List of notes")
lb_listing=QLabel("List of tags")
Listnote=QListWidget()
Listing=QListWidget()
look=QLineEdit("Enter tag.")

create_note=QPushButton("Create note")
Save_note=QPushButton("Save note")
Delete_note=QPushButton("Delete note")
Add_to_note=QPushButton("Add to note")
Untag=QPushButton("Untag from note")
Search=QPushButton("Search note by tag")

Full=QHBoxLayout()
col1=QVBoxLayout()
col2=QVBoxLayout()
col2_1=QHBoxLayout()
col2_2=QHBoxLayout()

col1.addWidget(textEdit)
col2.addWidget(lb_listnote)
col2.addWidget(Listnote)
col2_1.addWidget(create_note)
col2_1.addWidget(Delete_note)
col2.addLayout(col2_1)
col2.addWidget(Save_note)
col2.addWidget(lb_listing)
col2.addWidget(Listing)
col2.addWidget(look)
col2_2.addWidget(Add_to_note)
col2_2.addWidget(Untag)
col2.addLayout(col2_2)
col2.addWidget(Search)

with open("note_data.json", 'r') as file:
    notes = json.load(file)

Listnote.addItems(notes)

def show_note():
    title = Listnote.selectedItems()[0].text()
    textEdit.setText(notes[title]["text"])

    Listing.clear()
    Listing.addItems(notes[title]["tag"])
def show_msg(text):
    msg=QMessageBox()
    msg.setWindowTitle("Importent message!")
    msg.setText(text)
    msg.show()
    msg.exec()
def add_note():
    note_name, ok = QInputDialog.getText(
        window,"Add note","Note name:"
    )
    if ok and note_name != "":
        notes[note_name]={
            "text": "",
            "tag":[]
        }
        Listnote.addItem(note_name)

def write_to_file():
    with open("note_data.json","w") as file:
        json.dump(notes,file,sort_keys=True)

def save_note():
    if Listnote.selectedItems():
        note_name=Listnote.selectedItems()[0].text()
        notes[note_name]["text"] = textEdit.toPlainText()
        write_to_file()
        show_msg("Note has been saved")
    else:
        show_msg("Note has not been selected!")

def del_note():
    if Listnote.selectedItems():
        note_name=Listnote.selectedItems()[0].text()
        del notes[note_name]
        write_to_file()
        textEdit.clear()
        Listing.clear()
        Listnote.clear()
        Listnote.addItems(notes)
        show_msg("Note has been deleted!")
    else:
        show_msg("Note has not been selected!")

def add_tag():
    if Listnote.selectedItems():
        note_name=Listnote.selectedItems()[0].text()
        tag=look.text()
        if tag:
            notes[note_name]["tag"].append(tag)
            write_to_file()
            look.clear()
            Listing.clear()
            Listing.addItems(notes[note_name]["tag"])
    else:
        show_msg("Note has not been selected!")

def del_tag():
    if Listnote.selectedItems():
        note_name=Listnote.selectedItems()[0].text()
        if Listing.selectedItems():
            tag=Listing.selectedItems()[0].text()
            if tag:
                notes[note_name]["tag"].remove(tag)
                write_to_file()
                look.clear()
                Listing.clear()
                Listing.addItems(notes[note_name]["tag"])
        else:
            show_msg("Tag is not selected!")
    else:
        show_msg("Note is not selected!")

def search_tag():
    if Search.text()=="Search note by tag":
        Search.setText("Clear Search")
        filter_note=[]
        tag=look.text()
        for note in notes:
            if tag in notes[note]["tag"]:
                filter_note.append(note)
        Listnote.clear()
        Listnote.addItems(filter_note)
    else:
        Search.setText("Search note by tag")
        textEdit.clear()
        Listing.clear()
        look.clear()
        Listnote.clear()
        Listnote.addItems(notes)

Listnote.clicked.connect(show_note)
create_note.clicked.connect(add_note)
Save_note.clicked.connect(save_note)
Delete_note.clicked.connect(del_note)
Add_to_note.clicked.connect(add_tag)
Untag.clicked.connect(del_tag)
Search.clicked.connect(search_tag)
Full.addLayout(col1,stretch=2)
Full.addLayout(col2,stretch=1)
window.setLayout(Full)
window.show()
app.exec_()