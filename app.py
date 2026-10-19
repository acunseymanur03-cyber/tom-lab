import ast
import math
import operator

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# =====================================================
# TOM LAB: POKEMON SCIENCE UNIVERSE
# =====================================================

st.set_page_config(
    page_title="Tom Lab | Pokémon Science Universe",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------- SESSION STATE ------------------

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "completed" not in st.session_state:
    st.session_state.completed = []

if "history" not in st.session_state:
    st.session_state.history = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_pi" not in st.session_state:
    st.session_state.last_pi = None

# --------------------- TRANSLATIONS -------------------

TEXT = {
    "English": {
        "home": "🌌 Command Center",
        "math": "🧮 Math Arcade",
        "functions": "📈 Function Lab",
        "physics": "⚡ Physics Lab",
        "pokemon": "🐉 Pokémon Energy",
        "battle": "🎲 Probability Arena",
        "pi": "🎯 Monte Carlo π",
        "sphere": "🌐 4D Universe",
        "about": "🔬 About Tom Lab",
        "welcome": "WELCOME TO TOM LAB",
        "subtitle": "Where mathematics becomes an adventure.",
        "level": "Explorer level",
        "xp": "Experience points",
        "missions": "Completed missions",
        "choose": "Choose your next experiment",
        "calculate": "Calculate",
        "expression": "Mathematical expression",
        "result": "Result",
        "run": "RUN EXPERIMENT",
        "points": "Random points",
        "estimate": "Estimated π",
        "actual": "Actual π",
        "voltage": "Voltage (V)",
        "resistance": "Resistance (Ω)",
        "current": "Current",
        "power": "Power",
        "bulb": "Light bulb power (W)",
        "pikachu": "Hypothetical Pikachu power (W)",
        "count": "Pikachu needed",
        "function": "Choose a function",
        "language": "Language",
        "description": "Experiment, discover, and earn XP!",
    },
    "Türkçe": {
        "home": "🌌 Komuta Merkezi",
        "math": "🧮 Matematik Arenası",
        "functions": "📈 Fonksiyon Laboratuvarı",
        "physics": "⚡ Fizik Laboratuvarı",
        "pokemon": "🐉 Pokémon Enerjisi",
        "battle": "🎲 Olasılık Arenası",
        "pi": "🎯 Monte Carlo π",
        "sphere": "🌐 4B Evren",
        "about": "🔬 Tom Lab Hakkında",
        "welcome": "TOM LAB'A HOŞ GELDİN",
        "subtitle": "Matematiğin bir maceraya dönüştüğü yer.",
        "level": "Kaşif seviyesi",
        "xp": "Deneyim puanı",
        "missions": "Tamamlanan görevler",
        "choose": "Yeni deneyini seç",
        "calculate": "Hesapla",
        "expression": "Matematiksel ifade",
        "result": "Sonuç",
        "run": "DENEYİ BAŞLAT",
        "points": "Rastgele nokta sayısı",
        "estimate": "Tahmini π",
        "actual": "Gerçek π",
        "voltage": "Gerilim (V)",
        "resistance": "Direnç (Ω)",
        "current": "Akım",
        "power": "Güç",
        "bulb": "Ampul gücü (W)",
        "pikachu": "Varsayımsal Pikachu gücü (W)",
        "count": "Gereken Pikachu",
        "function": "Fonksiyon seç",
        "language": "Dil",
        "description": "Deney yap, keşfet ve XP kazan!",
    },
}


def t(key):
    lang = st.session_state.language
    return TEXT.get(lang, TEXT["English"]).get(
        key, TEXT["English"].get(key, key)
    )


def award_xp(mission, points=10):
    """Award XP once for each named mission."""
    if mission not in st.session_state.completed:
        st.session_state.completed.append(mission)
        st.session_state.xp += points
        st.toast(f"⭐ +{points} XP! Mission completed!")


# --------------------- DESIGN -------------------------

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@400;600;800&display=swap'
    );

    .stApp {
        background:
          radial-gradient(ellipse at 15% 10%,
              rgba(0, 220, 255, 0.15), transparent 38%),
          radial-gradient(ellipse at 85% 20%,
              rgba(150, 60, 255, 0.18), transparent 40%),
          radial-gradient(ellipse at 50% 100%,
              rgba(255, 190, 0, 0.09), transparent 40%),
          #080b18;
        color: #f5f7ff;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.4px;
    }

    [data-testid="stSidebar"] {
        background:
          linear-gradient(180deg, #10182c, #080b18);
        border-right: 1px solid rgba(0, 220, 255, 0.35);
    }

    [data-testid="stMetric"] {
        background: rgba(20, 29, 54, 0.8);
        border: 1px solid rgba(0, 220, 255, 0.35);
        border-radius: 15px;
        padding: 16px;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.07);
    }

    .hero {
        padding: 32px 20px;
        text-align: center;
        border-radius: 24px;
        background:
          linear-gradient(135deg,
            rgba(0, 225, 255, 0.13),
            rgba(140, 60, 255, 0.19),
            rgba(255, 200, 0, 0.08));
        border: 1px solid rgba(0, 220, 255, 0.5);
        box-shadow: 0 0 28px rgba(0, 200, 255, 0.1);
        margin-bottom: 24px;
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(27px, 5vw, 52px);
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(0, 225, 255, 0.6);
    }

    .hero-subtitle {
        font-size: 18px;
        color: #b7d9ff;
    }

    .pokemon-banner {
        text-align: center;
        font-size: clamp(35px, 6vw, 70px);
        padding: 12px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-9px); }
    }

    .mission-card {
        background: rgba(17, 28, 52, 0.85);
        padding: 18px;
        border-radius: 17px;
        border: 1px solid rgba(135, 110, 255, 0.4);
        min-height: 120px;
        margin-bottom: 10px;
    }

    .small-label {
        color: #9fb9e8;
        font-size: 13px;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #00d9ff;
        background: linear-gradient(110deg, #123b65, #452276);
        color: white;
        font-weight: 700;
        min-height: 44px;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        border-color: #ffe066;
        color: #ffe066;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.25);
    }

    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #00d9ff, #b76bff, #ffe066);
    }

    .footer {
        text-align: center;
        color: #8b9abd;
        padding: 25px;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------- SAFE CALCULATOR ----------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}

