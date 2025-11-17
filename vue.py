import tkinter as tk

class Vue:
    def __init__(self, controleur, modele):
        self.controleur = controleur
        self.modele = modele
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
        self.canevas = tk.Canvas(self.frame_principale, width=600, height=700, bg="black")
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
        self.btn_rejouer.pack(pady=10)

    # ---------- Affichage du jeu ----------
    def afficher_jeu(self):
        modele = self.modele
        self.canevas.delete("all")

        # --- Vaisseau du joueur ---
        v = modele.vaisseau
        self.canevas.create_rectangle(
            v.x - v.taille_x,
            v.y - 5,
            v.x + v.taille_x,
            v.y + 5,
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
        for o in modele.ovnis:
            self.canevas.create_rectangle(
                o.x - o.taille_x,
                o.y - o.taille_y,
                o.x + o.taille_x,
                o.y + o.taille_y,
                fill="red"
            )
            self.canevas.create_line(
                o.x,
                o.y + o.taille_y,
                o.x,
                o.y + o.taille_y + 6,
                fill="orange",
                width=2
            )

        # --- Astéroïdes ---
        for a in modele.asteroides:
            self.canevas.create_oval(
                a.x - a.taille_x,
                a.y - a.taille_y,
                a.x + a.taille_x,
                a.y + a.taille_y,
                fill="gray"
            )

        # --- Infos ---
        self.label_vie.config(text=f"Vies : {v.vie}")
        self.label_niveau.config(text=f"Niveau : {modele.niveau}")

    def deplacer_vaisseau(self,evt):
        # on pourrait vouloir le déplacer en y aussi
        self.controleur.deplacer_vaisseau(evt.x)

    def tirer(self,evt):
        self.controleur.tirer()

    def rejouer(self):
        self.controleur.rejouer()
