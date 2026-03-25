import tkinter as tk
from tkinter import Toplevel, font as tkfont  # Importation pour créer des fenêtres secondaires
from PIL import Image, ImageTk
from programme import main  # Assurez-vous que le module de jeu est nommé jeu.py

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Menu Jeu")
fenetre.attributes("-fullscreen", True)  # Affiche la fenêtre en plein écran

# Chargement et redimensionnement de l'image de fond
bg_image = Image.open("fondba.png")
bg_image = bg_image.resize((fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_image)

# Conserver une référence à l'objet ImageTk.PhotoImage
fenetre.bg_photo = bg_image

# Placement de l'image de fond
bg_label = tk.Label(fenetre, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Definir des polices
label_font = tkfont.Font(family="Helvetica", size=18)
button_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

# Initialisation des valeurs par défaut pour les options
width_valeur = tk.Entry(fenetre)
width_valeur.insert(0, "1050")
height_valeur = tk.Entry(fenetre)
height_valeur.insert(0, "650")
turtle_count_valeur = tk.Entry(fenetre)
turtle_count_valeur.insert(0, "20")

# Fonction pour démarrer le jeu


def start_game():
    """
    Appelle la fonction principale `main` du module `programme` avec les paramètres demandés à l'utilisateur.
    :return: Aucun
    """
    width = int(width_valeur.get())
    height = int(height_valeur.get())
    n = int(turtle_count_valeur.get())
    fenetre.destroy()  # Ferme la fenêtre tkinter avant de démarrer le jeu
    main(width, height, n)

# Fonction pour ouvrir la fenêtre d'options


def open_options():
    """
    Ouvre une fenêtre d'options pour configurer les paramètres du jeu.
    :return: Aucun
    """
    options_window = Toplevel(fenetre)
    options_window.title("Options")
    options_window.attributes("-fullscreen", True)

    # Chargement et redimensionnement de l'image de fond pour la fenêtre d'options
    mode_bg_image = Image.open("fondba.png")
    mode_bg_image = mode_bg_image.resize((options_window.winfo_screenwidth(), options_window.winfo_screenheight()))
    mode_bg_photo = ImageTk.PhotoImage(mode_bg_image)

    # Conserver une référence à l'objet ImageTk.PhotoImage
    options_window.mode_bg_photo = mode_bg_photo

    # Placement de l'image de fond
    mode_bg_label = tk.Label(options_window, image=mode_bg_photo)
    mode_bg_label.image = mode_bg_photo
    mode_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Ajout d'un cadre pour les options
    options_frame = tk.Frame(options_window, bg="#222222", bd=10)
    options_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=250)

    # Ajout des champs de saisie et des labels pour les options
    label_width = 255  # Largeur des textes devant les champs de saisie
    entry_width = 200  # Largeur des champs de saisie

    (tk.Label(options_frame, text="Largeur de la fenêtre :", font=label_font, bg="#222222", fg="white")
     .place(x=10, y=10, width=label_width, height=30))
    width_valeur_option = tk.Entry(options_frame, font=label_font)
    width_valeur_option.place(x=label_width + 20, y=10, width=entry_width, height=30)
    width_valeur_option.insert(0, width_valeur.get())

    (tk.Label(options_frame, text="Longueur de la fenêtre :", font=label_font, bg="#222222", fg="white")
     .place(x=10, y=50, width=label_width, height=30))
    height_valeur_option = tk.Entry(options_frame, font=label_font)
    height_valeur_option.place(x=label_width + 20, y=50, width=entry_width, height=30)
    height_valeur_option.insert(0, height_valeur.get())

    (tk.Label(options_frame, text="Nombre de tortues :", font=label_font, bg="#222222", fg="white")
     .place(x=10, y=90, width=label_width, height=30))
    turtle_count_valeur_option = tk.Entry(options_frame, font=label_font)
    turtle_count_valeur_option.place(x=label_width + 20, y=90, width=entry_width, height=30)
    turtle_count_valeur_option.insert(0, turtle_count_valeur.get())

    # Fonction pour enregistrer les options
    def save_options():
        """
        Enregistre les options saisies par l'utilisateur et ferme la fenêtre d'options.
        :return: Aucun
        """
        width_valeur.delete(0, tk.END)
        width_valeur.insert(0, width_valeur_option.get())

        height_valeur.delete(0, tk.END)
        height_valeur.insert(0, height_valeur_option.get())

        turtle_count_valeur.delete(0, tk.END)
        turtle_count_valeur.insert(0, turtle_count_valeur_option.get())

        options_window.destroy()

    # Bouton pour enregistrer les options
    save_button = tk.Button(options_frame, text="Enregistrer", font=button_font, bg="#444444", fg="white",
                            command=save_options)
    save_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER, width=150, height=40)


# Création des boutons avec une taille agrandie

start_button = tk.Button(fenetre, text="START", font=button_font, bg="#00AA00", fg="white", command=start_game)
start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=-50, width=200, height=50)

options_button = tk.Button(fenetre, text="OPTIONS", font=button_font, bg="#0055AA", fg="white", command=open_options)
options_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=0, width=200, height=50)

exit_button = tk.Button(fenetre, text="EXIT", font=button_font, bg="#AA0000", fg="white", command=fenetre.quit)
exit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=50, width=200, height=50)

fenetre.mainloop()