FUNCS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "abs": abs,
}


def safe_eval(expression):
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        if isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e

        if isinstance(node, ast.BinOp):
            if type(node.op) not in OPS:
                raise ValueError("Unsupported operator")

            left = visit(node.left)
            right = visit(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")

            return OPS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in OPS:
                raise ValueError("Unsupported unary operator")
            return OPS[type(node.op)](visit(node.operand))

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in FUNCS and len(node.args) == 1:
                return FUNCS[name](visit(node.args[0]))

        raise ValueError("Unsupported expression")

    result = visit(tree)

    if not math.isfinite(float(result)):
        raise ValueError("Non-finite result")

    return result


# --------------------- SIDEBAR ------------------------

st.sidebar.markdown("## ⚡ TOM LAB")

st.sidebar.selectbox(
    t("language"),
    ["English", "Türkçe"],
    key="language",
)

pages = [
    t("home"),
    t("math"),
    t("functions"),
    t("physics"),
    t("pokemon"),
    t("battle"),
    t("pi"),
    t("sphere"),
    t("about"),
]

page = st.sidebar.radio("🚀 Navigation", pages)

xp = st.session_state.xp
level_number = xp // 100 + 1
progress = (xp % 100) / 100

st.sidebar.markdown("---")
st.sidebar.metric("⭐ XP", xp)
st.sidebar.metric("🏆 Level", level_number)
st.sidebar.progress(progress)
st.sidebar.caption(
    f"{100 - (xp % 100)} XP to the next level"
)
st.sidebar.caption(
    f"Completed missions: {len(st.session_state.completed)}"
)


# --------------------- HOME ---------------------------

if page == t("home"):

    st.markdown(
        f"""
        <div class="hero">
          <div class="pokemon-banner">⚡ 🐉 🔥 🌌 💎</div>
          <div class="hero-title">{t("welcome")}</div>
          <p class="hero-subtitle">{t("subtitle")}</p>
          <p>{t("description")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("⭐ Experience", st.session_state.xp)
    c2.metric("🏆 Explorer level", level_number)
    c3.metric("✅ Missions", len(st.session_state.completed))

    st.markdown("## 🚀 " + t("choose"))

    cards = [
        ("🧮", t("math"), "Solve expressions and earn XP."),
        ("⚡", t("physics"), "Explore electricity and energy."),
        ("🐉", t("pokemon"), "Build your own energy experiment."),
        ("🎲", t("battle"), "Discover probability through battles."),
        ("🎯", t("pi"), "Estimate π with random points."),
        ("🌐", t("sphere"), "Explore a four-dimensional sphere."),
    ]

    for start in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, card in zip(cols, cards[start:start + 3]):
            emoji, title, description = card
            with col:
                st.markdown(
                    f"""
                    <div class="mission-card">
                    <h2>{emoji}</h2>
                    <b>{title}</b><br>
                    <span class="small-label">{description}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("## 🎯 Daily challenge")

    st.write(
        "Estimate π using a random simulation. "
        "Can you get within 0.05 of the real value?"
    )

    if st.button("🚀 Start a new adventure"):
        st.session_state["home_hint"] = True
        st.rerun()

    if st.session_state.get("home_hint"):
        st.success("Choose Monte Carlo π in the sidebar to begin!")


# --------------------- MATH ARCADE --------------------

elif page == t("math"):

    st.title(t("math"))
    st.write("🧠 Solve the challenge to earn 10 XP!")

    expression = st.text_input(
        t("expression"),
        value="50 * 3 + sqrt(400)",
    )

    if st.button("✨ Calculate", key="calc"):
        try:
            answer = safe_eval(expression)
            st.success(f"🎉 {t('result')}: {answer:,.8g}")
            award_xp("math_calculator", 10)
            st.session_state.history.append(
                f"{expression} = {answer}"
            )
        except Exception:
            st.error("That expression is not supported. Try another.")

    st.markdown("### ⚡ Quick challenges")

    challenges = [
        ("What is 12²?", "144"),
        ("What is √225?", "15"),
        ("What is 7 × 8?", "56"),
    ]

    choice = st.selectbox(
        "Choose a challenge",
        [c[0] for c in challenges],
    )

    answer = st.text_input("Your answer", key="math_answer")

    if st.button("Check answer", key="check_math"):
        correct = dict(challenges)[choice]

        if answer.strip() == correct:
            st.success("Correct! +10 XP 🌟")
            award_xp("challenge_" + choice, 10)
        else:
            st.warning("Not quite. Try again!")

    if st.session_state.history:
        with st.expander("📓 Your calculation history"):
            for item in reversed(st.session_state.history[-10:]):
                st.write(item)


# --------------------- FUNCTION LAB -------------------

elif page == t("functions"):

    st.title(t("functions"))
    st.write("Change the function and watch its shape transform.")

    function = st.selectbox(
        t("function"),
        [
            "x²",
            "x³",
            "sin(x)",
            "cos(x)",
            "eˣ",
            "√|x|",
        ],
    )

    limit = st.slider("Graph range", 2, 20, 5)

    x = np.linspace(-limit, limit, 500)

    if function == "x²":
        y = x**2
    elif function == "x³":
        y = x**3
    elif function == "sin(x)":
        y = np.sin(x)
    elif function == "cos(x)":
        y = np.cos(x)
    elif function == "eˣ":
        y = np.exp(np.clip(x, -10, 10))
    else:
        y = np.sqrt(np.abs(x))

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("#10182c")
    ax.plot(x, y, linewidth=2)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.2)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(function)
    st.pyplot(fig)
    plt.close(fig)

    if st.button("🏆 Complete graph mission"):
        award_xp("function_graph", 10)


# --------------------- PHYSICS LAB --------------------

elif page == t("physics"):

    st.title(t("physics"))
    st.write("⚡ Build a virtual circuit.")

    voltage = st.slider(t("voltage"), 0.0, 240.0, 12.0)
    resistance = st.slider(t("resistance"), 1.0, 1000.0, 4.0)

    current = voltage / resistance
    power = voltage * current

    c1, c2, c3 = st.columns(3)
    c1.metric(t("current"), f"{current:.3f} A")
    c2.metric(t("power"), f"{power:.2f} W")
    c3.metric("Energy in 10 s", f"{power * 10:.1f} J")

    st.latex(r"I = \frac{V}{R}")
    st.latex(r"P = VI")
    st.latex(r"E = Pt")

    st.info(
        "Try increasing voltage or changing resistance. "
        "Observe how current and power respond."
    )

    if st.button("⚡ Complete physics mission"):
        award_xp("physics_circuit", 10)


# --------------------- POKEMON ENERGY -----------------

elif page == t("pokemon"):

    st.title(t("pokemon"))
    st.markdown(
        '<div class="pokemon-banner">⚡ 🐭 🔥 🐉</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Imagine a fictional Pokémon power system. "
        "The values below are adjustable assumptions, not official measurements."
    )

    pokemon = st.selectbox(
        "Choose your Pokémon",
        ["Pikachu ⚡", "Charizard 🔥", "Eevee ✨", "Gengar 👻"],
    )

    bulb = st.slider(t("bulb"), 1, 200, 10)
    power_per_pokemon = st.slider(
        t("pikachu"), 1, 1000, 100
    )

    count = math.ceil(bulb / power_per_pokemon)

    c1, c2 = st.columns(2)
    c1.metric("💡 Bulb power", f"{bulb} W")
    c2.metric("🐾 Pokémon needed", count)

    st.progress(min(1.0, power_per_pokemon / max(1, bulb)))

    st.markdown("### 🔬 The science")

    st.latex(
        r"\text{Number needed} = "
        r"\left\lceil \frac{P_{\text{bulb}}}"
        r"{P_{\text{Pokémon}}} \right\rceil"
    )

    st.write(
        f"Under these assumptions, {count} {pokemon} "
        f"would provide enough power for the bulb."
    )

    if st.button("🌟 Complete energy mission"):
        award_xp("pokemon_energy", 15)


# --------------------- PROBABILITY ARENA --------------

elif page == t("battle"):

    st.title(t("battle"))
    st.write(
        "Can you predict the outcome? Run a probability experiment."
    )

    probability = st.slider(
        "Probability of success (%)",
        0, 100, 50,
    )

    trials = st.slider(
        "Number of attempts",
        10, 10000, 1000, step=10,
    )

    seed = st.number_input(
        "Random seed",
        0, 999999, 42,
        key="battle_seed",
    )

    if st.button("🎲 Run probability experiment"):
        rng = np.random.default_rng(int(seed))
        outcomes = rng.random(trials) < probability / 100
        successes = int(np.sum(outcomes))
        observed = successes / trials * 100

        c1, c2 = st.columns(2)
        c1.metric("Expected success rate", f"{probability}%")
        c2.metric("Observed success rate", f"{observed:.2f}%")

        fig, ax = plt.subplots()
        ax.bar(
            ["Success", "Failure"],
            [successes, trials - successes],
        )
        ax.set_ylabel("Number of outcomes")
        ax.set_title("Simulation results")
        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "Random experiments vary. More trials often give a "
            "result closer to the theoretical probability."
        )

        award_xp("probability_experiment", 15)


