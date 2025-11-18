import random

# ------------------ CLASSES ------------------

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vitesse = -10  # vers le haut
        self.taille_x = 2
        self.taille_y = 10

    def mise_a_jour(self):
        self.y += self.vitesse

class Mine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vitesse = 4   # vers le bas
        self.taille = 5     # est un carré donc meme taille pour les deux côté

    def mise_a_jour(self):
        self.y += self.vitesse


class Vaisseau:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 3
        self.projectiles = []
        self.taille_x = 15
        self.taille_y = 15

    def deplacer(self, x):
        self.x = x
    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y - 20)
        self.projectiles.append(nouveau_proj)

    def mise_a_jour(self):
        for p in self.projectiles:
            p.mise_a_jour()

        # Détruit les projectiles qui sortent du canvas
        self.projectiles = [
            p for p in self.projectiles
            if p.y > 0
        ]


class OVNI:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 12
        self.taille_y = 6
        self.mines = []

    def tirer(self):
        nouvelle_mine = Mine(self.x, self.y + 10)
        self.mines.append(nouvelle_mine)

    def mise_a_jour(self):
        self.y += self.vy

        for m in self.mines:
            m.mise_a_jour()

        self.mines = [
            m for m in self.mines
            if m.y > 0
        ]


class Vague:
    def __init__(self):
        self.liste_ovnis = []
        for i in range(10):
            newOvni = OVNI(random.randint(0, 600), 0, random.randint(1,2 ))
            self.liste_ovnis.append(newOvni)

    def mise_a_jour(self):
        for i in self.liste_ovnis:
            i.mise_a_jour()


class Asteroide:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 10
        self.taille_y = 10

    def mise_a_jour(self):
        self.y += self.vy


# ------------------ MODÈLE ------------------

class Modele:
    def __init__(self, parent, largeur, hauteur):
        self.parent = parent
        self.largeur = 600
        self.hauteur = 700
        self.vaisseau = Vaisseau(self.largeur // 2, self.hauteur - 50)
        self.ovnis = []
        self.asteroides = []
        self.score = 0
        self.niveau = 1

        self.vague = Vague()

    def deplacer_vaisseau(self,x):
        self.vaisseau.deplacer(x)
    def tirer(self):
        self.vaisseau.tirer()
    def collisionAvec(self, objet):
        if ( not(
                self.vaisseau.x + self.vaisseau.taille_x < objet.x or
                self.vaisseau.x > objet.x + objet.taille_x or
                self.vaisseau.y + self.vaisseau.taille_y < objet.y or
                self.vaisseau.y > objet.y + objet.taille_y )):
                print("hit par ovni")
                self.vaisseau.vie -= 1
                return True
        
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.vague.mise_a_jour()

        # Apparition aléatoire des ennemis
        alea_ovni = random.random()
        if alea_ovni < 0.02:
            nouvel_ovni = OVNI(
                random.randint(0, self.largeur),
                0,
                random.randint(2, 5)
            )
            self.ovnis.append(nouvel_ovni)

        alea_asteroide = random.random()
        if alea_asteroide < 0.01:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6)
            )
            self.asteroides.append(nouvel_ast)

        # Tir aléatoire des ovnis
        for o in self.vague.liste_ovnis:
            alea_tir = random.random()
            if alea_tir < 0.01:
                o.tirer()

        # Déplacement des ennemis
        for o in self.ovnis:
            o.mise_a_jour()
            if(self.collisionAvec(o)):
                self.ovnis.remove(o)

        for a in self.asteroides:
            a.mise_a_jour()
            if(self.collisionAvec(a)):
                self.asteroides.remove(a)

        # Nettoyage des objets sortis de l'écran
        self.ovnis = [
            o for o in self.ovnis
            if o.y < self.hauteur
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur
        ]
