import tkinter as tk
import transfer_csv_to_excel as ce
from tkinter import filedialog

root = tk.Tk()
root.title("Zinan's sweet secretary")
root.geometry('800x1000')

e1 = tk.Entry(root, width=70, show=None, relief='groove')
e1.insert(0,"C:/Users/C5293427/Desktop/Data_exported/csv_file/")
e1.place(x=160,y=300, anchor='nw')

e2 = tk.Entry(root, width=70, show=None)
e2.insert(0,"C:/Users/C5293427/Desktop/Data_exported/成品/")
e2.place(x=160, y=350, anchor='nw')

l1 = tk.Label(root, text='input path', show = None)
l1.place(x=80,y=300, anchor='nw')

l1 = tk.Label(root, text='output path', show = None)
l1.place(x=78,y=350, anchor='nw')

def select_open_path():
    '''
    为browse按钮写的，删除默认路径，填上选中路径
    :return:
    '''
    file_path = filedialog.askopenfilename(initialdir='C:/Users/C5293427/Desktop/Data_exported/csv_file')
    e1.delete(0, tk.END)
    e1.insert(0, file_path)

def select_save_path():
    '''
    为save as按钮写的
    :return:
    '''
    save_path = filedialog.asksaveasfilename(defaultextension='xlsx',initialdir='C:/Users/C5293427/Desktop/Data_exported/成品',filetypes=[('Excel file', '.xlsx'),('all files','.*')])
    e2.delete(0, tk.END)
    e2.insert(0, save_path)


def transfer_format():

    input_path = e1.get()
    output_path = e2.get()

    file = ce.ExportedData(input_path)
    file.to_xlsx(output_path)
    return

b1 = tk.Button(root,text='transfer',width=15,height=2,command=transfer_format)
b1.place(x=280, y=400, anchor='nw')

b2 = tk.Button(root,text='Browse...',width=15,height=1,command=select_open_path)   #Browse按钮
b2.place(x=600, y=298, anchor='nw')

b2 = tk.Button(root,text='Save as...',width=15,height=1,command=select_save_path)   #Save as按钮
b2.place(x=600, y=350, anchor='nw')


root.mainloop()
