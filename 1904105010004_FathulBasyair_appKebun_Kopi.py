from urllib.request import urlopen
from tkinter import *
from random import uniform
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import json
import sqlite3
import time

# Create window home Tkinter
home = Tk()
home.title("Aplikasi Data Kebun Kopi");home.geometry("600x300")

# Databases
# create a database or connect to one
conn = sqlite3.connect("kebun_kopi.db")

# Create cursor
kursor = conn.cursor()

# Create table data_pohon
kursor.execute("""CREATE TABLE IF NOT EXISTS data_pohon (
       id_tree INTEGER PRIMARY KEY,
       sensor_tree INTEGER,
       loc_lat REAL,
       loc_lon REAL,
       date TEXT
       )""")

# Create tabel sensor_pohon if not exists
kursor.execute("""CREATE TABLE IF NOT EXISTS type_sensor(
          id_tree INTEGER PRIMARY KEY, date_time TEXT,
          air_temp REAL, air_hum REAL,
          rainfall REAL, uv_lvl REAL,
          soil_temp REAL, soil_hum REAL,
          soil_ph REAL, n_ph REAL,
          p_ph REAL, k_ph REAL
          )""")

# Create submit function for database
def get_loc():
    tree = id_tree.get()

    # create a database or connect to one
    conn = sqlite3.connect("kebun_kopi.db")
    # Create cursor
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM data_pohon")

    alright = 0
    for row in kursor.fetchall():
        if int(row[0]) == int(tree):
            alright = 1

    if alright == 0:
        sensor = sensor_tree.get()
        # connect to api
        address = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm=1904105010004&id_tree={tree}&sensor_type={sensor}"
        # open Url
        url = urlopen(address)
        # read url
        documents = url.read().decode("utf-8")
        # process
        data = json.loads(documents)
        # Get data
        result_id = f"{data['id_tree']}"
        result_sensor = f"{data['sensor_type']}"
        result_date = f"{data['when']}"
        # Search Random location Latitude & Longitude
        for i in range(100):
            loc_lat = uniform(1, 20)
            for j in range(100):
                loc_lon = uniform(1, 360)


        # Insert Into Table data_pohon
        kursor.execute("INSERT INTO data_pohon VALUES (:id_tree, :sensor_tree, :loc_lat, :loc_lon, :date)",
            {
                'id_tree': result_id,
                'sensor_tree': result_sensor,
                'loc_lat': loc_lat,
                'loc_lon': loc_lon,
                'date': result_date
            })

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

    elif alright == 1:
        messagebox.showwarning('Informasi', 'No. ID Sudah Terdata')

    # Clear The Text Boxes
    id_tree.delete(0, END)
    sensor_tree.delete(0, END)

