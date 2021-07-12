import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import shutil




name = 'BFR'

class Elements:
    def __init__(self, master):
        self.master = master

    # method for all button processes
    def button(self, char, funct, lambdaVal, x_, y_, algn, rows):
        if lambdaVal == '':
            self.b = tk.Button(self.master, text=char, command=funct)
        else:
            self.b = tk.Button(self.master, text=char, command=lambda: funct(lambdaVal))
        self.b.grid(row=y_, column=x_, sticky=algn, rowspan=rows, ipadx=5, ipady=5)

    # method for calling a text entry dialog
    def textField(self, lbl, w_, x_, y_):
        textField = tk.Entry(self.master, width=w_)
        textField.grid(row=y_, column=x_ + 1, sticky=tk.W, ipadx=5, ipady=5)
        textField_lbl = tk.Label(self.master, text=lbl)
        textField_lbl.grid(row=y_, column=x_, sticky=tk.E, ipadx=5, ipady=5)
        return textField

    def check(self, char, var, x_, y_):
        check = tk.Checkbutton(self.master, text=char, variable=var)
        check.grid(column=x_, row=y_)

    def label1(self, char, x_, y_, algn, rows, cols):
        self.b = tk.Label(self.master, text=char)
        self.b.grid(row=y_, column=x_, sticky=algn, rowspan=rows, columnspan=cols)

    def label2(self, charVariable, x_, y_, algn):
        self.b = tk.Label(self.master, textvariable=charVariable)
        self.b.grid(row=y_, column=x_, sticky=algn)






class MainArea(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.master = master

        # Frame for all controls
        self.f1 = tk.LabelFrame(self, text='Controls', borderwidth=1, padx=10, pady=10, relief='raised')
        self.f1.grid(row=0, column=0, sticky='NSEW', columnspan=1)
        # Frame for source list
        self.f2 = tk.Frame(self, borderwidth=0, relief='raised', pady=10)
        self.f2.grid(row=1, column=0, sticky='NSEW',columnspan=1)
        self.f2.columnconfigure(0, weight=1)
        self.f2.rowconfigure(0, weight=1)


        # Individual elements
        # Display results and status
        self.file_tree = result_window(self.f2)

        # self.result_tree = result_window(self.f2, self.database, headers, headings)
        # Controls
        el = Elements(self.f1)
        el.button("Source", self.selectPath, '', 0, 0, tk.W + tk.E, 1)  # Selection of root directory
        el.button("Destination", self.selectDestination, '', 1, 0, tk.W + tk.E, 1)  # Selection of destination directory

        self.source_file_path = ''
        self.destination_file_path = ''
        self.db = []
        el.button("Copy", self.bulk_copy, '', 2, 0, tk.W + tk.E, 1)  # Execute bulk copy commnad

    # method for calling directory picker
    def selectPath(self):
        self.source_file_path = appFuncs.selectPath(self.source_file_path)
        self.structure()

    def selectDestination(self):
        self.destination_file_path = appFuncs.selectPath(self.destination_file_path)
        print(self.destination_file_path)

    def structure(self):
        file_list = Path(self.source_file_path).rglob("*.nii*")
        self.file_list = [row for row in file_list]
        self.file_tree.fileList = self.file_list
        self.file_tree.display()


    def bulk_copy(self):
        parent_directory = Path(self.source_file_path).parents[0]
        que = [int(i) for i in self.file_tree.tree.selection()]
        file_stems = [Path(self.file_list[i]).relative_to(self.source_file_path) for i in que]

        for subject_path in Path(parent_directory).iterdir():
            for file_stem in file_stems:
                in_path = subject_path/file_stem  # source file
                if in_path.is_file():
                    out_path = Path(self.destination_file_path)/Path(subject_path).name/file_stem # destination file
                    Path(out_path.parents[0]).mkdir(parents=True, exist_ok=True)    # create destination foldr if it does not exist
                    shutil.copyfile(in_path,out_path)



class result_window:
    def __init__(self, parent):
        # Draw a treeview of a fixed type

        self.parent = parent

        self.fileList = []
        self.tree = ttk.Treeview(self.parent, show='headings', columns='filename')
        self.tree.grid(sticky='NSEW')
        self.tree.column("#0", width=120, minwidth=25)
        self.tree.heading("#0", text="", anchor='w')
        self.tree.heading("filename", text = "File Name")
        self.tree.column("filename", width=200, stretch=tk.YES, anchor='center')


        self.tree.bind('<Button-1>', self.left_click)
        self.last_focus = None
        self.clickID = 1000000

    def display(self):
        self.delete()
        index = iid = 0

        for row in self.fileList:
            name = Path(row).name
            self.tree.insert("", index, iid, values=(name))
            index = iid = index + 1

        self.parent.update_idletasks()



    def delete(self):
        self.tree.delete(*self.tree.get_children())

    def left_click(self, event):
        iid = self.tree.identify_row(event.y)
        self.clickID = iid







#   helper class for common use functions
class appFuncs:

    # Generates file dialog box
    @staticmethod
    def selectPath(file_path):
        f = tk.filedialog.askdirectory()
        if f!='':
            file_path=f
        return file_path

    # generates output folder path
    @staticmethod
    def generateOutpath(inPath, prefix, suffix):
        z=inPath.stem.replace(prefix,'');  z=z+suffix
        outPath = (Path(inPath).parent) / z
        return outPath






class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.title(name)
        parent.minsize(800,500)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        # Components
        self.mainarea = MainArea(parent, borderwidth=1, relief=tk.RAISED)
        # configurations
        self.mainarea.grid(column=0, row=0, sticky='WENS')



root = tk.Tk()
PR = MainApp(root)
root.mainloop()