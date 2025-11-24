import random
import csv

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
        self.taille_x = 5     # est un carré donc meme taille pour les deux côté
        self.taille_y = 5

    def mise_a_jour(self):
        self.y += self.vitesse

class PowerUps:
    def __init__(self, x, y, vitesse, type):
        self.x = x
        self.y = y
        self.vitesse = 4
        self.inner = 10
        self.outer = 15
        self.type = type
    
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
        self.powerUps = []
        self.score = 0
        self.niveau = 1

        self.vague = Vague()

    def deplacer_vaisseau(self,x):
        self.vaisseau.deplacer(x)

    def tirer(self):
        self.vaisseau.tirer()

    def collisionAvec(self, objetA, objetB):
        if ( not(
                objetA.x + objetA.taille_x < objetB.x or
                objetA.x > objetB.x + objetB.taille_x or
                objetA.y + self.vaisseau.taille_y < objetB.y or
                objetA.y > objetB.y + objetB.taille_y )):
                # print(f"{objetA} + hit par + {objetB}")
                return True
        
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.vague.mise_a_jour()
        for p in self.powerUps:
            p.mise_a_jour()

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

        alea_powerup = random.random()
        if alea_powerup < 0.01:
            alea_type = random.randint(1,3)
            if (alea_type == 1):
                type = "yellow"
            elif (alea_type == 2):
                type = "green"
            else:
                type = "purple"
            nouveau_powerUp = PowerUps(
                random.randint(5, self.largeur-5),
                50,
                random.randint(2, 10),
                type
            )
            self.powerUps.append(nouveau_powerUp)

        # Tir aléatoire des ovnis
        for o in self.vague.liste_ovnis:
            alea_tir = random.random()
            if alea_tir < 0.01:
                o.tirer()
            for m in o.mines:
                if (self.collisionAvec(self.vaisseau, m)):
                    self.vaisseau.vie -= 1
                    o.mines.remove(m)

        # Déplacement des ennemis
        for o in self.vague.liste_ovnis:
            o.mise_a_jour()
            # si l'ovni est en bas de l'écran se remet en haut a une pos differente en x
            if (o.y > self.hauteur):
                o.y = 0
                o.x = random.randint(5, self.largeur - 5)
            if(self.collisionAvec(self.vaisseau, o)):
                self.vaisseau.vie -= 1 
                self.vague.liste_ovnis.remove(o)
            for p in self.vaisseau.projectiles:
                if (self.collisionAvec(o, p)):
                    print("ovni détruit")
                    self.score += 1
                    self.vague.liste_ovnis.remove(o)
                    self.vaisseau.projectiles.remove(p)

        for a in self.asteroides:
            a.mise_a_jour()
            if(self.collisionAvec(self.vaisseau, a)):
                self.vaisseau.vie -= 1
                self.asteroides.remove(a)
            for p in self.vaisseau.projectiles:
                if (self.collisionAvec(a, p)):
                    print("astéroide détruit")
                    self.score += 1
                    self.asteroides.remove(a)
                    self.vaisseau.projectiles.remove(p)


        # Nettoyage des objets sortis de l'écran
        self.ovnis = [
            o for o in self.ovnis
            if o.y < self.hauteur
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur
        ]

    #enregistrement des donnees
    def sauvegarder(self,nom):
        with open("donnees.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nom,self.score])