# Create Function to Sensor Tree
def option_sensor():
    def ambil_data():
        tree = id_tree.get()
        for i in range(2):
            time.sleep(i)

        # create Database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create kursor
        kursor = conn.cursor()
        kursor.execute("SELECT * FROM type_sensor")

        alright = 0
        for row in kursor.fetchall():
            if int(row[0]) == int(tree):
                alright = 1


        if alright == 0:
          # Create variabel
          result_api = []
          # Get data
          for sensor_type in range(10):
            address = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm=1904105010004&id_tree={tree}&sensor_type={sensor_type}"
            url = urlopen(address)
            documents = url.read().decode("utf-8")
            data = json.loads(documents)
            result_api.append(data['value'])

            id_kopi = f"{data['id_tree']}"
            date_time = f"{data['when']}"


          # Insert data in Table
          kursor.execute("INSERT INTO type_sensor VALUES (:id_tree, :date_time, :air_temp, :air_hum, :rainfall, :uv_lvl, :soil_temp, :soil_hum, :soil_ph, :n_ph, :p_ph, :k_ph)",
                        {
                            'id_tree': id_kopi,'date_time': date_time,
                            'air_temp': result_api[0],'air_hum': result_api[1],
                            'rainfall': result_api[2],'uv_lvl': result_api[3],
                            'soil_temp': result_api[4],'soil_hum': result_api[5],
                            'soil_ph': result_api[6],'n_ph': result_api[7],
                            'p_ph': result_api[8],'k_ph': result_api[9]
                        })
          # Commit changes
          conn.commit()
          # Close connection
          conn.close()

        elif alright == 1:
            messagebox.showwarning('Informasi', 'On. ID Sudah Terdata')

        id_tree.delete(0, END)


    def show_data():
        opsi_show = Tk()
        opsi_show.title("Semua Data Sensor")
        opsi_show.geometry("600x500")

        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result the database
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # loop thur result
        print_records = ""
        for record in records:
            #Print for looping
            print_records += f"\n\nID : {record[0]}\nDate : {record[1]}\n\nAir Temperature : {record[2]} | Air Humidity : {record[3]} | Rainfall : {record[4]} | UV Level : {record[5]}\nSoil Temperature : {record[6]} | Soil Humidity : {record[7]} | Soil pH : {record[8]}\nN Level : {record[9]} | P Level : {record[10]} | K Level : {record[11]}"

        # Result in label
        title_sensor_result = Label(opsi_show, text="Daftar Data Semua Sensor Setiap ID", font="chilanka")
        title_sensor_result.grid(row=1, column=0, columnspan=2)
        sensor_result = Label(opsi_show, text=print_records, font="chilanka");sensor_result.grid(row=2, column=0, rowspan=40, columnspan=2, padx=10, pady=10)

    def air_temp():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []

        for air_temp in records:
            x.append(air_temp[1]);y.append(air_temp[2])

        # Create plot
        plt.plot(x, y, 'c-o')
        plt.title('Air Temperature')
        plt.show()

        # connect close
        conn.close()
    def air_hum():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []

        for air_hum in records:
            x.append(air_hum[1]);y.append(air_hum[3])

        # Create plot
        plt.plot(x, y, 'c-o');plt.title('Air Humidity')
        plt.show()

        # connect close
        conn.close()
    def rainfall():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []

        for rainfall in records:
            x.append(rainfall[1]);y.append(rainfall[4])

        # Create plot
        plt.plot(x, y, 'b-o');plt.title('Rainfall')
        plt.show()

        # connect close
        conn.close()

    def uv_lvl():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []

        for uv_lvl in records:
            x.append(uv_lvl[1]);y.append(uv_lvl[5])

        # Create plot
        plt.plot(x, y, 'r-o');plt.title('UV Level')
        plt.show()

        # connect close
        conn.close()

    def soil_temp():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []
        for soil_temp in records:
            x.append(soil_temp[1]);y.append(soil_temp[6])

        # Create plot
        plt.plot(x, y, 'k-o');plt.title('Soil Temperature')
        plt.show()

        # connect close
        conn.close()

    def soil_hum():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []
        for uv_lvl in records:

            x.append(uv_lvl[1]);y.append(uv_lvl[7])

        # Create plot
        plt.plot(x, y, 'm-o');plt.title('Soil Humidity')
        plt.show()

        # connect close
        conn.close()
    def soil_ph():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []
        for soil_ph in records:
            x.append(soil_ph[1]);y.append(soil_ph[8])

        # Create plot
        plt.plot(x, y, 'k-o');plt.title('Soil pH')
        plt.show()

        # connect close
        conn.close()
    def n_lvl():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []
        for n_ph in records:

            x.append(n_ph[1]);y.append(n_ph[9])

        # Create plot
        plt.plot(x, y, 'r-o');plt.title('N Level')
        plt.show()

        # connect close
        conn.close()
    def p_lvl():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []
        for p_ph in records:

            x.append(p_ph[1]);y.append(p_ph[10])

        # Create plot
        plt.plot(x, y, 'b-o');plt.title('P Level')
        plt.show()

        # connect close
        conn.close()
    def k_lvl():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # Create variabel
        x = [];y = []

        for p_ph in records:
            x.append(p_ph[1]);y.append(p_ph[11])

        # Create plot
        plt.plot(x, y, 'y-o');plt.title('K Level')
        plt.show()

        # connect close
        conn.close()
    def total_sensor():
        # connect database
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result database from data_sensor
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall();rst_sensor = 2

        for one_tipe in range(0, 10):

            x = [];y = []

            for row in records:
                x.append(row[0]);y.append(row[rst_sensor])

            rst_sensor += 1

            plt.plot(x, y, '-o');plt.title('Hasil Sensor Semua Tanaman')
            plt.legend(['Suhu Udara', 'Kelembaban Udara', 'Curah Hujan', 'Sinar UV', 'SUhu Tanah', 'Kelembaban Tanah', 'pH Tanah', 'N Level', 'P Level','K Level'])
            plt.xlabel('ID Kopi');plt.ylabel('Sensor_type')

        plt.show()

        #connect Close
        conn.close()

    global option_sensor
    option_sensor = Tk()
    option_sensor.title("Sensor Tanaman")
    option_sensor.geometry("540x450")

    # Create text box
    id_tree = Entry(option_sensor, width=30)
    id_tree.grid(row=3, column=1, pady=5)
    # Create Label
    id_tree_lbl = Label(option_sensor, text="ID Pohon\t: ", font="Purisa")
    id_tree_lbl.grid(row=3, column=0, pady=5)
    # Create Button
    id_tree_btn = Button(option_sensor, text="Tambahkan Data", command=ambil_data, font="chilanka")
    id_tree_btn.grid(row=6, column=0, columnspan=1, pady=11, padx=11, ipadx=27)
    result_btn = Button(option_sensor, text="Tampilkan Semua Data", command=show_data, font="chilanka")
    result_btn.grid(row=6, column=1, columnspan=6, pady=12, padx=12, ipadx=5)
    # Create Button Graph
    # air_temp
    air_temp_btn = Button(option_sensor, text="Suhu udara", font="chilanka", command=air_temp)
    air_temp_btn.grid(row=8, column=0, columnspan=1, pady=10, padx=10, ipadx=48)
    # air_hum
    air_hum_btn = Button(option_sensor, text="Kelembaban udara", font="chilanka", command=air_hum)
    air_hum_btn.grid(row=9, column=0, columnspan=1, pady=11, padx=11, ipadx=22)
    # rainfall
    rainfall_btn = Button(option_sensor, text="Curah Hujan", font="chilanka", command=rainfall)
    rainfall_btn.grid(row=10, column=0, columnspan=1,pady=11, padx=11, ipadx=44)
    # uv_lvl
    uv_lvl_btn = Button(option_sensor, text="UV Level", font="chilanka", command=uv_lvl)
    uv_lvl_btn.grid(row=11, column=0, columnspan=1, pady=11, padx=11, ipadx=58)
    # soil_temp
    soil_temp_btn = Button(option_sensor, text="Suhu Tanah", font="chilanka", command=soil_temp)
    soil_temp_btn.grid(row=12, column=0, columnspan=1, pady=11, padx=11, ipadx=45)
    # soil_hum
    soil_hum_btn = Button(option_sensor, text="Kelembaban Tanah", font="chilanka", command=soil_hum)
    soil_hum_btn.grid(row=8, column=1, columnspan=1, pady=11, padx=11, ipadx=15)
    #soil_ph
    soil_ph_btn = Button(option_sensor, text="ph Tanah", font="chilanka", command=soil_ph)
    soil_ph_btn.grid(row=9, column=1, columnspan=1, pady=11, padx=11, ipadx=50)
    #n_lvl
    n_lvl_btn = Button(option_sensor, text="N Level", font="chilanka", command=n_lvl)
    n_lvl_btn.grid(row=10, column=1, columnspan=1, pady=11, padx=11, ipadx=60)
    # p_lvl
    p_lvl_btn = Button(option_sensor, text="P Level", font="chilanka", command=p_lvl)
    p_lvl_btn.grid(row=11, column=1, columnspan=1, pady=11, padx=11, ipadx=60)
    # k_lvl
    k_lvl_btn = Button(option_sensor, text="K Level", font="chilanka", command=k_lvl)
    k_lvl_btn.grid(row=12, column=1, columnspan=1, pady=11, padx=11, ipadx=60)
    # Show all_grafik
    all_grafik_btn = Button(option_sensor, text="Tampilkan Semua Grafik", font="chilanka", command=total_sensor)
    all_grafik_btn.grid(row=13, column=0, columnspan=2, pady=11, padx=11, ipadx=22)



    # Main Loop
    option_sensor.mainloop()


