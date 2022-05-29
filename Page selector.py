from tkinter import filedialog
import PyPDF2
from tkinter import *
from os import walk

class Parameters:
    first_time = True #will be set to false after a file is selected for the first time
    lower = None #lower bound of the range
    upper = None #upper bound of the range
    lower_filled = False 
    upper_filled = False
    extra_pages = set() #additional pages
    all_pages = [] #all pages that will be exported
    filename = "" #address of the input file
    directory = "" #address of the output folder
    
    @classmethod
    def first_select(cls):
        cls.first_time = False

    @classmethod
    def set_lower(cls, value):
        cls.lower = value

    @classmethod
    def set_upper(cls, value):
        cls.upper = value

    @classmethod
    def lower_fill(cls, value):
        cls.lower_filled = value
    
    @classmethod
    def upper_fill(cls, value):
        cls.upper_filled = value
        
    @classmethod
    def clear_extra(cls):
        cls.extra_pages.clear()

    @classmethod
    def add_extra(cls, value):
        cls.extra_pages.add(int(value))

    @classmethod
    def remove_extra(cls, value):
        cls.extra_pages.remove(int(value))

    @classmethod
    def set_all_pages(cls, value):
        cls.all_pages = value

    @classmethod
    def set_filename(cls, value):
        cls.filename = value

    @classmethod
    def set_directory(cls, value):
        cls.directory = value

    @classmethod
    def range_filled(cls):
        return cls.lower_filled and cls.upper_filled

def combine_pages(span, extra): #combines the range with the extra pages into a single list
    before = [] 
    after = []
    for i in range(len(extra)):
        if extra[i] < min(span):
            before.append(extra[i]) #if a page comes before the range, add it to "before"
        elif extra[i] > max(span):
            after.append(extra[i]) #if a page comes after the range, add it to "after"
    before.sort()
    after.sort()
    return before + span + after

def select_file(): 
    selected = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    if len(selected) > 0:
        Parameters.filename = selected 
        button_pdf.config(text=Parameters.filename)
        button_pdf.config(fg="#000000")
        
        with open(selected, "rb") as temp:
            content = PyPDF2.PdfFileReader(temp)
            label_pages.config(text="Number of pages: " + str(content.numPages))
        if Parameters.first_time: #make sure we're not adding a widget on top of another widget
                Parameters.first_select()
                check_same_folder.grid(row=4, column=5)
                label_same_folder.grid(row=4, column=6, sticky = W)
                label_pages.grid(row=2, column=5, columnspan=2)
        else:
            entry_lower.delete(0, END) #reset the selected pages if it's not the first time a pdf is selected
            entry_upper.delete(0, END)
            pageclear()
        if check.get() == 1: #if the tick box is checked, update the folder button to match
            folder = selected.split("/")[0:-1]
            folder = "/".join(folder)
            Parameters.directory = folder
            button_folder.config(text=folder)         

def select_folder():
    selected = filedialog.askdirectory(title="Select a folder for the output")
    if len(selected) > 0: 
        Parameters.directory = selected
        button_folder.config(text=Parameters.directory, fg="#000000")

def check_changed():
    if check.get() == 1:
        button_folder['state'] = DISABLED
        excess = Parameters.filename.split("/") #split the input address by /
        excess = len(excess[-1]) + 1 #take the length of the namefile +1 to account for the / symbol
        Parameters.directory = Parameters.filename[0:len(Parameters.filename) - excess] #the folder component of the address
        button_folder.config(text=Parameters.directory)
    else:
        button_folder.config(state=NORMAL, fg="#000000")

def lower_callback(a, b, c):
    if len(lower_text.get()) > 0:
        if lower_text.get() == "0":
            entry_lower.delete(0, END) #page 0 is not allowed
        else:
            char = lower_text.get()[-1]
            if not ("0" <= char and char <="9"): #check if the latest input is an interger
                temp = lower_text.get()[:-1]
                entry_lower.delete(0, END) 
                entry_lower.insert(0, temp) #if not, delete it
            else:
                Parameters.lower_fill(True)
    else:
        Parameters.lower_fill(False)
    Parameters.set_lower(lower_text.get())
    if Parameters.range_filled():
        show_summary_range()
    else:
        label_range_info.config(text="")        

def upper_callback(a, b, c):
    if len(upper_text.get()) > 0:
        if upper_text.get() == "0":
            entry_upper.delete(0, END) #page 0 not allowed
        else:
            char = upper_text.get()[-1]
            if not ("0" <= char and char <="9"): #check if the latest input is an interger
                temp = upper_text.get()[:-1]
                entry_upper.delete(0, END)
                entry_upper.insert(0, temp) #if not, delete it
            else:
                Parameters.upper_fill(True)
    else:
        Parameters.upper_fill(False)
    Parameters.set_upper(upper_text.get())
    if Parameters.range_filled():
        show_summary_range()
    else:
        label_range_info.config(text="")

