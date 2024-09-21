import matplotlib.pyplot as plt
import tkinter as tk #käyttöliittymäkirjasto
from PIL import Image, ImageTk
# jotta voit käyttää matplotlibiä näppärästi tkinterissä
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# pääikkuna
ikkuna=tk.Tk() #luodaan ikkuna
ikkuna.title("Heittokisa") #ikkunan otsikko
ikkuna.geometry("800x800+500+500") #määritellään ikkunan koko ja sijainti

# luodaan kuvaaja
fig=Figure(figsize=(7,7), dpi=100)
ax=fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_xticklabels([])
ax.set_yticklabels([])

ernu_placement = None
kernu_placement = None
tomato_placement = None
maalitaulunPaikka = [40, 60, 40, 60]
plots_placement = [45, 55, 45, 55]
tomato_x = 0

def place_ernu():
    global ernu_placement
    if ernu_placement is not None:
        ernu_placement.remove()
        ernu_placement = None
    ernu = Image.open("kotit3-4\\erne.png")
    ernu = ernu.resize((50, 50))

    random_y = random.randint(5, 95) # satunnainen y-koordinaatti

    ernu_extent = [0, 10,random_y - 5, random_y + 5]
    ernu_placement = ax.imshow(ernu, extent=ernu_extent)

    kuvaaja_canvas.draw() # päivitetään kuvaaja

def place_kernu():
    global kernu_placement
    if kernu_placement is not None:
        kernu_placement.remove()
        kernu_placement = None
    kernu = Image.open("kotit3-4\\kerne.png")
    kernu = kernu.resize((50, 50))

    random_y = random.randint(5, 95) # satunnainen y-koordinaatti

    kernu_extent = [90, 100,random_y - 5, random_y + 5]
    kernu_placement = ax.imshow(kernu, extent=kernu_extent)

    kuvaaja_canvas.draw() # päivitetään kuvaaja

def throw_ernu():
    global tomato_placement, maalitaulunPaikka, tomato_x
    tomato = Image.open("kotit3-4\\tomaatti.png")
    tomato = tomato.resize((50, 50))
    ernu_extent = ernu_placement.get_extent() # otetaan ernun sijainti
    tomato_extent = [ernu_extent[0] + 5, ernu_extent[1] + 5, ernu_extent[2], ernu_extent[3]]
    tomato_placement = ax.imshow(tomato, extent=tomato_extent)

    tomato_x = tomato_extent[0]
    maalitaulunPaikka = ax.get_images()[0].get_extent() # otetaan maalitaulun sijainti
    animate_tomato_ernu()    # animoidaan tomaatti

def throw_kernu():
    global tomato_placement, maalitaulunPaikka, tomato_x
    tomato = Image.open("kotit3-4\\tomaatti.png")
    tomato = tomato.resize((50, 50))
    kernu_extent = kernu_placement.get_extent() # otetaan kernun sijainti
    tomato_extent = [kernu_extent[0] - 5, kernu_extent[1] - 5, kernu_extent[2], kernu_extent[3]]
    tomato_placement = ax.imshow(tomato, extent=tomato_extent)

    tomato_x = tomato_extent[0]
    maalitaulunPaikka = ax.get_images()[0].get_extent() # otetaan maalitaulun sijainti
    animate_tomato_kernu()    # animoidaan tomaatti

def animate_tomato_ernu():
    global tomato_placement, tomato_x
    tomato_x += 1
    tomato_extent = [tomato_x, tomato_x + 10, tomato_placement.get_extent()[2], tomato_placement.get_extent()[3]] 
    tomato_placement.set_extent(tomato_extent)
    ax.figure.canvas.draw()


    if (tomato_extent[0] > maalitaulunPaikka[0] and tomato_extent[1] < maalitaulunPaikka[1] and tomato_extent[2] > maalitaulunPaikka[2] and tomato_extent[3] < maalitaulunPaikka[3]):
        print("Ernesti osui maalitauluun")
        tomato_placement.remove()
        plots = Image.open("kotit3-4\\splat.png")
        plots = plots.resize((60, 60))
        ax.imshow(plots, extent=plots_placement)
        ax.figure.canvas.draw()
        return
    if tomato_extent[0] > 100:
        tomato_placement.remove()
        tomato_placement = None
        return
    
    # repeat
    ikkuna.after(10, animate_tomato_ernu)

def animate_tomato_kernu():
    global tomato_placement, tomato_x
    tomato_x -= 1
    
    tomato_extent = [tomato_x, tomato_x -10, tomato_placement.get_extent()[2], tomato_placement.get_extent()[3]] 
    tomato_placement.set_extent(tomato_extent)
    ax.figure.canvas.draw()

    plots = Image.open("kotit3-4\\splat.png")
    plots = plots.resize((50, 50))


    if (tomato_extent[0] > maalitaulunPaikka[0] and tomato_extent[1] < maalitaulunPaikka[1] and tomato_extent[2] > maalitaulunPaikka[2] and tomato_extent[3] < maalitaulunPaikka[3]):
        print("Kernu osui maalitauluun")
        tomato_placement.remove()
        plots = Image.open("kotit3-4\\splat.png")
        plots = plots.resize((60, 60))
        ax.imshow(plots, extent=plots_placement)
        ax.figure.canvas.draw()

        return
    if tomato_extent[0] < 0:
        tomato_placement.remove()
        tomato_placement = None
        return
    # repeat
    ikkuna.after(30, animate_tomato_kernu)

    
# upotetaan kuvaaja tkinteriin
kuvaaja_canvas=FigureCanvasTkAgg(fig, master=ikkuna)
kuvaaja_canvas.draw()
kuvaaja_canvas.get_tk_widget().place(x=10, y=100)
kuvaaja_canvas.get_tk_widget().pack()

# kuvat
maalitaulu = Image.open("kotit3-4\\maalitaulu.png")
maalitaulu = maalitaulu.resize((400, 400))

ax.imshow(maalitaulu, extent=maalitaulunPaikka) # keskelle


# napit
ernuNappi=tk.Button(ikkuna, text="Ernu", command=place_ernu)
ernuNappi.place(x=300, y=20)
ernunHeitto=tk.Button(ikkuna, text="Ernun heitto", command=throw_ernu)
ernunHeitto.place(x=300, y=50)

kernuNappi=tk.Button(ikkuna, text="Kernu", command=place_kernu)
kernuNappi.place(x=400, y=20)
kernunHeitto=tk.Button(ikkuna, text="Kernun heitto", command=throw_kernu)
kernunHeitto.place(x=400, y=50)



ikkuna.mainloop() #käynnistetään ikkuna