# Create Function to Delete A Record
def option_delete():
    global option_delete
    option_delete = Tk()
    option_delete.title("Hapus Data")
    option_delete.geometry('450x200')
    # delete from ID data
    def delete_1():
        # create a database or connect to one
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        # Create a Delete Button
        kursor = conn.cursor()
        # Delete a record
        kursor.execute("DELETE FROM data_pohon WHERE oid = " + delete_box.get())
        kursor.execute("DELETE FROM type_sensor WHERE oid = " + delete_box.get())
        delete_box.delete(0, END)
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

    # Delete a Tabel data_pohon
    def delete_2():
        # create a database or connect to one
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Delete a tabel
        kursor.execute("DROP TABLE IF EXISTS data_pohon;")
        # Create table data_pohon
        kursor.execute("""CREATE TABLE IF NOT EXISTS data_pohon (
               id_tree INTEGER PRIMARY KEY, sensor_tree INTEGER,
               loc_lat REAL, loc_lon REAL, date TEXT)""")

        kursor.execute("DROP TABLE IF EXISTS sensor_type;")
        # Create Tabel sensor_pohon
        # Create tabel sensor_pohon if not exists
        kursor.execute("""CREATE TABLE IF NOT EXISTS type_sensor (
                  id_tree INTEGER PRIMARY KEY, date_time TEXT,
                  air_temp REAL, air_hum REAL,
                  rainfall REAL, uv_lvl REAL,
                  soil_temp REAL, soil_hum REAL,
                  soil_ph REAL, n_ph REAL,
                  p_ph REAL, k_ph REAL
                  )""")

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

    # Create Text Boxes
    delete_box = Entry(option_delete, width=30)
    delete_box.grid(row=3, column=1, pady=5)
    # Create a label delete
    delete_box_lbl = Label(option_delete, text="Select ID : ", font="Purisa")
    delete_box_lbl.grid(row=3, column=0, pady=5)
    # Create a Delete Button
    delete_btn = Button(option_delete, text="Hapus Data ID", command=delete_1, font="chilanka")
    delete_btn.grid(row=4, column=1, columnspan=1, pady=11, padx=11, ipadx=27)
    # Create a Delete All Button
    del_all_btn = Button(option_delete, text="Hapus Semua Data", command=delete_2, font="chilanka")
    del_all_btn.grid(row=5, column=1, columnspan=1, ipadx=7)

    # Main loop
    option_delete.mainloop()