# --------------------- MONTE CARLO PI -----------------

elif page == t("pi"):

    st.title(t("pi"))
    st.write(
        "Estimate π by throwing random points into a square "
        "containing a circle."
    )

    n = st.slider(t("points"), 100, 20000, 3000, step=100)

    seed = st.number_input(
        "Random seed",
        0, 999999, 42,
        key="pi_seed",
    )

    if st.button(t("run"), key="run_pi"):
        rng = np.random.default_rng(int(seed))

        x = rng.uniform(-1, 1, n)
        y = rng.uniform(-1, 1, n)

        mask = x**2 + y**2 <= 1
        estimate = 4 * np.mean(mask)

        st.session_state.last_pi = estimate

        c1, c2, c3 = st.columns(3)
        c1.metric(t("estimate"), f"{estimate:.6f}")
        c2.metric(t("actual"), f"{math.pi:.6f}")
        c3.metric("Absolute error", f"{abs(estimate - math.pi):.6f}")

        fig, ax = plt.subplots()
        ax.set_facecolor("#10182c")
        ax.scatter(x[mask], y[mask], s=5, label="Inside")
        ax.scatter(x[~mask], y[~mask], s=5, label="Outside")

        circle = plt.Circle(
            (0, 0), 1, fill=False, linewidth=2
        )
        ax.add_patch(circle)
        ax.set_aspect("equal")
        ax.set_title("Random points and the unit circle")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.latex(
            r"\pi \approx 4 \times "
            r"\frac{\text{points inside circle}}"
            r"{\text{total points}}"
        )

        award_xp("monte_carlo_pi", 20)


