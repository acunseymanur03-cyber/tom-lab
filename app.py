import ast
import math
import random
import operator
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TOM LAB 5.0
# Interactive Mathematics, Physics & Pokemon Research Lab
# ============================================================

st.set_page_config(
    page_title="Tom Lab | Maths Beyond Imagination",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# LANGUAGE SYSTEM
# ------------------------------------------------------------

LANGUAGES = {
    "English": "en",
    "Türkçe": "tr",
    "Français": "fr",
    "Español": "es",
    "Deutsch": "de",
}

TEXT = {
    "en": {
        "tagline": "Maths Beyond Imagination",
        "welcome": "Welcome to Tom Lab!",
        "intro": (
            "Explore mathematics, physics, probability and "
            "the science behind imaginary worlds."
        ),
        "inspired": (
            "An independent educational project inspired by the "
            "joy of exploring mathematics through curiosity and "
            "popular culture. Not an official Tom Crawford project."
        ),
        "language": "Language",
        "level": "Learning level",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "nav": "LAB NAVIGATION",
        "home": "Home",
        "math": "Mathematics Engine",
        "functions": "Function Explorer",
        "physics": "Physics Lab",
        "pokemon": "Pokemon Energy Lab",
        "probability": "Pokemon Probability Lab",
        "growth": "Evolution & Growth",
        "mc": "Monte Carlo Lab",
        "sphere": "4D Sphere Experiment",
        "challenges": "Challenge Studio",
        "constants": "Constants Library",
        "notebook": "Research Notebook",
        "about": "About Tom Lab",
        "choose": "Choose a laboratory from the sidebar.",
        "simple": "Simple explanation",
        "intermediate_explanation": "Mathematical explanation",
        "advanced_explanation": "Advanced explanation",
        "calculate": "Calculate",
        "result": "Result",
        "expression": "Mathematical expression",
        "expression_help": "Example: 50 * 3 + sqrt(400)",
        "function": "Function of x",
        "function_help": "Example: x**2 - 3*x + 2",
        "calculate_graph": "Draw graph",
        "voltage": "Voltage (volts)",
        "current": "Current (amperes)",
        "resistance": "Resistance (ohms)",
        "power": "Power (watts)",
        "run": "Run simulation",
        "trials": "Number of trials",
        "success": "Successful outcomes",
        "probability": "Probability",
        "seed": "Random seed",
        "points": "Number of random points",
        "estimate": "Estimated value",
        "theory": "Theoretical value",
        "error": "Absolute error",
        "pi_intro": (
            "Imagine a square containing a circle. Random points "
            "help us estimate the value of pi."
        ),
        "pi_simple": (
            "Points inside the circle count toward the circle. "
            "Points outside count toward the square."
        ),
        "pi_intermediate": (
            "The ratio of points inside the circle to all points "
            "approaches pi/4 as the number of random points grows."
        ),
        "pi_advanced": (
            "For independent uniform samples, the estimator is "
            "4 times the proportion of points satisfying x²+y² ≤ 1."
        ),
        "sphere_intro": (
            "Can random points help us estimate the volume of a "
            "sphere in four dimensions?"
        ),
        "sphere_simple": (
            "We randomly generate points inside a four-dimensional "
            "cube. The fraction inside the 4D sphere helps estimate "
            "its volume."
        ),
        "sphere_intermediate": (
            "The unit 4-ball has volume pi²/2. The cube [-1,1]^4 "
            "has volume 16, so the estimate is 16 times the "
            "fraction of sampled points inside the sphere."
        ),
        "sphere_advanced": (
            "The unit 4-ball is defined by the sum of the squares "
            "of four coordinates being at most one. The Monte Carlo "
            "estimator converges to pi²/2 as sample size increases."
        ),
        "sample_count": "Samples",
        "convergence": "Convergence toward the theoretical value",
        "inside": "Points inside",
        "outside": "Points outside",
        "pokemon_power": "Hypothetical Pikachu power (watts)",
        "bulb_power": "Lightbulb power (watts)",
        "pokemon_count": "Pikachu needed",
        "pokemon_note": (
            "This is a hypothetical educational model, not a claim "
            "about real-world electricity or official Pokemon stats."
        ),
        "energy_rate": "Hypothetical energy used per second (joules)",
        "duration": "Duration (seconds)",
        "total_energy": "Total energy (joules)",
        "initial": "Initial population",
        "growth_rate": "Growth rate per step (%)",
        "steps": "Number of steps",
        "population": "Population",
        "pokemon_a": "Pokemon A win probability (%)",
        "pokemon_b": "Pokemon B win probability (%)",
        "battles": "Number of simulated battles",
        "wins_a": "Pokemon A wins",
        "wins_b": "Pokemon B wins",
        "draws": "Draws",
        "notes": "Your research notes",
        "save_note": "Add note to session notebook",
        "download": "Download notebook",
        "note_added": "Note added!",
        "challenge": "Choose a challenge",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "check": "Check answer",
        "your_answer": "Your answer",
        "correct": "Correct! Great work!",
        "incorrect": "Not quite. Try again!",
        "constants_title": "Useful mathematical and physical constants",
        "home_tip": "Select a lab to start experimenting.",
        "upload_tom": "Optional: upload a Tom Crawford photo",
        "upload_book": "Optional: upload the book cover",
        "photo_caption": (
            "Use only images you are permitted to use. "
            "The image does not imply endorsement."
        ),
        "image_url": "Optional image URL",
        "clear": "Clear",
    },
    "tr": {
        "tagline": "Hayal Gücünün Ötesinde Matematik",
        "welcome": "Tom Lab'a hoş geldin!",
        "intro": (
            "Matematiği, fiziği, olasılığı ve hayalî dünyaların "
            "arkasındaki bilimi keşfet."
        ),
        "inspired": (
            "Merak ve popüler kültür aracılığıyla matematiği "
            "keşfetme fikrinden ilham alan bağımsız bir eğitim "
            "projesidir. Resmî bir Tom Crawford projesi değildir."
        ),
        "language": "Dil",
        "level": "Öğrenme seviyesi",
        "beginner": "Başlangıç",
        "intermediate": "Orta",
        "advanced": "İleri",
        "nav": "LABORATUVAR MENÜSÜ",
        "home": "Ana Sayfa",
        "math": "Matematik Motoru",
        "functions": "Fonksiyon Kaşifi",
        "physics": "Fizik Laboratuvarı",
        "pokemon": "Pokémon Enerji Laboratuvarı",
        "probability": "Pokémon Olasılık Laboratuvarı",
        "growth": "Evrim ve Büyüme",
        "mc": "Monte Carlo Laboratuvarı",
        "sphere": "4 Boyutlu Küre Deneyi",
        "challenges": "Görev Merkezi",
        "constants": "Sabitler Kütüphanesi",
        "notebook": "Araştırma Defteri",
        "about": "Tom Lab Hakkında",
        "choose": "Sol menüden bir laboratuvar seç.",
        "simple": "Basit anlatım",
        "intermediate_explanation": "Matematiksel anlatım",
        "advanced_explanation": "İleri düzey anlatım",
        "calculate": "Hesapla",
        "result": "Sonuç",
        "expression": "Matematiksel ifade",
        "expression_help": "Örnek: 50 * 3 + sqrt(400)",
        "function": "x'e bağlı fonksiyon",
        "function_help": "Örnek: x**2 - 3*x + 2",
        "calculate_graph": "Grafiği çiz",
        "voltage": "Gerilim (volt)",
        "current": "Akım (amper)",
        "resistance": "Direnç (ohm)",
        "power": "Güç (watt)",
        "run": "Simülasyonu çalıştır",
        "trials": "Deneme sayısı",
        "success": "Başarılı sonuçlar",
        "probability": "Olasılık",
        "seed": "Rastgelelik tohumu",
        "points": "Rastgele nokta sayısı",
        "estimate": "Tahmini değer",
        "theory": "Teorik değer",
        "error": "Mutlak hata",
        "pi_intro": (
            "Bir çemberin etrafında bir kare olduğunu düşün. "
            "Rastgele noktalarla pi sayısını tahmin edebiliriz."
        ),
        "pi_simple": (
            "Çemberin içindeki noktaları sayarız. "
            "Kalan noktalar karenin dışında kalan bölüme aittir."
        ),
        "pi_intermediate": (
            "Çember içindeki noktaların tüm noktalara oranı, "
            "örnek sayısı arttıkça pi/4 değerine yaklaşır."
        ),
        "pi_advanced": (
            "Bağımsız ve düzgün dağılımlı örnekler için tahmin, "
            "x²+y² ≤ 1 koşulunu sağlayan noktaların oranının "
            "4 ile çarpılmasıdır."
        ),
        "sphere_intro": (
            "Rastgele noktalar kullanarak dört boyutlu bir "
            "kürenin hacmini tahmin edebilir miyiz?"
        ),
        "sphere_simple": (
            "Dört boyutlu bir küp içinde rastgele noktalar üretiriz. "
            "4 boyutlu kürenin içindeki noktaların oranı, "
            "hacmi tahmin etmemize yardımcı olur."
        ),
        "sphere_intermediate": (
            "Birim 4-kürenin hacmi pi²/2'dir. [-1,1]^4 küpünün "
            "hacmi 16 olduğundan tahmin, küre içindeki noktaların "
            "oranının 16 ile çarpılmasıyla bulunur."
        ),
        "sphere_advanced": (
            "Birim 4-küre, dört koordinatın kareleri toplamı "
            "birden küçük veya eşit olan noktalardan oluşur. "
            "Monte Carlo tahmini, örnek sayısı arttıkça pi²/2'ye "
            "yaklaşır."
        ),
        "sample_count": "Örnek sayısı",
        "convergence": "Teorik değere yaklaşma",
        "inside": "İçerideki noktalar",
        "outside": "Dışarıdaki noktalar",
        "pokemon_power": "Varsayımsal Pikachu gücü (watt)",
        "bulb_power": "Ampulün gücü (watt)",
        "pokemon_count": "Gereken Pikachu sayısı",
        "pokemon_note": (
            "Bu, eğitim amacıyla oluşturulmuş varsayımsal bir "
            "modeldir; gerçek elektrik üretimi veya resmî Pokémon "
            "istatistikleri hakkında bir iddia değildir."
        ),
        "energy_rate": "Saniyede kullanılan varsayımsal enerji (joule)",
        "duration": "Süre (saniye)",
        "total_energy": "Toplam enerji (joule)",
        "initial": "Başlangıç nüfusu",
        "growth_rate": "Adım başına büyüme oranı (%)",
        "steps": "Adım sayısı",
        "population": "Nüfus",
        "pokemon_a": "Pokémon A'nın kazanma olasılığı (%)",
        "pokemon_b": "Pokémon B'nin kazanma olasılığı (%)",
        "battles": "Simüle edilen karşılaşma sayısı",
        "wins_a": "Pokémon A galibiyetleri",
        "wins_b": "Pokémon B galibiyetleri",
        "draws": "Beraberlik",
        "notes": "Araştırma notların",
        "save_note": "Notu oturum defterine ekle",
        "download": "Araştırma defterini indir",
        "note_added": "Not eklendi!",
        "challenge": "Bir görev seç",
        "easy": "Kolay",
        "medium": "Orta",
        "hard": "Zor",
        "check": "Cevabı kontrol et",
        "your_answer": "Cevabın",
        "correct": "Doğru! Harika iş!",
        "incorrect": "Tam değil. Tekrar dene!",
        "constants_title": "Yararlı matematik ve fizik sabitleri",
        "home_tip": "Deney yapmak için bir laboratuvar seç.",
        "upload_tom": "İsteğe bağlı: Tom Crawford fotoğrafını yükle",
        "upload_book": "İsteğe bağlı: kitabın kapağını yükle",
        "photo_caption": (
            "Yalnızca kullanma izniniz olan görselleri kullanın. "
            "Görselin kullanılması onay verildiği anlamına gelmez."
        ),
        "image_url": "İsteğe bağlı görsel bağlantısı",
        "clear": "Temizle",
    },
    "fr": {
        "tagline": "Les mathématiques sans limites",
        "welcome": "Bienvenue dans Tom Lab !",
        "intro": "Explore les mathématiques, la physique et les probabilités.",
        "inspired": "Projet éducatif indépendant, non officiel.",
        "language": "Langue",
        "level": "Niveau",
        "beginner": "Débutant",
        "intermediate": "Intermédiaire",
        "advanced": "Avancé",
        "nav": "LABORATOIRES",
        "home": "Accueil",
        "math": "Calcul mathématique",
        "functions": "Explorateur de fonctions",
        "physics": "Laboratoire de physique",
        "pokemon": "Énergie Pokémon",
        "probability": "Probabilités Pokémon",
        "growth": "Évolution et croissance",
        "mc": "Laboratoire Monte Carlo",
        "sphere": "Expérience de sphère 4D",
        "challenges": "Défis",
        "constants": "Constantes",
        "notebook": "Carnet de recherche",
        "about": "À propos",
        "choose": "Choisis un laboratoire dans le menu.",
        "simple": "Explication simple",
        "intermediate_explanation": "Explication mathématique",
        "advanced_explanation": "Explication avancée",
        "calculate": "Calculer",
        "result": "Résultat",
        "expression": "Expression mathématique",
        "expression_help": "Exemple : 50 * 3 + sqrt(400)",
        "function": "Fonction de x",
        "function_help": "Exemple : x**2 - 3*x + 2",
        "calculate_graph": "Tracer le graphique",
        "voltage": "Tension (volts)",
        "current": "Courant (ampères)",
        "resistance": "Résistance (ohms)",
        "power": "Puissance (watts)",
        "run": "Lancer la simulation",
        "trials": "Nombre d'essais",
        "success": "Résultats réussis",
        "probability": "Probabilité",
        "seed": "Graine aléatoire",
        "points": "Nombre de points aléatoires",
        "estimate": "Estimation",
        "theory": "Valeur théorique",
        "error": "Erreur absolue",
        "pi_intro": "Estimons pi avec des points aléatoires.",
        "pi_simple": "Les points dans le cercle nous aident à estimer pi.",
        "pi_intermediate": "La proportion de points dans le cercle tend vers pi/4.",
        "pi_advanced": "L'estimateur est quatre fois la proportion x²+y² ≤ 1.",
        "sphere_intro": "Estimons le volume d'une sphère en quatre dimensions.",
        "sphere_simple": "La proportion de points dans la sphère aide à estimer son volume.",
        "sphere_intermediate": "Le volume de la boule unité 4D est pi²/2.",
        "sphere_advanced": "L'estimateur converge vers pi²/2 avec plus d'échantillons.",
        "sample_count": "Échantillons",
        "convergence": "Convergence",
        "inside": "Points intérieurs",
        "outside": "Points extérieurs",
        "pokemon_power": "Puissance hypothétique de Pikachu (W)",
        "bulb_power": "Puissance de l'ampoule (W)",
        "pokemon_count": "Nombre de Pikachu nécessaires",
        "pokemon_note": "Modèle hypothétique à but éducatif.",
        "energy_rate": "Énergie par seconde (joules)",
        "duration": "Durée (secondes)",
        "total_energy": "Énergie totale (joules)",
        "initial": "Population initiale",
        "growth_rate": "Taux de croissance (%)",
        "steps": "Nombre d'étapes",
        "population": "Population",
        "pokemon_a": "Probabilité de victoire de A (%)",
        "pokemon_b": "Probabilité de victoire de B (%)",
        "battles": "Combats simulés",
        "wins_a": "Victoires de A",
        "wins_b": "Victoires de B",
        "draws": "Égalités",
        "notes": "Notes de recherche",
        "save_note": "Ajouter une note",
        "download": "Télécharger les notes",
        "note_added": "Note ajoutée !",
        "challenge": "Choisir un défi",
        "easy": "Facile",
        "medium": "Moyen",
        "hard": "Difficile",
        "check": "Vérifier",
        "your_answer": "Ta réponse",
        "correct": "Correct !",
        "incorrect": "Essaie encore !",
        "constants_title": "Constantes utiles",
        "home_tip": "Choisis un laboratoire pour commencer.",
        "upload_tom": "Importer une photo de Tom Crawford",
        "upload_book": "Importer la couverture du livre",
        "photo_caption": "Utilise uniquement des images autorisées.",
        "image_url": "URL facultative de l'image",
        "clear": "Effacer",
    },
    "es": {
        "tagline": "Matemáticas más allá de la imaginación",
        "welcome": "¡Bienvenido a Tom Lab!",
        "intro": "Explora las matemáticas, la física y la probabilidad.",
        "inspired": "Proyecto educativo independiente, no oficial.",
        "language": "Idioma",
        "level": "Nivel",
        "beginner": "Principiante",
        "intermediate": "Intermedio",
        "advanced": "Avanzado",
        "nav": "LABORATORIOS",
        "home": "Inicio",
        "math": "Motor matemático",
        "functions": "Explorador de funciones",
        "physics": "Laboratorio de física",
        "pokemon": "Energía Pokémon",
        "probability": "Probabilidad Pokémon",
        "growth": "Evolución y crecimiento",
        "mc": "Laboratorio Monte Carlo",
        "sphere": "Experimento de esfera 4D",
        "challenges": "Desafíos",
        "constants": "Constantes",
        "notebook": "Cuaderno de investigación",
        "about": "Acerca de",
        "choose": "Elige un laboratorio en el menú.",
        "simple": "Explicación sencilla",
        "intermediate_explanation": "Explicación matemática",
        "advanced_explanation": "Explicación avanzada",
        "calculate": "Calcular",
        "result": "Resultado",
        "expression": "Expresión matemática",
        "expression_help": "Ejemplo: 50 * 3 + sqrt(400)",
        "function": "Función de x",
        "function_help": "Ejemplo: x**2 - 3*x + 2",
        "calculate_graph": "Dibujar gráfica",
        "voltage": "Voltaje (voltios)",
        "current": "Corriente (amperios)",
        "resistance": "Resistencia (ohmios)",
        "power": "Potencia (vatios)",
        "run": "Ejecutar simulación",
        "trials": "Número de ensayos",
        "success": "Resultados exitosos",
        "probability": "Probabilidad",
        "seed": "Semilla aleatoria",
        "points": "Puntos aleatorios",
        "estimate": "Estimación",
        "theory": "Valor teórico",
        "error": "Error absoluto",
        "pi_intro": "Estimemos pi usando puntos aleatorios.",
        "pi_simple": "Los puntos dentro del círculo ayudan a estimar pi.",
        "pi_intermediate": "La proporción interior se aproxima a pi/4.",
        "pi_advanced": "El estimador es cuatro veces la proporción x²+y² ≤ 1.",
        "sphere_intro": "Estimemos el volumen de una esfera en cuatro dimensiones.",
        "sphere_simple": "La proporción interior permite estimar el volumen.",
        "sphere_intermediate": "El volumen de la bola unidad 4D es pi²/2.",
        "sphere_advanced": "La estimación converge a pi²/2 con más muestras.",
        "sample_count": "Muestras",
        "convergence": "Convergencia",
        "inside": "Puntos interiores",
        "outside": "Puntos exteriores",
        "pokemon_power": "Potencia hipotética de Pikachu (W)",
        "bulb_power": "Potencia de la bombilla (W)",
        "pokemon_count": "Pikachu necesarios",
        "pokemon_note": "Modelo hipotético educativo.",
        "energy_rate": "Energía por segundo (julios)",
        "duration": "Duración (segundos)",
        "total_energy": "Energía total (julios)",
        "initial": "Población inicial",
        "growth_rate": "Tasa de crecimiento (%)",
        "steps": "Número de pasos",
        "population": "Población",
        "pokemon_a": "Probabilidad de victoria de A (%)",
        "pokemon_b": "Probabilidad de victoria de B (%)",
        "battles": "Combates simulados",
        "wins_a": "Victorias de A",
        "wins_b": "Victorias de B",
        "draws": "Empates",
        "notes": "Notas de investigación",
        "save_note": "Añadir nota",
        "download": "Descargar notas",
        "note_added": "¡Nota añadida!",
        "challenge": "Elegir desafío",
        "easy": "Fácil",
        "medium": "Medio",
        "hard": "Difícil",
        "check": "Comprobar respuesta",
        "your_answer": "Tu respuesta",
        "correct": "¡Correcto!",
        "incorrect": "¡Inténtalo otra vez!",
        "constants_title": "Constantes útiles",
        "home_tip": "Elige un laboratorio para comenzar.",
        "upload_tom": "Subir una foto de Tom Crawford",
        "upload_book": "Subir la portada del libro",
        "photo_caption": "Usa solo imágenes autorizadas.",
        "image_url": "URL opcional de imagen",
        "clear": "Borrar",
    },
    "de": {
        "tagline": "Mathematik jenseits der Vorstellungskraft",
        "welcome": "Willkommen bei Tom Lab!",
        "intro": "Entdecke Mathematik, Physik und Wahrscheinlichkeit.",
        "inspired": "Unabhängiges, nicht offizielles Bildungsprojekt.",
        "language": "Sprache",
        "level": "Lernniveau",
        "beginner": "Anfänger",
        "intermediate": "Mittelstufe",
        "advanced": "Fortgeschritten",
        "nav": "LABORE",
        "home": "Startseite",
        "math": "Mathematik-Rechner",
        "functions": "Funktionslabor",
        "physics": "Physiklabor",
        "pokemon": "Pokémon-Energielabor",
        "probability": "Pokémon-Wahrscheinlichkeit",
        "growth": "Entwicklung und Wachstum",
        "mc": "Monte-Carlo-Labor",
        "sphere": "4D-Kugel-Experiment",
        "challenges": "Herausforderungen",
        "constants": "Konstanten",
        "notebook": "Forschungsnotizbuch",
        "about": "Über Tom Lab",
        "choose": "Wähle ein Labor im Menü.",
        "simple": "Einfache Erklärung",
        "intermediate_explanation": "Mathematische Erklärung",
        "advanced_explanation": "Fortgeschrittene Erklärung",
        "calculate": "Berechnen",
        "result": "Ergebnis",
        "expression": "Mathematischer Ausdruck",
        "expression_help": "Beispiel: 50 * 3 + sqrt(400)",
        "function": "Funktion von x",
        "function_help": "Beispiel: x**2 - 3*x + 2",
        "calculate_graph": "Graph zeichnen",
        "voltage": "Spannung (Volt)",
        "current": "Strom (Ampere)",
        "resistance": "Widerstand (Ohm)",
        "power": "Leistung (Watt)",
        "run": "Simulation starten",
        "trials": "Anzahl der Versuche",
        "success": "Erfolgreiche Ergebnisse",
        "probability": "Wahrscheinlichkeit",
        "seed": "Zufallsstartwert",
        "points": "Zufällige Punkte",
        "estimate": "Schätzwert",
        "theory": "Theoretischer Wert",
        "error": "Absoluter Fehler",
        "pi_intro": "Schätzen wir pi mit zufälligen Punkten.",
        "pi_simple": "Punkte im Kreis helfen, pi zu schätzen.",
        "pi_intermediate": "Der Anteil im Kreis nähert sich pi/4.",
        "pi_advanced": "Der Schätzer ist viermal der Anteil mit x²+y² ≤ 1.",
        "sphere_intro": "Schätzen wir das Volumen einer vierdimensionalen Kugel.",
        "sphere_simple": "Der Anteil der inneren Punkte schätzt das Volumen.",
        "sphere_intermediate": "Das Volumen der 4D-Einheitskugel ist pi²/2.",
        "sphere_advanced": "Mit mehr Stichproben nähert sich die Schätzung pi²/2.",
        "sample_count": "Stichproben",
        "convergence": "Konvergenz",
        "inside": "Innere Punkte",
        "outside": "Äußere Punkte",
        "pokemon_power": "Hypothetische Pikachu-Leistung (W)",
        "bulb_power": "Glühlampenleistung (W)",
        "pokemon_count": "Benötigte Pikachu",
        "pokemon_note": "Hypothetisches Lernmodell.",
        "energy_rate": "Energie pro Sekunde (Joule)",
        "duration": "Dauer (Sekunden)",
        "total_energy": "Gesamtenergie (Joule)",
        "initial": "Anfangspopulation",
        "growth_rate": "Wachstumsrate (%)",
        "steps": "Anzahl der Schritte",
        "population": "Population",
        "pokemon_a": "Siegwahrscheinlichkeit von A (%)",
        "pokemon_b": "Siegwahrscheinlichkeit von B (%)",
        "battles": "Simulierte Kämpfe",
        "wins_a": "Siege von A",
        "wins_b": "Siege von B",
        "draws": "Unentschieden",
        "notes": "Forschungsnotizen",
        "save_note": "Notiz hinzufügen",
        "download": "Notizen herunterladen",
        "note_added": "Notiz hinzugefügt!",
        "challenge": "Aufgabe auswählen",
        "easy": "Einfach",
        "medium": "Mittel",
        "hard": "Schwer",
        "check": "Antwort prüfen",
        "your_answer": "Deine Antwort",
        "correct": "Richtig!",
        "incorrect": "Versuche es erneut!",
        "constants_title": "Nützliche Konstanten",
        "home_tip": "Wähle ein Labor, um zu beginnen.",
        "upload_tom": "Tom-Crawford-Foto hochladen",
        "upload_book": "Buchcover hochladen",
        "photo_caption": "Verwende nur Bilder, die du nutzen darfst.",
        "image_url": "Optionale Bild-URL",
        "clear": "Löschen",
    },
}

# Fallback: French, Spanish and German contain the main navigation
# and common labels. Missing advanced descriptions fall back to English.

def tr(key):
    lang = st.session_state.get("language_code", "en")
    return TEXT.get(lang, TEXT["en"]).get(
        key, TEXT["en"].get(key, key)
    )


# ------------------------------------------------------------
# SIDEBAR SETTINGS
# ------------------------------------------------------------

st.sidebar.title("⚡ TOM LAB")

language = st.sidebar.selectbox(
    tr("language"),
    list(LANGUAGES.keys()),
    index=0,
    key="language_choice",
)
st.session_state["language_code"] = LANGUAGES[language]

level_options = [
    tr("beginner"),
    tr("intermediate"),
    tr("advanced"),
]
level = st.sidebar.selectbox(tr("level"), level_options)

st.sidebar.caption("Version 5.0 • Independent educational project")

pages = [
    tr("home"),
    tr("math"),
    tr("functions"),
    tr("physics"),
    tr("pokemon"),
    tr("probability"),
    tr("growth"),
    tr("mc"),
    tr("sphere"),
    tr("challenges"),
    tr("constants"),
    tr("notebook"),
    tr("about"),
]

page = st.sidebar.radio(tr("nav"), pages)

st.sidebar.divider()
st.sidebar.subheader("🖼️ Personalise the welcome page")

tom_upload = st.sidebar.file_uploader(
    tr("upload_tom"),
    type=["png", "jpg", "jpeg", "webp"],
    key="tom_photo_upload",
)

book_upload = st.sidebar.file_uploader(
    tr("upload_book"),
    type=["png", "jpg", "jpeg", "webp"],
    key="book_cover_upload",
)

st.sidebar.caption(tr("photo_caption"))


# ------------------------------------------------------------
# SESSION NOTEBOOK
# ------------------------------------------------------------

if "research_notes" not in st.session_state:
    st.session_state["research_notes"] = []


def add_note(text):
    st.session_state["research_notes"].append(text)


# ------------------------------------------------------------
# SAFE MATHEMATICAL EXPRESSION EVALUATOR
# ------------------------------------------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def safe_eval_node(node):
    if isinstance(node, ast.Expression):
        return safe_eval_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")
        left = safe_eval_node(node.left)
        right = safe_eval_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")

        return ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")
        return ALLOWED_OPERATORS[op_type](
            safe_eval_node(node.operand)
        )

    if isinstance(node, ast.Name):
        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]
        raise ValueError("Unknown name.")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Function not allowed.")

        name = node.func.id
        if name not in ALLOWED_FUNCTIONS:
            raise ValueError("Function not allowed.")

        if node.keywords:
            raise ValueError("Keyword arguments are not allowed.")

        args = [safe_eval_node(arg) for arg in node.args]
        return ALLOWED_FUNCTIONS[name](*args)

    raise ValueError("Unsupported expression.")


