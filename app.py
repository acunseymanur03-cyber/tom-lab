import ast
import math
import operator

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# =====================================================
# TOM LAB 6.0
# Interactive Mathematics & Science Learning Universe
# =====================================================

st.set_page_config(
    page_title="Tom Lab | Learn by Experimenting",
    page_icon="⚡",
    layout="wide",
)

# ---------------- SESSION STATE ----------------

if "language" not in st.session_state:
    st.session_state.language = "English"

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "completed" not in st.session_state:
    st.session_state.completed = []

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- TRANSLATIONS ----------------

TEXT = {
    "English": {
        "home": "🌌 Command Center",
        "math": "🧮 Math Arcade",
        "functions": "📈 Function Lab",
        "physics": "⚡ Physics Lab",
        "pokemon": "🐉 Pokémon Energy",
        "probability": "🎲 Probability Arena",
        "pi": "🎯 Monte Carlo π",
        "sphere": "🌐 4D Universe",
        "about": "🔬 About",
        "language": "Language",
        "welcome": "WELCOME TO TOM LAB",
        "subtitle": "See mathematics. Understand it. Experiment with it.",
        "xp": "Experience points",
        "level": "Explorer level",
        "missions": "Completed missions",
        "expression": "Mathematical expression",
        "calculate": "Calculate and explain",
        "result": "Result",
        "run": "RUN EXPERIMENT",
        "points": "Number of random points",
        "voltage": "Voltage (V)",
        "resistance": "Resistance (Ω)",
        "bulb": "Bulb power (W)",
        "pikachu": "Hypothetical Pokémon power (W)",
        "function": "Choose a function",
        "steps": "🧠 How is the result calculated?",
        "try": "🎯 Your turn",
        "correct": "Correct! You have understood the idea.",
        "error": "Please enter a valid mathematical expression.",
    },
    "Türkçe": {
        "home": "🌌 Komuta Merkezi",
        "math": "🧮 Matematik Arenası",
        "functions": "📈 Fonksiyon Laboratuvarı",
        "physics": "⚡ Fizik Laboratuvarı",
        "pokemon": "🐉 Pokémon Enerjisi",
        "probability": "🎲 Olasılık Arenası",
        "pi": "🎯 Monte Carlo π",
        "sphere": "🌐 4B Evren",
        "about": "🔬 Hakkında",
        "language": "Dil",
        "welcome": "TOM LAB'A HOŞ GELDİN",
        "subtitle": "Matematiği gör. Anla. Deneyerek keşfet.",
        "xp": "Deneyim puanı",
        "level": "Kaşif seviyesi",
        "missions": "Tamamlanan görevler",
        "expression": "Matematiksel ifade",
        "calculate": "Hesapla ve açıkla",
        "result": "Sonuç",
        "run": "DENEYİ BAŞLAT",
        "points": "Rastgele nokta sayısı",
        "voltage": "Gerilim (V)",
        "resistance": "Direnç (Ω)",
        "bulb": "Ampul gücü (W)",
        "pikachu": "Varsayımsal Pokémon gücü (W)",
        "function": "Fonksiyon seç",
        "steps": "🧠 Sonuç nasıl hesaplanıyor?",
        "try": "🎯 Şimdi sıra sende",
        "correct": "Doğru! Mantığı anlamışsın.",
        "error": "Lütfen geçerli bir matematiksel ifade gir.",
    },
}


def t(key):
    lang = st.session_state.get("language", "English")
    return TEXT.get(lang, TEXT["English"]).get(
        key, TEXT["English"].get(key, key)
    )


def award_xp(mission, points=10):
    if mission not in st.session_state.completed:
        st.session_state.completed.append(mission)
        st.session_state.xp += points
        st.toast(f"⭐ +{points} XP!")


# ---------------- DESIGN ----------------

