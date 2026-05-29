import random
import os
import re

class IACognitive:
    def __init__(self, order=2):
        """
        L'ordre (order) définit la mémoire de l'IA.
        Un ordre de 2 signifie qu'elle regarde les 2 derniers mots pour inventer le suivant.
        """
        self.order = order
        self.chain = {}
        self.mots_de_depart = []

    def nettoyer_texte(self, texte: str) -> list:
        """Nettoie le texte pour que l'IA apprenne correctement."""
        # On sépare les mots et la ponctuation proprement
        texte = texte.lower()
        mots = re.findall(r"\w+|[.,!?;]", texte)
        return mots

    def apprendre_depuis_fichier(self, chemin_fichier: str):
        """Lit un fichier texte brut pour éduquer l'IA de manière autonome."""
        if not os.path.exists(chemin_fichier):
            print(f"Erreur : Le fichier {chemin_fichier} n'existe pas.")
            print("Créez le fichier et ajoutez du texte (des paragraphes, des livres, des cours).")
            return

        try:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                contenu = f.read()

            mots = self.nettoyer_texte(contenu)
            if len(mots) < self.order:
                print("Le fichier texte est trop court pour l'apprentissage.")
                return

            # On mémorise les débuts de phrases possibles
            self.mots_de_depart.append(tuple(mots[:self.order]))

            # Algorithme d'apprentissage automatique de probabilité
            for i in range(len(mots) - self.order):
                etat = tuple(mots[i:i + self.order])
                mot_suivant = mots[i + self.order]

                # Si l'IA détecte une fin de phrase, le mot suivant commence une nouvelle logique
                if etat[-1] in [".", "!", "?", ";"]:
                    if i + self.order + self.order < len(mots):
                        prochain_debut = tuple(mots[i + self.order : i + self.order + self.order])
                        self.mots_de_depart.append(prochain_debut)

                if etat not in self.chain:
                    self.chain[etat] = []
                self.chain[etat].append(mot_suivant)

            print(f"Apprentissage terminé avec succès. Connexions neuronales : {len(self.chain)}")

        except Exception as e:
            print(f"Une erreur est survenue lors de l'entraînement : {e}")

    def generer_reponse(self, longueur_max=30) -> str:
        """Génère une phrase totalement inédite mot par mot."""
        if not self.chain:
            return "Mon esprit est vide. Donnez-moi un fichier texte pour apprendre."

        try:
            # L'IA choisit de manière autonome comment démarrer sa phrase
            etat_actuel = random.choice(self.mots_de_depart)
            phrase = list(etat_actuel)

            for _ in range(longueur_max):
                if etat_actuel in self.chain:
                    # Choix probabiliste du mot suivant
                    mot_suivant = random.choice(self.chain[etat_actuel])
                    phrase.append(mot_suivant)
                    
                    # On met à jour la mémoire immédiate de l'IA
                    etat_actuel = tuple(phrase[-self.order:])
                    
                    # Si l'IA décide de mettre un point final, elle s'arrête de parler
                    if mot_suivant in [".", "!", "?"]:
                        break
                else:
                    break

            # Reconstruction propre de la phrase pour l'utilisateur
            reponse_formatee = " ".join(phrase)
            # Nettoyage cosmétique des espaces avant la ponctuation
            reponse_formatee = re.sub(r'\s+([.,!?;])', r'\1', reponse_formatee)
            return reponse_formatee.capitalize()

        except Exception as e:
            return f"Erreur de génération : {str(e)}"

# --- INTERFACE DE CHAT ---
if __name__ == "__main__":
    # 1. Instanciation de l'IA
    mon_ia = IACognitive(order=2)

    # 2. Entraînement automatique via le fichier de connaissances
    print("Initialisation de l'IA...")
    mon_ia.apprendre_depuis_fichier("apprentissage.txt")

    # 3. Boucle de discussion autonome
    print("\nL'IA est en ligne et autonome ! (Tapez 'quitter' pour fermer)")
    while True:
        prompt = input("\nLouis > ")
        if prompt.lower() == "quitter":
            break
        
        # L'IA formule sa propre phrase en se basant sur ce qu'elle a appris
        reponse = mon_ia.generer_reponse()
        print(f"IA > {reponse}")
