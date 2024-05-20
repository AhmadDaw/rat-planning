from tkinter import *
import pandas as pd
from tkinter import filedialog
import customtkinter as ctk
import math 

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = ctk.CTk()
app.geometry("400x500")
app.title("RAT Planning v1")

root = ctk.CTkFrame(master=app)
root.pack(pady=20, padx=20, fill="both", expand=True)

e=Entry(root, width=40)
l=ctk.CTkLabel(root, text=" ")
ll=ctk.CTkLabel(root, text=" ")
stats=ctk.CTkLabel(root, text="-")
stats_cln=ctk.CTkLabel(root, text="-")

kml_title=ctk.CTkLabel(root, text="RAT Planning v1")
data_cln_title=ctk.CTkLabel(root, text="RAT Planning v1")

long_in=ctk.CTkEntry(root)
lat_in=ctk.CTkEntry(root)
long_txt=ctk.CTkLabel(root, text="Longitude")
lat_txt=ctk.CTkLabel(root, text="Latitude")

# -----------------------------------------------------

choc_cln = IntVar()
rb_2g = ctk.CTkRadioButton(root, text="2G (Frequency)", variable=choc_cln, value=2)
rb_3g = ctk.CTkRadioButton(root, text="3G (PSC)", variable=choc_cln, value=3)
rb_4g = ctk.CTkRadioButton(root, text="4G (PCI)", variable=choc_cln, value=4)

# -----------------------------------------------------
def chk():
    return
# ----------------------------------------------------

#status = Label(root, text = "Coded by: Ahmad Dawara", bd=2, relief=SUNKEN, anchor = E)
def cln():

    rat='2G'
    # Read the dataframe
    df = pd.read_csv(fp1)

    # Define the constant longitude and latitude
    constant_long = float(long_in.get())
    constant_lat = float(lat_in.get())

    # Calculate the geographic distance between each pair of coordinates and add a distance column to the DataFrame
    def calculate_distance(row):
        radius = 6371  # Earth's radius in kilometers

        dlat = math.radians(constant_lat - row['latitude'])
        dlon = math.radians(constant_long - row['longitude'])
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(row['latitude'])) \
            * math.cos(math.radians(constant_lat)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c

        return distance

    df['distance_km'] = df.apply(calculate_distance, axis=1)
    df['distance_km'] = df['distance_km'].round(2)

    # Sort the dataframe by distance in ascending order
    df = df.sort_values(by='distance_km', ascending=True)
    
    if (choc_cln.get() == 2):
        rat='2G'

        # Drop the duplicated 'Frequency' values
        df = df.drop_duplicates(subset='Frequency')

        # Select the desired columns
        df = df[['cell', 'distance_km', 'Frequency']]

    if (choc_cln.get() == 3):
        rat='3G'

        # Drop the duplicated PSC values
        df = df.drop_duplicates(subset='PSC')

        # Select the desired columns
        df = df[['cell', 'distance_km', 'PSC']]

    if (choc_cln.get() == 4):
        rat='4G'

        # Drop the duplicated PCI values
        df = df.drop_duplicates(subset='PCI')

        # Select the desired columns
        df = df[['cell', 'distance_km', 'PCI']]

    # Sort the dataframe by distance in descending order
    df = df.sort_values(by='distance_km', ascending=False)

    # Print the output dataframe
    print(df)

    df.to_csv(rat + ' out.csv',index=False)

    stats_cln.configure(text='Done.')

# -------------------------------------------------------------------
def opn_cln():
    global fp1
    fp1=filedialog.askopenfilename()

# -------------------------------------------------------------
b_opn_cln=ctk.CTkButton(root, text="Browse" ,command=opn_cln)
b_browse_cln=ctk.CTkButton(root, text="Run" ,command=cln)
# ----------------------------------------------------------
data_cln_title.grid(row = 1, column = 2,pady=10,padx=10)
b_opn_cln.grid(row = 2, column = 2, pady=10)

long_in.grid(row = 3, column = 3, pady=10, padx=10)
lat_in.grid(row = 4, column = 3, pady=10, padx=10)

long_txt.grid(row = 3, column = 2, pady=10, padx=10)
lat_txt.grid(row = 4, column = 2, pady=10, padx=10)

stats_cln.grid(row = 8, column = 2, pady=10, padx=10)
b_browse_cln.grid(row = 10, column = 2, pady=10)

rb_2g.grid(row = 5, column = 2, pady=10, padx=10)
rb_3g.grid(row = 6, column = 2, pady=10, padx=10)
rb_4g.grid(row = 7, column = 2, pady=10, padx=10)
# ---------------------------------------------------------
l.grid(row = 1, column = 1, pady=10, padx=10)
ll.grid(row = 1, column = 0, pady=10, padx=10)

#status.grid(row=6, column=0, columnspan=2, sticky=W+E)
# ---------------------------------------------------------
app.mainloop()



