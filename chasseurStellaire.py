from modele import Modele
from vue import Vue

class Controleur:
    def __init__(self):
        self.modele = Modele(self,600,800)
        self.vue = Vue(self, self.modele)
        self.boucle_jeu()
        self.vue.root.mainloop()

    def boucle_jeu(self):
        self.modele.mise_a_jour()
        self.vue.afficher_jeu()
        self.vue.root.after(30, self.boucle_jeu)

    # Méthodes appelées par la Vue (via bindings)
    def deplacer_vaisseau(self, x):
        self.modele.deplacer_vaisseau(x)

    def tirer(self):
        self.modele.tirer()

    def rejouer(self):
        self.modele = Modele(self,600,800)
        self.vue.modele = self.modele


if __name__ == "__main__":
    c = Controleur()