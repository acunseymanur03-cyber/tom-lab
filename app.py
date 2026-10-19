import ast
import math
import operator
import random

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tom Lab | Interactive Maths & Science",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LANGUAGE
# ============================================================

LANGUAGES = {
    "English": {
        "home": "Command Centre",
        "math": "Math Arcade",
        "power": "Pokémon Power Lab",
        "pi": "Monte Carlo π Lab",
        "sphere": "4D Sphere Lab",
        "functions": "Function Lab",
        "physics": "Physics Lab",
        "calculator": "Calculator",
        "about": "About the Project",
        "welcome": "WELCOME TO TOM LAB",
        "subtitle": "Where mathematical ideas become interactive experiments.",
        "mission": "YOUR MISSION",
        "mission_text": (
            "Explore mathematics and physics through simulations, "
            "experiments and step-by-step explanations."
        ),
        "choose": "Choose a laboratory",
        "trials": "Number of random points",
        "run": "Run experiment",
        "result": "Your result",
        "steps": "How does it work?",
        "formula": "Mathematical formula",
        "learn": "What does this mean?",
        "voltage": "Voltage (V)",
        "resistance": "Resistance (Ω)",
        "power_w": "Bulb power (watts)",
        "pokemon_power": "Energy per Pokémon (watts)",
        "calculate": "Calculate",
        "expression": "Enter a mathematical expression",
        "solve": "Calculate expression",
        "question": "Practice question",
        "check": "Check answer",
        "your_answer": "Your answer",
        "correct": "Correct! Well done!",
        "incorrect": "Not quite. Read the explanation and try again.",
        "level": "Researcher level",
        "xp": "Research XP",
        "language": "Language",
        "independent": "Independent educational project",
    },
    "Türkçe": {
        "home": "Kontrol Merkezi",
        "math": "Matematik Arenası",
        "power": "Pokémon Enerji Laboratuvarı",
        "pi": "Monte Carlo π Laboratuvarı",
        "sphere": "4B Küre Laboratuvarı",
        "functions": "Fonksiyon Laboratuvarı",
        "physics": "Fizik Laboratuvarı",
        "calculator": "Hesap Makinesi",
        "about": "Proje Hakkında",
        "welcome": "TOM LAB'E HOŞ GELDİN",
        "subtitle": "Matematiksel fikirlerin etkileşimli deneylere dönüştüğü yer.",
        "mission": "GÖREVİN",
        "mission_text": (
            "Simülasyonlar, deneyler ve adım adım açıklamalarla "
            "matematiği ve fiziği keşfet."
        ),
        "choose": "Bir laboratuvar seç",
        "trials": "Rastgele nokta sayısı",
        "run": "Deneyi başlat",
        "result": "Sonucun",
        "steps": "Bu nasıl çalışıyor?",
        "formula": "Matematiksel formül",
        "learn": "Bu ne anlama geliyor?",
        "voltage": "Gerilim (V)",
        "resistance": "Direnç (Ω)",
        "power_w": "Ampul gücü (watt)",
        "pokemon_power": "Pokémon başına enerji (watt)",
        "calculate": "Hesapla",
        "expression": "Matematiksel bir ifade gir",
        "solve": "İfadeyi hesapla",
        "question": "Alıştırma sorusu",
        "check": "Cevabı kontrol et",
        "your_answer": "Cevabın",
        "correct": "Doğru! Harika iş!",
        "incorrect": "Tam değil. Açıklamayı oku ve tekrar dene.",
        "level": "Araştırmacı seviyesi",
        "xp": "Araştırma puanı",
        "language": "Dil",
        "independent": "Bağımsız eğitim projesi",
    },
}


def t(key):
    language = st.session_state.get("language", "English")
    return LANGUAGES[language].get(key, LANGUAGES["English"].get(key, key))


# ============================================================
# SESSION STATE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "completed" not in st.session_state:
    st.session_state.completed = []

if "last_pi" not in st.session_state:
    st.session_state.last_pi = None