def safe_calculate(expression):
    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    tree = ast.parse(expression, mode="eval")
    result = safe_eval_node(tree)

    if not isinstance(result, (int, float)):
        raise ValueError("Result must be numeric.")

    if not math.isfinite(float(result)):
        raise ValueError("Result is not finite.")

    return result


# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------

def show_home():
    st.title("⚡ TOM LAB")
    st.subheader(tr("tagline"))
    st.write("### " + tr("welcome"))
    st.write(tr("intro"))

    left, right = st.columns([1.2, 1])

    with left:
        if tom_upload is not None:
            st.image(tom_upload, use_container_width=True)
            st.caption("Tom Crawford — uploaded image")
        else:
            st.info(
                "📷 Add a permitted Tom Crawford photo using "
                "the uploader in the sidebar."
            )

    with right:
        if book_upload is not None:
            st.image(book_upload, use_container_width=True)
            st.caption("Book cover — uploaded image")
        else:
            st.info(
                "📚 Add the book cover using the uploader "
                "in the sidebar."
            )

        st.markdown("### 🔬 Explore. Experiment. Understand.")

        st.write(
            "Discover the ideas behind mathematics and physics "
            "through interactive experiments."
        )

    st.divider()

    st.markdown("### 🧪 Choose your next experiment")

    cards = [
        ("⚡", tr("pokemon"), tr("pokemon_note")),
        ("🎲", tr("probability"), tr("pi_intro")),
        ("🌌", tr("sphere"), tr("sphere_intro")),
        ("📈", tr("functions"), tr("function_help")),
    ]

    columns = st.columns(2)

    for index, card in enumerate(cards):
        with columns[index % 2]:
            with st.container(border=True):
                st.subheader(f"{card[0]} {card[1]}")
                st.write(card[2])

    st.divider()
    st.caption(tr("inspired"))


