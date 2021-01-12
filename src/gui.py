from encode_decode import *
from tkinter import Tk,Label,filedialog,Frame,Button,Entry
from PIL import ImageTk

class Gui():
    
    def __init__(self):
        self.root=Tk()
        Label(self.root,text="Enter mesage:").pack()
        self.msg=Entry(self.root,width=35)
        self.msg.pack()
        self.button = Button(self.root,text="Browse Image", command=self.read_image)
        self.button.pack()

    def read_image(self):
        path=filedialog.askopenfilename(title="Select Image",filetypes=[("JPG File","*.jpg"),("PNG File","*.png")])
        self.image = Image.open(path)


if __name__ == "__main__":
    g=Gui()
    g.root.mainloop()