def award_xp(mission, points=10):
    if mission not in st.session_state.completed:
        st.session_state.completed.append(mission)
        st.session_state.xp += points
        st.toast(f"+{points} XP ⚡")


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800'
      '&family=Inter:wght@400;500;600;700&display=swap'
    );

    .stApp {
        background:
            radial-gradient(
                ellipse at top left,
                rgba(0, 190, 255, 0.13),
                transparent 38%
            ),
            radial-gradient(
                ellipse at bottom right,
                rgba(150, 65, 255, 0.12),
                transparent 35%
            ),
            #07111f;
        color: #edf5ff;
    }

    h1, h2, h3 {
        color: #e9f5ff !important;
    }

    .hero {
        padding: 32px 28px;
        border: 1px solid rgba(91, 203, 255, .4);
        border-radius: 22px;
        background: linear-gradient(
            120deg,
            rgba(9, 45, 77, .95),
            rgba(31, 22, 70, .95)
        );
        box-shadow: 0 0 30px rgba(0, 174, 255, .08);
        margin-bottom: 22px;
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(26px, 4vw, 42px);
        font-weight: 800;
        letter-spacing: 1px;
        color: #74e4ff;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.7;
        color: #d1e6ff;
    }

    .lab-card {
        background: rgba(15, 34, 55, .85);
        border: 1px solid rgba(103, 184, 255, .25);
        border-radius: 17px;
        padding: 19px;
        min-height: 150px;
        margin-bottom: 14px;
    }

    .lab-card h3 {
        margin-top: 0;
        color: #75e6ff !important;
    }

    .lab-card p {
        color: #cbd9ed;
        line-height: 1.6;
    }

    .formula-box {
        background: rgba(0, 183, 255, .08);
        border-left: 4px solid #4dd8ff;
        padding: 15px;
        border-radius: 9px;
        margin: 12px 0;
    }

    .small-note {
        color: #a9c1df;
        font-size: 13px;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #42d8ff;
        background: linear-gradient(90deg, #087ca5, #5343a8);
        color: white;
        font-weight: 700;
        min-height: 42px;
    }

    div.stButton > button:hover {
        border-color: #ffffff;
        color: white;
        box-shadow: 0 0 14px rgba(66, 216, 255, .3);
    }

    [data-testid="stMetric"] {
        background: rgba(16, 39, 64, .8);
        border: 1px solid rgba(103, 184, 255, .2);
        border-radius: 13px;
        padding: 12px;
    }

    section[data-testid="stSidebar"] {
        background: #091827;
    }

    hr {
        border-color: rgba(116, 228, 255, .2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER AND NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## ⚡ TOM LAB")

    st.selectbox(
        t("language"),
        ["English", "Türkçe"],
        key="language",
    )

    pages = [
        "home",
        "math",
        "power",
        "pi",
        "sphere",
        "functions",
        "physics",
        "calculator",
        "about",
    ]

    page_labels = [t(p) for p in pages]

    selected_label = st.radio(
        "Navigation",
        page_labels,
        label_visibility="collapsed",
    )

    page = pages[page_labels.index(selected_label)]

    st.divider()

    st.metric(t("xp"), st.session_state.xp)

    level = 1 + st.session_state.xp // 50
    st.markdown(f"**{t('level')}: {level}**")

    st.progress(min((st.session_state.xp % 50) / 50, 1.0))

    st.caption(
        f"{len(st.session_state.completed)} experiments completed"
    )


# ============================================================
# POKÉMON IMAGE HELPER
# ============================================================

def pokemon_image(number, caption, width=130):
    url = (
        "https://raw.githubusercontent.com/"
        f"PokeAPI/sprites/master/sprites/pokemon/{number}.png"
    )
    try:
        st.image(url, width=width, caption=caption)
    except Exception:
        st.markdown(f"### ⚡ {caption}")


# ============================================================
# HOME
# ============================================================

if page == "home":
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">⚡ {t("welcome")}</div>
            <div class="hero-subtitle">{t("subtitle")}</div>
            <hr>
            <h3>{t("mission")}</h3>
            <div class="hero-subtitle">{t("mission_text")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        pokemon_image(25, "Pikachu • Energy", 115)

    with col2:
        pokemon_image(6, "Charizard • Power", 115)

    with col3:
        pokemon_image(150, "Mewtwo • Probability", 115)

    st.subheader(t("choose"))

    cards = [
        (
            "⚡ Pokémon Power",
            "Explore energy, electrical power and estimation.",
        ),
        (
            "🎯 Monte Carlo π",
            "Use random points to estimate a famous constant.",
        ),
        (
            "🌌 4D Sphere",
            "Explore probability and higher-dimensional geometry.",
        ),
        (
            "📈 Function Lab",
            "See how equations become curves.",
        ),
        (
            "🔌 Physics Lab",
            "Experiment with voltage, current and resistance.",
        ),
        (
            "🧠 Math Arcade",
            "Solve problems and earn research XP.",
        ),
    ]

    columns = st.columns(3)

    for i, (title, description) in enumerate(cards):
        with columns[i % 3]:
            st.markdown(
                f"""
                <div class="lab-card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "Research principle: every simulation is a mathematical model. "
        "Check its assumptions before interpreting the result."
    )


# ============================================================
# POKÉMON POWER LAB
# ============================================================

elif page == "power":
    st.title("⚡ Pokémon Power Laboratory")

    st.write(
        "Can a team of Pokémon provide enough energy to power a lightbulb?"
    )

    left, right = st.columns([1, 2])

    with left:
        pokemon_image(25, "Pikachu", 150)

        bulb_watts = st.slider(
            t("power_w"),
            min_value=1,
            max_value=200,
            value=60,
        )

        pokemon_watts = st.slider(
            t("pokemon_power"),
            min_value=1,
            max_value=100,
            value=10,
        )

        if st.button(t("calculate"), key="power_calc"):
            st.session_state.power_result = (
                math.ceil(bulb_watts / pokemon_watts)
            )
            award_xp("power")

    with right:
        result = getattr(st.session_state, "power_result", None)

        if result is not None:
            st.metric("Pokémon needed", result)

            st.markdown(
                f"""
                <div class="formula-box">
                <b>Step 1:</b> Bulb power = {bulb_watts} W<br>
                <b>Step 2:</b> Assumed power per Pokémon = {pokemon_watts} W<br>
                <b>Step 3:</b> Divide {bulb_watts} by {pokemon_watts}.<br>
                <b>Step 4:</b> Round up to a whole Pokémon.<br>
                <b>Result:</b> {result} Pokémon.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.latex(
                rf"N = \left\lceil "
                rf"\frac{{{bulb_watts}}}{{{pokemon_watts}}}"
                rf"\right\rceil = {result}"
            )

        st.warning(
            "This is a fictional educational model. The power assigned "
            "to each Pokémon is an adjustable assumption, not a real "
            "scientific measurement."
        )


# ============================================================
# MONTE CARLO PI LAB
# ============================================================

elif page == "pi":
    st.title("🎯 Monte Carlo π Laboratory")

    st.write(
        "Estimate π by throwing random points into a square "
        "containing a quarter-circle."
    )

    trials = st.slider(
        t("trials"),
        min_value=100,
        max_value=10000,
        value=2000,
        step=100,
    )

    if st.button(t("run"), key="run_pi"):
        rng = np.random.default_rng()

        x = rng.random(trials)
        y = rng.random(trials)

        inside = x**2 + y**2 <= 1
        count_inside = int(np.sum(inside))

        estimate = 4 * count_inside / trials

        st.session_state.last_pi = {
            "estimate": estimate,
            "trials": trials,
            "inside": count_inside,
            "x": x,
            "y": y,
            "inside_mask": inside,
        }

        award_xp("pi")

    data = st.session_state.last_pi

    if data is not None:
        x = data["x"]
        y = data["y"]
        inside = data["inside_mask"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Estimated π", f"{data['estimate']:.6f}")

        with col2:
            st.metric("Actual π", f"{math.pi:.6f}")

        fig, ax = plt.subplots(figsize=(7, 6))

        ax.scatter(
            x[inside],
            y[inside],
            s=8,
            alpha=0.65,
            label="Inside quarter-circle",
        )

        ax.scatter(
            x[~inside],
            y[~inside],
            s=8,
            alpha=0.65,
            label="Outside quarter-circle",
        )

        theta = np.linspace(0, np.pi / 2, 300)

        ax.plot(
            np.cos(theta),
            np.sin(theta),
            linewidth=2,
            label="Quarter-circle boundary",
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Monte Carlo experiment")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.markdown(f"### {t('steps')}")

        st.markdown(
            f"""
            **1. Generate random points**

            Each point has coordinates x and y between 0 and 1.

            **2. Test whether a point is inside the quarter-circle**

            A point is inside when:

            x² + y² ≤ 1

            **3. Find the proportion inside**

            - Total points: {data['trials']}
            - Points inside: {data['inside']}

            **4. Estimate π**

            The area of the quarter-circle is π/4, while the square's
            area is 1. The fraction of random points inside therefore
            approximates π/4.

            Multiply that fraction by 4:

            π ≈ 4 × (inside points / total points)

            **5. Interpret the result**

            Random variation means this estimate may differ from π.
            More points often improve the estimate, but improvement
            is not guaranteed in every individual run.
            """
        )

        st.latex(
            rf"\pi \approx 4 \times "
            rf"\frac{{{data['inside']}}}{{{data['trials']}}}"
            rf" = {data['estimate']:.6f}"
        )

        st.caption(
            f"Absolute error in this run: "
            f"{abs(data['estimate'] - math.pi):.6f}"
        )


# ============================================================
# 4D SPHERE LAB
# ============================================================

elif page == "sphere":
    st.title("🌌 Four-Dimensional Sphere Laboratory")

    st.write(
        "Estimate the volume of a unit sphere in four dimensions "
        "using random sampling."
    )

    st.markdown(
        """
        In 2D, a circle is described by x² + y² ≤ 1.

        In 3D, a sphere is described by x² + y² + z² ≤ 1.

        In 4D, we add another coordinate, w:

        x² + y² + z² + w² ≤ 1.
        """
    )

    trials = st.slider(
        t("trials"),
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        key="sphere_trials",
    )

    if st.button(t("run"), key="run_sphere"):
        rng = np.random.default_rng()

        points = rng.uniform(-1, 1, size=(trials, 4))
        inside = np.sum(points**2, axis=1) <= 1

        count_inside = int(np.sum(inside))

        # The 4D bounding hypercube has side length 2.
        # Its volume is 2^4 = 16.
        estimated_volume = 16 * count_inside / trials

        st.session_state.sphere_result = {
            "trials": trials,
            "inside": count_inside,
            "estimate": estimated_volume,
            "points": points,
            "inside_mask": inside,
        }

        award_xp("sphere")

    result = getattr(st.session_state, "sphere_result", None)

    if result is not None:
        exact_volume = math.pi**2 / 2

        a, b = st.columns(2)

        with a:
            st.metric(
                "Estimated volume",
                f"{result['estimate']:.5f}",
            )

        with b:
            st.metric(
                "Exact volume",
                f"{exact_volume:.5f}",
            )

        points = result["points"]
        inside = result["inside_mask"]

        fig, ax = plt.subplots(figsize=(7, 6))

        ax.scatter(
            points[inside, 0],
            points[inside, 1],
            s=5,
            alpha=0.45,
            label="Inside the 4D sphere",
        )

        ax.scatter(
            points[~inside, 0],
            points[~inside, 1],
            s=5,
            alpha=0.2,
            label="Outside the 4D sphere",
        )

        ax.set_xlabel("x coordinate")
        ax.set_ylabel("y coordinate")
        ax.set_title("2D projection of sampled 4D points")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.markdown(f"### {t('steps')}")

        st.markdown(
            f"""
            **Step 1 — Sample the 4D box**

            Generate points with x, y, z and w between -1 and 1.

            **Step 2 — Check all four coordinates**

            A point is inside when:

            x² + y² + z² + w² ≤ 1

            **Step 3 — Estimate the fraction inside**

            - Total samples: {result['trials']}
            - Samples inside: {result['inside']}

            **Step 4 — Calculate the volume**

            The surrounding 4D box has side length 2, so its volume is:

            2⁴ = 16

            Multiply 16 by the fraction of points inside the sphere.

            **Important:** The graph shows only the x and y coordinates
            of the sampled points. Whether a point is inside the sphere
            is decided using all four coordinates.
            """
        )

        st.latex(
            rf"V \approx 16 \times "
            rf"\frac{{{result['inside']}}}{{{result['trials']}}}"
            rf" = {result['estimate']:.5f}"
        )

        st.latex(r"V_{\text{exact}} = \frac{\pi^2}{2}")

        st.caption(
            "Monte Carlo estimates vary between runs. "
            "Increasing the number of samples often improves accuracy."
        )


# ============================================================
# FUNCTION LAB
# ============================================================

elif page == "functions":
    st.title("📈 Function Laboratory")

    st.write(
        "Change the mathematical function and explore its graph."
    )

    choices = {
        "x²": lambda x: x**2,
        "x³": lambda x: x**3,
        "sin(x)": lambda x: np.sin(x),
        "cos(x)": lambda x: np.cos(x),
        "eˣ": lambda x: np.exp(np.clip(x, -20, 20)),
        "√|x|": lambda x: np.sqrt(np.abs(x)),
    }

    name = st.selectbox("Choose a function", list(choices.keys()))

    x_min = st.slider("Minimum x", -10, -1, -5)
    x_max = st.slider("Maximum x", 1, 10, 5)

    x = np.linspace(x_min, x_max, 500)
    y = choices[name](x)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(x, y, linewidth=2.5)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Graph of f(x) = {name}")
    ax.grid(True, alpha=0.25)

    st.pyplot(fig)
    plt.close(fig)

    st.markdown("### Understanding the graph")

    explanations = {
        "x²": (
            "Squaring a number makes its result non-negative. "
            "The graph is a U-shaped parabola."
        ),
        "x³": (
            "Cubing preserves the sign of x. Negative x values "
            "produce negative y values."
        ),
        "sin(x)": (
            "The sine function oscillates between -1 and 1."
        ),
        "cos(x)": (
            "Cosine also oscillates between -1 and 1, "
            "but its value at x = 0 is 1."
        ),
        "eˣ": (
            "The exponential function grows rapidly for positive x "
            "and approaches zero for very negative x."
        ),
        "√|x|": (
            "The square root is applied to the absolute value, "
            "so the output is defined for every real x."
        ),
    }

    st.info(explanations[name])

    st.markdown("### Try a value")

    value = st.number_input("Enter x", value=2.0)

    st.metric("f(x)", f"{float(choices[name](np.array([value]))[0]):.6f}")

    st.latex(r"y = f(x)")


# ============================================================
# PHYSICS LAB
# ============================================================

elif page == "physics":
    st.title("🔌 Physics Laboratory")

    st.write("Experiment with Ohm's law and electrical power.")

    voltage = st.slider(
        t("voltage"),
        min_value=1,
        max_value=240,
        value=12,
    )

    resistance = st.slider(
        t("resistance"),
        min_value=1,
        max_value=100,
        value=4,
    )

    current = voltage / resistance
    power = voltage * current

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Current", f"{current:.3f} A")

    with c2:
        st.metric("Electrical power", f"{power:.3f} W")

    st.markdown(f"### {t('steps')}")

    st.markdown(
        f"""
        **Step 1 — Write Ohm's law**

        Current equals voltage divided by resistance.

        **Step 2 — Substitute the values**

        Voltage = {voltage} V

        Resistance = {resistance} Ω

        **Step 3 — Calculate current**

        {voltage} ÷ {resistance} = {current:.3f} A

        **Step 4 — Calculate electrical power**

        Power = voltage × current

        {voltage} × {current:.3f} = {power:.3f} W
        """
    )

    st.latex(r"I = \frac{V}{R}")

    st.latex(r"P = VI")


# ============================================================
# MATH ARCADE
# ============================================================

elif page == "math":
    st.title("🧠 Math Arcade")

    st.write(
        "Solve a challenge, understand the reasoning and earn XP."
    )

    questions = [
        {
            "question": "What is 12 × 8?",
            "answer": 96,
            "explanation": (
                "12 × 8 means eight groups of twelve. "
                "10 × 8 = 80 and 2 × 8 = 16. "
                "80 + 16 = 96."
            ),
        },
        {
            "question": "What is 15²?",
            "answer": 225,
            "explanation": (
                "15² means 15 × 15. "
                "15 × 10 = 150 and 15 × 5 = 75. "
                "150 + 75 = 225."
            ),
        },
        {
            "question": "What is √144?",
            "answer": 12,
            "explanation": (
                "The square root of 144 is the positive number "
                "that multiplied by itself gives 144. "
                "12 × 12 = 144."
            ),
        },
        {
            "question": "A 60 W bulb uses 12 V. What current flows?",
            "answer": 5,
            "explanation": (
                "Power P = VI. Rearrange to I = P/V. "
                "Substitute: 60/12 = 5 amperes."
            ),
        },
    ]

    index = st.selectbox(
        "Choose a challenge",
        range(len(questions)),
        format_func=lambda i: f"Challenge {i + 1}",
    )

    q = questions[index]

    st.markdown(
        f"""
        <div class="lab-card">
            <h3>{q['question']}</h3>
            <p>Work it out before revealing the solution.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answer = st.number_input(
        t("your_answer"),
        value=0.0,
        step=1.0,
        key=f"answer_{index}",
    )

    if st.button(t("check"), key=f"check_{index}"):
        if math.isclose(answer, q["answer"], abs_tol=0.0001):
            st.success(t("correct"))
            award_xp(f"math_{index}", 15)
        else:
            st.warning(t("incorrect"))

        st.markdown("### Solution")

        st.write(q["explanation"])

        st.markdown(f"**Answer: {q['answer']}**")


# ============================================================
# SAFE CALCULATOR
# ============================================================

def safe_calculate(expression):
    allowed_binary = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    allowed_unary = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    allowed_functions = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "abs": abs,
    }

    constants = {
        "pi": math.pi,
        "e": math.e,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in allowed_binary:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if op_type is ast.Pow and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            return allowed_binary[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in allowed_unary:
                raise ValueError("Unsupported unary operator.")

            return allowed_unary[op_type](evaluate(node.operand))

        if isinstance(node, ast.Name):
            if node.id in constants:
                return constants[node.id]

            raise ValueError("Unknown name.")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call.")

            name = node.func.id

            if name not in allowed_functions:
                raise ValueError("Function not allowed.")

            if len(node.args) != 1 or node.keywords:
                raise ValueError("Use one argument per function.")

            return allowed_functions[name](evaluate(node.args[0]))

        raise ValueError("Unsupported expression.")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree)

    if isinstance(result, complex):
        raise ValueError("Complex results are not supported.")

    if not math.isfinite(float(result)):
        raise ValueError("The result is not finite.")

    return result


elif_placeholder = None

Önemli: Yukarıdaki kodun sonundaki "elif_placeholder = None" satırından sonra aşağıdaki bölümü de aynı "app.py" dosyasına ekle. Bu bölüm hesap makinesini ve proje hakkında sayfasını tamamlar.

# ============================================================
# CALCULATOR
# ============================================================

if page == "calculator":
    st.title("🧮 Mathematical Calculation Engine")

    st.write(
        "Use arithmetic, powers and selected mathematical functions."
    )

    st.caption(
        "Examples: 50 * 3 + sqrt(400) | sin(pi / 2) | log(e)"
    )

    expression = st.text_input(
        t("expression"),
        value="50 * 3 + sqrt(400)",
    )

    if st.button(t("solve"), key="calculate_expression"):
        try:
            result = safe_calculate(expression)

            st.metric(t("result"), f"{result:.8g}")

            st.markdown("### Calculation notes")

            st.write(
                "The calculator parses the expression and evaluates "
                "the supported operations. Parentheses and operator "
                "precedence determine the order of calculations."
            )

            st.latex(
                r"\text{Result} = "
                + str(result)
            )

            award_xp("calculator")

        except (ValueError, TypeError, SyntaxError, ZeroDivisionError,
                OverflowError) as error:
            st.error(f"Could not calculate this expression: {error}")


# ============================================================
# ABOUT
# ============================================================

elif page == "about":
    st.title("🔬 About Tom Lab")

    st.markdown(
        """
        ## Learning through experiments

        Tom Lab is an independent educational project exploring
        mathematics, physics, probability and scientific modelling.

        It includes interactive experiments, visualizations and
        explanations designed to help learners understand the
        reasoning behind mathematical results.

        ### Educational principles

        - Explain the formula.
        - Show how values are substituted.
        - Visualize the result where possible.
        - Distinguish a mathematical model from a real-world measurement.
        - Encourage experimentation and critical thinking.

        ### A note about the project

        This is an independent fan-made educational project inspired
        by mathematics and science communication. It is not an official
        Professor Tom Crawford project and is not endorsed by him.

        Pokémon characters and names belong to their respective
        rights holders. This project is not affiliated with or
        endorsed by The Pokémon Company or Nintendo.
        """
    )

    st.divider()

    st.markdown(
        """
        **Built with:** Python, Streamlit, NumPy and Matplotlib.

        **Goal:** Make mathematical ideas easier to explore.
        """
        )