# ------------------------------------------------------------
# MATHEMATICS ENGINE
# ------------------------------------------------------------

def show_math():
    st.title("🧮 " + tr("math"))
    st.write(tr("expression_help"))

    expression = st.text_input(
        tr("expression"),
        value="50 * 3 + sqrt(400)",
    )

    st.write(
        "**" + tr("simple") + ":** "
        "Enter a mathematical expression and calculate its value."
        if st.session_state["language_code"] == "en"
        else tr("simple")
    )

    if st.button(tr("calculate"), key="math_calc"):
        try:
            result = safe_calculate(expression)
            st.success(f"{tr('result')}: {result}")
            add_note(f"Calculator: {expression} = {result}")
        except Exception as error:
            st.error(f"Could not calculate: {error}")

    st.markdown("### Useful functions")
    st.code(
        "sqrt(25)\nsin(pi / 2)\nlog(10)\n"
        "2**8\n50 * 3 + sqrt(400)"
    )

    if level == tr("beginner"):
        st.info(
            "Tip: * means multiply, / means divide, and ** "
            "means a power. For example, 2**3 = 8."
        )
    elif level == tr("intermediate"):
        st.info(
            "The calculator supports arithmetic, powers, "
            "parentheses and selected mathematical functions."
        )
    else:
        st.info(
            "Expressions are parsed using Python's abstract syntax "
            "tree. Only selected numeric operations and functions "
            "are accepted."
        )


