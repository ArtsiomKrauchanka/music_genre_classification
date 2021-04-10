import os
from tkinter import *
from tkinter import ttk
from classifier import Classifier
from tkinter import filedialog


class Main:
    def __init__(self, root):
        self._classifier = Classifier()
        self._bd_name = os.path.basename(self._classifier.get_db_name())
        self._track_path = ''
        self.root = root
        self.root.title("Genre classificator")
        self.bdPathLab = Label(root, text="Data base: " + str(self._bd_name))
        self.bdPathLab.config(font=("Courier", 10), width=25)
        self.bdPathLab.grid(row=0, column=0, ipadx=10, sticky=W)
        self.trPathLab = Label(root, text="Audio: " + str(self._track_path))
        self.trPathLab.config(font=("Courier", 10), width=25)
        self.trPathLab.grid(row=0, column=2, ipadx=10, sticky=W)
        self.delimiter1 = ttk.Separator(root, orient='horizontal')
        self.delimiter1.grid(row=1, column=0, columnspan=3, ipadx=10, sticky=W + E)
        self.optionsLab = Label(root, text="Menu:")
        self.optionsLab.grid(row=2, column=1, ipadx=10, sticky=W)
        self.changeBdLab = Label(root, text="choose data base")
        self.changeBdLab.grid(row=3, column=0, ipadx=10, sticky=W)
        self.changeTrLab = Label(root, text="choose audio")
        self.changeTrLab.grid(row=4, column=0, ipadx=10, sticky=W)
        self.delimiter2 = ttk.Separator(root, orient='horizontal')
        self.delimiter2.grid(row=5, column=0, columnspan=3, ipadx=10, sticky=W + E)
        self.startLab = Label(root, text=" Start")
        self.startLab.grid(row=6, column=1, ipadx=10, sticky=W)
        self.delimiter3 = ttk.Separator(root, orient='horizontal')
        self.delimiter3.grid(row=7, column=0, columnspan=3, ipadx=10, sticky=W + E)
        self.knnLab = Label(root, text="KNN")
        self.knnLab.config(font=("Courier", 10))
        self.knnLab.grid(row=8, column=0, ipadx=10, sticky=W)
        self.bayesLab = Label(root, text="Bayes")
        self.bayesLab.config(font=("Courier", 10), width=15)
        self.bayesLab.grid(row=8, column=2, ipadx=10, sticky=W)
        self.knnGenre1 = Label(root, text="1.")
        self.knnGenre1.grid(row=9, column=0, ipadx=10, sticky=W)
        self.knnGenre2 = Label(root, text="2.")
        self.knnGenre2.grid(row=10, column=0, ipadx=10, sticky=W)
        self.knnGenre3 = Label(root, text="3.")
        self.knnGenre3.grid(row=11, column=0, ipadx=10, sticky=W)
        self.knnGenre4 = Label(root, text="4.")
        self.knnGenre4.grid(row=12, column=0, ipadx=10, sticky=W)
        self.knnGenre5 = Label(root, text="5.")
        self.knnGenre5.grid(row=13, column=0, ipadx=10, sticky=W)
        self.bayesGenre1 = Label(root, text="1.")
        self.bayesGenre1.grid(row=9, column=2, ipadx=10, sticky=W)
        self.bayesGenre2 = Label(root, text="2.")
        self.bayesGenre2.grid(row=10, column=2, ipadx=10, sticky=W)
        self.bayesGenre3 = Label(root, text="3.")
        self.bayesGenre3.grid(row=11, column=2, ipadx=10, sticky=W)
        self.bayesGenre4 = Label(root, text="4.")
        self.bayesGenre4.grid(row=12, column=2, ipadx=10, sticky=W)
        self.bayesGenre5 = Label(root, text="5.")
        self.bayesGenre5.grid(row=13, column=2, ipadx=10, sticky=W)
        self.delimiter4 = ttk.Separator(root, orient='horizontal')
        self.delimiter4.grid(row=14, column=0, columnspan=3, ipadx=10, sticky=W + E)
        self.statusLab = Label(root, text="Status")
        self.statusLab.grid(row=15, column=1, ipadx=10, sticky=W)
        self.delimiter5 = ttk.Separator(root, orient='horizontal')
        self.delimiter5.grid(row=16, column=0, columnspan=3, ipadx=10, sticky=W + E)

        self.changeBdLab.bind('<Enter>', self.enter_leave)
        self.changeBdLab.bind('<Leave>', self.enter_leave)
        self.changeBdLab.bind("<Button-1>", self.change_db)

        self.changeTrLab.bind('<Enter>', self.enter_leave)
        self.changeTrLab.bind('<Leave>', self.enter_leave)
        self.changeTrLab.bind('<Button-1>', self.choose_file)

        self.startLab.bind('<Enter>', self.enter_leave)
        self.startLab.bind('<Leave>', self.enter_leave)
        self.startLab.bind('<Button-1>', self.count_approx)

    def enter_leave(self, event):
        if str(event.type) == 'Enter':
            event.widget.configure(foreground="blue")
        elif str(event.type) == 'Leave':
            event.widget.configure(foreground="black")

    def change_db(self, event):
        path = filedialog.askdirectory(parent=self.root, title='Please select a directory')
        self.statusLab['text'] = "Changing db"
        self._classifier.change_db(path)
        self._bd_name = self._classifier.get_db_name()
        base_name = os.path.basename(self._bd_name)
        self.bdPathLab['text'] = "Data base: " + str(base_name)
        self.statusLab['text'] = "Done"

    def choose_file(self, event):
        path = filedialog.askopenfile(parent=self.root, title='Please select an audio .wav').name
        base_name = os.path.basename(path)
        self.trPathLab['text'] = "Audio: " + str(base_name)
        self._track_path = path

    def count_approx(self, event):
        if len(self._track_path) > 0:
            self.statusLab['text'] = "Analyzing"
            knn_genres = self._classifier.approximate(self._track_path, mode="knn")[0]
            bayes_genres = self._classifier.approximate(self._track_path, mode="bayes")[0]

            self.knnGenre1['text'] = "1. " + knn_genres[0]
            self.knnGenre2['text'] = "2. " + knn_genres[1]
            self.knnGenre3['text'] = "3. " + knn_genres[2]
            self.knnGenre4['text'] = "4. " + knn_genres[3]
            self.knnGenre5['text'] = "5. " + knn_genres[4]
            self.bayesGenre1['text'] = "1. " + bayes_genres[0]
            self.bayesGenre2['text'] = "2. " + bayes_genres[1]
            self.bayesGenre3['text'] = "3. " + bayes_genres[2]
            self.bayesGenre4['text'] = "4. " + bayes_genres[3]
            self.bayesGenre5['text'] = "5. " + bayes_genres[4]

            self.statusLab['text'] = "Done"
        else:
            self.statusLab['text'] = "Choose audio"


def main():
    root = Tk()
    app = Main(root)
    root.mainloop()


if __name__ == "__main__":
    main()
