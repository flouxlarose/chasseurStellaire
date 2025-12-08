import random
import csv
import time

# ------------------ CLASSES ------------------

class Projectile:
    def __init__(self, x, y, estLarge):
        self.x = x
        self.y = y
        self.taille_x = 2
        self.vitesse = -10  # vers le haut
        self.taille_y = 10
        if (estLarge):
            self.taille_x = 6
            self.vitesse = -5

    def mise_a_jour(self):
        self.y += self.vitesse

class Mine:
    def __init__(self, x, y, taille_x, taille_y):
        self.x = x
        self.y = y
        self.vitesse = 4   # vers le bas
        self.taille_x = taille_x     # est un carré donc meme taille pour les deux côté
        self.taille_y = taille_y

    def mise_a_jour(self):
        self.y += self.vitesse

class PowerUps:
    def __init__(self, x, y, vitesse, type):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.taille_x = 10
        self.taille_y = 15
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
    
    def tirer(self, multiple, large):
        if (multiple):
            self.projectiles.append(Projectile(self.x - 18, self.y - 20, large))
            self.projectiles.append(Projectile(self.x, self.y - 20, large))
            self.projectiles.append(Projectile(self.x + 18, self.y - 20, large))
        else:
            nouveau_proj = Projectile(self.x, self.y - 20, large)
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
    def __init__(self, x, y, vy, taille_x, taille_y, type):
        self.type = type
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.mines = []
        self.vie = 3 if (self.type == "boss") else 1

    def tirer(self):
        if(self.type == "normal"):
            taille = 5
        elif (self.type == "boss"):
            taille = 10
        nouvelle_mine = Mine(self.x, self.y + 10, taille, taille)
        self.mines.append(nouvelle_mine)

    def mise_a_jour(self, ennemisLents):
        self.y += self.vy if not ennemisLents else self.vy / 2

        for m in self.mines:
            m.mise_a_jour()

        self.mines = [
            m for m in self.mines
            if m.y > 0
        ]


class Vague:
    def __init__(self, parent):
        self.premier_tick = False
        self.vitesse_ovni = [1, 2]
        self.parent = parent
        self.nombre_ovni = 10
        self.liste_ovnis = []
        self.nombre_boss = 0
        self.level_up()

    def creer_ovni(self):
        for i in range(self.nombre_ovni):
            newOvni = OVNI(random.randint(0, 600), 0, self.vitesse_ovni[random.randint(0, 1)], 12, 6, "normal")
            self.liste_ovnis.append(newOvni)
    
    def creer_ovni_boss(self):
        for i in range(self.nombre_boss):
            newOvni = OVNI(random.randint(0, 600), 0, self.vitesse_ovni[random.randint(0, 1)], 20, 14, "boss")
            self.liste_ovnis.append(newOvni)

    def mise_a_jour(self):
        for i in self.liste_ovnis:
            i.mise_a_jour(self.parent.ennemisLents)
    
    def level_up(self):
        if (not self.liste_ovnis):
            
            if(self.premier_tick):
                self.parent.niveau += 1
            else:
                self.premier_tick = True
                
            self.nombre_ovni = 10 + (5 * self.parent.niveau)
            self.vitesse_ovni[0] = self.vitesse_ovni[0] + (0.2 * self.parent.niveau)
            self.vitesse_ovni[1] = self.vitesse_ovni[1] + (0.2 * self.parent.niveau)
            self.creer_ovni()
            if (self.parent.niveau % 3 == 0):
                self.nombre_boss = int(self.parent.niveau / 3)
                self.creer_ovni_boss()
    
    def kill_all(self):
        for o in self.liste_ovnis:
            self.liste_ovnis.remove(o)


class Asteroide:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 10
        self.taille_y = 10

    def mise_a_jour(self):
        self.y += self.vy

class Effets:
    def __init__(self, type):
        self.type = type
        self.time = time.time()

# ------------------ MODÈLE ------------------