# ------------------------------------------------------------
# FUNCTION EXPLORER
# ------------------------------------------------------------

def show_functions():
    st.title("📈 " + tr("functions"))

    expression = st.text_input(
        tr("function"),
        value="x**2 - 3*x + 2",
        help=tr("function_help"),
    )

    xmin, xmax = st.slider(
        "x range",
        min_value=-20,
        max_value=20,
        value=(-10, 10),
    )

    st.write(tr("function_help"))

    if st.button(tr("calculate_graph")):
        try:
            # Restrict function expressions to numeric syntax,
            # x, selected functions and selected constants.
            tree = ast.parse(expression, mode="eval")

            allowed_names = (
                set(ALLOWED_FUNCTIONS.keys())
                | set(ALLOWED_CONSTANTS.keys())
                | {"x"}
            )

            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if node.id not in allowed_names:
                        raise ValueError("Unknown name in function.")
                elif isinstance(node, ast.Call):
                    if not isinstance(node.func, ast.Name):
                        raise ValueError("Unsupported function.")
                    if node.func.id not in ALLOWED_FUNCTIONS:
                        raise ValueError("Unsupported function.")
                elif isinstance(node, ast.BinOp):
                    if type(node.op) not in ALLOWED_OPERATORS:
                        raise ValueError("Unsupported operator.")
                elif isinstance(node, ast.UnaryOp):
                    if type(node.op) not in ALLOWED_OPERATORS:
                        raise ValueError("Unsupported operator.")
                elif isinstance(node, (ast.Expression, ast.Load,
                                       ast.Constant, ast.Name,
                                       ast.Call, ast.Add, ast.Sub,
                                       ast.Mult, ast.Div, ast.Pow,
                                       ast.Mod, ast.USub, ast.UAdd)):
                    pass
                else:
                    raise ValueError("Unsupported expression.")

            x = np.linspace(xmin, xmax, 500)

            namespace = {
                "x": x,
                **ALLOWED_FUNCTIONS,
                **ALLOWED_CONSTANTS,
            }

            y = eval(
                compile(tree, "<function>", "eval"),
                {"__builtins__": {}},
                namespace,
            )

            y = np.asarray(y, dtype=float)

            if y.ndim == 0:
                y = np.full_like(x, y)

            if y.shape != x.shape:
                raise ValueError("Function output has an invalid shape.")

            y = np.where(np.isfinite(y), y, np.nan)

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.axhline(0, linewidth=0.8)
            ax.axvline(0, linewidth=0.8)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"f(x) = {expression}")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

            if level == tr("beginner"):
                st.info(
                    "A function takes an input, x, and produces "
                    "an output, f(x). The graph shows this relationship."
                )
            elif level == tr("intermediate"):
                st.info(
                    "Each point on the graph represents an input x "
                    "and its corresponding output f(x)."
                )
            else:
                st.info(
                    "Inspect roots, turning points and the behaviour "
                    "of the function over the selected domain."
                )

        except Exception as error:
            st.error(f"Could not plot this function: {error}")


