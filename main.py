import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import csv
import os

DATA_FILE = "veriler.csv"

# Verileri yükle
def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            data = [row for row in reader]
    return data

# Verileri kaydet
def save_data():
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Deneme","Türkçe","Matematik","Fizik","Kimya","Biyoloji","Sosyal","Toplam Net"])
        for row in denemeler:
            writer.writerow(row)

def hesapla_net(dogru, yanlis):
    try:
        return float(dogru) - float(yanlis)/4
    except:
        return 0.0

def deneme_ekle():
    deneme = deneme_entry.get()
    if not deneme:
        messagebox.showwarning("Uyarı","Deneme adını gir kanka")
        return
    dersler = [türkçe_d, matematik_d, fizik_d, kimya_d, biyoloji_d, sosyal_d]
    yanlislar = [türkçe_y, matematik_y, fizik_y, kimya_y, biyoloji_y, sosyal_y]
    netler = [hesapla_net(d.get(), y.get()) for d,y in zip(dersler, yanlislar)]
    toplam = sum(netler)
    row = [deneme]+[n for n in netler]+[toplam]
    denemeler.append(row)
    save_data()
    tablo.insert("", "end", values=row)
    deneme_entry.delete(0,"end")
    for d,y in zip(dersler, yanlislar):
        d.delete(0,"end")
        y.delete(0,"end")

def grafik_goster():
    if not denemeler:
        messagebox.showinfo("Bilgi","Grafik gösterecek veri yok kanka")
        return
    deneme_adlari = [r[0] for r in denemeler]
    netler = [float(r[-1]) for r in denemeler]
    plt.plot(deneme_adlari, netler, marker='o', color='b')
    plt.title("TYT Net Artış Grafiği")
    plt.xlabel("Deneme")
    plt.ylabel("Toplam Net")
    plt.grid(True)
    plt.show()

# Ana pencere
pencere = tk.Tk()
pencere.title("TYT Deneme Takip")
pencere.geometry("1000x600")

denemeler = load_data()

# Sol panel (deneme girişi)
sol = ttk.Frame(pencere, padding=10)
sol.pack(side="left", fill="y")

ttk.Label(sol, text="Yeni Deneme Ekle", font=(None,12,"bold")).pack(pady=5)
deneme_entry = ttk.Entry(sol, width=25)
deneme_entry.pack(pady=3)

ders_labels = ["Türkçe","Matematik","Fizik","Kimya","Biyoloji","Sosyal"]
ders_d = []
ders_y = []

for d in ders_labels:
    f = ttk.Frame(sol)
    f.pack(pady=2, anchor="w")
    ttk.Label(f,text=d+": ").pack(side="left")
    ed = ttk.Entry(f,width=5); ed.pack(side="left", padx=(0,5)); ed.insert(0,"0")
    ttk.Label(f,text="D").pack(side="left")
    ey = ttk.Entry(f,width=5); ey.pack(side="left", padx=(5,5)); ey.insert(0,"0")
    ttk.Label(f,text="Y").pack(side="left")
    ders_d.append(ed)
    ders_y.append(ey)

türkçe_d, matematik_d, fizik_d, kimya_d, biyoloji_d, sosyal_d = ders_d
türkçe_y, matematik_y, fizik_y, kimya_y, biyoloji_y, sosyal_y = ders_y

btn_frame = ttk.Frame(sol)
btn_frame.pack(pady=5)
ttk.Button(btn_frame,text="Ekle", command=deneme_ekle).pack(side="left", padx=5)
ttk.Button(btn_frame,text="Grafik Göster", command=grafik_goster).pack(side="left", padx=5)

# Sağ panel (tablo)
sag = ttk.Frame(pencere, padding=10)
sag.pack(side="right", fill="both", expand=True)

tablo = ttk.Treeview(sag, columns=ders_labels+["Toplam Net"], show="headings")
for col in ders_labels+["Toplam Net"]:
    tablo.heading(col,text=col)
    tablo.column(col,width=80)
tablo.pack(fill="both", expand=True)

# Yüklü verileri tabloya ekle
for row in denemeler:
    tablo.insert("", "end", values=row)

pencere.mainloop()
