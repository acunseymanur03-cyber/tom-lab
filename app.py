import ast
import math
import operator

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tom Lab | Maths & Science",
    page_icon="⚡",
    layout="wide",
)


# ============================================================
# LANGUAGE
# ============================================================

TEXT = {
    "English": {
        "home": "Command Centre",
        "math": "Math Arcade",
        "power": "Pokémon Power Lab",
        "pi": "Monte Carlo π Lab",
        "sphere": "4D Sphere Lab",
        "functions": "Function Lab",
        "physics": "Physics Lab",
        "calculator": "Calculator",
        "about": "About",
        "language": "Language",
        "xp": "Research XP",
        "level": "Researcher Level",
        "welcome": "WELCOME TO TOM LAB",
        "subtitle": "Where mathematical ideas become interactive experiments.",
        "mission": "YOUR MISSION",
        "mission_text": (
            "Explore mathematics and physics through simulations, "
            "visualisations and step-by-step explanations."
        ),
        "choose": "Choose a laboratory",
        "run": "Run experiment",
        "trials": "Number of random points",
        "calculate": "Calculate",
        "result": "Result",
        "steps": "How does it work?",
        "your_answer": "Your answer",
        "check": "Check answer",
        "correct": "Correct! Well done!",
        "incorrect": "Not quite. Read the explanation and try again.",
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
        "about": "Hakkında",
        "language": "Dil",
        "xp": "Araştırma XP",
        "level": "Araştırmacı Seviyesi",
        "welcome": "TOM LAB'E HOŞ GELDİN",
        "subtitle": "Matematiksel fikirlerin etkileşimli deneylere dönüştüğü yer.",
        "mission": "GÖREVİN",
        "mission_text": (
            "Simülasyonlar, görselleştirmeler ve adım adım açıklamalarla "
            "matematiği ve fiziği keşfet."
        ),
        "choose": "Bir laboratuvar seç",
        "run": "Deneyi başlat",
        "trials": "Rastgele nokta sayısı",
        "calculate": "Hesapla",
        "result": "Sonuç",
        "steps": "Bu nasıl çalışıyor?",
        "your_answer": "Cevabın",
        "check": "Cevabı kontrol et",
        "correct": "Doğru! Harika iş!",
        "incorrect": "Tam değil. Açıklamayı oku ve tekrar dene.",
    },
}


if "language" not in st.session_state:
    st.session_state.language = "English"

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "completed" not in st.session_state:
    st.session_state.completed = set()


def t(key):
    return TEXT[st.session_state.language].get(key, key)


def award_xp(name, points=10):
    if name not in st.session_state.completed:
        st.session_state.completed.add(name)
        st.session_state.xp += points
        st.toast(f"+{points} XP ⚡")