# ------------------------------------------------------------
# PHYSICS LAB
# ------------------------------------------------------------

def show_physics():
    st.title("🔌 " + tr("physics"))
    st.subheader("Ohm's Law")

    mode = st.radio(
        "Calculate",
        ["Current", "Voltage", "Resistance", "Power"],
        horizontal=True,
    )

    voltage = st.number_input(
        tr("voltage"), min_value=0.0, value=12.0
    )
    resistance = st.number_input(
        tr("resistance"),
        min_value=0.01,
        value=4.0,
    )
    current = st.number_input(
        tr("current"),
        min_value=0.0,
        value=3.0,
    )

    if mode == "Current":
        result = voltage / resistance
        st.metric(tr("current"), f"{result:.4f} A")
        formula = "I = V / R"
    elif mode == "Voltage":
        result = current * resistance
        st.metric(tr("voltage"), f"{result:.4f} V")
        formula = "V = I × R"
    elif mode == "Resistance":
        if current == 0:
            st.warning("Current must be greater than zero.")
            return
        result = voltage / current
        st.metric(tr("resistance"), f"{result:.4f} Ω")
        formula = "R = V / I"
    else:
        result = voltage * current
        st.metric(tr("power"), f"{result:.4f} W")
        formula = "P = V × I"

    st.latex(formula)

    if level == tr("beginner"):
        st.info(
            "Voltage is the electrical push, current is the flow "
            "of charge, and resistance makes that flow harder."
        )
    elif level == tr("intermediate"):
        st.info(
            "Ohm's law relates voltage, current and resistance. "
            "Electrical power can be calculated using P = V × I."
        )
    else:
        st.info(
            "These calculations assume a simple idealised circuit. "
            "Real components may have non-linear behaviour."
        )