def show_summary_range():
    a = int(entry_lower.get())
    b = int(entry_upper.get())
    label_range_info.config(text="All pages between " + str(min(a, b)) + " and " + str(max(a, b)) + ".")

def extra_callback(a, b, c):
    if len(extra_text.get()) > 0:
        if extra_text.get() == "0":
            entry_extra_pages.delete(0,END) #page 0 not allowed
        else:
            char = extra_text.get()[-1]
            if not char.isdigit():
                temp = extra_text.get()[0:-1]
                entry_extra_pages.delete(0,END)
                entry_extra_pages.insert(0,temp)

def pageadd(*args): #needs argument when the enter key calls it
    if len(entry_extra_pages.get()) > 0:
        Parameters.add_extra(entry_extra_pages.get()) #add the element in the entry box to the set
        entry_extra_pages.delete(0, END)
        summary()
        
def pageremove():
    temp = entry_extra_pages.get()
    if len(temp) > 0:
        if int(temp) in Parameters.extra_pages:
            Parameters.remove_extra(entry_extra_pages.get()) #remove the element in the entry box from the set
            entry_extra_pages.delete(0, END)
            summary()

def pageclear():
    Parameters.clear_extra()
    summary()

def summary():
    if len(Parameters.extra_pages) > 0:
        sorted = list(Parameters.extra_pages)
        sorted.sort()
        temp = ", ".join([str(i) for i in sorted])
        label_pages_added.config(text=temp)
    else:
        label_pages_added.config(text="-")

def create_file_name(iteration):
    address = Parameters.filename.split("/")
    filename = address[-1] #filename plus extension
    filename = filename.split(".")[0] #extract the filename with no extension
    files = []
    for (dirpath, dirnames, filenames) in walk(Parameters.directory):
        files.extend(filenames)
        break
    if filename + "_trimmed.pdf" in files:
        if filename + "_trimmed(" + str(iteration) + ").pdf" in files:
            return create_file_name(iteration + 1)
        else:
            output = Parameters.directory + "/" + filename + "_trimmed(" + str(iteration) + ").pdf"
            return output
    else:      
        output = Parameters.directory + "/" + filename + "_trimmed.pdf"
        return output

def make_pdf(all_pages):
    file = open(Parameters.filename, 'rb')
    reader = PyPDF2.PdfFileReader(file)
    writer = PyPDF2.PdfFileWriter()
    number_pages = 0
    for i in all_pages:
        try:
            writer.addPage(reader.getPage(i))
            number_pages += 1
        except:
            pass #if a selected page is not in the initial file, ignore it
    if number_pages > 0:
        msg = "Successfully exported to \n" + create_file_name(1).split("/")[-1]
        output = open(create_file_name(1), 'wb')
        writer.write(output)
        output.close()
        file.close()
        label_export_result.config(text=msg)
        if number_pages == len(all_pages): #if every selected page is in the initial file
            label_export.config(text="")
        else:
            label_export.config(text="Some pages were not exported", fg="#000000")
    else:
        label_export.config(text="The file doesn't contain any selected page", fg="#C23033")
        label_export_result.config(text="")

def export():
    label_export_result.config(text="")
    filled_pages = (Parameters.range_filled()) or (len(Parameters.extra_pages) > 0)
    filled_file = len(Parameters.filename) > 0
    filled_folder = len(Parameters.directory) > 0
    value = filled_pages and filled_file and filled_folder
    if value:
        label_export.config(text="Exporting...", fg="#3F3F3F")
        additional_pages = list(Parameters.extra_pages)
        additional_pages = [i-1 for i in additional_pages] #take the index offset into account
        try: #if lower and upper bound are specified do this
            lower = int(Parameters.lower)
            upper = int(Parameters.upper)
            region = list(range(min(lower, upper)-1, max(lower, upper)))
            Parameters.set_all_pages(combine_pages(region, additional_pages))
        except: #otherwise do this
            additional_pages.sort() 
            Parameters.set_all_pages(additional_pages) #contains the index for all the selected pages 
        make_pdf(Parameters.all_pages)
    elif filled_pages and filled_file:
        label_export.config(text="Please select a folder", fg="#C23033")
    elif filled_pages and filled_folder:
        label_export.config(text="Please select a file", fg="#C23033")
    elif filled_folder and filled_file:
        label_export.config(text="Please select some pages", fg="#C23033")
    elif filled_pages:
        label_export.config(text="Please select a file and a folder", fg="#C23033")
    elif filled_folder:
        label_export.config(text="Please select a file and some pages", fg="#C23033")
    elif filled_file:
        label_export.config(text="Please select a folder and some pages", fg="#C23033")
    else:
        label_export.config(text="Please select some parameters", fg="#C23033")
     