# Create result function
def result():
    option_result = Tk()
    option_result.title("Tampilkan Data")
    option_result.geometry("900x450")

    # create a database or connect to one
    conn = sqlite3.connect("kebun_kopi.db")
    # Create cursor
    kursor = conn.cursor()
    # Result the database
    kursor.execute("SELECT *, oid FROM data_pohon")

    records = kursor.fetchall()

    # loop thur Result
    print_records = ""
    for record in records:
        # Print for looping
        print_records += f"\n\n id pohon : {record[0]}    |   no. : {record[1]}    |  Latitude : - {record[2]:1.7f}    |  Longitude : {record[3]:1.7f}     |   Date : {record[4]}"

    # Result in box
    title_result = Label(option_result, text="Daftar Data Koordinat ID dan Sensor", font="chilanka")
    title_result.grid(row=1,column=0, columnspan=2)
    result_lbl = Label(option_result, text=print_records, font="chilanka")
    result_lbl.grid(row=2, column=0, rowspan=40, columnspan=2, padx=10, pady=10)
    # Commit changes
    conn.commit()
    # Close connection
    conn.close()

    #Main loop
    option_result.mainloop()

def exit_window():
    answer = messagebox.askquestion("Keluar", "Anda yakin keluar dari Aplikasi?")
    if answer == 'yes':
        quit()