# ------------------------------------------------------------
# POKEMON ENERGY LAB
# ------------------------------------------------------------

def show_pokemon():
    st.title("⚡ " + tr("pokemon"))

    st.markdown("### ⚡ How Many Pikachus Would Power a Lightbulb?")

    bulb_power = st.number_input(
        tr("bulb_power"),
        min_value=1.0,
        max_value=100000.0,
        value=60.0,
        step=1.0,
    )

    pikachu_power = st.number_input(
        tr("pokemon_power"),
        min_value=0.1,
        max_value=100000.0,
        value=10.0,
        step=0.5,
    )

    if st.button(tr("calculate"), key="pikachu_calc"):
        number = math.ceil(bulb_power / pikachu_power)

        st.metric(tr("pokemon_count"), number)
        st.write(
            f"{bulb_power:g} W ÷ {pikachu_power:g} W "
            f"= {bulb_power / pikachu_power:.2f}"
        )

        st.info(tr("pokemon_note"))

        add_note(
            f"Pikachu model: bulb={bulb_power} W, "
            f"power per Pikachu={pikachu_power} W, "
            f"required={number}"
        )

    st.divider()
    st.markdown("### 🔥 Charizard Energy Lab")

    energy_rate = st.number_input(
        tr("energy_rate"),
        min_value=0.0,
        value=1000.0,
        step=100.0,
    )

    duration = st.number_input(
        tr("duration"),
        min_value=0.0,
        value=60.0,
        step=5.0,
    )

    total_energy = energy_rate * duration

    st.metric(tr("total_energy"), f"{total_energy:,.2f} J")

    st.caption(
        "Educational model: the energy rate is an adjustable "
        "assumption, not an official Pokemon statistic."
    )

    if level == tr("beginner"):
        st.info(
            "Energy is measured in joules. If a model uses "
            "1,000 joules each second for 60 seconds, the total "
            "energy is 60,000 joules."
        )
    elif level == tr("intermediate"):
        st.latex(r"E = P \times t")
        st.write(
            "Energy equals power multiplied by time when power "
            "is constant."
        )
    else:
        st.latex(r"E = \int_0^t P(\tau)\,d\tau")
        st.write(
            "For changing power, total energy is the integral "
            "of power over time."
        )


