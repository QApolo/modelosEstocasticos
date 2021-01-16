from tkinter import *

from volumen_exca import VolumenExcavacion

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

import time
import threading

from PIL import ImageTk,Image 

SIZE_WINDOW = "680x480"
window = Tk()

window.title("Volumen")

window.geometry(SIZE_WINDOW)

lbl_lado = Label(window, text="Lado:")

lbl_lado.grid(column=0, row=0)

txt_lado = Entry(window,width=10)

txt_lado.grid(column=1, row=0)


lbl_ed = Label(window, text="Espesor de empalme:")

lbl_ed.grid(column=0, row=1)

txt_ed = Entry(window,width=10)

txt_ed.grid(column=1, row=1)



lbl_tn = Label(window, text="Terreno Natural: (A,B,C,D)")
lbl_tn.grid(column=0, row=2)

txt_tn = Entry(window,width=20, textvariable=StringVar(window, "90.1, 90.1, 78.6, 79.0"))
txt_tn.grid(column=1, row=2)


lbl_sr = Label(window, text="Cota del terreno: (A,B,C,D)")
lbl_sr.grid(column=0, row=3)

txt_sr = Entry(window,width=20, textvariable=StringVar(window, "63.5, 63.5, 63.5, 63.5"))
txt_sr.grid(column=1, row=3)


lbl_hx = Label(window, text="Hx: ")
lbl_hx.grid(column = 4, row = 5)

lbl_vol = Label(window, text="Volumen: ")
lbl_vol.grid(column = 4, row = 6)

def calcular_relleno():
    abundamiento = float(txt_abundam.get())
    compactacion = float(txt_compacta.get())

    vol_banco = fix2(ve.getVolumen()/ compactacion / 100.0)
    lbl_vol_banco = Label(relleno_window, text="Volumen banco: "+str(vol_banco))
    lbl_vol_banco.grid(column=1, row=4)

    vol_suelto = fix2((1.0 + abundamiento / 100.0) * vol_banco)
    lbl_vol_suelto = Label(relleno_window, text="Vol suelto total: "+str(vol_suelto))
    lbl_vol_suelto.grid(column = 1, row = 5)

def rellenoOpen(): 
      
    # Toplevel object which will  
    # be treated as a new window 
    global relleno_window
    relleno_window = Toplevel(window)
    relleno_window.title("Volumen de relleno")
    relleno_window.geometry(SIZE_WINDOW)

    lbl_volGeom = Label(relleno_window, text="Volumen: "+str(fix2(ve.getVolumen())))
    lbl_volGeom.grid(column = 1, row = 1)

    lbl_abundam = Label(relleno_window, text="Factor abundamiento: ")
    lbl_abundam.grid(column = 1, row = 2)
    
    global txt_abundam
    txt_abundam = Entry(relleno_window,width=10, textvariable=StringVar(relleno_window, ""))
    txt_abundam.grid(column=2, row=2)

    lbl_compactacion = Label(relleno_window, text="Factor Compactación: ")
    lbl_compactacion.grid(column = 1, row = 3)
    
    global txt_compacta
    txt_compacta = Entry(relleno_window,width=10, textvariable=StringVar(relleno_window, ""))
    txt_compacta.grid(column=2, row=3)
    
    btn_calc_relleno = Button(relleno_window, text="Calcular Vol Relleno", command=calcular_relleno)
    btn_calc_relleno.grid(column=2, row = 6)

    relleno_window.mainloop()
    """
    newWindow = Toplevel(window) 
  
    # sets the title of the 
    # Toplevel widget 
    newWindow.title("New Window") 
  
    # sets the geometry of toplevel 
    newWindow.geometry("640x480") 
    
    canvas = Canvas(newWindow, width=640, height=480)
    canvas.pack()
    #img = PhotoImage(file='./volumen.png')
    img = ImageTk.PhotoImage(Image.open("volumen.png"))  
    
    canvas.create_image(0, 0, image=img)
    newWindow.mainloop()
    """
def computeImage(lado, ve, sr, tn):
    fig = plt.figure()
    ax = Axes3D(fig)

    x = [0,0,lado,lado]
    y = [0,lado,lado,0]
    z = sr[:]

    za = [a + abs(b) for a, b in zip(z, ve.getHx())]

    zb = tn[:]
    
    verts3 = [list(zip(x,y,zb))]

    ax.set_xlim3d(0, lado)
    ax.set_ylim3d(0,lado)
    ax.set_zlim3d(min(sr),max(zb))

    
    verts = [list(zip(x,y,z))]
    ax.add_collection3d(Poly3DCollection(verts))

    ax.scatter(x,y,z)
    ax.scatter(x,y,za)
    ax.scatter(x,y,zb)

    verts2 = [list(zip(x,y,za))]
    #ax.autoscale(False)
    ax.add_collection3d(Poly3DCollection(verts2, facecolors='g'))

  
    ax.add_collection3d(Poly3DCollection(verts3, facecolors='r'))
    plt.savefig("volumen.png")
    plt.show()

def fix2(num: float):
    return float("{:.2f}".format(num))
def fix2List(l: list):
    return [fix2(x) for x in l]

"""def configureText(lab, txt: str):
    lab.configure(text = txt)"""

def clicked():

    #res = "Welcome to " + txt_lado.get()
    lado = float(txt_lado.get())
    ed = float(txt_ed.get())

    tn = txt_tn.get().split(',')
    tn = [float(val) for val in tn]

    sr = txt_sr.get().split(',')
    sr = [float(val) for val in sr]

    global ve
    ve = VolumenExcavacion(lado, ed, tn, sr)
    
    btn_relleno.configure(state='active')
    """threads = list()
    
    t1 = threading.Thread(target=configureText, args=(lbl_hx, "Hx: "+str(fix2List(ve.getHx()))))
    t2 = threading.Thread(target=configureText, args=(lbl_vol, "Volumen: "+str(fix2(ve.getVolumen()))))
    t1.start()
    t2.start()"""
    lbl_hx.configure(text = "Hx: "+str(fix2List(ve.getHx())))
    lbl_vol.configure(text = "Volumen: "+str(fix2(ve.getVolumen())))    
    

    computeImage(lado, ve, sr, tn)

    """threads = list()
#for i in range(3):
    t = threading.Thread(target=computeImage, args=(lado,ve,sr,tn))
    threads.append(t)
    t.start()"""

    ##here goes first
    
    
    #openNewWindow() 
    
def reset():
    lbl_hx.configure(text = "Hx: ")
    lbl_vol.configure(text = "Volumen: ")

    txt_ed.delete(0, len(txt_ed.get()))
    txt_lado.delete(0, len(txt_lado.get()))
    txt_tn.delete(0, len(txt_tn.get()))
    txt_sr.delete(0, len(txt_sr.get()))
    
    #lbl_lado.configure(text= res)

btn_calcular = Button(window, text="Calcular", command=clicked)
btn_reset = Button(window, text="reset", command=reset)
btn_relleno = Button(window, text="Sig (Vol relleno)", command =rellenoOpen) 
btn_relleno.configure(state=DISABLED)

btn_calcular.grid(column=1, row=4)

btn_reset.grid(column=3, row=4)

btn_relleno.grid(column = 0, row = 7)

window.mainloop()