st.markdown("""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&display=swap'
);

.stApp {
    background:
      radial-gradient(ellipse at 10% 10%,
      rgba(0,220,255,.15), transparent 38%),
      radial-gradient(ellipse at 90% 20%,
      rgba(145,65,255,.17), transparent 40%),
      #080b18;
    color: #f5f7ff;
}

h1, h2, h3 {
    font-family: Orbitron, sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#111a32,#080b18);
    border-right: 1px solid #164d72;
}

[data-testid="stMetric"] {
    background: rgba(20,32,58,.8);
    border: 1px solid rgba(0,220,255,.35);
    border-radius: 15px;
    padding: 12px;
}

.hero {
    text-align: center;
    padding: 30px 16px;
    margin-bottom: 20px;
    border-radius: 24px;
    border: 1px solid #247caa;
    background: linear-gradient(
      130deg,
      rgba(0,220,255,.12),
      rgba(120,65,255,.18),
      rgba(255,205,50,.08)
    );
}

.hero h1 {
    text-shadow: 0 0 20px rgba(0,220,255,.5);
}

.lesson {
    padding: 16px;
    margin: 12px 0;
    border-radius: 14px;
    background: rgba(20,32,58,.7);
    border-left: 4px solid #00d9ff;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid #00d9ff;
    background: linear-gradient(110deg,#123b65,#452276);
    color: white;
    font-weight: 700;
    min-height: 42px;
}

.footer {
    text-align: center;
    padding: 24px;
    color: #9baaca;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SAFE CALCULATOR ----------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
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
                raise ValueError("Unsupported operation")

            left = visit(node.left)
            right = visit(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")

            return OPS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in OPS:
                raise ValueError("Unsupported unary operation")
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


# ---------------- SIDEBAR ----------------

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
    t("probability"),
    t("pi"),
    t("sphere"),
    t("about"),
]

page = st.sidebar.radio("🚀 Navigation", pages)

xp = st.session_state.xp
level = xp // 100 + 1

st.sidebar.markdown("---")
st.sidebar.metric("⭐ " + t("xp"), xp)
st.sidebar.metric("🏆 " + t("level"), level)
st.sidebar.progress((xp % 100) / 100)
st.sidebar.caption(
    f"{100 - (xp % 100)} XP to the next level"
)
st.sidebar.caption(
    f"{t('missions')}: {len(st.session_state.completed)}"
)


# =====================================================
# HOME
# =====================================================

if page == t("home"):

    st.markdown(
        f"""
        <div class="hero">
          <div style="font-size:60px">⚡ 🐉 🔥 🌌</div>
          <h1>{t('welcome')}</h1>
          <p>{t('subtitle')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)
    a.metric("⭐ XP", xp)
    b.metric("🏆 Level", level)
    c.metric("✅ Missions", len(st.session_state.completed))

    st.markdown("## 🚀 Choose your adventure")

    cards = [
        ("🧮", t("math"), "Calculate and understand."),
        ("📈", t("functions"), "Discover mathematical patterns."),
        ("⚡", t("physics"), "Experiment with electricity."),
        ("🐉", t("pokemon"), "Build a fictional energy model."),
        ("🎲", t("probability"), "Explore chance and randomness."),
        ("🎯", t("pi"), "Estimate π visually."),
        ("🌐", t("sphere"), "Explore a 4D sphere."),
    ]

    for start in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, card in zip(cols, cards[start:start + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="lesson">
                    <h3>{card[0]} {card[1]}</h3>
                    <p>{card[2]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.info(
        "Learn by experimenting: change values, observe results, "
        "and read the explanation."
    )


# =====================================================
# MATH ARCADE
# =====================================================

elif page == t("math"):

    st.title(t("math"))

    st.markdown("""
    <div class="lesson">
    <b>🧠 The idea</b><br>
    A calculator gives an answer. A mathematician asks why.
    Try an expression, calculate it, and then inspect its structure.
    </div>
    """, unsafe_allow_html=True)

    expression = st.text_input(
        t("expression"),
        value="50 * 3 + sqrt(400)",
    )

    st.caption(
        "Supported: +, -, *, /, **, sqrt(), sin(), cos(), tan(), log(), pi, e"
    )

    if st.button(t("calculate"), key="calculate_math"):
        try:
            result = safe_eval(expression)

            st.success(f"{t('result')}: {result:,.8g}")

            st.markdown(f"### {t('steps')}")

            st.write("**Step 1 — Identify the operations.**")
            st.code(expression)

            st.write(
                "**Step 2 — Follow the order of operations.** "
                "Brackets and functions are evaluated before "
                "multiplication, division, addition and subtraction."
            )

            st.write(
                "**Step 3 — Evaluate the expression.** "
                "The calculator applies the supported mathematical "
                "operations to produce the result."
            )

            st.write(f"**Step 4 — Final result:** `{result:,.8g}`")

            st.caption(
                "Note: these are general solution steps. "
                "For complex expressions, expand the expression into "
                "smaller operations to inspect each intermediate value."
            )

            award_xp("math_calculator", 10)

            st.session_state.history.append(
                f"{expression} = {result}"
            )

        except Exception:
            st.error(t("error"))

    st.markdown("### 🎯 Your turn")

    challenges = {
        "What is 12²?": "144",
        "What is √225?": "15",
        "What is 7 × 8?": "56",
        "What is 2³ + 4?": "12",
    }

    challenge = st.selectbox(
        "Choose a challenge",
        list(challenges.keys()),
    )

    answer = st.text_input("Your answer", key="challenge_answer")

    if st.button("Check answer", key="check_answer"):
        if answer.strip() == challenges[challenge]:
            st.success("Correct! You understood the calculation.")
            award_xp("challenge_" + challenge, 10)
        else:
            st.warning("Try again. Break the problem into smaller steps.")

    if st.session_state.history:
        with st.expander("📓 Calculation history"):
            for item in reversed(st.session_state.history[-10:]):
                st.write(item)


# =====================================================
# FUNCTION LAB
# =====================================================

elif page == t("functions"):

    st.title(t("functions"))

    st.markdown("""
    <div class="lesson">
    <b>🧠 What is a function?</b><br>
    A function takes an input x and produces an output y.
    The graph shows how that output changes as x changes.
    </div>
    """, unsafe_allow_html=True)

    function = st.selectbox(
        t("function"),
        ["x²", "x³", "sin(x)", "cos(x)", "eˣ", "√|x|"],
    )

    limit = st.slider("Explore the x-axis", 2, 15, 5)

    x = np.linspace(-limit, limit, 500)

    if function == "x²":
        y = x**2
        formula = "f(x) = x²"
        explanation = (
            "Each output is the input multiplied by itself. "
            "For example, f(3) = 3² = 9."
        )
    elif function == "x³":
        y = x**3
        formula = "f(x) = x³"
        explanation = (
            "The input is multiplied by itself three times. "
            "Negative inputs produce negative outputs."
        )
    elif function == "sin(x)":
        y = np.sin(x)
        formula = "f(x) = sin(x)"
        explanation = (
            "The sine function oscillates between -1 and 1. "
            "The input angle is measured in radians."
        )
    elif function == "cos(x)":
        y = np.cos(x)
        formula = "f(x) = cos(x)"
        explanation = (
            "Cosine is periodic and oscillates between -1 and 1. "
            "It begins at 1 when x = 0."
        )
    elif function == "eˣ":
        y = np.exp(np.clip(x, -20, 20))
        formula = "f(x) = eˣ"
        explanation = (
            "The exponential function grows rapidly for positive x "
            "and approaches zero as x becomes very negative."
        )
    else:
        y = np.sqrt(np.abs(x))
        formula = "f(x) = √|x|"
        explanation = (
            "Take the absolute value first, then its square root. "
            "This keeps the output real for every real input."
        )

    st.latex(formula)

    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Input x")
    ax.set_ylabel("Output f(x)")
    ax.set_title(formula)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(f"### {t('steps')}")
    st.write("1. Choose an input value x.")
    st.write("2. Apply the rule shown in the formula.")
    st.write("3. The result is the corresponding y-value.")
    st.write("4. Repeat for many x-values to draw the curve.")
    st.info(explanation)

    test_x = st.number_input("Try your own x-value", value=2.0)

    if function == "x²":
        test_y = test_x**2
    elif function == "x³":
        test_y = test_x**3
    elif function == "sin(x)":
        test_y = math.sin(test_x)
    elif function == "cos(x)":
        test_y = math.cos(test_x)
    elif function == "eˣ":
        test_y = math.exp(max(-20, min(20, test_x)))
    else:
        test_y = math.sqrt(abs(test_x))

    st.success(f"f({test_x}) = {test_y:.6f}")

    if st.button("Complete function mission"):
        award_xp("function_lab", 10)


# =====================================================
# PHYSICS LAB
# =====================================================

elif page == t("physics"):

    st.title(t("physics"))

    st.markdown("""
    <div class="lesson">
    <b>⚡ Mission: power the laboratory</b><br>
    Change the voltage and resistance. Observe what happens to
    the electric current and power.
    </div>
    """, unsafe_allow_html=True)

    voltage = st.slider(t("voltage"), 0.0, 240.0, 12.0)
    resistance = st.slider(t("resistance"), 1.0, 1000.0, 4.0)

    current = voltage / resistance
    power = voltage * current

    a, b, c = st.columns(3)
    a.metric("Voltage", f"{voltage:.2f} V")
    b.metric("Current", f"{current:.3f} A")
    c.metric("Power", f"{power:.3f} W")

    st.markdown(f"### {t('steps')}")

    st.write("**Step 1 — Start with Ohm's law.**")
    st.latex(r"I = \frac{V}{R}")

    st.write("**Step 2 — Substitute the selected values.**")
    st.latex(
        rf"I = \frac{{{voltage:.2f}}}{{{resistance:.2f}}}"
    )

    st.write("**Step 3 — Calculate the current.**")
    st.latex(rf"I = {current:.4f}\ \mathrm{{A}}")

    st.write("**Step 4 — Calculate electrical power.**")
    st.latex(r"P = VI")

    st.latex(
        rf"P = {voltage:.2f}\times {current:.4f}"
        rf" = {power:.4f}\ \mathrm{{W}}"
    )

    st.info(
        "For a fixed voltage, increasing resistance reduces current. "
        "Power is calculated here using P = VI for the selected "
        "idealized circuit."
    )

    if st.button("Complete physics mission"):
        award_xp("physics_lab", 10)


# =====================================================
# POKEMON ENERGY LAB
# =====================================================

elif page == t("pokemon"):

    st.title(t("pokemon"))

    st.markdown(
        '<div style="font-size:60px;text-align:center">'
        '⚡ 🐉 🔥 ✨</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Build a fictional Pokémon energy model. "
        "These values are assumptions for a learning exercise, "
        "not official measurements of Pokémon."
    )

    pokemon = st.selectbox(
        "Choose a Pokémon",
        ["Pikachu", "Charizard", "Eevee", "Gengar"],
    )

    bulb = st.slider(t("bulb"), 1, 200, 10)
    pokemon_power = st.slider(
        t("pikachu"), 1, 1000, 100
    )

    count = math.ceil(bulb / pokemon_power)
    supplied = count * pokemon_power

    a, b = st.columns(2)
    a.metric("Bulb power", f"{bulb} W")
    b.metric("Pokémon needed", count)

    st.markdown(f"### {t('steps')}")

    st.write("**Step 1 — Define the model.**")
    st.write(
        f"We assume each {pokemon} can supply "
        f"{pokemon_power} watts."
    )

    st.write("**Step 2 — Divide the required power by one Pokémon's power.**")
    st.latex(
        rf"\frac{{{bulb}\ \mathrm{{W}}}}"
        rf"{{{pokemon_power}\ \mathrm{{W}}}}"
        rf" = {bulb / pokemon_power:.4f}"
    )

    st.write("**Step 3 — Use a whole number of Pokémon.**")
    st.write(
        "Round up, because a fraction of a Pokémon is not allowed "
        "in this simplified model."
    )

    st.latex(
        rf"N = \left\lceil \frac{{{bulb}}}"
        rf"{{{pokemon_power}}} \right\rceil = {count}"
    )

    st.write("**Step 4 — Check the supplied power.**")
    st.write(
        f"{count} × {pokemon_power} W = {supplied} W."
    )

    st.info(
        "Scientific thinking: the mathematics follows from the "
        "assumptions. The assumptions themselves are fictional."
    )

    if st.button("Complete energy mission"):
        award_xp("pokemon_energy", 15)


# =====================================================
# PROBABILITY ARENA
# =====================================================

elif page == t("probability"):

    st.title(t("probability"))

    st.markdown("""
    <div class="lesson">
    <b>🎲 Theory versus experiment</b><br>
    Probability predicts what should happen in the long run.
    A simulation shows what happens in one particular experiment.
    </div>
    """, unsafe_allow_html=True)

    probability = st.slider("Success probability (%)", 0, 100, 50)
    trials = st.slider("Number of trials", 10, 10000, 1000, step=10)

    seed = st.number_input(
        "Random seed", 0, 999999, 42,
        key="probability_seed",
    )

    if st.button("Run probability experiment"):

        rng = np.random.default_rng(int(seed))
        outcomes = rng.random(trials) < probability / 100

        successes = int(np.sum(outcomes))
        failures = trials - successes
        observed = successes / trials * 100

        a, b, c = st.columns(3)
        a.metric("Expected probability", f"{probability}%")
        b.metric("Observed probability", f"{observed:.2f}%")
        c.metric("Successes", successes)

        st.markdown(f"### {t('steps')}")

        st.write("**Step 1 — Convert the percentage to a probability.**")
        st.latex(
            rf"p = \frac{{{probability}}}{{100}}"
            rf" = {probability / 100:.4f}"
        )

        st.write(
            "**Step 2 — Generate a random outcome for each trial.** "
            "Each trial succeeds with probability p."
        )

        st.write("**Step 3 — Count the successful trials.**")
        st.latex(
            rf"\text{{Observed probability}}"
            rf" = \frac{{{successes}}}{{{trials}}}"
            rf" = {successes / trials:.5f}"
        )

        st.write("**Step 4 — Compare theory and experiment.**")
        st.write(
            f"The theoretical probability is {probability}%, "
            f"while this simulation produced {observed:.2f}%."
        )

        fig, ax = plt.subplots()
        ax.bar(["Success", "Failure"], [successes, failures])
        ax.set_ylabel("Number of trials")
        ax.set_title("Simulation results")
        st.pyplot(fig)
        plt.close(fig)

        st.info(
            "The simulated result does not have to equal the "
            "theoretical probability. Random variation is normal; "
            "larger samples often give more stable estimates."
        )

        award_xp("probability_lab", 15)


# =====================================================
# MONTE CARLO PI
# =====================================================

elif page == t("pi"):

    st.title(t("pi"))

    st.markdown("""
    <div class="lesson">
    <b>🎯 The big idea</b><br>
    We can estimate π without measuring a circle's circumference.
    We throw random points into a square and count how many land
    inside a circle drawn within it.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 — Understand the geometry")

    st.write(
        "Imagine a circle of radius 1 inside a square of side length 2."
    )

    st.latex(r"A_{\text{circle}} = \pi r^2 = \pi")
    st.latex(r"A_{\text{square}} = 2\times2 = 4")

    st.write("The fraction of the square covered by the circle is:")

    st.latex(
        r"\frac{A_{\text{circle}}}{A_{\text{square}}}"
        r" = \frac{\pi}{4}"
    )

    st.markdown("### Step 2 — Throw random points")

    n = st.slider(t("points"), 100, 20000, 3000, step=100)

    seed = st.number_input(
        "Random seed", 0, 999999, 42,
        key="pi_seed",
    )

    if st.button(t("run"), key="run_pi"):

        rng = np.random.default_rng(int(seed))

        x = rng.uniform(-1, 1, n)
        y = rng.uniform(-1, 1, n)

        # A point is inside the unit circle if x² + y² <= 1.
        inside_mask = x**2 + y**2 <= 1

        inside = int(np.sum(inside_mask))
        outside = n - inside

        fraction = inside / n
        estimate = 4 * fraction
        error = abs(estimate - math.pi)

        st.markdown("### Step 3 — See the experiment")

        fig, ax = plt.subplots(figsize=(7, 7))

        ax.scatter(
            x[inside_mask],
            y[inside_mask],
            s=7,
            alpha=0.65,
            label=f"Inside circle: {inside}",
        )

        ax.scatter(
            x[~inside_mask],
            y[~inside_mask],
            s=7,
            alpha=0.5,
            label=f"Outside circle: {outside}",
        )

        circle = plt.Circle(
            (0, 0), 1, fill=False, linewidth=2
        )
        ax.add_patch(circle)

        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Monte Carlo estimation of π")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.markdown("### Step 4 — Calculate the estimate")

        a, b, c = st.columns(3)
        a.metric("Points inside", inside)
        b.metric("Total points", n)
        c.metric("Estimated π", f"{estimate:.6f}")

        st.write("First, calculate the fraction of points inside the circle.")

        st.latex(
            rf"\frac{{N_{{\mathrm{{inside}}}}}}"
            rf"{{N_{{\mathrm{{total}}}}}}"
            rf" = \frac{{{inside}}}{{{n}}}"
            rf" = {fraction:.6f}"
        )

        st.write("Next, use the geometric relationship to estimate π.")

        st.latex(
            rf"\pi \approx 4\times"
            rf"\frac{{{inside}}}{{{n}}}"
            rf" = {estimate:.6f}"
        )

        st.write("Finally, compare the estimate with the actual value.")

        st.latex(
            rf"\pi \approx 3.14159265,\qquad"
            rf"\text{{absolute error}} = {error:.6f}"
        )

        st.info(
            "Why does this work? The circle occupies π/4 of the "
            "square's area. With many uniformly distributed random "
            "points, the fraction landing inside the circle tends "
            "to approach π/4."
        )

        st.markdown("### 🎯 Experiment challenge")

        st.write(
            "Run the simulation with 100, 1,000, and 10,000 points. "
            "Compare the estimates and see how the results change."
        )

        award_xp("monte_carlo_pi", 20)


# =====================================================
# 4D SPHERE MONTE CARLO
# =====================================================

elif page == t("sphere"):

    st.title(t("sphere"))

    st.markdown("""
    <div class="lesson">
    <b>🌐 Can we estimate the volume of a shape we cannot directly see?</b><br>
    Yes! Monte Carlo methods also work in higher dimensions.
    We cannot draw a four-dimensional sphere on an ordinary screen,
    but we can sample four-dimensional points and test which ones
    lie inside the sphere.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 — Define the 4D sphere")

    st.write(
        "A point (x₁, x₂, x₃, x₄) lies inside the unit 4D sphere when:"
    )

    st.latex(
        r"x_1^2+x_2^2+x_3^2+x_4^2 \leq 1"
    )

    st.write(
        "We sample points inside a four-dimensional cube whose "
        "coordinates range from -1 to 1."
    )

    st.latex(r"V_{\text{hypercube}} = 2^4 = 16")

    st.markdown("### Step 2 — Choose the sample size")

    n = st.slider(
        "Number of 4D samples",
        1000, 50000, 10000, step=1000,
    )

    seed = st.number_input(
        "Random seed",
        0, 999999, 42,
        key="sphere_seed",
    )

    if st.button("Explore the 4D universe"):

        rng = np.random.default_rng(int(seed))

        points = rng.uniform(-1, 1, size=(n, 4))

        squared_distance = np.sum(points**2, axis=1)
        inside_mask = squared_distance <= 1

        inside = int(np.sum(inside_mask))
        fraction = inside / n

        # The 4D cube has volume 16.
        estimate = 16 * fraction

        # The exact volume of a unit 4D ball is pi² / 2.
        theoretical = math.pi**2 / 2

        error = abs(estimate - theoretical)

        st.markdown("### Step 3 — Visualize a projection")

        st.write(
            "The plot shows only coordinates x₁ and x₂. "
            "The classification still uses all four coordinates."
        )

        fig, ax = plt.subplots(figsize=(7, 7))

        ax.scatter(
            points[~inside_mask, 0],
            points[~inside_mask, 1],
            s=5,
            alpha=0.2,
            label="Outside 4D sphere",
        )

        ax.scatter(
            points[inside_mask, 0],
            points[inside_mask, 1],
            s=5,
            alpha=0.5,
            label="Inside 4D sphere",
        )

        ax.set_xlabel("Coordinate x₁")
        ax.set_ylabel("Coordinate x₂")
        ax.set_title("2D projection of 4D samples")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.markdown("### Step 4 — Estimate the volume")

        a, b, c = st.columns(3)
        a.metric("Points inside", inside)
        b.metric("Estimated volume", f"{estimate:.5f}")
        c.metric("Theoretical volume", f"{theoretical:.5f}")

        st.write("First, calculate the fraction of points inside.")

        st.latex(
            rf"f = \frac{{{inside}}}{{{n}}}"
            rf" = {fraction:.6f}"
        )

        st.write(
            "Next, multiply this fraction by the volume of the "
            "surrounding 4D hypercube."
        )

        st.latex(
            rf"V_{{\mathrm{{estimate}}}}"
            rf" = 16\times\frac{{{inside}}}{{{n}}}"
            rf" = {estimate:.5f}"
        )

        st.write("Compare the estimate with the exact mathematical result.")

        st.latex(
            r"V_4 = \frac{\pi^2}{2}"
        )

        st.latex(
            rf"V_4 \approx {theoretical:.5f},\qquad"
            rf"\text{{absolute error}} = {error:.5f}"
        )

        st.info(
            "The simulation estimates the volume. It will generally "
            "not match the exact value perfectly because it uses a "
            "finite random sample. More samples can improve the "
            "estimate, but do not guarantee that every run is more accurate."
        )

        st.markdown("### 🧠 Why is this interesting?")

        st.write(
            "The same idea works in 2D, 3D, 4D, and higher dimensions: "
            "sample points in a known region, count the fraction "
            "inside the target shape, and multiply by the region's volume."
        )

        award_xp("four_dimensional_sphere", 20)


# =====================================================
# ABOUT
# =====================================================

elif page == t("about"):

    st.title(t("about"))

    st.markdown("""
    ## Learn by experimenting

    Tom Lab is an independent educational project designed to make
    mathematics and science interactive and approachable.

    ### Learning principles

    - **Visualize:** See what the mathematics describes.
    - **Calculate:** Work through the formulas.
    - **Understand:** Read the reasoning behind the result.
    - **Experiment:** Change parameters and compare outcomes.
    - **Reflect:** Think about why the result changes.

    The project includes mathematics, physics, probability,
    Monte Carlo estimation, higher-dimensional geometry, and
    fictional Pokémon-inspired models.

    This is an independent fan-made educational project.
    It is not an official Professor Tom Crawford project and is
    not endorsed by him.
    """)

    st.markdown("### 🏆 Your achievements")

    if st.session_state.completed:
        for mission in st.session_state.completed:
            st.write("✅ " + mission)
    else:
        st.info("Complete an experiment to earn your first achievement!")

    st.metric("Total XP", st.session_state.xp)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
⚡ TOM LAB · LEARN BY EXPERIMENTING<br>
Mathematics is not just something to calculate. It is something to discover.
</div>
""", unsafe_allow_html=True)
