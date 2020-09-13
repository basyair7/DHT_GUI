#from tkinter import *
#from tkinter import messagebox
import serial
import time
#import sqlite3

board_com = dict()

def input_data(board_com):
    board = str(input("Masukkan tipe arduino(ex : uno) : "))
    for i in board_com.keys():
        if board == i:
            print("Coba lagi!")
            return 0
            break
        
    seri = int(input("Serial port COM(*angkanya saja, ex: 3): "))
    board_com[board] = [seri]
    return 1

def show_data(board_com):
    # Show data
    try:
        board = str(input("Masukkan tipe arduino : "))
        loop = int(input("Berapa kali diulang datanya? : "))
        for i in board_com.keys():
            if board == i:
                seri = board_com[board][0]
                print(f"\nSerial port : COM{seri}")
                print("Result Data : ")

        seri = board_com[board][0]
        arduino = serial.Serial(f"com{seri}", 9600)
        for i in range(loop):
            data_dht = arduino.readline()
            decode_values = str(data_dht[0:len(data_dht)].decode("utf-8"))
            print(decode_values)
            time.sleep(1)
        
        arduino.close()
    except:
        print("\nTerjadi kesalahan... Silahkan coba lagi")
        print("\n1. Pastikan serial port sama di arduino ide... \n2. Pastikan board sudah diupload program utamanya dan tidak terputus kabel datanya")
        print("3. Masukan replay angka saja")

    return 0

while True:
    print("\nProgram include data dht to python")
    print("Version : 1.0\n")
    print("1. Input data \n2. Tampilkan data\n3. Exit")
    select = input("Select : ")

    if(select == "1"):
        input_data(board_com)
    elif(select == "2"):
        show_data(board_com)
    elif(select == "3"):
        break