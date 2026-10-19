import ast
import math
import operator
import random

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tom Lab | Maths & Pokémon",
    page_icon="⚡",
    layout="wide",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap'
    );

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                #17345b 0%,
                #0b1424 42%,
                #070b14 100%
            );
        color: #f2f6ff;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
    }

    .hero {
        padding: 28px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            rgba(23, 52, 91, 0.95),
            rgba(24, 20, 55, 0.95)
        );
        border: 1px solid rgba(90, 180, 255, 0.4);
        margin-bottom: 22px;
    }

    .hero p {
        font-size: 1.05rem;
        color: #d8e7ff;
    }

    .note {
        padding: 14px;
        border-left: 4px solid #55c7ff;
        background: rgba(45, 100, 150, 0.16);
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("⚡ TOM LAB")
st.sidebar.caption("Interactive Maths & Science Laboratory")

page = st.sidebar.radio(
    "Choose your laboratory",
    [
        "Command Centre",
        "Pokémon Power Lab",
        "Monte Carlo π",
        "4D Sphere Lab",
        "Function Lab",
        "Physics Lab",
        "Safe Calculator",
        "Math Arcade",
        "About",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Learn • Experiment • Discover")


# ============================================================
# COMMAND CENTRE
# ============================================================

if page == "Command Centre":

    st.markdown(
        """
        <div class="hero">
            <h1>⚡ Welcome to Tom Lab</h1>
            <p>
                Explore mathematics, physics, probability,
                functions and Pokémon-inspired scientific models.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Maths", "∞", "Explore ideas")

    with col2:
        st.metric("Experiments", "6+", "Interactive labs")

    with col3:
        st.metric("Curiosity", "100%", "Always encouraged")

    st.subheader("🔬 Choose your next experiment")

    st.write(
        """
        - **Pokémon Power Lab:** Estimate how many fictional
          Pokémon would be needed to power a lightbulb.
        - **Monte Carlo π:** Estimate pi using random points.
        - **4D Sphere Lab:** Explore a four-dimensional volume.
        - **Function Lab:** Visualise mathematical functions.
        - **Physics Lab:** Experiment with voltage, current,
          resistance and electrical power.
        """
    )

    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
        "sprites/pokemon/25.png",
        width=120,
        caption="Pikachu — your maths lab companion",
    )

    st.info(
        "Choose a laboratory from the sidebar to begin."
    )


# ============================================================
# POKÉMON POWER LAB
# ============================================================

elif page == "Pokémon Power Lab":

    st.title("⚡ Pokémon Power Laboratory")

    st.write(
        "How many Pokémon would it take to power a lightbulb?"
    )

    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
        "sprites/pokemon/25.png",
        width=120,
    )

    st.markdown(
        """
        This is a mathematical model. Pokémon power values are
        fictional assumptions, not measured scientific data.
        """
    )

    bulb_power = st.number_input(
        "Lightbulb power (watts)",
        min_value=1.0,
        max_value=1000000.0,
        value=60.0,
        step=10.0,
    )

    pokemon_power = st.number_input(
        "Assumed power per Pokémon (watts)",
        min_value=0.1,
        max_value=1000000.0,
        value=10.0,
        step=1.0,
    )

    if pokemon_power > 0:

        number = math.ceil(bulb_power / pokemon_power)

        st.success(
            f"Estimated number of Pokémon: {number}"
        )

        st.markdown(
            f"""
            <div class="note">
                <b>Step 1:</b> Lightbulb power =
                {bulb_power:g} watts.<br><br>
                <b>Step 2:</b> Assumed power per Pokémon =
                {pokemon_power:g} watts.<br><br>
                <b>Step 3:</b> Divide the required power by
                the assumed power of one Pokémon.<br><br>
                <b>Step 4:</b> Round upward because we need
                a whole number of Pokémon.<br><br>
                <b>Answer:</b> {number} Pokémon
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.latex(
            rf"N = \left\lceil \frac{{{bulb_power}}}"
            rf"{{{pokemon_power}}} \right\rceil = {number}"
        )

    st.warning(
        "The Pokémon power values are fictional assumptions "
        "used for educational modelling."
    )


# ============================================================
# MONTE CARLO PI
# ============================================================

elif page == "Monte Carlo π":

    st.title("🎯 Monte Carlo π Laboratory")

    st.write(
        "Estimate π by placing random points inside a square "
        "and checking how many fall inside a quarter-circle."
    )

    trials = st.slider(
        "Number of random points",
        min_value=100,
        max_value=20000,
        value=2000,
        step=100,
    )

    if st.button("Run π experiment"):

        x = np.random.uniform(0, 1, trials)
        y = np.random.uniform(0, 1, trials)

        inside = x**2 + y**2 <= 1

        count = int(np.sum(inside))
        estimate = 4 * count / trials

        st.session_state["pi_result"] = {
            "trials": trials,
            "count": count,
            "estimate": estimate,
            "x": x,
            "y": y,
            "inside": inside,
        }

    if "pi_result" in st.session_state:

        data = st.session_state["pi_result"]

        st.metric(
            "Estimated π",
            f"{data['estimate']:.6f}",
            delta=f"Error: {abs(math.pi - data['estimate']):.6f}",
        )

        st.latex(
            rf"\pi \approx 4 \times "
            rf"\frac{{{data['count']}}}{{{data['trials']}}}"
            rf" = {data['estimate']:.6f}"
        )

        fig, ax = plt.subplots()

        inside = data["inside"]
        x = data["x"]
        y = data["y"]

        ax.scatter(
            x[inside],
            y[inside],
            s=8,
            label="Inside quarter-circle",
        )

        ax.scatter(
            x[~inside],
            y[~inside],
            s=8,
            label="Outside quarter-circle",
        )

        theta = np.linspace(0, math.pi / 2, 300)

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
        ax.set_title("Monte Carlo estimation of π")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "The estimate generally becomes more reliable "
            "as the number of random points increases."
        )


# ============================================================
# FOUR-DIMENSIONAL SPHERE LAB
# ============================================================

elif page == "4D Sphere Lab":

    st.title("🧊 Four-Dimensional Sphere Lab")

    st.write(
        "Estimate the volume of a four-dimensional unit sphere "
        "using Monte Carlo sampling."
    )

    st.latex(
        r"V_4 = \frac{\pi^2}{2} \approx 4.9348"
    )

    trials = st.slider(
        "Number of random points",
        min_value=1000,
        max_value=100000,
        value=10000,
        step=1000,
    )

    if st.button("Estimate 4D sphere volume"):

        points = np.random.uniform(
            -1.0,
            1.0,
            size=(trials, 4),
        )

        inside = np.sum(points**2, axis=1) <= 1.0
        count = int(np.sum(inside))

        estimate = 16.0 * count / trials
        exact = math.pi**2 / 2.0

        st.session_state["sphere_result"] = {
            "trials": trials,
            "count": count,
            "estimate": estimate,
            "points": points,
            "inside": inside,
            "exact": exact,
        }

    if "sphere_result" in st.session_state:

        data = st.session_state["sphere_result"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Estimated volume",
                f"{data['estimate']:.5f}",
            )

        with col2:
            st.metric(
                "Exact volume",
                f"{data['exact']:.5f}",
            )

        st.latex(
            rf"V_4 \approx 16 \times "
            rf"\frac{{{data['count']}}}{{{data['trials']}}}"
            rf" = {data['estimate']:.5f}"
        )

        points = data["points"]
        inside = data["inside"]

        fig, ax = plt.subplots()

        ax.scatter(
            points[inside, 0],
            points[inside, 1],
            s=5,
            label="Points inside the 4D sphere",
        )

        ax.scatter(
            points[~inside, 0],
            points[~inside, 1],
            s=5,
            label="Points outside the 4D sphere",
        )

        ax.set_xlabel("First coordinate")
        ax.set_ylabel("Second coordinate")
        ax.set_title("2D projection of sampled 4D points")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.info(
            "The plot shows only the first two coordinates of "
            "the sampled points. Membership in the 4D sphere "
            "is determined using all four coordinates."
        )


# ============================================================
# FUNCTION LAB
# ============================================================

elif page == "Function Lab":

    st.title("📈 Function Laboratory")

    function_name = st.selectbox(
        "Choose a function",
        [
            "x²",
            "x³",
            "sin(x)",
            "cos(x)",
            "eˣ",
            "sqrt(|x|)",
        ],
    )

    xmin = st.slider(
        "Minimum x",
        min_value=-20,
        max_value=0,
        value=-10,
    )

    xmax = st.slider(
        "Maximum x",
        min_value=1,
        max_value=20,
        value=10,
    )

    x = np.linspace(xmin, xmax, 500)

    if function_name == "x²":
        y = x**2
        formula = "y = x^2"

    elif function_name == "x³":
        y = x**3
        formula = "y = x^3"

    elif function_name == "sin(x)":
        y = np.sin(x)
        formula = "y = \\sin(x)"

    elif function_name == "cos(x)":
        y = np.cos(x)
        formula = "y = \\cos(x)"

    elif function_name == "eˣ":
        y = np.exp(np.clip(x, -50, 50))
        formula = "y = e^x"

    else:
        y = np.sqrt(np.abs(x))
        formula = "y = \\sqrt{|x|}"

    st.latex(formula)

    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.3)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Graph of {function_name}")

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# PHYSICS LAB
# ============================================================

elif page == "Physics Lab":

    st.title("🔌 Physics Laboratory")

    st.subheader("Ohm's law")

    st.latex(r"V = I R")

    resistance = st.number_input(
        "Resistance (ohms)",
        min_value=0.1,
        max_value=1000000.0,
        value=10.0,
    )

    current = st.number_input(
        "Current (amperes)",
        min_value=0.0,
        max_value=1000000.0,
        value=2.0,
    )

    voltage = resistance * current

    st.metric("Voltage", f"{voltage:.3f} V")

    st.divider()

    st.subheader("Electrical power")

    st.latex(r"P = V I")

    voltage_input = st.number_input(
        "Voltage for power calculation (volts)",
        min_value=0.0,
        max_value=1000000.0,
        value=12.0,
    )

    current_input = st.number_input(
        "Current for power calculation (amperes)",
        min_value=0.0,
        max_value=1000000.0,
        value=0.5,
    )

    power = voltage_input * current_input

    st.metric("Electrical power", f"{power:.3f} W")

    st.caption(
        "These calculations use idealised circuit relationships."
    )


# ============================================================
# SAFE CALCULATOR
# ============================================================

def safe_calculate(expression):

    allowed_operators = {
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

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in allowed_operators:
                raise ValueError("Operator not allowed.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if op_type is ast.Pow and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            result = allowed_operators[op_type](left, right)

            if abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in allowed_unary:
                raise ValueError("Operator not allowed.")

            return allowed_unary[op_type](evaluate(node.operand))

        raise ValueError(
            "Use only numbers and +, -, *, /, %, and **."
        )

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree)


if page == "Safe Calculator":

    st.title("🧮 Safe Mathematics Calculator")

    st.write(
        "Enter an arithmetic expression using numbers and "
        "+, -, *, /, %, and **."
    )

    expression = st.text_input(
        "Expression",
        value="50 * 3 + 20",
    )

    if st.button("Calculate"):

        try:
            result = safe_calculate(expression)
            st.success(f"Result: {result}")

        except (
            ValueError,
            SyntaxError,
            ZeroDivisionError,
            OverflowError,
            TypeError,
        ):
            st.error(
                "Invalid expression. Check the numbers "
                "and operators, then try again."
            )


# ============================================================
# MATH ARCADE
# ============================================================

elif page == "Math Arcade":

    st.title("🧠 Math Arcade")

    questions = [
        {
            "question": "What is 12 × 8?",
            "options": ["86", "96", "108", "88"],
            "answer": "96",
            "explanation": "12 multiplied by 8 equals 96.",
        },
        {
            "question": "What is the approximate value of π?",
            "options": ["2.718", "1.414", "3.142", "4.000"],
            "answer": "3.142",
            "explanation": "π is approximately 3.14159.",
        },
        {
            "question": "What is the derivative of x²?",
            "options": ["x", "2x", "x³", "2"],
            "answer": "2x",
            "explanation": "The power rule gives d(x²)/dx = 2x.",
        },
        {
            "question": "What is 2⁵?",
            "options": ["10", "16", "25", "32"],
            "answer": "32",
            "explanation": "2 × 2 × 2 × 2 × 2 = 32.",
        },
    ]

    if "quiz_index" not in st.session_state:
        st.session_state["quiz_index"] = 0

    if "quiz_score" not in st.session_state:
        st.session_state["quiz_score"] = 0

    index = st.session_state["quiz_index"]

    if index < len(questions):

        item = questions[index]

        st.write(
            f"Question {index + 1} of {len(questions)}"
        )

        st.subheader(item["question"])

        choice = st.radio(
            "Choose your answer",
            item["options"],
            key=f"quiz_choice_{index}",
        )

        if st.button("Submit answer"):

            if choice == item["answer"]:
                st.session_state["quiz_score"] += 1
                st.success("Correct! 🎉")

            else:
                st.info(
                    f"The correct answer is {item['answer']}."
                )

            st.write(item["explanation"])

            st.session_state["quiz_index"] += 1
            st.rerun()

    else:

        score = st.session_state["quiz_score"]

        st.success(
            f"Quiz complete! Your score: {score}/{len(questions)}"
        )

        if st.button("Play again"):

            st.session_state["quiz_index"] = 0
            st.session_state["quiz_score"] = 0
            st.rerun()


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    st.title("ℹ️ About Tom Lab")

    st.write(
        """
        Tom Lab is an independent educational project exploring
        mathematics and physics through interactive experiments
        and Pokémon-inspired examples.
        """
    )

    st.subheader("Learning goals")

    st.write(
        """
        - Understand mathematical modelling.
        - Explore probability and Monte Carlo estimation.
        - Visualise mathematical functions.
        - Apply basic electrical equations.
        - Learn through experimentation.
        """
    )

    st.warning(
        "This is an independent fan-made educational project. "
        "It is not an official Professor Tom Crawford project "
        "and is not affiliated with or endorsed by Nintendo, "
        "The Pokémon Company, or their affiliates."
    )

    st.caption(
        "Pokémon names and imagery belong to their respective "
        "rights holders. This project uses fictional assumptions "
        "for educational purposes."
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()
st.sidebar.caption("Tom Lab • Independent learning project")