# ------------------------------------------------------------
# POKEMON PROBABILITY AND BATTLE SIMULATION
# ------------------------------------------------------------

def show_probability():
    st.title("🎲 " + tr("probability"))

    st.write(
        "Simulate fictional encounters to learn how theoretical "
        "probability compares with observed results."
    )

    col1, col2 = st.columns(2)

    with col1:
        prob_a = st.slider(
            tr("pokemon_a"), 0, 100, 50
        ) / 100

    with col2:
        prob_b = st.slider(
            tr("pokemon_b"), 0, 100, 30
        ) / 100

    battles = st.slider(
        tr("battles"),
        min_value=100,
        max_value=20000,
        value=3000,
        step=100,
    )

    if prob_a + prob_b > 1:
        st.warning(
            "The two win probabilities cannot sum to more than 100%. "
            "Please adjust them."
        )
        return

    if st.button(tr("run"), key="battle_sim"):
        rng = np.random.default_rng()

        outcomes = rng.random(battles)

        wins_a = int(np.sum(outcomes < prob_a))
        wins_b = int(
            np.sum(
                (outcomes >= prob_a)
                & (outcomes < prob_a + prob_b)
            )
        )
        draws = battles - wins_a - wins_b

        col1, col2, col3 = st.columns(3)

        col1.metric(tr("wins_a"), wins_a)
        col2.metric(tr("wins_b"), wins_b)
        col3.metric(tr("draws"), draws)

        observed = pd.DataFrame({
            "Outcome": [
                "Pokemon A",
                "Pokemon B",
                "Draw",
            ],
            "Count": [wins_a, wins_b, draws],
        })

        st.bar_chart(
            observed.set_index("Outcome")
        )

        st.caption(
            "The model uses the probabilities you entered. "
            "It does not represent official Pokemon battle mechanics."
        )

        add_note(
            f"Battle simulation: {battles} trials, "
            f"A={wins_a}, B={wins_b}, draws={draws}"
        )

    if level == tr("beginner"):
        st.info(
            "Probability describes how likely an event is. "
            "A probability of 50% does not guarantee half the "
            "outcomes in a small experiment."
        )
    elif level == tr("intermediate"):
        st.info(
            "The observed frequency is the number of outcomes "
            "divided by the number of trials. It may differ from "
            "the theoretical probability."
        )
    else:
        st.info(
            "For independent trials, the observed proportion "
            "typically becomes more stable as the sample size grows."
        )