class Modele:
    def __init__(self, parent, largeur, hauteur):
        self.parent = parent
        self.largeur = largeur
        self.hauteur = hauteur
        self.vaisseau = Vaisseau(self.largeur // 2, self.hauteur - 50)
        self.ovnis = []
        self.asteroides = []
        self.powerUps = []
        self.score = 0
        self.niveau = self.parent.vue.radio_value.get()
        self.effetsEnCours = []

        self.projectilesLarges = False
        self.projectilesMultiples = False
        self.projectilesInvincibles = False
        self.tirContinu = False
        self.bouclierActif = False
        self.ennemisLents = False

        self.vague = Vague(self)

    def deplacer_vaisseau(self,x):
        self.vaisseau.deplacer(x)

    def tirer(self):
        self.vaisseau.tirer(self.projectilesMultiples, self.projectilesLarges)

    def collisionAvec(self, objetA, objetB):
        x1 = objetA.x - objetA.taille_x
        y1 = objetA.y - objetA.taille_y
        x2 = objetA.x + objetA.taille_x
        y2 = objetA.y + objetA.taille_y

        a1 = objetA.x - objetA.taille_x
        b1 = objetA.y + objetA.taille_y
        a2 = objetA.x + objetA.taille_x
        b2 = objetA.y - objetA.taille_y

        z1 = objetB.x - objetB.taille_x
        w1 = objetB.y - objetB.taille_y
        z2 = objetB.x + objetB.taille_x
        w2 = objetB.y + objetB.taille_y

        c1 = objetB.x - objetB.taille_x
        d1 = objetB.y + objetB.taille_y
        c2 = objetB.x + objetB.taille_x
        d2 = objetB.y - objetB.taille_y
        if ((
                (
                    z1 >= x1 and z1 <= x2 and
                    w1 >= y1 and w1 <= y2 or
                    z2 >= x1 and z2 <= x2 and
                    w2 >= y1 and w2 <= y2
                )
                or
                (
                    c2 >= a1 and c2 <= a2 and
                    d2 >= b1 and d2 <= b2 or
                    c1 >= a1 and c1 <= a2 and
                    d1 >= b1 and d1 <= b2
                )
            )):
                # print(f"{objetA} + hit par + {objetB}")
                return True
        
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.vague.mise_a_jour()
        self.vague.level_up()


        # PLUS BESOINS VUE QUE SPAWN ENNEMIS DANS VAGUE ?
        # Apparition aléatoire des ennemis
        # alea_ovni = random.random()
        # if alea_ovni < 0.02:
        #     nouvel_ovni = OVNI(
        #         random.randint(0, self.largeur),
        #         0,
        #         random.randint(2, 5)
        #     )
        #     self.ovnis.append(nouvel_ovni)

        alea_asteroide = random.random()
        if alea_asteroide < 0.003:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6)
            )
            self.asteroides.append(nouvel_ast)

        alea_powerup = random.random()
        if alea_powerup < 0.01:
            alea_type = random.randint(1,30)
            if (alea_type < 5):
                type = "red"
            elif (alea_type < 15):
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
                if (self.collisionAvec(self.vaisseau, m) and not self.bouclierActif):
                    self.vaisseau.vie -= 1
                    o.mines.remove(m)

        # Déplacement des ennemis
        for o in self.vague.liste_ovnis:
            o.mise_a_jour(self.ennemisLents)
            # si l'ovni est en bas de l'écran se remet en haut a une pos differente en x
            if (o.y > self.hauteur):
                o.y = 0
                o.x = random.randint(5, self.largeur - 5)
            if(self.collisionAvec(self.vaisseau, o) and not self.bouclierActif):
                self.vaisseau.vie -= 1
                if (o in self.vague.liste_ovnis): 
                    self.vague.liste_ovnis.remove(o)
            for p in self.vaisseau.projectiles:
                if (self.collisionAvec(o, p)):
                    o.vie -= 1
                    if (o.vie <= 0 and o in self.vague.liste_ovnis):
                        self.score += 1
                        self.vague.liste_ovnis.remove(o)
                    if (not self.projectilesInvincibles):
                        self.vaisseau.projectiles.remove(p)
        
        # Déplacement astéroides
        for a in self.asteroides:
            a.mise_a_jour()
            if(self.collisionAvec(self.vaisseau, a) and not self.bouclierActif):
                self.vaisseau.vie -= 1
                self.asteroides.remove(a)
            for p in self.vaisseau.projectiles:
                if (self.collisionAvec(a, p)):
                    self.score += 1
                    self.asteroides.remove(a)
                    if (not self.projectilesInvincibles):
                        self.vaisseau.projectiles.remove(p)

        # Déplacement power ups
        for p in self.powerUps:
            p.mise_a_jour()
            if (self.collisionAvec(self.vaisseau, p)):
                if (p.type == "red"):
                    if (random.randint(1,5) % 2):
                        self.vague.kill_all()
                    else:
                        self.effetsEnCours.append(Effets("r-1"))
                        print("r-lent")
                elif (p.type == "purple"):
                    rng = random.randint(1,30)
                    if (rng <= 7):
                        self.projectilesMultiples = True
                        self.effetsEnCours.append(Effets("p-1"))
                        print("p-mult")
                    elif (rng <= 15): 
                        self.projectilesLarges = True
                        self.effetsEnCours.append(Effets("p-2"))
                        print("p-larg")
                    elif (rng <= 25):
                        self.projectilesInvincibles = True
                        self.effetsEnCours.append(Effets("p-3"))
                        print("p-inv")
                    elif (rng <= 30):
                        self.tirContinu = True
                        self.effetsEnCours.append(Effets("p-4"))
                        print("p-continu")
                else: 
                    if (random.randint(1,2) % 2):
                        if (self.vaisseau.vie < 3):
                            self.vaisseau.vie += 1
                            print("g-vie")
                    else: 
                        self.bouclierActif = True
                        self.effetsEnCours.append(Effets("g-1"))
                        print("g-bouclier")

                self.powerUps.remove(p)

        # Nettoyage des objets sortis de l'écran
        self.ovnis = [
            o for o in self.ovnis 
            if o.y < self.hauteur
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur
        ]
        
        if (self.tirContinu):
            self.vaisseau.tirer(self.projectilesMultiples, self.projectilesLarges)

        # Compte le temps restant pour chaque effet en cours
        for e in self.effetsEnCours:
            if (time.time() - e.time > 10):
                self.effetsEnCours.remove(e)
                if (e.type == "p-1"):
                    self.projectilesMultiples = False
                elif (e.type == "p-2"):
                    self.projectilesLarges = False
                elif (e.type == "p-3"):
                    self.projectilesInvincibles = False
                elif (e.type == "p-4"):
                    self.tirContinu = False
                elif (e.type == "g-1"):
                    self.bouclierActif = False
                elif (e.type == "r-1"):
                    self.ennemisLents = False


    #enregistrement des donnees
    def sauvegarder(self,nom):
        with open("donnees.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nom,self.score*100])
    
    def highScore(self):
        score_col = []
        with open("donnees.csv", "r") as file: 
            contenu = csv.reader(file, delimiter=',')
            for row in contenu:
                if len(row) > 1:
                    score_col.append(int(row[1]))

        high = max(score_col)
        return high 
