import ast
import math
import operator

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Tom Lab | Math & Pokémon",
    page_icon="⚡",
    layout="wide",
)

# -----------------------------
# LANGUAGE SETTINGS
# -----------------------------

TEXT = {
    "English": {
        "home": "Home",
        "calculator": "Math Calculator",
        "functions": "Function Explorer",
        "physics": "Physics Lab",
        "pokemon": "Pokémon Energy Lab",
        "probability": "Probability Lab",
        "montecarlo": "Monte Carlo π",
        "sphere": "4D Sphere Experiment",
        "about": "About",
        "welcome": "Welcome to Tom Lab!",
        "subtitle": "Explore mathematics, physics and Pokémon-inspired experiments.",
        "language": "Language",
        "level": "Learning level",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "expression": "Mathematical expression",
        "calculate": "Calculate",
        "result": "Result",
        "function": "Function",
        "plot": "Draw graph",
        "voltage": "Voltage (V)",
        "current": "Current (A)",
        "resistance": "Resistance (Ω)",
        "power": "Power",
        "points": "Number of random points",
        "run": "Run simulation",
        "estimate": "Estimated value of π",
        "theoretical": "Actual value of π",
        "sphere_intro": "Estimate the volume of a 4D unit sphere using Monte Carlo sampling.",
        "sphere_estimate": "Estimated 4D sphere volume",
        "pokemon_intro": "Explore a hypothetical Pokémon energy model.",
        "pikachu": "Hypothetical Pikachu power (watts)",
        "bulb": "Light bulb power (watts)",
        "about_text": "An independent educational project exploring maths and science through interactive experiments.",
        "error": "Please enter a valid expression.",
        "energy": "Power required for one bulb",
        "count": "Estimated Pikachu count",
        "heads": "Probability of heads (%)",
    },
    "Türkçe": {
        "home": "Ana Sayfa",
        "calculator": "Matematik Hesaplayıcı",
        "functions": "Fonksiyon Grafikleri",
        "physics": "Fizik Laboratuvarı",
        "pokemon": "Pokémon Enerji Laboratuvarı",
        "probability": "Olasılık Laboratuvarı",
        "montecarlo": "Monte Carlo π",
        "sphere": "4B Küre Deneyi",
        "about": "Hakkında",
        "welcome": "Tom Lab'a hoş geldin!",
        "subtitle": "Matematik, fizik ve Pokémon temalı deneyleri keşfet.",
        "language": "Dil",
        "level": "Öğrenme seviyesi",
        "beginner": "Başlangıç",
        "intermediate": "Orta",
        "advanced": "İleri",
        "expression": "Matematiksel ifade",
        "calculate": "Hesapla",
        "result": "Sonuç",
        "function": "Fonksiyon",
        "plot": "Grafiği çiz",
        "voltage": "Gerilim (V)",
        "current": "Akım (A)",
        "resistance": "Direnç (Ω)",
        "power": "Güç",
        "points": "Rastgele nokta sayısı",
        "run": "Simülasyonu çalıştır",
        "estimate": "Tahmini π değeri",
        "theoretical": "Gerçek π değeri",
        "sphere_intro": "Monte Carlo örneklemesiyle 4 boyutlu birim kürenin hacmini tahmin et.",
        "sphere_estimate": "Tahmini 4B küre hacmi",
        "pokemon_intro": "Varsayımsal bir Pokémon enerji modelini keşfet.",
        "pikachu": "Varsayımsal Pikachu gücü (watt)",
        "bulb": "Ampul gücü (watt)",
        "about_text": "Matematik ve bilimi etkileşimli deneylerle keşfetmek için hazırlanmış bağımsız bir eğitim projesi.",
        "error": "Lütfen geçerli bir ifade gir.",
        "energy": "Bir ampul için gereken güç",
        "count": "Tahmini Pikachu sayısı",
        "heads": "Yazı gelme olasılığı (%)",
    },
    "Français": {
        "home": "Accueil",
        "calculator": "Calculatrice",
        "functions": "Graphiques de fonctions",
        "physics": "Laboratoire de physique",
        "pokemon": "Énergie Pokémon",
        "probability": "Probabilités",
        "montecarlo": "Monte-Carlo π",
        "sphere": "Sphère 4D",
        "about": "À propos",
        "welcome": "Bienvenue dans Tom Lab !",
        "subtitle": "Explorez les mathématiques, la physique et Pokémon.",
        "language": "Langue",
        "level": "Niveau",
        "beginner": "Débutant",
        "intermediate": "Intermédiaire",
        "advanced": "Avancé",
        "expression": "Expression mathématique",
        "calculate": "Calculer",
        "result": "Résultat",
        "function": "Fonction",
        "plot": "Tracer",
        "voltage": "Tension (V)",
        "current": "Courant (A)",
        "resistance": "Résistance (Ω)",
        "power": "Puissance",
        "points": "Nombre de points aléatoires",
        "run": "Lancer la simulation",
        "estimate": "Estimation de π",
        "theoretical": "Valeur réelle de π",
        "sphere_intro": "Estimez le volume d'une sphère unité 4D par Monte-Carlo.",
        "sphere_estimate": "Volume estimé",
        "pokemon_intro": "Explorez un modèle énergétique hypothétique Pokémon.",
        "pikachu": "Puissance hypothétique de Pikachu (watts)",
        "bulb": "Puissance de l'ampoule (watts)",
        "about_text": "Un projet éducatif indépendant consacré aux mathématiques et aux sciences.",
        "error": "Veuillez saisir une expression valide.",
        "energy": "Puissance nécessaire",
        "count": "Nombre estimé de Pikachu",
        "heads": "Probabilité de pile (%)",
    },
    "Español": {
        "home": "Inicio",
        "calculator": "Calculadora",
        "functions": "Funciones",
        "physics": "Laboratorio de física",
        "pokemon": "Energía Pokémon",
        "probability": "Probabilidad",
        "montecarlo": "Monte Carlo π",
        "sphere": "Esfera 4D",
        "about": "Acerca de",
        "welcome": "¡Bienvenido a Tom Lab!",
        "subtitle": "Explora matemáticas, física y experimentos Pokémon.",
        "language": "Idioma",
        "level": "Nivel",
        "beginner": "Principiante",
        "intermediate": "Intermedio",
        "advanced": "Avanzado",
        "expression": "Expresión matemática",
        "calculate": "Calcular",
        "result": "Resultado",
        "function": "Función",
        "plot": "Dibujar gráfica",
        "voltage": "Voltaje (V)",
        "current": "Corriente (A)",
        "resistance": "Resistencia (Ω)",
        "power": "Potencia",
        "points": "Número de puntos aleatorios",
        "run": "Ejecutar simulación",
        "estimate": "Estimación de π",
        "theoretical": "Valor real de π",
        "sphere_intro": "Estima el volumen de una esfera unitaria 4D mediante Monte Carlo.",
        "sphere_estimate": "Volumen estimado",
        "pokemon_intro": "Explora un modelo energético hipotético de Pokémon.",
        "pikachu": "Potencia hipotética de Pikachu (vatios)",
        "bulb": "Potencia de la bombilla (vatios)",
        "about_text": "Un proyecto educativo independiente sobre matemáticas y ciencias.",
        "error": "Introduce una expresión válida.",
        "energy": "Potencia necesaria",
        "count": "Número estimado de Pikachu",
        "heads": "Probabilidad de cara (%)",
    },
    "Deutsch": {
        "home": "Startseite",
        "calculator": "Taschenrechner",
        "functions": "Funktionsgraphen",
        "physics": "Physiklabor",
        "pokemon": "Pokémon-Energie",
        "probability": "Wahrscheinlichkeit",
        "montecarlo": "Monte Carlo π",
        "sphere": "4D-Kugel",
        "about": "Über das Projekt",
        "welcome": "Willkommen bei Tom Lab!",
        "subtitle": "Entdecke Mathematik, Physik und Pokémon-Experimente.",
        "language": "Sprache",
        "level": "Lernniveau",
        "beginner": "Anfänger",
        "intermediate": "Mittelstufe",
        "advanced": "Fortgeschritten",
        "expression": "Mathematischer Ausdruck",
        "calculate": "Berechnen",
        "result": "Ergebnis",
        "function": "Funktion",
        "plot": "Graph zeichnen",
        "voltage": "Spannung (V)",
        "current": "Strom (A)",
        "resistance": "Widerstand (Ω)",
        "power": "Leistung",
        "points": "Anzahl zufälliger Punkte",
        "run": "Simulation starten",
        "estimate": "Geschätzter π-Wert",
        "theoretical": "Tatsächlicher π-Wert",
        "sphere_intro": "Schätze das Volumen einer 4D-Einheitskugel mit Monte Carlo.",
        "sphere_estimate": "Geschätztes Volumen",
        "pokemon_intro": "Erkunde ein hypothetisches Pokémon-Energiemodell.",
        "pikachu": "Hypothetische Pikachu-Leistung (Watt)",
        "bulb": "Glühlampenleistung (Watt)",
        "about_text": "Ein unabhängiges Bildungsprojekt über Mathematik und Naturwissenschaften.",
        "error": "Bitte gib einen gültigen Ausdruck ein.",
        "energy": "Benötigte Leistung",
        "count": "Geschätzte Pikachu-Anzahl",
        "heads": "Wahrscheinlichkeit für Kopf (%)",
    },
}

