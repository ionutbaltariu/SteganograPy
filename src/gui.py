import logging
from encode_decode import *
from tkinter import Tk, Label, filedialog, Button, Entry, ttk, END, Frame
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
decoded_msg = ""


# class for the log element
class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.setLevel(logging.DEBUG)
        self.widget = widget
        self.widget.config(state='disabled')
        self.widget.tag_config("INFO", foreground="black")
        self.widget.tag_config("DEBUG", foreground="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("ERROR", foreground="red")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)
        self.red = self.widget.tag_configure("red", foreground="red")

    def emit(self, record):
        self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(END, record.asctime + ": " + self.format(record) + '\n', record.levelname)
        self.widget.see(END)  # Scroll to the bottom
        self.widget.config(state='disabled')
        self.widget.update()  # Refresh the widget


class Gui:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.altered_image = None
        self.root = Tk()
        self.root.title("LSB Steganography Encoder & Decoder")
        self.root.geometry("700x600")
        self.save_path = ""

        self.notebook = ttk.Notebook(self.root)
        self.encode_frame = ttk.Frame(self.notebook)
        self.decode_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        self.console_frame = Frame(self.root)
        self.console_frame.grid(row=0, column=10)

        # encode tab
        Label(self.encode_frame, text="Enter message:").grid(row=0, column=0)
        self.msg = Entry(self.encode_frame, width=35)
        self.msg.grid(row=1, column=0)
        self.browse_button = Button(self.encode_frame, text="Browse Image", command=self.read_image)
        self.store_location_button = Button(self.encode_frame, text="Save Location",
                                            command=lambda: self.save_location())
        self.submit_button = Button(self.encode_frame, text="Encode",
                                    command=lambda: self.encode_img(self.msg.get(), self.save_path))
        self.browse_button.grid(row=2, column=0)
        self.store_location_button.grid(row=3, column=0)
        self.submit_button.grid(row=4, column=0)

        # decode tab
        self.decode_browse_button = Button(self.decode_frame, text="Browse Image", command=self.read_image)
        self.decode_submit_button = Button(self.decode_frame, text="Decode",
                                           command=lambda: self.decode_msg(self.image))
        self.decode_browse_button.grid(row=0, column=0)
        self.decode_submit_button.grid(row=1, column=0)

        # about tab
        self.about_text = Label(self.about_frame, text="\nEncode and decode messages from images\n"
                                                       "Using LSB Steganography.\n"
                                                       "@Baltariu Ionut & Bejenariu Razvan\n"
                                                       "Log provides information in case of misuse.")
        self.about_statistics = Button(self.about_frame, text="Proof of concept.",
                                       command=lambda: self.render_statistics_buttons())
        self.about_text.grid(row=0, column=0)
        self.about_statistics.grid(row=1, column=0)

        self.notebook.add(self.encode_frame, text='Encode')
        self.notebook.add(self.decode_frame, text='Decode')
        self.notebook.add(self.about_frame, text='About')
        self.notebook.grid()

        # Add text widget to display logging info
        self.st = ScrolledText(self.root, state='disabled')
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=0, row=15, sticky='w', columnspan=4)
        # Create textLogger
        text_handler = WidgetLogger(self.st)
        # Logging configuration
        logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)

    def read_image(self):
        # opens a prompt to select the image for the message to be encoded in
        path = filedialog.askopenfilename(title="Select Image to encode a message in",
                                          filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png")])
        logging.info("You've selected the image with the path: " + str(path) + ".")
        try:
            self.image = Image.open(path)
        except AttributeError:
            pass

    def encode_img(self, text, save_path):
        if self.image is None:
            logging.error("Please insert the image to be encoded.")
        elif text == "":
            logging.error("Please insert the message to be encoded in the image.")
        else:
            encode(text, self.image, save_path)
            logging.info("Message successfully encoded.")
            logging.warning("A new window will pop up with the image that contains your message embedded in it.")
            self.image.show(title="Image with encoded message.")
            self.image = None
            logging.warning("If you want to encode in other images select the path again.")

    def decode_msg(self, img):
        # if image is browsed
        if img is not None:
            global decoded_msg
            decoded_msg = decode(img)
            logging.info("The decoded message is: " + decoded_msg)
            self.image = None
        else:
            logging.error("Please insert the image to be decoded.")

    def save_location(self):
        self.save_path = filedialog.askdirectory(title="Select where to save the encoded image. Defaults to /src.")
        logging.warning("You changed the save path to  " + str(self.save_path) + ".")

    def read_original_image(self):
        # opens a prompt to select the image for the message to be encoded in
        path = filedialog.askopenfilename(title="Select Image to encode a message in",
                                          filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png")])
        logging.info("You've selected the image with the path: " + str(path) + ".")
        try:
            self.original_image = Image.open(path)
        except AttributeError:
            pass

    def read_altered_image(self):
        # opens a prompt to select the image for the message to be encoded in
        path = filedialog.askopenfilename(title="Select Image to encode a message in",
                                          filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png")])
        logging.info("You've selected the image with the path: " + str(path) + ".")
        try:
            self.altered_image = Image.open(path)
        except AttributeError:
            pass

    def render_statistics_buttons(self):
        self.notebook.grid_forget()
        Button(self.root, text="Browse original image.",
               command=lambda: self.read_original_image()).grid(row=0, column=0, sticky="NESW")
        Button(self.root, text="Browse image with encoded message.",
               command=lambda: self.read_altered_image()).grid(row=1, column=0, sticky="NESW")

        Button(self.root, text="Submit.",
               command=lambda: self.show_statistics()).grid(row=2, column=0, sticky="NESW")

    def show_statistics(self):
        if self.original_image is None:
            logging.error("Please insert original image.")
        elif self.altered_image is None:
            logging.error("Please insert altered image.")
        else:
            self.st.grid_forget()
            values = []
            original_r, original_g, original_b = self.original_image.split()
            original_r_hist = original_r.histogram()
            original_g_hist = original_g.histogram()
            original_b_hist = original_b.histogram()

            altered_r, altered_g, altered_b = self.altered_image.split()
            altered_r_hist = altered_r.histogram()
            altered_g_hist = altered_g.histogram()
            altered_b_hist = altered_b.histogram()
            fig, axs = plt.subplots(3, 3)
            fig.suptitle('LSB Steganography effects on the image.')
            for i in range(0, 256):
                values.append(i)
            for i in range(0, 3):
                for j in range(0, 3):
                    axs[i, j].autoscale()
            axs[0, 0].set_title('Original')
            axs[0, 1].set_title('Altered')
            axs[0, 2].set_title('Overlapped')
            axs[0, 0].plot(values, original_r_hist, color="red")
            axs[0, 1].plot(values, altered_r_hist, color="red")
            axs[0, 2].plot(values, original_r_hist, color="red")
            axs[0, 2].plot(values, altered_r_hist, color="black")
            axs[1, 0].plot(values, original_g_hist, color="blue")
            axs[1, 1].plot(values, altered_g_hist, color="blue")
            axs[1, 2].plot(values, original_g_hist, color="blue")
            axs[1, 2].plot(values, altered_g_hist, color="black")
            axs[2, 0].plot(values, original_b_hist, color="green")
            axs[2, 1].plot(values, altered_b_hist, color="green")
            axs[2, 2].plot(values, original_b_hist, color="green")
            axs[2, 2].plot(values, altered_b_hist, color="black")

            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().grid(row=4, column=0, sticky="NESW")


if __name__ == "__main__":
    g = Gui()
    g.root.mainloop()
