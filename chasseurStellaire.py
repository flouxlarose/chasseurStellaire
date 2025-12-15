from modele import Modele
from vue import Vue

class Controleur:
    def __init__(self):
        self.vue = Vue(self, 600, 700)
        self.Paused = True
        # self.alive = self.modele.alive
        self.vue.root.mainloop()

    def boucle_jeu(self):
        if self.Paused:
            if (self.modele.vaisseau.vie > 0): ## funct return
                self.vue.mettre_a_jour_top_scores()
                self.modele.mise_a_jour()
                self.vue.afficher_jeu()
                self.id_loop = self.vue.root.after(30, self.boucle_jeu)
            else:
                self.vue.afficher_game_over()
        else: 
            #vérification de l'état de vie à faire dans le modèle 
            self.id_loop = self.vue.root.after(30, self.boucle_jeu)
            
        

    # Méthodes appelées par la Vue (via bindings)
    def commencer_jeu(self):
        self.modele = Modele(self,600,700)
        self.modele.highScore()
        self.modele.niveau = self.vue.radio_value.get()
        self.vue.frame_titre.destroy()
        self.vue.creer_frame_canevas()
        self.vue.creer_frame_infos()
        self.modele.creer_vague()
        self.boucle_jeu()

    def deplacer_vaisseau(self, x, y):
        self.modele.deplacer_vaisseau(x, y)

    def tirer(self):
        self.modele.tirer()

    def rejouer(self, isGameOver):
        self.deplacer_vaisseau
        self.modele = Modele(self,600,700)
        self.modele.creer_vague()
        if (isGameOver):
            self.boucle_jeu()
    
    def sauvegarder(self,nom):
        self.modele.sauvegarder(nom)

    def is_paused(self, evt):
        self.Paused = not self.Paused
       
    def infos_scores(self):
        x, y = self.modele.topscore.rerturn_info()
        return x, y


if __name__ == "__main__":
    c = Controleur()