from encode_decode import *
from tkinter import Tk, Label, filedialog, Button, Entry, ttk

decoded_msg = ""


class Gui:
    def __init__(self):
        self.image = None
        self.root = Tk()
        self.root.geometry("400x400")

        self.notebook = ttk.Notebook(self.root)
        self.encode_frame = ttk.Frame(self.notebook)
        self.decode_frame = ttk.Frame(self.notebook)

        # encode tab
        Label(self.encode_frame, text="Enter message:").pack()
        self.msg = Entry(self.encode_frame, width=35)
        self.msg.pack()
        self.browse_button = Button(self.encode_frame, text="Browse Image", command=self.read_image)
        self.submit_button = Button(self.encode_frame, text="Encode", command=lambda: self.encode_img(self.msg.get()))
        self.browse_button.pack()
        self.submit_button.pack()

        # decode tab
        self.decode_browse_button = Button(self.decode_frame, text="Browse Image", command=self.read_image)
        self.decode_submit_button = Button(self.decode_frame, text="Decode",
                                           command=lambda: self.decode_msg(self.image))
        self.decode_browse_button.pack()
        self.decode_submit_button.pack()
        Label(self.decode_frame, text="Decoded Message:").pack()

        self.notebook.add(self.encode_frame, text='Encode')
        self.notebook.add(self.decode_frame, text='Decode')
        self.notebook.pack()

    def read_image(self):
        path = filedialog.askopenfilename(title="Select Image",
                                          filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png")])
        self.image = Image.open(path)

    def encode_img(self, text):
        if self.image is None:
            Label(self.root, text="Please insert image").pack()
        elif text == "":
            Label(self.root, text="Please insert text.").pack()
        else:
            encode(text, self.image)
            Label(self.root, text="Successfully encoded image.").pack()

    def decode_msg(self, img):
        # if image is browsed
        if img is not None:
            global decoded_msg
            decoded_msg = decode(img)
            Label(self.decode_frame, text=decoded_msg).pack()
        else:
            Label(self.decode_frame, text="Please insert image.").pack()


if __name__ == "__main__":
    g = Gui()
    g.root.mainloop()