window = Tk()
window.title("PDF page selector")
window.geometry("700x387")
window.minsize(700, 387)
window.maxsize(700, 500)

try:
    window.iconbitmap("E:/Downloads/maya.ico")
except:
    pass

#labels

label_freespace = Label(window)
label_freespace.grid(row=1)

label_freespace1 = Label(window).grid(row=8, column=0)

label_freespace2 = Label(window).grid(row=5, column=0)

label_pdf = Label(window, padx = 10, text="Select an input file:")
label_pdf.grid(row=2, column=0)

label_pages = Label(window, width=22)
label_pages.grid(row=2, column=5, columnspan=2)

label_output_folder = Label(window, padx = 10, pady=10, text="Select output folder:")
label_output_folder.grid(row=4, column=0)

label_same_folder = Label(window, text="same as the input file", width=17) #will show on the screen after selecting file

label_range = Label(window, text="Select a range:", pady=10)
label_range.grid(row=7, column=0, rowspan=1)

label_from = Label(window, text="From page:", padx=10)
label_from.grid(row=6, column=1, columnspan=1)

label_to = Label(window, text="To page:", padx=10)
label_to.grid(row=6, column=2, columnspan=1)

label_extra_pages = Label(window, text="Add or remove pages: ", padx=10, pady= 10)
label_extra_pages.grid(row=9, column=0)

label_additional = Label(window, text="Additional pages: ", padx=10, pady= 20)
label_additional.grid(row=11, column=0)

label_pages_added = Label(window, text="-", padx=10, pady= 10, wraplength=360)
label_pages_added.grid(row=11, column=1, columnspan=4, sticky = W) 

label_range_info = Label(window, pady= 10, wraplength=300) #will appear after filling in the range
label_range_info.grid(row=7, column=3, rowspan=1, columnspan=2)

label_selected_pages = Label(window, text="The output will contain all the pages between ",pady=10)

label_export = Label(window, padx=0, wraplength=130, pady=0, fg="#C23033", width=0)
label_export.grid(row=13, column=5, rowspan=1, columnspan=2)

label_export_result = Label(window, padx=0, wraplength=300, pady=10, fg="#249D2E")
label_export_result.grid(row=14, column=1, columnspan=4)

#buttons

button_pdf = Button(window, width=54, text="No file selected", fg="#4D4D4D", pady=5, borderwidth=1, command=select_file)
button_pdf.grid(row=2, column=1, columnspan=4)

button_folder = Button(window, width=54, text="No folder selected", fg="#4D4D4D", pady=5, borderwidth=1, command=select_folder)
button_folder.grid(row=4, column=1, columnspan=4)

button_add = Button(window, width=10, text="Add page", padx=8, pady=5, bg="#D9F2DB", borderwidth=1, command= pageadd)
button_add.grid(row=9, column=2)

button_remove = Button(window, width=10, text="Remove page", padx=8, pady=5, bg="#F2D9D9", borderwidth=1, command=pageremove)
button_remove.grid(row=9, column=3)

button_clear = Button(window, width=10, text="Clear pages", padx=8, pady=5, bg="#CECECE", borderwidth=1, command=pageclear)
button_clear.grid(row=9, column=4)

check = IntVar()
check_same_folder = Checkbutton(window, variable=check, onvalue=1, offvalue=0, command=check_changed, padx=2)

button_export = Button(window, text="Export", font="Lucida 14",width=15, padx=100, borderwidth=1, bg="#797979", fg="#F0F0F0", command=export)
button_export.grid(row=13, column=1, columnspan=4, rowspan=1)

#text boxes
lower_text = StringVar()
lower_text.trace_add("write", lower_callback)
entry_lower = Entry(width=8, justify='center', font=('Arial 13'), textvariable=lower_text)
entry_lower.grid(row=7, column=1, columnspan=1)

upper_text = StringVar()
upper_text.trace_add("write", upper_callback)
entry_upper = Entry(width=8, justify='center', font=('Arial 13'), textvariable=upper_text)
entry_upper.grid(row=7, column=2, columnspan=1)

extra_text = StringVar()
extra_text.trace_add("write", extra_callback)
entry_extra_pages = Entry(window, width=8, justify='center', font=('Arial 13'), textvariable=extra_text)
entry_extra_pages.bind('<Return>', pageadd) #bind the enter key to call pageadd
entry_extra_pages.grid(row=9, column=1, columnspan=1)

window.mainloop()
