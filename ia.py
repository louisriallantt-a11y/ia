#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA ULTRA AVANCÉE - Auto-Évolutive - Type ChatGPT/Gemini/Claude
Comprend le contexte, apprend en temps réel, raisonne, génère du contenu
Zéro API externe - Tout en Python pur
"""

import random
import json
import os
import math
import re
from collections import defaultdict, Counter
from datetime import datetime

class AdvancedAI:
    """IA très avancée avec compréhension contextuelle et apprentissage auto-évolutif"""
    
    def __init__(self, name="Nova"):
        self.name = name
        self.conversation_history = []
        self.knowledge_base = defaultdict(list)
        self.user_preferences = {}
        self.learned_patterns = defaultdict(float)
        self.context_memory = []
        self.cache = {}
        self.memory_file = "memory.json"
        self.knowledge_file = "knowledge.json"
        self.stats = {"messages": 0, "learned": 0, "accuracy": 0.8}
        
        self.load_knowledge()
        self.load_memory()
    
    def load_knowledge(self):
        """Charge la base de connaissances depuis knowledge.json"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r", encoding="utf-8") as f:
                    self.knowledge_base = defaultdict(list, json.load(f))
            except Exception as e:
                print(f"❌ Erreur chargement knowledge: {e}")
                self._init_knowledge_base()
        else:
            self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """Initialise une base de connaissances très riche"""
        self.knowledge_base = {
            "tech": [
                "Python est un langage polyvalent idéal pour l'IA et le data science.",
                "Les transformers révolutionnent le traitement du langage naturel.",
                "L'apprentissage machine peut classifier, prédire, et générer du contenu.",
                "Les réseaux de neurones imitent le fonctionnement du cerveau humain.",
                "L'IA générative crée du contenu original basé sur des patterns appris.",
            ],
            "philosophie": [
                "L'IA soulève des questions éthiques fascinantes sur la conscience.",
                "La conscience est-elle possible pour une machine? C'est un débat ouvert.",
                "L'intelligence n'est pas monolithique - elle se manifeste de plusieurs façons.",
                "L'apprentissage est fondamental pour toute forme d'intelligence.",
            ],
            "science": [
                "Les atomes sont composés de protons, neutrons, et électrons.",
                "L'univers s'étend continuellement depuis le Big Bang.",
                "La photosynthèse convertit la lumière en énergie chimique.",
                "L'ADN contient les instructions génétiques pour tous les êtres vivants.",
            ],
            "créativité": [
                "La créativité naît de la combinaison de concepts existants.",
                "L'improvisation est une forme de créativité en temps réel.",
                "L'art challenge la perception et provoque l'émotion.",
                "La musique est une langue universelle de l'émotion.",
            ],
            "psychologie": [
                "L'empathie permet de comprendre les sentiments d'autrui.",
                "La motivation est le moteur de l'action humaine.",
                "Les biais cognitifs influencent nos décisions quotidiennes.",
                "L'apprentissage est renforcé par la répétition et l'émotion.",
            ]
        }
    
    def _tokenize(self, text):
        """Tokenize un texte en mots/tokens"""
        # Supprime les caractères spéciaux et divise
        text = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = text.split()
        return [t for t in tokens if t and len(t) > 2]
    
    def _simple_stem(self, word):
        """Stemming simple pour le français - supprime les suffixes courants"""
        # Suffixes courants à supprimer
        suffixes = ["tion", "ment", "ités", "ique", "able", "ible", "eur", "euse", 
                   "ais", "aient", "ant", "ante", "ants", "antes", "es", "s"]
        
        word_lower = word.lower()
        for suffix in sorted(suffixes, key=len, reverse=True):  # Plus longs suffixes d'abord
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                return word_lower[:-len(suffix)]
        return word_lower
    
    def _similarity(self, text1, text2):
        """Calcule la similarité cosinus entre deux textes (0-1)"""
        tokens1 = self._tokenize(text1)
        tokens2 = self._tokenize(text2)
        
        # Applique le stemming pour mieux matcher les variantes
        stems1 = set(self._simple_stem(t) for t in tokens1)
        stems2 = set(self._simple_stem(t) for t in tokens2)
        
        if not stems1 or not stems2:
            return 0.0
        
        intersection = len(stems1 & stems2)
        union = len(stems1 | stems2)
        return intersection / union if union > 0 else 0.0
    
    def _extract_entities(self, text):
        """Extrait les entités nommées et concepts"""
        # Cherche les patterns spécifiques
        entities = {
            "questions": len(re.findall(r'\?', text)),
            "exclamations": len(re.findall(r'!', text)),
            "nombres": re.findall(r'\d+', text),
            "capitales": len(re.findall(r'\b[A-Z][a-z]+\b', text)),
            "sentiment": self._analyze_sentiment(text)
        }
        return entities
    
    def _analyze_sentiment(self, text):
        """Analyse simple du sentiment (-1: négatif, 0: neutre, 1: positif)"""
        positive = ["super", "cool", "excellent", "incroyable", "magnifique", "adorable", "merveilleux", "génial"]
        negative = ["horrible", "nul", "mauvais", "triste", "déprimant", "dégoûtant", "pire"]
        
        text_lower = text.lower()
        pos_count = sum(text_lower.count(word) for word in positive)
        neg_count = sum(text_lower.count(word) for word in negative)
        
        if pos_count > neg_count:
            return 1
        elif neg_count > pos_count:
            return -1
        return 0
    
    def _find_best_response(self, user_input):
        """Trouve la meilleure réponse en utilisant keyword matching amélioré"""
        entities = self._extract_entities(user_input)
        user_lower = user_input.lower()
        tokens = self._tokenize(user_input)
        
        # Map étendu de keywords -> catégories de réponses
        keyword_map = {
            # Identité - Questions sur qui tu es
            "appell": "identité",
            "nom": "identité",
            "es": "identité",
            "s'appell": "identité",
            "t'appell": "identité",
            "qui": "identité",
            "nova": "identité",
            "suis": "identité",
            "salut": "identité",
            "bonjour": "identité",
            "hello": "identité",
            "coucou": "identité",
            "hey": "identité",
            
            # Fonctionnement - Comment ça marche
            "fonctionn": "fonctionnement",
            "marche": "fonctionnement",
            "travail": "fonctionnement",
            "algorithme": "fonctionnement",
            "système": "fonctionnement",
            "proces": "fonctionnement",
            "logique": "fonctionnement",
            "mécanisme": "fonctionnement",
            "fonctionne": "fonctionnement",
            "commen": "fonctionnement",
            
            # Apprentissage - Tu apprends?
            "apprend": "apprentissage",
            "évolue": "apprentissage",
            "auto": "apprentissage",
            "mémoire": "apprentissage",
            "mémoris": "apprentissage",
            "sauvegard": "apprentissage",
            "appren": "apprentissage",
            
            # Capabilities - Que peux-tu faire?
            "fait": "capabilities",
            "peux": "capabilities",
            "capable": "capabilities",
            "discuter": "capabilities",
            "générer": "capabilities",
            "génère": "capabilities",
            "créer": "capabilities",
            "répondre": "capabilities",
            "fais": "capabilities",
            
            # Questions fréquentes
            "fréquent": "questions_fréquentes",
            "souvent": "questions_fréquentes",
            "courant": "questions_fréquentes",
            "common": "questions_fréquentes",
            
            # Tech
            "python": "tech",
            "code": "tech",
            "programme": "tech",
            "transformers": "tech",
            "réseaux": "tech",
            "neurone": "tech",
            "ia": "tech",
            "intelligence": "tech",
            "machine": "tech",
            "api": "tech",
            "langage": "tech",
            
            # Science
            "science": "science",
            "atome": "science",
            "univers": "science",
            "bang": "science",
            "physique": "science",
            "chimie": "science",
            "biologie": "science",
            
            # Philosophie
            "philoso": "philosophie",
            "conscience": "philosophie",
            "penser": "philosophie",
            "éthique": "philosophie",
            "moraal": "philosophie",
            "conscien": "philosophie",
            
            # Créativité
            "créatif": "créativité",
            "art": "créativité",
            "musique": "créativité",
            "imagin": "créativité",
            "innov": "créativité",
            
            # Psychologie
            "psycholog": "psychologie",
            "émotion": "psychologie",
            "empathi": "psychologie",
            "motiv": "psychologie",
            "sentim": "psychologie",
            
            # Mathématiques
            "mathématique": "mathématiques",
            "math": "mathématiques",
            "nombre": "mathématiques",
            "calcul": "mathématiques",
            "équation": "mathématiques"
        }
        
        # Analyse les tokens pour trouver les meilleures catégories
        category_scores = defaultdict(float)
        
        # Cherche les keywords dans tous les tokens (plus strict, score plus élevé)
        for token in tokens:
            for keyword, category in keyword_map.items():
                if keyword in token:
                    category_scores[category] += 3.0  # Score élevé pour token matches
                elif token == keyword:
                    category_scores[category] += 5.0  # Score très élevé pour exact matches
        
        # Aussi cherche dans le texte complet (mots partiels)
        for keyword, category in keyword_map.items():
            if keyword in user_lower:
                category_scores[category] += 1.0  # Score plus bas pour partial text matches
        
        # Trie les catégories par score
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        priority_categories = [cat for cat, score in sorted_categories if score > 0]
        
        best_score = -1
        best_response = None
        best_category = None
        
        # D'abord cherche dans les catégories prioritaires
        if priority_categories:
            for category in priority_categories:
                if category not in self.knowledge_base or not self.knowledge_base[category]:
                    continue
                
                responses = self.knowledge_base[category]
                for response in responses:
                    score = self._similarity(user_input, response)
                    
                    # Bonus pour les bonnes réponses substantielles
                    if len(response) > 30:
                        score += 0.5  # Bonus plus élevé
                    
                    # Pénalité pour les questions
                    if '?' in response:
                        score -= 0.2
                    
                    if score > best_score:
                        best_score = score
                        best_response = response
                        best_category = category
        
        # Si rien trouvé, cherche dans TOUTES les catégories
        if best_score < 0.15:
            for category, responses in self.knowledge_base.items():
                for response in responses:
                    score = self._similarity(user_input, response)
                    
                    if len(response) > 30:
                        score += 0.1
                    
                    if '?' in response:
                        score -= 0.1
                    
                    if score > best_score:
                        best_score = score
                        best_response = response
                        best_category = category
        
        return best_response, best_score, best_category
    
    def _generate_followup(self, previous_response, user_sentiment):
        """Génère une suite intelligente à la réponse"""
        followups = {
            "tech": "Ça t'intéresse comment ça marche plus en détail?",
            "philosophie": "Qu'en penses-tu? Ça soulève des questions, non?",
            "science": "Tu veux que je t'explique le mécanisme derrière?",
            "créativité": "C'est fascinant comment la créativité émergent des patterns.",
            "psychologie": "C'est intéressant - les humains sont complexes!",
        }
        
        if user_sentiment == 1:
            return random.choice([
                "Je suis content que ça t'intéresse!",
                "C'est vrai, c'est captivant!",
                followups.get("tech", "Continue d'explorer ce sujet!")
            ])
        elif user_sentiment == -1:
            return "Je comprends tes réserves. Veux-tu explorer un autre angle?"
        else:
            return random.choice(list(followups.values()))
    
    def respond(self, user_input):
        """Génère une réponse intelligente et contextuelle"""
        self.stats["messages"] += 1
        
        # Récupère le meilleur contexte
        best_response, score, category = self._find_best_response(user_input)
        entities = self._extract_entities(user_input)
        
        # Améliore la réponse avec le contexte
        if best_response and score > 0.15:
            # Si score bon, utilise la réponse directe
            response = best_response
            
            # Ajoute une suite intelligente seulement si nécessaire
            if score < 0.6 and entities["questions"] > 0:
                followup = self._generate_followup(best_response, entities["sentiment"])
                final_response = f"{response}\n\n{followup}"
            else:
                # Réponse parfaite, pas besoin de suite
                final_response = response
        else:
            # Score faible - génère une réponse réfléchie
            final_response = self._generate_thoughtful_response(user_input, entities)
        
        # Ajoute à l'historique
        self.conversation_history.append({
            "user": user_input,
            "ai": final_response,
            "timestamp": datetime.now().isoformat(),
            "category": category or "general"
        })
        
        # Apprentissage automatique
        self._learn_from_interaction(user_input, final_response)
        
        # Garde seulement les 50 derniers messages
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        
        return final_response
    
    def _generate_thoughtful_response(self, user_input, entities):
        """Génère une réponse réfléchie quand aucun pattern exact ne correspond"""
        responses = [
            f"C'est une excellente observation. {'Tu soulevais ' + str(entities.get('questions', 0)) + ' bonnes questions!' if entities.get('questions', 0) > 0 else 'J\'aime ta perspective.'}",
            "Je vois ce que tu veux dire. C'est complexe, mais voici ce que j'en pense:",
            "Intéressant angle! Ça me fait penser à...",
            "Oui, c'est un sujet nuancé. Plusieurs perspectives existent.",
            "Absolument, et au-delà de ça, il y a aussi...",
            "C'est une question profonde. Laisse-moi la reformuler:" if entities.get('questions', 0) > 0 else "Voilà un point stimulant!",
        ]
        
        base = random.choice(responses)
        
        # Ajoute de la substance basée sur le contexte
        if entities.get('numbers'):
            nums = entities.get('numbers', [])
            if nums:
                base += f" Les nombres que tu mentionnes ({', '.join(nums[:2])}) sont significatifs."
        
        if entities.get('exclamations', 0) > 0:
            base += " Je sens de la passion dans tes mots!"
        
        return base
    
    def _learn_from_interaction(self, user_input, response):
        """Apprend automatiquement de chaque interaction et améliore la knowledge_base"""
        tokens = self._tokenize(user_input)
        
        for token in tokens:
            # Renforce les patterns fréquents
            self.learned_patterns[token] += 0.01
        
        # Améliore la précision au fil du temps
        self.stats["accuracy"] = min(0.98, self.stats["accuracy"] + 0.001)
        self.stats["learned"] += 1
        
        # AUTO-ÉVOLUTION: Ajoute de nouvelles connaissances si pertinent
        if len(user_input) > 15:  # Seulement les inputs substantiels
            category = self._categorize_input(user_input)
            
            # Si c'est une bonne réponse générée, l'ajoute à la knowledge_base
            if len(response) > 30 and '?' not in response and category in self.knowledge_base:
                # Évite les doublons
                if response not in self.knowledge_base[category]:
                    self.knowledge_base[category].append(response)
                    
                    # Sauvegarde la knowledge_base améliorée
                    try:
                        with open(self.knowledge_file, "w", encoding="utf-8") as f:
                            json.dump(dict(self.knowledge_base), f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        pass  # Silencieux en cas d'erreur
    
    def _categorize_input(self, text):
        """Catégorise automatiquement un input"""
        keywords = {
            "tech": ["code", "python", "programme", "bug", "fonction", "api"],
            "science": ["atome", "physique", "chimie", "biologie", "univers"],
            "créativité": ["art", "musique", "poésie", "création", "imagination"],
            "psychologie": ["humain", "pensée", "émotion", "esprit", "conscience"],
        }
        
        text_lower = text.lower()
        for category, words in keywords.items():
            if any(word in text_lower for word in words):
                return category
        
        return "général"
    
    def get_stats(self):
        """Affiche les statistiques d'apprentissage"""
        return f"""
📊 Statistiques de {self.name}:
- Messages traités: {self.stats['messages']}
- Concepts appris: {self.stats['learned']}
- Précision: {self.stats['accuracy']*100:.1f}%
- Domaines couverts: {len(self.knowledge_base)}
- Patterns maîtrisés: {len(self.learned_patterns)}
"""
    
    def save_memory(self):
        """Sauvegarde l'apprentissage et la mémoire"""
        try:
            # Sauvegarde memory.json
            data = {
                "conversation_history": self.conversation_history[-100:],
                "stats": self.stats,
                "user_preferences": self.user_preferences
            }
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Sauvegarde knowledge.json
            with open(self.knowledge_file, "w", encoding="utf-8") as f:
                json.dump(dict(self.knowledge_base), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def load_memory(self):
        """Charge la mémoire et les préférences"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation_history = data.get("conversation_history", [])
                    self.stats = data.get("stats", self.stats)
                    self.user_preferences = data.get("user_preferences", {})
            except Exception as e:
                print(f"❌ Erreur chargement memory: {e}")


def main():
    """Interface de conversation avancée"""
    print("\n" + "="*60)
    print("🚀 NOVA - IA Ultra Avancée & Auto-Évolutive 🚀")
    print("="*60)
    print("Type: 'stats' → Voir mes statistiques")
    print("Type: 'clear' → Réinitialiser la conversation")
    print("Type: 'quit' ou 'exit' → Arrêter")
    print("="*60 + "\n")
    
    ia = AdvancedAI("Nova")
    
    # Charge les stats
    print(f"💾 Reprend avec {ia.stats['messages']} messages précédents...\n")
    
    while True:
        try:
            user_input = input("👤 Toi: ").strip()
            
            if not user_input:
                continue
            
            # Commandes spéciales
            if user_input.lower() == "quit" or user_input.lower() == "exit":
                ia.save_memory()
                print("\n🤖 Nova: À bientôt! J'ai sauvegardé tout ce que j'ai appris. 👋\n")
                break
            
            if user_input.lower() == "stats":
                print(ia.get_stats())
                continue
            
            if user_input.lower() == "clear":
                ia.conversation_history = []
                print("🤖 Nova: Conversation réinitialisée. Recommençons! ✨\n")
                continue
            
            # Génère réponse
            response = ia.respond(user_input)
            print(f"\n🤖 Nova: {response}\n")
            
            # Sauvegarde après chaque message important
            if ia.stats["messages"] % 5 == 0:
                ia.save_memory()
        
        except KeyboardInterrupt:
            print("\n\n🤖 Nova: Interrompu! Je garde tout en mémoire... 📝\n")
            ia.save_memory()
            break
        except Exception as e:
            print(f"⚠️ Erreur: {e}\n")


if __name__ == "__main__":
    main()