LANGUAGES = {
    "English": "English",
    "Türkçe": "Türkçe",
    "Français": "Français",
    "Español": "Español",
    "Deutsch": "Deutsch",
}

def tr(key):
    language = st.session_state.get("language_choice", "English")
    return TEXT.get(language, TEXT["English"]).get(
        key, TEXT["English"].get(key, key)
    )

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("⚡ Tom Lab")

language = st.sidebar.selectbox(
    "Language / Dil / Langue",
    list(LANGUAGES.keys()),
    key="language_choice",
)

level = st.sidebar.selectbox(
    tr("level"),
    [tr("beginner"), tr("intermediate"), tr("advanced")],
)

pages = [
    tr("home"),
    tr("calculator"),
    tr("functions"),
    tr("physics"),
    tr("pokemon"),
    tr("probability"),
    tr("montecarlo"),
    tr("sphere"),
    tr("about"),
]

page = st.sidebar.radio(tr("home") + " / Navigation", pages)

# -----------------------------
# SAFE CALCULATOR
# -----------------------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "abs": abs,
}

def safe_eval(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")
            return OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](evaluate(node.operand))
        if isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in FUNCTIONS and len(node.args) == 1:
                return FUNCTIONS[name](evaluate(node.args[0]))
        raise ValueError("Unsupported expression")

    result = evaluate(tree)
    if not math.isfinite(float(result)):
        raise ValueError("Result is not finite")
    return result

