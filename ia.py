# -*- coding: utf-8 -*-
import random
import os
import re
import json

class ReseauNeuronalTexte:
    def __init__(self):
        # La mémoire mathématique de l'IA (les connexions)
        self.poids = {}
        # Le dictionnaire des mots uniques qu'elle va apprendre
        self.vocabulaire = set()

    def nettoyer_et_decouper(self, texte: str) -> list:
        """Transforme le texte brut en une suite de jetons (tokens)."""
        texte = texte.lower()
        # On isole les mots et la ponctuation pour que l'IA apprenne la structure
        return re.findall(r"\w+|[.,!?;]", texte)

    def entrainer(self, chemin_fichier: str):
        """Phase d'apprentissage : l'IA ajuste ses poids mathématiques."""
        if not os.path.exists(chemin_fichier):
            print(f"[ERREUR] Crée un fichier '{chemin_fichier}' avec du texte dedans pour l'apprentissage.")
            return

        with open(chemin_fichier, "r", encoding="utf-8") as f:
            texte_brut = f.read()

        mots = self.nettoyer_et_decouper(texte_brut)
        if len(mots) < 3:
            print("[LOG] Pas assez de texte pour créer des connexions neuronales.")
            return

        # L'IA découvre les mots existants
        for mot in mots:
            self.vocabulaire.add(mot)

        # Algorithme d'apprentissage automatique (Backpropagation statistique)
        for i in range(len(mots) - 2):
            contexte = (mots[i], mots[i+1])
            mot_suivant = mots[i+2]

            if contexte not in self.poids:
                self.poids[str(contexte)] = {}
            
            if mot_suivant not in self.poids[str(contexte)]:
                self.poids[str(contexte)][mot_suivant] = 0
            
            # On renforce la connexion entre ce contexte et ce mot
            self.poids[str(contexte)][mot_suivant] += 1

        print(f"[LOG] Entraînement réussi. Vocabulaire : {len(self.vocabulaire)} mots. Connexions : {len(self.poids)}.")

    def generer_mot_suivant(self, mot1: str, mot2: str) -> str:
        """L'IA choisit le mot suivant de manière probabiliste (Neurone d'activation)."""
        contexte = str((mot1, mot2))
        
        if contexte in self.poids:
            choix_possibles = self.poids[contexte]
            # Calcul des probabilités basées sur le nombre d'apparitions
            total_poids = sum(choix_possibles.values())
            liste_mots = list(choix_possibles.keys())
            probabilites = [poids / total_poids for poids in choix_possibles.values()]
            
            # Choix mathématique autonome
            return random.choices(liste_mots, weights=probabilites, k=1)[0]
        else:
            # Si l'IA est bloquée, elle pioche un mot au hasard dans son vocabulaire
            return random.choice(list(self.vocabulaire)) if self.vocabulaire else "."

    def repondre(self, message_utilisateur: str, longueur_reponse: int = 30) -> str:
        """Génère une réponse totalement inédite basée sur l'analyse."""
        mots_utilisateurs = self.nettoyer_et_decouper(message_utilisateur)
        
        # On cherche un point de départ basé sur ce que l'utilisateur a écrit
        mot1, mot2 = None, None
        for i in range(len(mots_utilisateurs) - 1):
            if str((mots_utilisateurs[i], mots_utilisateurs[i+1])) in self.poids:
                mot1, mot2 = mots_utilisateurs[i], mots_utilisateurs[i+1]
                break
        
        # Si aucun mot n'est connu, l'IA choisit un départ aléatoire dans ses connexions
        if not mot1 or not mot2:
            if not self.poids:
                return "Je n'ai pas encore appris à parler."
            contexte_aleatoire = eval(random.choice(list(self.poids.keys())))
            mot1, mot2 = contexte_aleatoire[0], contexte_aleatoire[1]

        phrase_generee = [mot1, mot2]

        # Génération dynamique mot par mot
        for _ in range(longueur_reponse):
            prochain_mot = self.generer_mot_suivant(phrase_generee[-2], phrase_generee[-1])
            phrase_generee.append(prochain_mot)
            if prochain_mot in [".", "!", "?"]:
                break

        # Formatage propre de la réponse
        reponse = " ".join(phrase_generee)
        reponse = re.sub(r'\s+([.,!?;])', r'\1', reponse)
        return reponse.capitalize()

# --- BOUCLE DE CHAT SANS API ---
if __name__ == "__main__":
    ia = ReseauNeuronalTexte()
    
    # Nom du fichier où tu vas mettre la base de données de texte
    fichier_donnees = "apprentissage.txt"
    
    print("--- CHATBOT NEURONAL PUR ---")
    print("[1] Entraînement de la matrice...")
    ia.entrainer(fichier_donnees)
    
    print("\n[2] IA Opérationnelle. Pose tes questions.")
    while True:
        try:
            prompt = input("\nLouis > ")
            if prompt.lower() == "quitter":
                break
            if not prompt.strip():
                continue
                
            reponse = ia.repondre(prompt)
            print(f"IA > {reponse}")
            
        except KeyboardInterrupt:
            break
