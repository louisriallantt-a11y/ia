# -*- coding: utf-8 -*-
import sys
import os

# Vérification et importation sécurisée d'Ollama
try:
    import ollama
except ImportError:
    print("[ERREUR] La bibliothèque 'ollama' est manquante.")
    print("Pour l'installer, ouvre un Terminal et tape : pip3 install ollama")
    sys.exit(1)

class MonIASouveraine:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        # Le System Prompt définit la personnalité de ton IA
        self.system_prompt = (
            "Tu es Cogitron, une IA de haute précision créée par le développeur Louis Riallant. "
            "Tu fonctionnes de manière 100% locale et autonome. Réponds de façon claire, concise, "
            "sans phrases pré-écrites. Si on te demande comment signaler un bug ou donner une suggestion, "
            "indique l'adresse e-mail : suggestion.cogitron@outlook.fr."
        )

    def verifier_modele(self):
        """Vérifie si le modèle est bien installé localement."""
        try:
            # Test rapide pour voir si Ollama répond
            ollama.list()
        except Exception:
            print("[ERREUR] L'application Ollama n'est pas lancée sur ton Mac.")
            print("Télécharge et lance Ollama depuis : https://ollama.com")
            sys.exit(1)

    def chatter(self):
        print("--- COGITRON INITIALISÉE (100% AUTONOME) ---")
        print("Écris ton message (ou 'quitter' pour fermer).\n")
        
        while True:
            try:
                user_input = input("Louis > ")
                if user_input.lower() == "quitter":
                    print("Arrêt du système.")
                    break
                
                if not user_input.strip():
                    continue

                # Appel du modèle local sans aucune API externe
                flux_reponse = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                reponse_ia = flux_reponse['message']['content']
                print(f"IA > {reponse_ia}\n")

            except KeyboardInterrupt:
                print("\nInterruption détectée. Fermeture.")
                break
            except Exception as e:
                print(f"\n[ERREUR INTERNE] Une erreur est survenue : {e}\n")

if __name__ == "__main__":
    # On lance l'IA
    ia = MonIASouveraine(model_name="llama3") # Tu peux remplacer par "mistral" si tu préfères
    ia.verifier_modele()
    ia.chatter()