# -----------------------------
# PAGE ROUTES
# -----------------------------

if page == tr("home"):
    st.title("⚡ " + tr("welcome"))
    st.subheader(tr("subtitle"))
    st.success("The app is running. Choose a lab from the sidebar.")
    st.markdown("""
    ### 🔬 Explore
    - Mathematics and graphs
    - Physics and electricity
    - Pokémon-inspired energy models
    - Probability simulations
    - Monte Carlo estimation of π
    - Four-dimensional geometry
    """)
    st.info(
        "Tom Lab is an independent educational project. "
        "It is not an official Professor Tom Crawford project."
    )

elif page == tr("calculator"):
    st.title("🧮 " + tr("calculator"))
    expression = st.text_input(
        tr("expression"),
        value="50 * 3 + sqrt(400)",
    )
    if st.button(tr("calculate")):
        try:
            st.metric(tr("result"), f"{safe_eval(expression):,.8g}")
        except Exception:
            st.error(tr("error"))
    st.caption("Supported: +, -, *, /, **, sqrt(), sin(), cos(), tan(), log(), pi, e")

elif page == tr("functions"):
    st.title("📈 " + tr("functions"))
    st.write("Plot a mathematical function of x.")
    function = st.selectbox(
        tr("function"),
        ["x**2", "x**3", "sin(x)", "cos(x)", "sqrt(abs(x))", "exp(x)"],
    )
    x = np.linspace(-5, 5, 400)
    if function == "x**2":
        y = x**2
    elif function == "x**3":
        y = x**3
    elif function == "sin(x)":
        y = np.sin(x)
    elif function == "cos(x)":
        y = np.cos(x)
    elif function == "sqrt(abs(x))":
        y = np.sqrt(np.abs(x))
    else:
        y = np.exp(np.clip(x, -20, 20))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