# --------------------- 4D UNIVERSE --------------------

elif page == t("sphere"):

    st.title(t("sphere"))
    st.write(
        "Explore a four-dimensional unit sphere using random samples. "
        "Its volume can be estimated without directly visualizing "
        "all four dimensions."
    )

    n = st.slider(
        "Number of samples",
        1000, 50000, 10000, step=1000,
    )

    seed = st.number_input(
        "Random seed",
        0, 999999, 42,
        key="sphere_seed",
    )

    if st.button("🌌 Explore 4D space"):
        rng = np.random.default_rng(int(seed))

        points = rng.uniform(-1, 1, (n, 4))
        mask = np.sum(points**2, axis=1) <= 1

        # The 4D bounding hypercube has volume 2^4 = 16.
        estimate = 16 * np.mean(mask)
        actual = math.pi**2 / 2

        c1, c2, c3 = st.columns(3)
        c1.metric("Estimated volume", f"{estimate:.5f}")
        c2.metric("Theoretical volume", f"{actual:.5f}")
        c3.metric("Absolute error", f"{abs(estimate - actual):.5f}")

        fig, ax = plt.subplots()
        inside = points[mask]
        outside = points[~mask]

        ax.scatter(
            outside[:, 0], outside[:, 1],
            s=3, alpha=0.2, label="Outside",
        )
        ax.scatter(
            inside[:, 0], inside[:, 1],
            s=4, alpha=0.6, label="Inside",
        )

        ax.set_xlabel("Coordinate 1")
        ax.set_ylabel("Coordinate 2")
        ax.set_title("2D projection of 4D random samples")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.latex(r"V_4 = \frac{\pi^2}{2}")

        st.info(
            "The plot shows only the first two coordinates of each "
            "sample. The calculation uses all four coordinates."
        )

        award_xp("four_dimensional_geometry", 20)


# --------------------- ABOUT --------------------------

elif page == t("about"):

    st.title(t("about"))

    st.markdown(
        """
        ## 🌌 Mathematics is an adventure

        Tom Lab is an independent educational project combining:

        - 🧮 Mathematics
        - ⚡ Physics
        - 🐉 Pokémon-inspired models
        - 🎲 Probability
        - 🎯 Monte Carlo methods
        - 🌐 Higher-dimensional geometry

        The goal is to make difficult ideas more interactive,
        visual, and enjoyable.

        This is an independent fan-made project. It is not an
        official Professor Tom Crawford project and is not
        endorsed by him.
        """
    )

    st.markdown("### 🏆 Your achievements")

    if st.session_state.completed:
        for mission in st.session_state.completed:
            st.write(f"✅ {mission}")
    else:
        st.info("Complete your first experiment to unlock an achievement!")

    st.metric("Total XP", st.session_state.xp)


# --------------------- FOOTER -------------------------

st.markdown(
    """
    <div class="footer">
      ⚡ TOM LAB · POKÉMON SCIENCE UNIVERSE<br>
      Learn. Experiment. Discover.
    </div>
    """,
    unsafe_allow_html=True,
)
