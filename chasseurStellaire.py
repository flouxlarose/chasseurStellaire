from modele import Modele
from vue import Vue

class Controleur:
    def __init__(self):
        self.modele = Modele(self,600,800)
        self.vue = Vue(self, self.modele)
        self.boucle_jeu()
        self.vue.root.mainloop()

    def boucle_jeu(self):
        if (self.modele.vaisseau.vie > 0):
            self.modele.mise_a_jour()
            self.vue.afficher_jeu()
            self.vue.root.after(30, self.boucle_jeu)
        else:
            self.vue.afficher_game_over()

    # Méthodes appelées par la Vue (via bindings)
    def deplacer_vaisseau(self, x):
        self.modele.deplacer_vaisseau(x)

    def tirer(self):
        self.modele.tirer()

    def rejouer(self):
        self.vue.root.after(30, self.boucle_jeu)
        self.modele = Modele(self,600,800)
        self.vue.modele = self.modele
    
    def sauvegarder(self,nom):
        self.modele.sauvegarder(nom)


if __name__ == "__main__":
    c = Controleur()