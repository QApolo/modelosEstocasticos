from tkinter import *

from volumen_exca import VolumenExcavacion
from Costo import CostoConsumo, CostoFijo, CostosDirectos, CostoOperacion

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

import math
import time
import threading

from PIL import ImageTk,Image 

colores = ["#262338", "#00acc1"]
SIZE_WINDOW = "680x480"
COLOR_ROJO = colores[0]
COLOR_BLANCO = "white"
FUENTE = ("Courier", 16)

window = Tk()
window.title("Volumen de excavacion")
window.config(background=COLOR_ROJO)
window.geometry(SIZE_WINDOW)


lbl_lado = Label(window, text="Lado (m):", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
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

lbl_h_promedio = Label(window, text="H promedio (m): ", bg=COLOR_ROJO, fg=COLOR_BLANCO, font=FUENTE)
lbl_h_promedio.grid(column = 1, row=6)

lbl_hx = Label(window, text="Hx (m): ", bg=COLOR_ROJO, fg=COLOR_BLANCO, font=FUENTE)
lbl_hx.grid(column = 0, row = 5)

lbl_vol = Label(window, text="Volumen (m^3)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
lbl_vol.grid(column = 0, row = 6)

def calcular_relleno():
    abundamiento = float(txt_abundam.get())
    compactacion = float(txt_compacta.get())

    vol_banco = fix2(ve.getVolumen() / (compactacion / 100.0) )
    lbl_vol_banco = Label(relleno_window, text="Volumen banco: "+str(vol_banco)+ "m^3", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_vol_banco.grid(column=1, row=4)

    global vol_suelto
    vol_suelto = fix2((1.0 + abundamiento / 100.0) * vol_banco)
    lbl_vol_suelto = Label(relleno_window, text="Volumen suelto total: "+str(vol_suelto)+"m^3", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_vol_suelto.grid(column = 1, row = 5)

def rellenoOpen(): 
      
    # Toplevel object which will  
    # be treated as a new window 
    global relleno_window
    relleno_window = Toplevel(window)
    relleno_window.config(background=COLOR_ROJO)
    relleno_window.title("Volumen de relleno")
    relleno_window.geometry(SIZE_WINDOW)

    lbl_volGeom = Label(relleno_window, text="Volumen: "+str(fix2(ve.getVolumen()))+" (m^3)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_volGeom.grid(column = 1, row = 1)

    lbl_abundam = Label(relleno_window, text="Factor abundamiento: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_abundam.grid(column = 1, row = 2)
    
    global txt_abundam
    txt_abundam = Entry(relleno_window,width=10, textvariable=StringVar(relleno_window, ""))
    txt_abundam.grid(column=2, row=2)

    lbl_compactacion = Label(relleno_window, text="Factor Compactación: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
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
    lbl_viajes = Label(viajes_window, text="Viajes a realizar: "+str(math.ceil(viajes)), bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_viajes.grid(column = 0, row = 1)

def viajesOpen():
    global viajes_window
    viajes_window = Toplevel(relleno_window)
    viajes_window.config(background=COLOR_ROJO)
    viajes_window.title("Viajes")
    viajes_window.geometry(SIZE_WINDOW)

    lbl_capacidad = Label(viajes_window, text="Capacidad de la maquinaria: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_capacidad.grid(column = 0, row = 0)

    global txt_capacidad
    txt_capacidad = Entry(viajes_window,width=10, textvariable=StringVar(viajes_window, ""))
    txt_capacidad.grid(column=1, row=0)


    btn_calcularViajes = Button(viajes_window, text="Calcular", command=clickViajes)
    btn_calcularViajes.grid(column = 1, row = 2)
    viajes_window-mainloop()

def new_window_costos():
    global window_costos
    window_costos = Toplevel(window)
    window_costos.title("Costos")
    window_costos.config(background=COLOR_ROJO)
    window_costos.geometry(SIZE_WINDOW)

    lbl_costos_fijos = Label(window_costos, text="Costos Fijos: Horas Activas", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_costos_fijos.grid(column = 1, row = 0)

    lbl_depre = Label(window_costos, text="Depreciación $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_depre.grid(column = 0, row = 2)

    lbl_inversion = Label(window_costos, text="Inversión $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_inversion.grid(column = 0, row = 3)

    lbl_seguro = Label(window_costos, text="Seguro $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_seguro.grid(column = 0, row = 4)

    lbl_mantenimiento = Label(window_costos, text="Mantenimiento $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_mantenimiento.grid(column = 0, row = 5)

    global txt_depre
    txt_depre = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_depre.grid(column=1, row=2)

    global txt_inversion
    txt_inversion = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_inversion.grid(column=1, row=3)

    global txt_seguro
    txt_seguro = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_seguro.grid(column=1, row=4)

    global txt_mantenimiento
    txt_mantenimiento = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_mantenimiento.grid(column=1, row=5)

    #costos por consumo
    lbl_costos_consumo = Label(window_costos, text="Costos por Consumo: Horas Activas", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_costos_consumo.grid(column = 1, row = 6)

    lbl_combustible = Label(window_costos, text="Combustible $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_combustible.grid(column = 0, row = 8)

    lbl_lubricante = Label(window_costos, text="Lubricante $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_lubricante.grid(column = 0, row = 9)

    lbl_llantas = Label(window_costos, text="Llantas $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_llantas.grid(column = 0, row = 10)

    lbl_especiales = Label(window_costos, text="Especiales $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_especiales.grid(column = 0, row = 11)

    global txt_combustible
    txt_combustible = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_combustible.grid(column=1, row=8)

    global txt_lubricante
    txt_lubricante = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_lubricante.grid(column=1, row=9)

    global txt_llantas
    txt_llantas = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_llantas.grid(column=1, row=10)

    global txt_especiales
    txt_especiales = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_especiales.grid(column=1, row=11)

    #costos por operación
    lbl_costo_operacion = Label(window_costos, text="Costos por operación: Horas Activas", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_costo_operacion.grid(column = 1, row = 12)

    lbl_salario_real = Label(window_costos, text="Salario real operador $: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_salario_real.grid(column = 0, row = 14)

    global txt_salario_real
    txt_salario_real = Entry(window_costos,width=10, textvariable=StringVar(window_costos, ""))
    txt_salario_real.grid(column=1, row=14)


    """
    print("Hora activa: %5.2f " %(costo_fijo.getHoraActiva()))
    print("Hora inactiva: %5.2f " %(costo_fijo.getHoraInactiva()))
    print("Hora reserva: %5.2f " %(costo_fijo.getHoraReserva()))
    """

    btn_test = Button(window_costos, text="Calcular", command=click_costos)
    btn_test.grid(column = 1, row = 15)
    window_costos.mainloop()

def new_window_presupuesto():
    global window_presupuesto
    window_presupuesto = Toplevel(window)
    window_presupuesto.title("Presupuesto de obra")
    window_presupuesto.config(background=COLOR_ROJO)
    window_presupuesto.geometry(SIZE_WINDOW)
    
    lbl_costos_directos = Label(window_presupuesto, text="Costos Directos: ", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_costos_directos.grid(column = 0, row = 1)

    lbl_IVA = Label(window_presupuesto, text="IVA (%)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_IVA.grid(column = 0, row = 2)

    global txt_costos_directos
    txt_costos_directos = Entry(window_presupuesto,width=10, textvariable=StringVar(window_presupuesto, ""))
    txt_costos_directos.grid(column=1, row=1)

    global txt_IVA
    txt_IVA = Entry(window_presupuesto,width=10, textvariable=StringVar(window_presupuesto, ""))
    txt_IVA.grid(column=1, row=2)


    lbl_costos_indirectos = Label(window_presupuesto, text="Costos Indirectos (%)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_costos_indirectos.grid(column = 0, row = 3)

    global txt_costos_indirectos
    txt_costos_indirectos = Entry(window_presupuesto,width=10, textvariable=StringVar(window_presupuesto, ""))
    txt_costos_indirectos.grid(column=1, row=3)

    btn_calcularpresup = Button(window_presupuesto, text="Calcular", command=calcular_presupuestos)
    btn_calcularpresup.grid(column = 1, row = 4)

    window_presupuesto.mainloop()
def calcular_presupuestos():
    costos_directos2 = float(txt_costos_directos.get())
    total_presupuesto = costos_directos2 * (float(txt_IVA.get())/100 + float(txt_costos_indirectos.get())/100) 
    total_presupuesto = fix2(total_presupuesto)
    lbl_total_presupuesto = Label(window_presupuesto, text="Total presupuesto $"+str(total_presupuesto), bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_total_presupuesto.grid(column = 0, row = 5)

def new_window_cancha():
    global window_planchas
    window_planchas = Toplevel(window)
    window_planchas.title("Planchas")
    window_planchas.config(background=COLOR_ROJO)
    window_planchas.geometry(SIZE_WINDOW)

    lbl_title_cancha = Label(window_planchas, text="Cálculo Planchas \nDeslizantes de futbol", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_title_cancha.grid(column = 1, row = 0)

    lbl_dim_cancha = Label(window_planchas, text="Dimensiones cancha \n(lado m, ancho m)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_dim_cancha.grid(column = 0, row = 1)

    lbl_dim_plancha = Label(window_planchas, text="Dimensiones plancha \n(lado m, ancho m)", bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_dim_plancha.grid(column = 0, row = 2)

    global txt_lado_cancha
    txt_lado_cancha = Entry(window_planchas,width=10, textvariable=StringVar(window_planchas, ""))
    txt_lado_cancha.grid(column=1, row=1)

    global txt_ancho_cancha
    txt_ancho_cancha = Entry(window_planchas,width=10, textvariable=StringVar(window_planchas, ""))
    txt_ancho_cancha.grid(column=2, row=1)

    global txt_lado_plancha
    txt_lado_plancha = Entry(window_planchas,width=10, textvariable=StringVar(window_planchas, ""))
    txt_lado_plancha.grid(column=1, row=2)

    global txt_ancho_plancha
    txt_ancho_plancha = Entry(window_planchas,width=10, textvariable=StringVar(window_planchas, ""))
    txt_ancho_plancha.grid(column=2, row=2)

    btn_calcular_planchas = Button(window_planchas, text="Calcular", command=calcular_planchas)
    btn_calcular_planchas.grid(column = 0, row = 3)


    window_planchas.mainloop()


def calcular_planchas():
    lado_cancha = float(txt_lado_cancha.get())
    ancho_cancha = float(txt_ancho_cancha.get())

    lado_plancha = float(txt_lado_plancha.get())
    ancho_plancha = float(txt_ancho_plancha.get())

    area_cancha = lado_cancha * ancho_cancha
    area_plancha = lado_plancha * ancho_plancha

    numero_planchas = area_cancha // area_plancha

    #lbl_area_cancha = 
    lbl_area_cancha = Label(window_planchas, text="Area cancha: "+ str(area_cancha), bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_area_cancha.grid(column = 0, row = 4)

    lbl_area_plancha = Label(window_planchas, text="Area Plancha: "+ str(area_plancha), bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_area_plancha.grid(column = 0, row = 5)

    lbl_numero_planchas = Label(window_planchas, text="Total planchas: "+ str(numero_planchas), bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_numero_planchas.grid(column = 0, row = 6)
    

def click_costos():
    depreciacion = float(txt_depre.get())
    inversion = float(txt_inversion.get())
    seguro = float(txt_seguro.get())
    mantenimiento = float(txt_mantenimiento.get())

    global costo_fijo
    costo_fijo = CostoFijo(depreciacion, inversion, seguro, mantenimiento)
    
    combustible = float(txt_combustible.get())
    lubricante = float(txt_lubricante.get())
    llantas = float(txt_llantas.get())
    especiales = float(txt_especiales.get())

    global costo_consumo
    costo_consumo = CostoConsumo(combustible, lubricante, llantas, especiales)

    
    salario_real = float(txt_salario_real.get())
    costo_operacion = CostoOperacion(salario_real)

    global costos_directos
    costos_directos = CostosDirectos(costo_fijo, costo_consumo, costo_operacion)


    string_costos_fijos = "Costos fijos\n Hora Activa: $" + str(costo_fijo.getHoraActiva())\
    + "\n Hora Inactiva: $" + str(fix2( costo_fijo.getHoraInactiva() ) )\
    + "\n Hora reserva: $" + str(fix2( costo_fijo.getHoraReserva() ) )

    string_costos_consumo = "Costos Consumo\n Hora Activa: $" + str(costo_consumo.getHoraActiva())\
    + "\n Hora Inactiva: $" + str(fix2( costo_consumo.getHoraInactiva() ) )\
    + "\n Hora reserva: $" + str(fix2( costo_consumo.getHoraReserva() ) )

    string_costos_opera = "Costos por operación\n Hora Activa: $" + str(costo_operacion.getHoraActiva())\
    + "\n Hora Inactiva: $" + str(fix2( costo_operacion.getHoraInactiva() ) )\
    + "\n Hora reserva: $" + str(fix2( costo_operacion.getHoraReserva() ) )

    string_costos_direc = "\nCostos directos\n Hora Activa: $" + str(costos_directos.getHoraActiva())\
    + "\n Hora Inactiva: $" + str(fix2( costos_directos.getHoraInactiva() ) )\
    + "\n Hora reserva: $" + str(fix2( costos_directos.getHoraReserva() ) )


     
    lbl_res_costos_fijos = Label(window_costos, text=string_costos_fijos, bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_res_costos_fijos.grid(column = 0, row = 16)

    lbl_res_costos_consumo = Label(window_costos, text=string_costos_consumo, bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_res_costos_consumo.grid(column = 1, row = 16)

    lbl_res_costos_opera = Label(window_costos, text=string_costos_opera, bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_res_costos_opera.grid(column = 2, row = 16)

    lbl_res_costos_direc = Label(window_costos, text=string_costos_direc, bg=COLOR_ROJO, fg = COLOR_BLANCO, font=FUENTE)
    lbl_res_costos_direc.grid(column = 1, row = 18)

    


    """print("\ncosto fijo")
    print("Hora activa: %5.2f " %(costo_fijo.getHoraActiva()))
    print("Hora inactiva: %5.2f " %(costo_fijo.getHoraInactiva()))
    print("Hora reserva: %5.2f " %(costo_fijo.getHoraReserva()))

    print("\ncosto consumo")
    print("Hora activa: %5.2f " %(costo_consumo.getHoraActiva()))
    print("Hora inactiva: %5.2f " %(costo_consumo.getHoraInactiva()))
    print("Hora reserva: %5.2f " %(costo_consumo.getHoraReserva()))

    print("\ncosto por operacion")
    print("Hora activa: %5.2f " %(costo_operacion.getHoraActiva()))
    print("Hora inactiva: %5.2f " %(costo_operacion.getHoraInactiva()))
    print("Hora reserva: %5.2f " %(costo_operacion.getHoraReserva()))

    print("\ncosto directos")
    print("Hora activa: %5.2f " %(costos_directos.getHoraActiva()))
    print("Hora inactiva: %5.2f " %(costos_directos.getHoraInactiva()))
    print("Hora reserva: %5.2f " %(costos_directos.getHoraReserva()))"""

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
    lbl_hx.configure(text = "Hx: (m) "+str(fix2List(ve.getHx())))
    lbl_vol.configure(text = "Volumen: volumen de excavacion"+str(fix2(ve.getVolumen())) + " (m^3)")    
    lbl_h_promedio.configure(text = "Altura promedio: " + str(fix2(ve.getH_prom())))

    computeImage(lado, ve, sr, tn)

    """threads = list()
#for i in range(3):
    t = threading.Thread(target=computeImage, args=(lado,ve,sr,tn))
    threads.append(t)
    t.start()"""

    ##here goes first
    
    
    #openNewWindow() 
    
def reset():
    lbl_hx.configure(text = "Hx (m):")
    lbl_vol.configure(text = "Volumen (m^3):")

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


btn_costos = Button(window, text="Costos", command =new_window_costos) 
btn_costos.grid(column = 0, row = 8, padx=0, pady=200)

btn_costos = Button(window, text="Planchas", command =new_window_cancha) 
btn_costos.grid(column = 1, row = 8, padx=0, pady=200)

btn_calcular_Presupuesto = Button(window, text="Presupuesto", command=new_window_presupuesto)
btn_calcular_Presupuesto.grid(column = 2, row = 8)
window.mainloop()