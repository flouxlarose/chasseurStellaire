import tkinter as tk
from random import randint
import math

class Vue:
    def __init__(self, controleur, hauteur, largeur):
        self.controleur = controleur
        self.hauteur = hauteur
        self.largeur = largeur
        self.root = tk.Tk()
        self.root.title("Vertical Shooter - MVC")
 
        self.creer_fenetre_principale()
        self.creer_frame_canevas()
        self.creer_frame_infos()


    # ---------- Création de l'interface ----------
    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)
        self.frame_principale.pack()

    def creer_frame_canevas(self):
        self.canevas = tk.Canvas(self.frame_principale, width=self.hauteur, height=self.largeur, bg="black")
        self.canevas.grid(row=0, column=0)

        # Bindings (la Vue gère le canevas)
        self.canevas.bind("<Motion>", self.deplacer_vaisseau)
        self.canevas.bind("<Button-1>", self.tirer)

    def creer_frame_infos(self):
        self.frame_infos = tk.Frame(self.frame_principale, bg="#222")
        self.frame_infos.grid(row=0, column=1, sticky="n")

        self.label_vie = tk.Label(self.frame_infos, text="Vies : 3", fg="white", bg="#222", font=("Arial", 12))
        self.label_vie.pack(pady=10)

        self.label_niveau = tk.Label(self.frame_infos, text="Niveau : 1", fg="white", bg="#222", font=("Arial", 12))
        self.label_niveau.pack(pady=10)

        self.btn_rejouer = tk.Button(self.frame_infos, text="Rejouer", command=self.rejouer)
        self.btn_rejouer.pack(pady=50)

        #creer le label pour les informations 
        self.label_nom = tk.Entry(self.frame_infos, width=10, font=("Arial", 10))
        self.label_nom.pack(pady=10)

        #compteur de score (nombre d'ennemis tués)
        self.label_score = tk.Label(self.frame_infos, text="Score : 0", fg="white", bg="#222", font=("Arial", 12))
        self.label_score.pack(pady=10)
        #céer le bouton de sauvegarde
        self.btn_sauvegarder = tk.Button(self.frame_infos, text="Sauvegarder", command=self.sauvegarder)
        self.btn_sauvegarder.pack(pady=10)

    # ---------- Affichage du jeu ----------
    def afficher_jeu(self):
        self.canevas.delete("all")

        # --- Vaisseau du joueur ---
        v = self.controleur.modele.vaisseau
        self.canevas.create_rectangle(
            v.x - v.taille_x,
            v.y - 5,
            v.x + v.taille_x,
            v.y,
            fill="blue"
        )
        self.canevas.create_oval(
            v.x - (v.taille_x // 2),
            v.y - v.taille_y,
            v.x + (v.taille_x // 2),
            v.y - 5,
            fill="lightblue"
        )
        self.canevas.create_line(
            v.x,
            v.y - v.taille_y,
            v.x,
            v.y - v.taille_y - 5,
            fill="white",
            width=2
        )
        #bouclier 
        rayon = 40
        if (self.controleur.modele.bouclierActif):
            self.canevas.create_oval(
                v.x - rayon,
                v.y - rayon,
                v.x + rayon,
                v.y + rayon,
                outline="red",
                width=3
            )


        # --- Projectiles ---
        for p in v.projectiles:
            self.canevas.create_rectangle(
                p.x - p.taille_x,
                p.y - p.taille_y,
                p.x + p.taille_x,
                p.y,
                fill="yellow"
            )

        # --- OVNIs ---
        # for o in modele.ovnis:
        #     self.canevas.create_rectangle(
        #         o.x - o.taille_x,
        #         o.y - o.taille_y,
        #         o.x + o.taille_x,
        #         o.y + o.taille_y,
        #         fill="red"
        #     )
        #     self.canevas.create_line(
        #         o.x,
        #         o.y + o.taille_y,
        #         o.x,
        #         o.y + o.taille_y + 6,
        #         fill="orange",
        #         width=2
        #     )

        # --- Vague ---
        for o in self.controleur.modele.vague.liste_ovnis:
            self.canevas.create_rectangle(
                o.x - o.taille_x,
                o.y - o.taille_y,
                o.x + o.taille_x,
                o.y + o.taille_y,
                fill="yellow"
            )
            self.canevas.create_line(
                o.x,
                o.y + o.taille_y,
                o.x,
                o.y + o.taille_y + 6,
                fill="red",
                width=2
            )

        # --- Mines ---
        for o in self.controleur.modele.vague.liste_ovnis:
            for m in o.mines:
                self.canevas.create_rectangle(
                    m.x + m.taille_x,
                    m.y + m.taille_x,
                    m.x - m.taille_x,
                    m.y,
                    fill="red"
                )    

        # --- Astéroïdes ---
        for a in self.controleur.modele.asteroides:
            self.canevas.create_oval(
                a.x - a.taille_x,
                a.y - a.taille_y,
                a.x + a.taille_x,
                a.y + a.taille_y,
                fill="gray"
            )
        
        # --- Power ups ---
        for p in self.controleur.modele.powerUps:
            self.create_power_up(
                p.x,
                p.y,
                p.taille_x,
                p.taille_y,
                p.type
            )
        

        # --- Infos ---
        self.label_vie.config(text=f"Vies : {v.vie}")
        self.label_niveau.config(text=f"Niveau : {self.controleur.modele.niveau}")
        self.label_score.config(text=f"Score : {self.controleur.modele.score}")
    
    def create_power_up(self, x, y, inner, outer, fill):
        points = []
        for i in range(10):
            angle = i * 36
            if (i % 2):
                rayon = inner
            else:
                rayon = outer
            point_X = x + rayon * (math.cos(math.radians(angle - 90)))
            point_Y = y + rayon * (math.sin(math.radians(angle - 90)))
            points.append(point_X)
            points.append(point_Y)
        self.canevas.create_polygon(points, fill=fill, outline="black")

    def afficher_game_over(self):
        self.canevas.create_rectangle(
            150,150,
            450,450,
            fill="white"
        )
        self.canevas.create_text(
            300, 250,                       
            text="GAME OVER",
            fill="red",
            font=("Arial", 24, "bold")
        )
        self.canevas.create_text(
            300, 350,                       
            text="Best Score: ",         #rajouter le meilleur score 
            fill="black",
            font=("Arial", 20, "bold")
        )

    def deplacer_vaisseau(self,evt):
        # on pourrait vouloir le déplacer en y aussi
        self.controleur.deplacer_vaisseau(evt.x)

    def tirer(self,evt):
        self.controleur.tirer()

    def rejouer(self):
        self.controleur.rejouer(self.controleur.modele.vaisseau.vie == 0)

    def sauvegarder(self):
        nom = self.label_nom.get()
        self.controleur.sauvegarder(nom)
    