# ------------------------------------------------------------
# POKEMON POPULATION GROWTH
# ------------------------------------------------------------

def show_growth():
    st.title("📈 " + tr("growth"))

    initial = st.number_input(
        tr("initial"),
        min_value=1,
        max_value=1000000,
        value=10,
    )

    rate = st.slider(
        tr("growth_rate"),
        min_value=-50,
        max_value=100,
        value=10,
    ) / 100

    steps = st.slider(
        tr("steps"),
        min_value=1,
        max_value=100,
        value=20,
    )

    values = [float(initial)]

    for _ in range(steps):
        values.append(values[-1] * (1 + rate))

    frame = pd.DataFrame({
        "Step": list(range(steps + 1)),
        "Population": values,
    })

    st.line_chart(
        frame.set_index("Step")
    )

    st.metric(
        tr("population"),
        f"{values[-1]:,.2f}",
    )

    if level == tr("beginner"):
        st.info(
            "This model changes the population by the same percentage "
            "at every step. It is a simplified mathematical example."
        )
    elif level == tr("intermediate"):
        st.latex(r"P_n = P_0(1+r)^n")
        st.write(
            "The population after n steps is the initial value "
            "multiplied by the growth factor at each step."
        )
    else:
        st.info(
            "This is a discrete exponential model. It assumes a "
            "constant growth rate and ignores resource limits."
        )


# ------------------------------------------------------------
# MONTE CARLO PI EXPERIMENT
# ARCHIE'S FIRST SUGGESTION: VISUALISE THE RANDOM POINTS
# ------------------------------------------------------------

def show_monte_carlo():
    st.title("🎯 " + tr("mc"))

    st.write(tr("pi_intro"))

    if level == tr("beginner"):
        st.info(tr("pi_simple"))
    elif level == tr("intermediate"):
        st.info(tr("pi_intermediate"))
    else:
        st.info(tr("pi_advanced"))

    n = st.slider(
        tr("points"),
        min_value=100,
        max_value=20000,
        value=3000,
        step=100,
    )

    seed = st.number_input(
        tr("seed"),
        min_value=0,
        max_value=999999,
        value=42,
    )

    if st.button(tr("run"), key="mc_pi_run"):
        rng = np.random.default_rng(int(seed))

        x = rng.uniform(-1, 1, n)
        y = rng.uniform(-1, 1, n)

        inside_mask = x**2 + y**2 <= 1

        inside_count = int(np.sum(inside_mask))
        outside_count = n - inside_count

        estimate = 4 * inside_count / n
        theoretical = math.pi
        error = abs(estimate - theoretical)

        st.session_state["mc_pi_result"] = {
            "n": n,
            "seed": int(seed),
            "estimate": estimate,
            "inside": inside_count,
            "outside": outside_count,
            "x": x,
            "y": y,
            "mask": inside_mask,
        }

        add_note(
            f"Monte Carlo pi: n={n}, estimate={estimate:.6f}, "
            f"actual pi={math.pi:.6f}"
        )

    result = st.session_state.get("mc_pi_result")

    if result is None:
        st.caption(
            "Choose a point count and press Run simulation."
        )
        return
