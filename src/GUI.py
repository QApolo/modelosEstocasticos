from tkinter import *

from volumen_exca import VolumenExcavacion

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

from PIL import ImageTk,Image 

window = Tk()

window.title("Volumen")

window.geometry('1024x740')

lbl_lado = Label(window, text="Lado:")

lbl_lado.grid(column=0, row=0)

txt_lado = Entry(window,width=10)

txt_lado.grid(column=1, row=0)


lbl_ed = Label(window, text="ed:")

lbl_ed.grid(column=0, row=1)

txt_ed = Entry(window,width=10)

txt_ed.grid(column=1, row=1)



lbl_tn = Label(window, text="tn: (A,B,C,D)")
lbl_tn.grid(column=0, row=2)

txt_tn = Entry(window,width=20, textvariable=StringVar(window, "90.1, 90.1, 78.6, 79.0"))
txt_tn.grid(column=1, row=2)


lbl_sr = Label(window, text="sr: (A,B,C,D)")
lbl_sr.grid(column=0, row=3)

txt_sr = Entry(window,width=20, textvariable=StringVar(window, "63.5, 63.5, 63.5, 63.5"))
txt_sr.grid(column=1, row=3)


lbl_hx = Label(window, text="Hx: ")
lbl_hx.grid(column = 4, row = 5)

lbl_vol = Label(window, text="Volumen: ")
lbl_vol.grid(column = 4, row = 6)

canvas = Canvas(window, width = 640, height = 480)   
canvas.grid(row=8, column = 8) 

def openNewWindow(): 
      
    # Toplevel object which will  
    # be treated as a new window 
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
def clicked():

    #res = "Welcome to " + txt_lado.get()
    lado = float(txt_lado.get())
    ed = float(txt_ed.get())

    tn = txt_tn.get().split(',')
    tn = [float(val) for val in tn]

    sr = txt_sr.get().split(',')
    sr = [float(val) for val in sr]


    ve = VolumenExcavacion(lado, ed, tn, sr)
    lbl_hx.configure(text = "Hx: "+str(ve.getHx()))
    lbl_vol.configure(text = "Volumen: "+str(ve.getVolumen()))
    #print(ve.getHx())
    print(ve.getVolumen())

    ##here goes first
    computeImage(lado, ve, sr, tn)
    
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
btn_calcular.grid(column=1, row=4)

btn_reset = Button(window, text="reset", command=reset)
btn_reset.grid(column=3, row=4)

window.mainloop()