# ============================================================
# CSS
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
                rgba(150, 65, 255, 0.13),
                transparent 35%
            ),
            #07111f;
    }

    .hero {
        padding: 32px;
        border-radius: 22px;
        border: 1px solid rgba(91, 203, 255, .4);
        background:
            linear-gradient(
                120deg,
                rgba(9, 45, 77, .96),
                rgba(31, 22, 70, .96)
            );
        margin-bottom: 25px;
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(28px, 5vw, 44px);
        font-weight: 800;
        color: #74e4ff;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        color: #d1e6ff;
        font-size: 17px;
        line-height: 1.7;
    }

    .lab-card {
        background: rgba(15, 34, 55, .85);
        border: 1px solid rgba(103, 184, 255, .25);
        border-radius: 17px;
        padding: 20px;
        min-height: 145px;
        margin-bottom: 15px;
    }

    .lab-card h3 {
        color: #75e6ff !important;
    }

    .lab-card p {
        color: #cbd9ed;
        line-height: 1.6;
    }

    .formula-box {
        background: rgba(0, 183, 255, .08);
        border-left: 4px solid #4dd8ff;
        padding: 17px;
        border-radius: 9px;
        margin: 15px 0;
        line-height: 1.8;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #42d8ff;
        background: linear-gradient(90deg, #087ca5, #5343a8);
        color: white;
        font-weight: 700;
        min-height: 42px;
    }

    [data-testid="stMetric"] {
        background: rgba(16, 39, 64, .8);
        border: 1px solid rgba(103, 184, 255, .2);
        border-radius: 13px;
    }

    section[data-testid="stSidebar"] {
        background: #091827;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# ⚡ TOM LAB")

    st.selectbox(
        t("language"),
        ["English", "Türkçe"],
        key="language",
    )

    page_keys = [
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

    page_labels = [t(x) for x in page_keys]

    selected = st.radio(
        "Navigation",
        page_labels,
        label_visibility="collapsed",
    )

    page = page_keys[page_labels.index(selected)]

    st.divider()

    st.metric(t("xp"), st.session_state.xp)

    level = 1 + st.session_state.xp // 50

    st.markdown(
        f"**{t('level')}: {level}**"
    )

    st.progress(
        min((st.session_state.xp % 50) / 50, 1.0)
    )


# ============================================================
# POKÉMON IMAGE
# ============================================================

def pokemon_image(number, caption, width=140):

    url = (
        "https://raw.githubusercontent.com/"
        "PokeAPI/sprites/master/sprites/pokemon/"
        f"{number}.png"
    )

    st.image(
        url,
        width=width,
        caption=caption,
    )


# ============================================================
# HOME
# ============================================================

if page == "home":

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-title">
                ⚡ {t("welcome")}
            </div>

            <div class="hero-subtitle">
                {t("subtitle")}
            </div>

            <hr>

            <h3>{t("mission")}</h3>

            <div class="hero-subtitle">
                {t("mission_text")}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        pokemon_image(
            25,
            "Pikachu • Energy",
            130,
        )

    with c2:
        pokemon_image(
            6,
            "Charizard • Power",
            130,
        )

    with c3:
        pokemon_image(
            150,
            "Mewtwo • Probability",
            130,
        )

    st.subheader(t("choose"))

    cards = [
        (
            "⚡ Pokémon Power Lab",
            "Explore energy and electrical power.",
        ),
        (
            "🎯 Monte Carlo π Lab",
            "Estimate π using random points.",
        ),
        (
            "🌌 4D Sphere Lab",
            "Explore higher-dimensional geometry.",
        ),
        (
            "📈 Function Lab",
            "Turn equations into visual graphs.",
        ),
        (
            "🔌 Physics Lab",
            "Experiment with voltage and resistance.",
        ),
        (
            "🧠 Math Arcade",
            "Solve challenges and earn XP.",
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
        "Every simulation is a mathematical model. "
        "Always examine the assumptions behind a model."
    )


# ============================================================
# POKÉMON POWER LAB
# ============================================================

elif page == "power":

    st.title("⚡ Pokémon Power Laboratory")

    st.write(
        "Can a team of Pokémon provide enough power "
        "to operate a lightbulb?"
    )

    left, right = st.columns([1, 2])

    with left:

        pokemon_image(
            25,
            "Pikachu",
            170,
        )

        bulb_power = st.slider(
            "Bulb power (watts)",
            1,
            200,
            60,
        )

        pokemon_power = st.slider(
            "Assumed Pokémon power (watts)",
            1,
            100,
            10,
        )

        if st.button(
            t("calculate"),
            key="power_button",
        ):

            number = math.ceil(
                bulb_power / pokemon_power
            )

            st.session_state.power_result = number

            award_xp(
                "power",
                10,
            )

    with right:

        if "power_result" in st.session_state:

            number = st.session_state.power_result

            st.metric(
                "Pokémon required",
                number,
            )

            st.markdown(
                f"""
                <div class="formula-box">

                <b>Step 1:</b>
                Bulb power = {bulb_power} W

                <br>

                <b>Step 2:</b>
                One Pokémon = {pokemon_power} W

                <br>

                <b>Step 3:</b>
                Divide:

                {bulb_power} ÷ {pokemon_power}

                <br>

                <b>Step 4:</b>
                We need a whole number of Pokémon,
                so we round upward.

                <br>

                <b>Answer:</b>
                {number} Pokémon

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.latex(
                rf"N =
                \left\lceil
                \frac{{{bulb_power}}}
                {{{pokemon_power}}}
                \right\rceil
                = {number}"
            )

    st.warning(
        "The Pokémon power values are fictional assumptions "
        "used for educational modelling."
    )


# ============================================================
# MONTE CARLO PI
# ============================================================

elif page == "pi":

    st.title("🎯 Monte Carlo π Laboratory")

    st.write(
        "Estimate π by placing random points inside a square "
        "and checking how many fall inside a quarter-circle."
    )

    trials = st.slider(
        t("trials"),
        100,
        10000,
        2000,
        100,
    )

    if st.button(
        t("run"),
        key="pi_button",
    ):

        rng = np.random.default_rng()

        x = rng.random(trials)
        y = rng.random(trials)

        inside = (
            x**2 + y**2 <= 1
        )

        inside_count = int(
            np.sum(inside)
        )

        estimate = (
            4 * inside_count / trials
        )

        st.session_state.pi_data = {
            "x": x,
            "y": y,
            "inside": inside,
            "count": inside_count,
            "trials": trials,
            "estimate": estimate,
        }

        award_xp(
            "pi",
            15,
        )

    if "pi_data" in st.session_state:

        data = st.session_state.pi_data

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Estimated π",
                f"{data['estimate']:.6f}",
            )

        with col2:
            st.metric(
                "Actual π",
                f"{math.pi:.6f}",
            )

        fig, ax = plt.subplots(
            figsize=(7, 7)
        )

        inside = data["inside"]

        ax.scatter(
            data["x"][inside],
            data["y"][inside],
            s=7,
            alpha=0.65,
            label="Inside",
        )

        ax.scatter(
            data["x"][~inside],
            data["y"][~inside],
            s=7,
            alpha=0.35,
            label="Outside",
        )

        theta = np.linspace(
            0,
            np.pi / 2,
            300,
        )

        ax.plot(
            np.cos(theta),
            np.sin(theta),
            linewidth=2,
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(
            "Monte Carlo estimation of π"
        )

        ax.legend()

        st.pyplot(fig)

        plt.close(fig)

        st.subheader(t("steps"))

        st.markdown(
            f"""
            **Step 1 — Generate random points**

            Each point has an x and y coordinate between 0 and 1.

            **Step 2 — Check the circle**

            A point is inside the quarter-circle when:

            x² + y² ≤ 1

            **Step 3 — Count the points**

            Total points: {data['trials']}

            Points inside: {data['count']}

            **Step 4 — Estimate π**

            The quarter-circle occupies approximately π/4
            of the square.

            Therefore:

            π ≈ 4 × (points inside / total points)

            **Step 5 — Interpret**

            More samples usually give a more stable estimate,
            although individual random runs can vary.
            """
        )

        st.latex(
            rf"\pi \approx
            4 \times
            \frac{{{data['count']}}}
            {{{data['trials']}}
            =
            {data['estimate']:.6f}"
        )


# ============================================================
# 4D SPHERE
# ============================================================

elif page == "sphere":

    st.title("🌌 Four-Dimensional Sphere Laboratory")

    st.write(
        "Estimate the volume of a unit sphere in four dimensions "
        "using Monte Carlo sampling."
    )

    st.markdown(
        """
        In 2D:

        x² + y² ≤ 1

        In 3D:

        x² + y² + z² ≤ 1

        In 4D:

        x² + y² + z² + w² ≤ 1
        """
    )

    trials = st.slider(
        t("trials"),
        1000,
        50000,
        10000,
        1000,
        key="sphere_slider",
    )

    if st.button(
        t("run"),
        key="sphere_button",
    ):

        rng = np.random.default_rng()

        points = rng.uniform(
            -1,
            1,
            size=(trials, 4),
        )

        inside = (
            np.sum(points**2, axis=1)
            <= 1
        )

        count = int(
            np.sum(inside)
        )

        estimated_volume = (
            16 * count / trials
        )

        st.session_state.sphere_data = {
            "points": points,
            "inside": inside,
            "count": count,
            "trials": trials,
            "estimate": estimated_volume,
        }

        award_xp(
            "sphere",
            20,
        )

    if "sphere_data" in st.session_state:

        data = st.session_state.sphere_data

        exact = (
            math.pi**2 / 2
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Monte Carlo estimate",
                f"{data['estimate']:.5f}",
            )

        with c2:
            st.metric(
                "Exact volume",
                f"{exact:.5f}",
            )

        fig, ax = plt.subplots(
            figsize=(7, 6)
        )

        inside = data["inside"]
        points = data["points"]

        ax.scatter(
            points[inside, 0],
            points[inside, 1],
            s=5,
            alpha=0.45,
            label="Inside 4D sphere",
        )

        ax.scatter(
            points[~inside, 0],
            points[~inside, 1],
            s=5,
            alpha=0.2,
            label="Outside",
        )

        ax.set_xlabel("x")
        ax.set_ylabel("y")

        ax.set_title(
            "2D projection of 4D samples"
        )

        ax.legend()

        st.pyplot(fig)

        plt.close(fig)

        st.subheader(t("steps"))

        st.markdown(
            f"""
            **Step 1 — Create the surrounding 4D box**

            Every coordinate is between -1 and 1.

            **Step 2 — Check all four coordinates**

            A point is inside when:

            x² + y² + z² + w² ≤ 1

            **Step 3 — Count the successful samples**

            Total samples: {data['trials']}

            Inside: {data['count']}

            **Step 4 — Calculate the volume**

            Each side of the surrounding 4D box has length 2.

            Therefore:

            2⁴ = 16

            So:

            Estimated volume =
            16 × (inside / total)

            **Important**

            The graph only displays the x and y coordinates.
            The classification itself uses x, y, z and w.
            """
        )

        st.latex(
            rf"V \approx
            16 \times
            \frac{{{data['count']}}}
            {{{data['trials']}}}
            =
            {data['estimate']:.5f}"
        )

        st.latex(
            r"V_{\mathrm{exact}} =
            \frac{\pi^2}{2}"
        )


# ============================================================
# FUNCTION LAB
# ============================================================

elif page == "functions":

    st.title("📈 Function Laboratory")

    st.write(
        "See how mathematical equations become visual curves."
    )

    functions = {
        "x²": lambda x: x**2,
        "x³": lambda x: x**3,
        "sin(x)": lambda x: np.sin(x),
        "cos(x)": lambda x: np.cos(x),
        "eˣ": lambda x: np.exp(
            np.clip(x, -20, 20)
        ),
        "√|x|": lambda x: np.sqrt(
            np.abs(x)
        ),
    }

    selected = st.selectbox(
        "Choose a function",
        list(functions.keys()),
    )

    x_min = st.slider(
        "Minimum x",
        -10,
        -1,
        -5,
    )

    x_max = st.slider(
        "Maximum x",
        1,
        10,
        5,
    )

    x = np.linspace(
        x_min,
        x_max,
        500,
    )

    y = functions[selected](x)

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.plot(
        x,
        y,
        linewidth=2.5,
    )

    ax.axhline(
        0,
        linewidth=1,
    )

    ax.axvline(
        0,
        linewidth=1,
    )

    ax.grid(
        True,
        alpha=0.25,
    )

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    ax.set_title(
        f"f(x) = {selected}"
    )

    st.pyplot(fig)

    plt.close(fig)

    explanations = {
        "x²": (
            "Squaring a number gives a non-negative result. "
            "This creates a U-shaped parabola."
        ),
        "x³": (
            "Cubing preserves the sign of x, creating an "
            "S-shaped curve."
        ),
        "sin(x)": (
            "Sine oscillates between -1 and 1."
        ),
        "cos(x)": (
            "Cosine also oscillates between -1 and 1, "
            "and starts at 1 when x = 0."
        ),
        "eˣ": (
            "The exponential function grows rapidly for "
            "positive x."
        ),
        "√|x|": (
            "The absolute value makes the input non-negative "
            "before taking the square root."
        ),
    }

    st.info(
        explanations[selected]
    )

    value = st.number_input(
        "Enter x",
        value=2.0,
    )

    output = float(
        functions[selected](
            np.array([value])
        )[0]
    )

    st.metric(
        "f(x)",
        f"{output:.6f}",
    )


# ============================================================
# PHYSICS LAB
# ============================================================

elif page == "physics":

    st.title("🔌 Physics Laboratory")

    st.write(
        "Experiment with voltage, resistance, current and power."
    )

    voltage = st.slider(
        "Voltage (V)",
        1,
        240,
        12,
    )

    resistance = st.slider(
        "Resistance (Ω)",
        1,
        100,
        4,
    )

    current = (
        voltage / resistance
    )

    power = (
        voltage * current
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Current",
            f"{current:.3f} A",
        )

    with c2:
        st.metric(
            "Power",
            f"{power:.3f} W",
        )

    st.subheader(t("steps"))

    st.markdown(
        f"""
        **Step 1 — Ohm's law**

        Current = voltage ÷ resistance.

        **Step 2 — Substitute**

        {voltage} ÷ {resistance}

        **Step 3 — Calculate**

        Current = {current:.3f} A

        **Step 4 — Electrical power**

        Power = voltage × current

        {voltage} × {current:.3f}

        = {power:.3f} W
        """
    )

    st.latex(
        r"I = \frac{V}{R}"
    )

    st.latex(
        r"P = VI"
    )


# ============================================================
# MATH ARCADE
# ============================================================

elif page == "math":

    st.title("🧠 Math Arcade")

    st.write(
        "Solve a challenge and learn from the solution."
    )

    questions = [
        {
            "question": "What is 12 × 8?",
            "answer": 96,
            "explanation": (
                "12 × 8 = 96."
            ),
        },
        {
            "question": "What is 15²?",
            "answer": 225,
            "explanation": (
                "15² means 15 × 15. "
                "15 × 15 = 225."
            ),
        },
        {
            "question": "What is √144?",
            "answer": 12,
            "explanation": (
                "12 × 12 = 144, so √144 = 12."
            ),
        },
        {
            "question": "A 60 W bulb uses 12 V. "
            "What current flows?",
            "answer": 5,
            "explanation": (
                "Using I = P/V: "
                "60 ÷ 12 = 5 A."
            ),
        },
    ]

    number = st.selectbox(
        "Choose a challenge",
        range(len(questions)),
        format_func=lambda x:
        f"Challenge {x + 1}",
    )

    q = questions[number]

    st.markdown(
        f"""
        <div class="lab-card">
            <h3>{q['question']}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answer = st.number_input(
        t("your_answer"),
        value=0.0,
        step=1.0,
        key=f"math_answer_{number}",
    )

    if st.button(
        t("check"),
        key=f"math_check_{number}",
    ):

        if math.isclose(
            answer,
            q["answer"],
            abs_tol=0.0001,
        ):

            st.success(
                t("correct")
            )

            award_xp(
                f"math_{number}",
                15,
            )

        else:

            st.warning(
                t("incorrect")
            )

        st.markdown(
            "### Solution"
        )

        st.write(
            q["explanation"]
        )

        st.markdown(
            f"**Answer: {q['answer']}**"
        )


# ============================================================
# SAFE CALCULATOR
# ============================================================

def safe_calculate(expression):

    binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    unary_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    functions = {
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

        if isinstance(
            node,
            ast.Expression,
        ):
            return evaluate(
                node.body
            )

        if isinstance(
            node,
            ast.Constant,
        ):

            if isinstance(
                node.value,
                (int, float),
            ):
                return node.value

            raise ValueError(
                "Only numbers are allowed."
            )

        if isinstance(
            node,
            ast.BinOp,
        ):

            operation = type(
                node.op
            )

            if operation not in binary_ops:
                raise ValueError(
                    "Unsupported operator."
                )

            left = evaluate(
                node.left
            )

            right = evaluate(
                node.right
            )

            if (
                operation is ast.Pow
                and abs(right) > 100
            ):
                raise ValueError(
                    "Exponent is too large."
                )

            return binary_ops[
                operation
            ](
                left,
                right,
            )

        if isinstance(
            node,
            ast.UnaryOp,
        ):

            operation = type(
                node.op
            )

            if operation not in unary_ops:
                raise ValueError(
                    "Unsupported operator."
                )

            return unary_ops[
                operation
            ](
                evaluate(
                    node.operand
                )
            )

        if isinstance(
            node,
            ast.Name,
        ):

            if node.id in constants:
                return constants[
                    node.id
                ]

            raise ValueError(
                "Unknown name."
            )

        if isinstance(
            node,
            ast.Call,
        ):

            if not isinstance(
                node.func,
                ast.Name,
            ):
                raise ValueError(
                    "Unsupported function."
                )

            name = node.func.id

            if name not in functions:
                raise ValueError(
                    "Function not allowed."
                )

            if (
                len(node.args) != 1
                or node.keywords
            ):
                raise ValueError(
                    "Use one argument."
                )

            return functions[name](
                evaluate(
                    node.args[0]
                )
            )

        raise ValueError(
            "Unsupported expression."
        )

    tree = ast.parse(
        expression,
        mode="eval",
    )

    result = evaluate(tree)

    if isinstance(
        result,
        complex,
    ):
        raise ValueError(
            "Complex results are not supported."
        )

    if not math.isfinite(
        float(result)
    ):
        raise ValueError(
            "The result is not finite."
        )

    return result


# ============================================================
# CALCULATOR
# ============================================================

elif page == "calculator":

    st.title("🧮 Mathematical Calculation Engine")

    st.write(
        "Try arithmetic, powers and selected mathematical functions."
    )

    expression = st.text_input(
        "Enter a mathematical expression",
        value="50 * 3 + sqrt(400)",
    )

    st.caption(
        "Examples: 50 * 3 + sqrt(400), "
        "sin(pi / 2), log(e)"
    )

    if st.button(
        t("calculate"),
        key="calculator_button",
    ):

        try:

            result = safe_calculate(
                expression
            )

            st.metric(
                t("result"),
                f"{result:.8g}",
            )

            st.subheader(
                t("steps")
            )

            st.markdown(
                """
                The expression is evaluated according to
                normal mathematical operator precedence.

                Functions such as sqrt(), sin(), cos() and log()
                are also supported.
                """
            )

            award_xp(
                "calculator",
                10,
            )

        except (
            ValueError,
            TypeError,
            SyntaxError,
            ZeroDivisionError,
            OverflowError,
        ) as error:

            st.error(
                f"Could not calculate this expression: {error}"
            )


# ============================================================
# ABOUT
# ============================================================

elif page == "about":

    st.title("🔬 Tom Lab")

    st.markdown(
        """
        ## An independent educational project

        Tom Lab is an independent project exploring mathematics,
        physics, probability and scientific modelling through
        interactive experiments.

        ### What the project tries to do

        - Make mathematical ideas interactive.
        - Explain calculations step by step.
        - Use visual simulations.
        - Encourage experimentation.
        - Connect abstract mathematics with fun examples.

        ### Important note

        This is an independent fan-made educational project inspired
        by mathematics and science communication.

        It is **not an official Professor Tom Crawford project**
        and does **not imply endorsement by Professor Tom Crawford**.

        Pokémon characters and names belong to their respective
        rights holders. This project is not affiliated with or
        endorsed by The Pokémon Company or Nintendo.

        ### Built with

        Python • Streamlit • NumPy • Matplotlib
        """
        )
