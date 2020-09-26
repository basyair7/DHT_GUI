from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import serial
import datetime
import threading
import time

# Create a database to store data
conn = sqlite3.connect("DHT_Data.db")
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS port_board(
            id_dev INTEGER PRIMARY KEY,
            name_board TEXT,
            date TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS dht_data(
            id_dev INTEGER,
            name_board TEXT,
            real_data TEXT,
            date TEXT)""")

# Input port arduino in database
def conn_device():
    try:
        id_device = id_port.get()
        name_board = id_board.get()

        # Open database
        conn = sqlite3.connect("DHT_Data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM port_board")

        alright = 0
        for row in c.fetchall():
            if int(row[0]) == int(id_device):
                alright = 1

        if alright == 0:
            if messagebox.askokcancel('Informasi', '1. Pastikan Serial Port benar-benar sudah dihapus\n2. Serial Port hanya terisi 1x sekali dan jika mau mengganti port lain harap hapus port terlebih dahulu\n\nLanjutkan?', icon='warning') == True:
                id_device = id_port.get()
                name_board = id_board.get()

                # Create a real date and time
                now = datetime.datetime.now()
                date = now.day
                month = now.month
                year = now.year
                Time = (now.strftime("%H:%M:%S"))
                date_time = f"{date}/{month}/{year} {Time}"

                # Insert data in device
                c.execute("INSERT INTO port_board VALUES (:id_dev, :name_board, :date)",
                {
                    'id_dev': id_device,
                    'name_board': name_board,
                    'date': date_time
                })

                # Show port device
                c.execute("SELECT *, oid FROM port_board")
                device_port = c.fetchall()
                print_connection = ""
                for show in device_port:
                    print_connection += f"{show[1]} on COM{show[0]} ({show[2]})"

                # Show device in listbox
                messagebox.showinfo('Informasi', f"{name_board} (COM{id_device}) sudah terhubung")
                info_box.insert(END, " ", print_connection)


        elif alright == 1:
            messagebox.showwarning('Informasi', 'Serial Port sudah ada')

            # Show device in listbox
            c.execute("SELECT *, oid FROM port_board")
            device_port = c.fetchall()
            print_connection = ""
            for show in device_port:
                print_connection += f"{show[1]} on COM{show[0]} ({show[2]})"

            # Show device in listbox
            info_box.insert(END, " ", print_connection)

    except:
        messagebox.showerror('Terjadi kesalahan', '1. Serial Port tidak boleh kosong!\n2. Isi angka saja')
        info_box.insert(END, " ","Terjadi kesalahan, Silahkan coba lagi...")

    # Close database
    conn.commit()
    conn.close()

    # Clear input box
    id_port.delete(0,END)
    id_board.delete(0,END)

# Get data dht
def getData():
    try:
        # Create a real date and time
        now = datetime.datetime.now()
        date = now.day
        month = now.month
        year = now.year
        Time = (now.strftime("%H:%M:%S"))
        date_time = f"{date}/{month}/{year} {Time}"

        # Open database
        conn = sqlite3.connect("DHT_Data.db")
        c = conn.cursor()

        # connect to board
        c.execute("SELECT *, oid FROM port_board")
        device_port = c.fetchall()
        print_port = ""
        print_nameBoard = ""
        for show in device_port:
            print_port += f"COM{show[0]}"
            print_nameBoard += f"{show[1]}"

        board = serial.Serial(print_port, 9600) # see in device manager or port in tool arduino

        # Get data
        data_dht = board.readline()
        decode_values = str(data_dht[0:len(data_dht)].decode("utf-8"))
        print(f"\n{date_time} --> {print_nameBoard} ({print_port}) >> {decode_values}")
        # Save in database
        c.execute("INSERT INTO dht_data VALUES (:id_dev, :name_board, :real_data, :date)",
        {   'id_dev': print_port,
            'name_board': print_nameBoard,
            'real_data': decode_values,
            'date': date_time
        })

        # disconnected
        board.close()

        # Show information
        info_box.insert(END," ", '***Done***')
        messagebox.showinfo('Informasi', 'Data sudah diambil.')
        # Close database
        conn.commit()
        conn.close()

    except:
        messagebox.showerror("Terjadi kesalahan", "1. Pastikan Serial Port sudah diisi\n2. Pastikan Serial Port sama di arduino ide... \n3. Pastikan board sudah diupload program utamanya dan tidak terputus kabel datanya")
        info_box.insert(END," ","Terjadi kesalahan... Silahkan coba lagi")
        info_box.insert(END,"1.Pastikan serial port sama di arduino ide... ")
        info_box.insert(END,"2.Pastikan board sudah diupload program utamanya dan tidak terputus kabel datanya")

# Show data
def showData():
    def replay():
        try:
            replay_num = id_replay.get()
            minutes = id_minute.get()
            minutes = float(minutes)
            replay_num = int(replay_num)
            # Ask question yes or no
            ask = messagebox.askquestion("Konfirmasi", f"Data akan ditampilkan {replay_num}x selama {minutes} menit\n\n\nNote : \n1. Saat data diproses, mohon jangan ditutup\n2. Semakin banyak pengulangan, semakin lama prosesnya (Tergantung pada menitnya), Disarankan tidak lebih dari 30 menit.\n\nLanjutkan?")
            if ask == 'yes':
                # Open database
                conn = sqlite3.connect("DHT_Data.db")
                c = conn.cursor()

                for i in range(replay_num):
                    # connect to board
                    c.execute("SELECT *, oid FROM port_board")
                    device_port = c.fetchall()
                    print_port = ""
                    print_nameBoard = ""
                    for show in device_port:
                        print_port += f"COM{show[0]}"
                        print_nameBoard += f"{show[1]}"

                    board = serial.Serial(print_port, 9600) # see in device manager or port in tool arduino

                    # Create a real date and time
                    now = datetime.datetime.now()
                    date = now.day
                    month = now.month
                    year = now.year
                    Time = (now.strftime("%H:%M:%S"))
                    date_time = f"{date}/{month}/{year} {Time}"

                    # Get data
                    data_dht = board.readline()
                    decode_values = str(data_dht[0:len(data_dht)].decode("utf-8"))
                    print(f"\n{date_time} --> {print_nameBoard} ({print_port}) >> {decode_values}")
                    # Print data
                    result_box.insert(END, f"\n{date_time} --> {print_nameBoard} ({print_port}) >> {decode_values}")
                    # Save in database
                    c.execute("INSERT INTO dht_data VALUES (:id_dev, :name_board, :real_data, :date)",
                    {   'id_dev': print_port,
                        'name_board': print_nameBoard,
                        'real_data': decode_values,
                        'date': date_time
                    })

                    c.execute("SELECT *, oid FROM dht_data")
                    data = c.fetchall()
                    list_data = ""
                    for getdata in data:
                        list_data += f"\n{getdata[3]} --> {getdata[1]} ({getdata[0]}) >> {getdata[2]}"

                    # disconnected
                    board.close()

                    # Looping
                    proses_loop = minutes*60
                    proses_loop = float(proses_loop)
                    time.sleep(proses_loop)

                messagebox.showinfo('Informasi', 'Selesai...')

                # Close database
                conn.commit()
                conn.close()

        except:
            messagebox.showerror("Terjadi kesalahan", "1. Pastikan board sudah connect\n2. Isi data diulang, hanya angka saja (*ex : 5 1 = 5x perulangan per 1 menit)\n3. Jangan tutup layar saat proses pengambilan data...")
            info_box.insert(END," ","Terjadi kesalahan... Silahkan coba lagi")

        # Clear input box
        id_replay.delete(0, END)
        id_minute.delete(0, END)

    # Create tkinter home showData
    global home_showData
    home_showData = Tk()
    home_showData.title('Tampilkan Data')
    home_showData.geometry('890x540')

    # Frame
    frm_showData = Frame(home_showData, relief=RIDGE, borderwidth=5)
    frm_showData.grid(row=0, column=0, padx=(10,0), pady=12)
    frm_button2 = Frame(home_showData, relief=RIDGE, borderwidth=5)
    frm_button2.grid(row=1, column=0)

    # Label
    lbl_replay = Label(frm_button2, text="Data diulang :\t\t")
    lbl_replay.grid(row=0, column=0, padx=5, pady=(10,0))
    lbl_minute1 = Label(frm_button2, text="X  Per ")
    lbl_minute1.grid(row=0, column=2, padx=10, pady=(10,0))
    lbl_minute2 = Label(frm_button2, text="\tMenit")
    lbl_minute2.grid(row=0, column=3, padx=10, pady=(10,0))

    # Input box
    id_replay = Entry(frm_button2, width=10)
    id_replay.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,0))
    id_minute = Entry(frm_button2, width=10)
    id_minute.grid(row=0, column=2, columnspan=20, padx=10, pady=(10,0))

    # Scrollbar
    scrolltxt_y = Scrollbar(frm_showData, orient=VERTICAL)
    scrolltxt_y.grid(row=1, column=1, columnspan=1, ipady=170)

    # Result box
    result_box = Text(frm_showData, yscrollcommand=scrolltxt_y.set)
    result_box.grid(row=1, column=0, ipadx=100, ipady=2)
    scrolltxt_y.config(command=result_box.yview)

    # Button
    btn_replay = Button(frm_button2, text='OK', command=threading.Thread(target=replay).start)
    btn_replay.grid(row=2, column=1, padx=10, pady=12, ipadx=10)

    # Open Database
    conn = sqlite3.connect("DHT_Data.db")
    c = conn.cursor()
    # Get data
    c.execute("SELECT *, oid FROM dht_data")
    data = c.fetchall()
    list_data = ""
    for getdata in data:
        list_data += f"\n{getdata[3]} --> {getdata[1]} ({getdata[0]}) >> {getdata[2]}"

    # Print data
    result_box.insert(END, list_data)

    # Close database
    conn.commit()
    conn.close()

    # Mainloop
    home_showData.mainloop()

# Delete data in database
def delete():
    def del_port():
        ask = messagebox.askquestion('Hapus Data Port', 'yakin port akan dihapus?')
        if ask == 'yes':
            # Open database
            conn = sqlite3.connect("DHT_Data.db")
            c = conn.cursor()
            # Delete table port_board
            c.execute("DROP TABLE IF EXISTS port_board;")
            c.execute("""CREATE TABLE IF NOT EXISTS port_board(
                    id_dev INTEGER PRIMARY KEY,
                    name_board TEXT,
                    date TEXT)""")

            # Close database
            conn.commit()
            conn.close()

            # Clear info box
            info_box.delete(0, END)
            # Show messagebox
            if messagebox.askyesno('Informasi', 'Data sensor sudah dihapus\n\nKembali ke menu?') == True:
                home_del.destroy()
                info_box.insert(END, " ","***Data port sudah dihapus***")

    def del_data():
        ask = messagebox.askquestion('Hapus data sensor', 'yakin semua data sensor akan dihapus?')
        if ask == 'yes':
            # Open database
            conn = sqlite3.connect("DHT_Data.db")
            c = conn.cursor()
            # Delete table dht_data
            c.execute("DROP TABLE IF EXISTS dht_data;")
            c.execute("""CREATE TABLE IF NOT EXISTS dht_data(
                    id_dev INTEGER,
                    name_board TEXT,
                    real_data TEXT,
                    date TEXT)""")

            # Close database
            conn.commit()
            conn.close()

            # Show messagebox
            if messagebox.askyesno('Informasi', 'Data sensor sudah dihapus\n\nKembali ke menu?') == True:
                home_del.destroy()
                info_box.insert(END, " ","***Data sensor sudah dihapus***")

    global home_del
    home_del = Tk()
    home_del.title("Hapus Data"); home_del.geometry('250x128')

    # Frame
    frm_button3 = Frame(home_del, relief=RIDGE, borderwidth=5)
    frm_button3.grid(row=0, column=0, padx=12, pady=12, ipadx=30)

    # Button
    btn_del_port = Button(frm_button3, text="Hapus port", command=del_port)
    btn_del_port.grid(row=0, column=0, columnspan=2, padx=(10,0), pady=10, ipadx=30)
    btn_del_sensor = Button(frm_button3, text="Hapus data sensor", command=del_data)
    btn_del_sensor.grid(row=1, column=0, columnspan=2, padx=(10,0), pady=10, ipadx=10)

    # Mainloop
    home_del.mainloop()


# Save program in txt
def saveData():
    # Open Database
    conn = sqlite3.connect("DHT_Data.db")
    c = conn.cursor()
    # Result data
    c.execute("SELECT *, oid FROM dht_data")
    records = c.fetchall()
    print_connection = ""
    # get data
    for getdata in records:
        print_connection += f"{getdata[3]} --> {getdata[1]} ({getdata[0]}) >> {getdata[2]}"

    # Create name for txt
    f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if f is None:
        return

    # Save data in txt
    f.write(print_connection)
    f.close()

    # Show information
    info_box.insert(END," ", "Data Telah Disimpan...")
    messagebox.showinfo('Informasi', 'Data sudah disimpan')

    # Close database
    conn.commit()
    conn.close()


# Exit in program
def exit():
    ask = messagebox.askquestion('Keluar', 'yakin keluar dari aplikasi?')
    if ask == 'yes':
        quit()

# About application
def about_me():
    messagebox._show("About Me", "Aplikasi Data Sensor DHT GUI\n\nVersion : v1.1\nProgrammer : Basyair7")

#<----------------Main Menu-------------------->
# Create hmoe app tkinter
home = Tk(); home.geometry('355x480')
home.title("Aplikasi Data Sensor DHT")

# Frame layout
frm_port = Frame(home, relief=RIDGE, borderwidth=5)
frm_port.grid(row=0, column=0, ipadx=1, ipady=5, padx=5, pady=10)
frm_button = Frame(home, relief=RIDGE, borderwidth=5)
frm_button.grid(row=1, column=0, ipadx=10)
frm_info = Frame(home, relief=RIDGE, borderwidth=5)
frm_info.grid(row=2, column=0, padx=10, pady=10, ipadx=1)

# Label Port board
lbl_board = Label(frm_port, text="Type Arduino Board (*ex: Ardunio UNO) : ")
lbl_board.grid(row=0, column=1, columnspan=3, padx=10, pady=(10,0))
lbl_port = Label(frm_port, text="Serial Port COM (*ex: angkanya saja) : ")
lbl_port.grid(row=1, column=1, columnspan=3)

# Input Port board
id_board = Entry(frm_port, width=10)
id_board.grid(row=0, column=4, padx=10, pady=(10,0))
id_port = Entry(frm_port, width=10)
id_port.grid(row=1, column=4)

# Button Menu
# Button connect
btn_connect = Button(frm_button, text="Connect", command=conn_device)
btn_connect.grid(row=0, column=0, columnspan=2, padx=(10,0), pady=10, ipadx=23)
# Button get data
btn_getData = Button(frm_button, text="Ambil Data", command=getData)
btn_getData.grid(row=1, column=0, columnspan=2, padx=(10,0), ipadx=17)
# Button save data
btn_save = Button(frm_button, text="Simpan Data", command=saveData)
btn_save.grid(row=0, column=2, padx=30, ipadx=20)
# Button delete
btn_delete = Button(frm_button, text="Hapus Data", command=delete)
btn_delete.grid(row=1, column=2, ipadx=23)
# Button show data
btn_show = Button(frm_button, text="Tampilkan Data", command=showData)
btn_show.grid(row=2, column=0, padx=(10,0), pady=10, ipadx=6)
# Button exit
btn_exit = Button(frm_button, text="Keluar", command=exit)
btn_exit.grid(row=2, column=2, ipadx=38)
# Button about program
btn_about = Button(home, text='About Me', command=about_me)
btn_about.grid(row=3, column=0, padx=10, pady=8, ipadx=15)

# Scroll Bar
scroll_y = Scrollbar(frm_info, orient=VERTICAL)
scroll_y.grid(row=0, column=1, columnspan=1, ipady=57)
scroll_x = Scrollbar(frm_info, orient=HORIZONTAL)
scroll_x.grid(row=1, column=0, ipadx=100)

# Listbox
info_box = Listbox(frm_info, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
info_box.grid(row=0, column=0, columnspan=1, ipadx=85)
scroll_x.config(command=info_box.xview)
scroll_y.config(command=info_box.yview)

# home window mainloop
home.mainloop()