elif page == tr("physics"):
    st.title("⚡ " + tr("physics"))
    voltage = st.slider(tr("voltage"), 0.0, 240.0, 12.0)
    resistance = st.slider(tr("resistance"), 1.0, 1000.0, 4.0)
    current = voltage / resistance
    power = voltage * current
    c1, c2 = st.columns(2)
    c1.metric(tr("current"), f"{current:.3f} A")
    c2.metric(tr("power"), f"{power:.3f} W")
    st.latex(r"I=\frac{V}{R}")
    st.latex(r"P=VI")

elif page == tr("pokemon"):
    st.title("⚡ " + tr("pokemon"))
    st.write(tr("pokemon_intro"))
    bulb = st.slider(tr("bulb"), 1, 200, 10)
    pikachu = st.slider(tr("pikachu"), 1, 1000, 100)
    count = math.ceil(bulb / pikachu)
    c1, c2 = st.columns(2)
    c1.metric(tr("energy"), f"{bulb} W")
    c2.metric(tr("count"), str(count))
    st.caption(
        "These values are illustrative assumptions, not real Pokémon measurements."
    )
    st.progress(min(1.0, count / max(1, count)))

elif page == tr("probability"):
    st.title("🎲 " + tr("probability"))
    probability = st.slider(tr("heads"), 0, 100, 50)
    trials = st.slider("Number of trials", 10, 10000, 1000, step=10)
    rng = np.random.default_rng()
    outcomes = rng.random(trials) < probability / 100
    estimated = 100 * np.mean(outcomes)
    c1, c2 = st.columns(2)
    c1.metric("Theoretical probability", f"{probability}%")
    c2.metric("Simulated probability", f"{estimated:.2f}%")
    fig, ax = plt.subplots()
    ax.bar(["Heads", "Tails"], [np.sum(outcomes), trials - np.sum(outcomes)])
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close(fig)

elif page == tr("montecarlo"):
    st.title("🎯 " + tr("montecarlo"))
    st.write("Estimate π using random points inside a square.")
    n = st.slider(tr("points"), 100, 20000, 3000, step=100)
    seed = st.number_input("Random seed", 0, 999999, 42)
    if st.button(tr("run"), key="run_pi"):
        rng = np.random.default_rng(int(seed))
        x = rng.uniform(-1, 1, n)
        y = rng.uniform(-1, 1, n)
        mask = x*x + y*y <= 1
        estimate = 4 * np.mean(mask)
        st.metric(tr("estimate"), f"{estimate:.6f}")
        st.metric(tr("theoretical"), f"{math.pi:.6f}")
        fig, ax = plt.subplots()
        ax.scatter(x[mask], y[mask], s=5, label="Inside circle")
        ax.scatter(x[~mask], y[~mask], s=5, label="Outside circle")
        circle = plt.Circle((0, 0), 1, fill=False)
        ax.add_patch(circle)
        ax.set_aspect("equal")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.caption("Choose the number of points and run the simulation.")

elif page == tr("sphere"):
    st.title("🌐 " + tr("sphere"))
    st.write(tr("sphere_intro"))
    n = st.slider("Number of 4D samples", 1000, 100000, 20000, step=1000)
    seed = st.number_input("Random seed", 0, 999999, 42, key="sphere_seed")
    if st.button(tr("run"), key="run_sphere"):
        rng = np.random.default_rng(int(seed))
        points = rng.uniform(-1, 1, (n, 4))
        inside = np.sum(points**2, axis=1) <= 1
        estimate = 16 * np.mean(inside)
        st.metric(tr("sphere_estimate"), f"{estimate:.5f}")
        st.metric("Theoretical value (π² / 2)", f"{math.pi**2 / 2:.5f}")
        fig, ax = plt.subplots()
        ax.scatter(points[inside, 0], points[inside, 1], s=3, label="Inside")
        ax.scatter(points[~inside, 0], points[~inside, 1], s=3, label="Outside")
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.set_title("Projection of 4D samples onto the first two coordinates")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

elif page == tr("about"):
    st.title("ℹ️ " + tr("about"))
    st.write(tr("about_text"))
    st.markdown("""
    **Project features**
    - Interactive mathematics
    - Physics simulations
    - Pokémon-inspired models
    - Probability experiments
    - Monte Carlo methods
    - Four-dimensional geometry
    """)
    st.info(
        "This is an independent fan-made educational project. "
        "It is not affiliated with or endorsed by Professor Tom Crawford."
    )

else:
    st.title("⚡ Tom Lab")
    st.warning("The selected page could not be found.")
