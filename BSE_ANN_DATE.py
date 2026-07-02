import PIL.Image
import PIL.ImageTk
import json,tkinter as tk, requests,datetime as dt,threading,tkinter.messagebox as mg, os,PIL

# important for process

headers={"Accept": "application/json, text/plain, */*",
        # "Accept-Encoding":"gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "api.bseindia.com",
        "Origin": "https://www.bseindia.com",
        "Referer": "https://www.bseindia.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
list=[]
i,page_no=1,0
ann_date=0

#--------------------------------------------------------------------
def page():
    ann_date=v.get()
    date_entry.config(state='disabled')
    link=f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=-1&strPrevDate={ann_date}&strScrip=&strSearch=P&strToDate={ann_date}&strType=C&subcategory=-1"
    response=requests.get(url=link,headers=headers)
    count=0
    if response.status_code==200:
        try:
            data=response.json()["Table1"]
            for i in data:
                for j in i.values():
                    count=j
        except:blank_label.config(text=f"Error in Taking count.\n Status code: {response.status_code}")
        blank_label.config(text=f"{count} Announcement")
    else:blank_label.config(text=f"Error in connecting to BSE. Error code :{response.status_code}")
    global page_no
    page_no=int((count/50)+1)
    get_page.config(text=f'{int((count/50)+1)} Pages',state='disabled')
    return

#--------------------------------------------------------------------


    

        
#--------------------------------------------------------------------

def export_file():
    Export_btn.config(state='disabled')
    if os.path.exists(f'BSE_ann_{today}.json'):
        os.remove(f'BSE_ann_{today}.json')
        with open(f'BSE_ann_{today}.json','w') as my_file:
            json.dump(list,my_file,indent=4)
            my_file.close()
        mg.showinfo(title="Export Json file",message=f"sucessfuly exported file {len(list)}")
    else:
        with open(f'BSE_ann_{today}.json','w') as my_file:
            json.dump(list,my_file,indent=4)
            my_file.close()
        mg.showinfo(title="Export Json file",message=f"sucessfuly exported file {len(list)}")
    list.clear()
    app.destroy()
#--------------------------------------------------------------------

def get_data():
    print(page_no)
    download_ann.config(state='disabled')
    Export_btn.config(state='disabled')
    ann_date=v.get()
    for i in range(1,page_no+1):
        print("runing",i)
        url=f'https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno={i}&strCat=-1&strPrevDate={ann_date}&strScrip=&strSearch=P&strToDate={ann_date}&strType=C&subcategory='
        response=requests.get(url=url,headers=headers)
        if response.status_code==200:
            jsn=response.json()['Table']
            for j in range(len(jsn)):list.append(jsn)
        else:blank_label.config(text=f"Error code {i} downloading Ann",fg='#800000')
        download_ann.config(text=f"Page no.{i} Downloaded")
        app.update_idletasks()
    download_ann.config(fg='green',text='Downloading Done')
    Export_btn.config(state='normal')

#--------------------------------------------------------------------

if __name__=="__main__":
    today=dt.datetime.today().strftime('%Y%m%d')
    #--------------------------------------------------------------
    # app Start
    app=tk.Tk()
    app.title('BSE Announcement')
    app.resizable(False,False)
    #app.minsize(602,324)
    app.geometry('602x470')
    app.config(bg='white')
    # Main Container
    main_frame=tk.Frame(app,bg='white')
    main_frame.pack(fill='both')
    tk.Label(main_frame,text="BSE Announcement Process",font=('arial',22,'bold'),height=2,bg="white",fg='#800000').pack()
    
    #----------------------------------------------------------------------------------------------------------------------------
    # Frames for process
    second_frame=tk.Frame(main_frame,bg='#800000',height=2)
    second_frame.pack(fill='both')

    tk.Label(second_frame,text="Announcement Date: ",padx=10,pady=10,bg='#800000',fg='white',font=('arial',12,'bold'),width=25,anchor='e').grid(row=0,column=0,pady=10)
    #-----------------------------------------------------------------------------------------------------------------------------
    # Date Entry Section
    v=tk.StringVar()
    date_entry=tk.Entry(second_frame,font=('arial',12,'bold'),textvariable=v,width=10,justify='center')
    date_entry.grid(row=0,column=1)
    v.set(today)

    #---------------------------------------------------------------------------------------------------------
    #blank Label
    blank_label=tk.Label(second_frame,text="Blank Label",fg='white',font=('arial',12,'bold'),bg='#800000')
    blank_label.grid(row=0,column=2,padx=15)

    #----------------------------------------------------------------------------------------------------------
    # # Blank Space Label bg='#800000'
    tk.Label(main_frame,height=1,bg='#800000').pack(fill='x')
    
    #----------------------------------------------------------------------------------------------------------
    # Buttons Frame bg='#800000'
    third_frame=tk.Frame(main_frame,bg='#800000',height=20)
    third_frame.pack(fill='both',expand=True)
    #----------------------------------------------------------------------------------------------------------
    # Buttons
    get_page=tk.Button(third_frame,text="Get page counts",width=30,font=('arial',12,'bold'),height=1,command=lambda:page())
    get_page.pack(side='top',padx=10,pady=20)

    download_ann=tk.Button(third_frame,text="Download Announcement",width=30,font=('arial',12,'bold'),
                           activebackground='red',height=1,command=threading.Thread(target=get_data).start)
    download_ann.pack(side='top',padx=10,pady=20)

    Export_btn=tk.Button(third_frame,text="Export Json file",width=30,font=('arial',12,'bold'),height=1,command=export_file)
    Export_btn.pack(side='top',padx=10,pady=20)

    app.mainloop()

