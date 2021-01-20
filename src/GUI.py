from tkinter import *

from volumen_exca import VolumenExcavacion

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

import math
import time
import threading

from PIL import ImageTk,Image 

colores = ["#00838f", "#00acc1"]
SIZE_WINDOW = "680x480"
COLOR_ROJO = colores[1]
COLOR_BLANCO = "white"
FUENTE = ("Courier", 16)

window = Tk()
window.title("Volumen")
window.config(background=COLOR_ROJO)
window.geometry(SIZE_WINDOW)


lbl_lado = Label(window, text="Lado:", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_lado.grid(column=0, row=0)

txt_lado = Entry(window,width=10)
txt_lado.grid(column=1, row=0)


lbl_ed = Label(window, text="Espesor de empalme:", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_ed.grid(column=0, row=1)

txt_ed = Entry(window,width=10)
txt_ed.grid(column=1, row=1)



lbl_tn = Label(window, text="Terreno Natural: (A,B,C,D)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_tn.grid(column=0, row=2)

txt_tn = Entry(window,width=20, textvariable=StringVar(window, "90.1, 90.1, 78.6, 79.0"))
txt_tn.grid(column=1, row=2)


lbl_sr = Label(window, text="Cota del terreno: (A,B,C,D)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_sr.grid(column=0, row=3)

txt_sr = Entry(window,width=20, textvariable=StringVar(window, "63.5, 63.5, 63.5, 63.5"))
txt_sr.grid(column=1, row=3)


lbl_hx = Label(window, text="Hx: ", bg=COLOR_ROJO, fg=COLOR_BLANCO, font=FUENTE)
lbl_hx.grid(column = 0, row = 5)

lbl_vol = Label(window, text="Volumen: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_vol.grid(column = 0, row = 6)

def calcular_relleno():
    abundamiento = float(txt_abundam.get())
    compactacion = float(txt_compacta.get())

    vol_banco = fix2(ve.getVolumen() / (compactacion / 100.0) )
    lbl_vol_banco = Label(relleno_window, text="Volumen banco: "+str(vol_banco))
    lbl_vol_banco.grid(column=1, row=4)

    global vol_suelto
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


    btn_siguiente = Button(relleno_window, text="Sig: Viajes", command=viajesOpen)
    btn_siguiente.grid(column = 2, row = 7)
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
def clickViajes():    
    viajes = vol_suelto / float(txt_capacidad.get())
    lbl_viajes = Label(viajes_window, text="Viajes a realizar: "+str(math.ceil(viajes)))
    lbl_viajes.grid(column = 0, row = 1)

def viajesOpen():
    global viajes_window
    viajes_window = Toplevel(relleno_window)
    viajes_window.title("Viajes")
    viajes_window.geometry(SIZE_WINDOW)

    lbl_capacidad = Label(viajes_window, text="Capacidad de la maquinaria: ")
    lbl_capacidad.grid(column = 0, row = 0)

    global txt_capacidad
    txt_capacidad = Entry(viajes_window,width=10, textvariable=StringVar(viajes_window, ""))
    txt_capacidad.grid(column=1, row=0)


    btn_calcularViajes = Button(viajes_window, text="Calcular", command=clickViajes)
    btn_calcularViajes.grid(column = 1, row = 2)
    viajes_window-mainloop()

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
    ax.add_collection3d(Poly3DCollection(verts, facecolors='tan', alpha=.8))

    ax.scatter(x,y,z)
    ax.scatter(x,y,za)
    ax.scatter(x,y,zb)
    labels = ['A', 'B', 'C', 'D']
    for i in range(0, 4):
        ax.text(x[i],y[i],z[i],  '%s' % (labels[i]), size=15, zorder=1, color='k')
    middle = (max(zb)+min(z)) // 2
    for i in range(0, 4):
        ax.text(x[i],y[i],zb[i],  'T.N.%s=: %s' % (labels[i], str(zb[i])), size=15, zorder=1, color='k')
        ax.text(x[i], y[i], middle, 'h%s = %s' %(labels[i], abs(fix2(ve.getHx()[i])) ) )

    verts2 = [list(zip(x,y,za))]
    #ax.autoscale(False)
    ax.add_collection3d(Poly3DCollection(verts2, facecolors='gray', alpha=.8))

  
    ax.add_collection3d(Poly3DCollection(verts3, facecolors='g', alpha=.6))

    #ax.text(5,5, 50, "red", color='green')
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