def save_data():
    def save_data1():
        # create a database or connect to one
         conn = sqlite3.connect("kebun_kopi.db")
         # Create cursor
         kursor = conn.cursor()
         # Result the database
         kursor.execute("SELECT *, oid FROM data_pohon")
         records = kursor.fetchall()

         # loop thur Result
         print_records = ""
         for record in records:
             # Print for looping
             print_records += f"\n\n id pohon : {record[0]}    |   no. : {record[1]}    |  Latitude : - {record[2]:1.7f}    |  Longitude : {record[3]:1.7f}     |   Date : {record[4]}"

         f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
         if f is None:
             return

         f.write(print_records)
         f.close()

    def save_data2():
        # create a database or connect to one
        conn = sqlite3.connect("kebun_kopi.db")
        # Create cursor
        kursor = conn.cursor()
        # Result the database
        kursor.execute("SELECT *, oid FROM type_sensor")
        records = kursor.fetchall()

        # loop thur Result
        print_records = ""
        for record in records:
            # Print for looping
           print_records += f"\n\nID : {record[0]}\nDate : {record[1]}\n\nAir Temperature : {record[2]} | Air Humidity : {record[3]} | Rainfall : {record[4]} | UV Level : {record[5]}\nSoil Temperature : {record[6]} | Soil Humidity : {record[7]} | Soil pH : {record[8]}\nN Level : {record[9]} | P Level : {record[10]} | K Level : {record[11]}"

        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return

        f.write(print_records)
        f.close()

    global opsi_savedata
    opsi_savedata = Tk()
    opsi_savedata.title("Save Records Data")
    opsi_savedata.geometry("250x150")

    save_1 = Button(opsi_savedata, text="Save Semua Data\nKoordinat Pohon", font="chilanka", command=save_data1)
    save_1.grid(row=4, column=1, columnspan=1, pady=11, padx=11, ipadx=27)
    save_2 = Button(opsi_savedata, text="Save Semua Data\nSensor Pohon", font="chilanka", command=save_data2)
    save_2.grid(row=5, column=1, columnspan=1, ipadx=27)

    opsi_savedata.mainloop()

# Create Text Boxes
id_tree = Entry(home, width=20)
id_tree.grid(row=0, column=1, padx=20, pady=(10,0))
sensor_tree = Entry(home, width=20)
sensor_tree.grid(row=1, column=1)

# Create Text Box Labels
id_tree_lbl = Label(home, text="ID Pohon\t\t\t: ", font="Purisa")
id_tree_lbl.grid(row=0, column=0, pady=(10,0))
sensor_tree_lbl = Label(home, text="No. Koordinat (0 s/d 9)\t: ", font="Purisa")
sensor_tree_lbl.grid(row=1, column=0)

# Create text my identity
identitas_diri = Label(home, text="Fathul Basyair\n@basyair", font="chilanka")
identitas_diri.grid(row=11,column=0, columnspan=3, pady=12, padx=12)


# Create get_data Button
get_data_btn = Button(home, text="Tambahkan Data", font="chilanka", command=get_loc)
get_data_btn.grid(row=6, column=0, columnspan=1, pady=10, padx=10, ipadx=42)

# Create Result Button
result_btn = Button(home, text="Tampilkan\nKoordinat", font="chilanka",command=result)
result_btn.grid(row=7, column=0, columnspan=1, ipadx=63)

# Create Delete Button
delete_btn = Button(home, text="Hapus Data", font="chilanka", command=option_delete)
delete_btn.grid(row=8, column=0, columnspan=1, ipadx=60)

# Create an Sensor Button
sensor_btn = Button(home, text="Sensor Tanaman", font="chilanka", command=option_sensor)
sensor_btn.grid(row=6, column=1, columnspan=2, pady=11, padx=11, ipadx=22)

#Create an save data in file button
save_btn = Button(home, text="Simpan Data\nKedalam File", font="chilanka", command=save_data)
save_btn.grid(row=7, column=1, columnspan=2, pady=11, padx=11, ipadx=40)

# exit button
exit_btn = Button(home, text="Keluar", font="chilanka", command=exit_window)
exit_btn.grid(row=8, column=1, columnspan=2, ipadx=64)


# Commit changes
conn.commit()
# Close connection
conn.close()
# Main loop
home.mainloop()
