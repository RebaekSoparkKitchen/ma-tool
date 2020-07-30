'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-05-12 13:40:05
@LastEditors: FlyingRedPig
@LastEditTime: 2020-07-30 12:34:32
@FilePath: \EDM\edm\Transfer\gui.py
'''
import tkinter as tk
import edm.Transfer.transfer_csv_to_excel as ce
from tkinter import filedialog
import json

class DataTransfer(object):

    def __init__(self):

        self.input_path = self.readConfig()['transfer']['input_path']
        self.output_path = self.readConfig()['transfer']['output_path']
        
        self.root = tk.Tk()
        self.root.title("Data Transfer Tool")
        self.root.geometry('800x1000')

        self.e1 = tk.Entry(self.root, width=70, show=None, relief='groove')
        self.e1.insert(0,self.input_path)
        self.e1.place(x=160,y=300, anchor='nw')

        self.e2 = tk.Entry(self.root, width=70, show=None)
        self.e2.insert(0,self.output_path)
        self.e2.place(x=160, y=350, anchor='nw')

        self.l1 = tk.Label(self.root, text='input path', show = None)
        self.l1.place(x=80,y=300, anchor='nw')

        self.l1 = tk.Label(self.root, text='output path', show = None)
        self.l1.place(x=78,y=350, anchor='nw')

        self.b1 = tk.Button(self.root,text='transfer',width=15,height=2,command=self.transfer_format)
        self.b1.place(x=280, y=400, anchor='nw')

        self.b2 = tk.Button(self.root,text='Browse...',width=15,height=1,command=self.select_open_path)   #Browse按钮
        self.b2.place(x=600, y=298, anchor='nw')

        self.b2 = tk.Button(self.root,text='Save as...',width=15,height=1,command=self.select_save_path)   #Save as按钮
        self.b2.place(x=600, y=350, anchor='nw')
        return

    def readConfig(self):
        '''
        从config文件中读取tracker path
        '''
        configPath = r'../config/config.json'
        with open(configPath,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
        
        return json_data

    def select_open_path(self):
        '''
        为browse按钮写的，删除默认路径，填上选中路径
        :return:
        '''
        file_path = filedialog.askopenfilename(initialdir=self.input_path)
        self.e1.delete(0, tk.END)
        self.e1.insert(0, file_path)

    def select_save_path(self):
        '''
        为save as按钮写的
        :return:
        '''
        save_path = filedialog.asksaveasfilename(defaultextension='xlsx',initialdir=self.output_path,filetypes=[('Excel file', '.xlsx'),('all files','.*')])
        self.e2.delete(0, tk.END)
        self.e2.insert(0, save_path)


    def transfer_format(self):

        input_path = self.e1.get()
        output_path = self.e2.get()

        file = ce.ExportedData(input_path)
        file.to_xlsx(output_path)
        return

    def execute(self):
        self.root.mainloop()

if __name__ == "__main__":
    d = DataTransfer()
    d.execute()
