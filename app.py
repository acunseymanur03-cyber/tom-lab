import ast
import math
import random
import operator

import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Tom Lab | Math & Pokémon",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #0b1020 0%, #111a30 100%);
        color: #f1f5f9;
    }

    h1, h2, h3 {
        color: #67e8f9 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #22d3ee;
        font-weight: 600;
    }

    .lab-card {
        padding: 18px;
        border-radius: 14px;
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid #334155;
        margin-bottom: 12px;
    }

    .small-note {
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "notes" not in st.session_state:
    st.session_state.notes = []

if "challenge" not in st.session_state:
    st.session_state.challenge = None

if "challenge_answer" not in st.session_state:
    st.session_state.challenge_answer = None

if "challenge_hint" not in st.session_state:
    st.session_state.challenge_hint = None

if "challenge_solution" not in st.session_state:
    st.session_state.challenge_solution = None

if "math_result" not in st.session_state:
    st.session_state.math_result = None

if "type_result" not in st.session_state:
    st.session_state.type_result = None

if "voltage_result" not in st.session_state:
    st.session_state.voltage_result = None

if "catch_result" not in st.session_state:
    st.session_state.catch_result = None

if "cp_result" not in st.session_state:
    st.session_state.cp_result = None

if "constant_result" not in st.session_state:
    st.session_state.constant_result = None


# =========================================================
# SAFE MATHEMATICAL EXPRESSION EVALUATOR
# =========================================================

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

MATH_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "factorial": math.factorial,
    "floor": math.floor,
    "ceil": math.ceil,
    "abs": abs,
    "round": round,
}

MATH_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def safe_calculate(expression):
    """Evaluate a restricted mathematical expression without eval()."""

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node, depth=0):
        if depth > 30:
            raise ValueError("Expression is too complex.")

        if isinstance(node, ast.Expression):
            return evaluate(node.body, depth + 1)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are allowed.")
            if abs(node.value) > 1e100:
                raise ValueError("Number is too large.")
            return node.value

        if isinstance(node, ast.Name):
            if node.id in MATH_CONSTANTS:
                return MATH_CONSTANTS[node.id]
            raise ValueError(f"Unknown name: {node.id}")

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in BINARY_OPERATORS:
                raise ValueError("Operator is not supported.")

            left = evaluate(node.left, depth + 1)
            right = evaluate(node.right, depth + 1)

            if operator_type is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")

                if abs(left) > 1e100:
                    raise ValueError("Base is too large.")

            result = BINARY_OPERATORS[operator_type](left, right)

            if isinstance(result, complex):
                raise ValueError("Complex results are not supported.")

            if not math.isfinite(float(result)):
                raise ValueError("Result is not finite.")

            if abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in UNARY_OPERATORS:
                raise ValueError("Unary operator is not supported.")

            return UNARY_OPERATORS[operator_type](
                evaluate(node.operand, depth + 1)
            )

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only approved math functions are allowed.")

            function_name = node.func.id

            if function_name not in MATH_FUNCTIONS:
                raise ValueError(f"Function not allowed: {function_name}")

            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")

            arguments = [
                evaluate(argument, depth + 1)
                for argument in node.args
            ]

            if len(arguments) > 5:
                raise ValueError("Too many arguments.")

            return MATH_FUNCTIONS[function_name](*arguments)

        raise ValueError(
            "Unsupported expression. Use numbers and approved math functions."
        )

    result = evaluate(tree)

    if not math.isfinite(float(result)):
        raise ValueError("Result is not finite.")

    return result


# =========================================================
# HEADER
# =========================================================

st.title("⚡ TOM LAB")
st.subheader("Volts, Voltorbs & Variables")
st.markdown(
    """
    **An interactive mathematics, physics and Pokémon learning lab.**

    Explore mathematical expressions, investigate circuits,
    test type interactions and solve scientific challenges.
    """
)

st.info(
    "Independent educational fan project. This application is not "
    "officially affiliated with, sponsored by or endorsed by "
    "Professor Tom Crawford, Pokémon or their publishers."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔬 Research Console")

researcher_name = st.sidebar.text_input(
    "Researcher name",
    placeholder="Enter your name",
)

st.sidebar.caption(
    "Welcome to the interactive research environment."
)

st.sidebar.divider()

section = st.sidebar.radio(
    "Choose a laboratory",
    [
        "🏠 Overview",
        "🧮 Math Engine",
        "⚡ Ohm's Law",
        "🎮 Pokémon Lab",
        "🎯 Catch Probability",
        "🧠 Challenges",
        "📐 Constants",
        "📝 Research Notebook",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Educational simulations only. Verify scientific results "
    "before using them in formal research."
)


# =========================================================
# OVERVIEW
# =========================================================

if section == "🏠 Overview":

    display_name = researcher_name.strip() or "Researcher"

    st.success(f"Welcome, {display_name}! Your laboratory is ready.")

    st.markdown("## 🧪 Laboratory Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Laboratory Modules", "7")

    with col2:
        st.metric("Math Functions", len(MATH_FUNCTIONS))

    with col3:
        st.metric("Saved Notes", len(st.session_state.notes))

    st.divider()

    st.markdown("### 🔭 What can you investigate?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="lab-card">
            <h3>🧮 Mathematical Analysis</h3>
            Calculate expressions, explore constants and investigate
            mathematical relationships.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="lab-card">
            <h3>⚡ Electrical Physics</h3>
            Explore the relationship between voltage, current and
            resistance using Ohm's law.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="lab-card">
            <h3>🎮 Pokémon Mathematics</h3>
            Investigate a simplified type-effectiveness model and
            educational probability simulations.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="lab-card">
            <h3>🧠 Scientific Challenges</h3>
            Solve educational questions and reveal worked solutions.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 💡 Research principle")

    st.write(
        "A good scientific model makes its assumptions explicit, "
        "shows how results are calculated and explains its limitations."
    )


# =========================================================
# MATHEMATICS ENGINE
# =========================================================

elif section == "🧮 Math Engine":

    st.header("🧮 Universal Mathematics Engine")

    st.write(
        "Use arithmetic operators and approved functions. "
        "For example: `50 * 3 + sqrt(400)`"
    )

    st.markdown(
        """
        **Supported functions:** `sqrt`, `sin`, `cos`, `tan`,
        `log`, `log10`, `exp`, `factorial`, `floor`, `ceil`,
        `abs`, `round`

        **Constants:** `pi`, `e`

        Trigonometric functions use radians.
        """
    )

    expression = st.text_input(
        "Mathematical expression",
        value="50 * 3 + sqrt(400)",
        key="math_expression",
    )

    if st.button("⚡ Calculate", key="math_calculate"):
        try:
            st.session_state.math_result = (
                expression,
                safe_calculate(expression.strip()),
                None,
            )
        except Exception as error:
            st.session_state.math_result = (
                expression,
                None,
                str(error),
            )

    if st.session_state.math_result is not None:
        old_expression, result, error = st.session_state.math_result

        if error:
            st.error(f"Calculation error: {error}")
        else:
            st.success(f"Result: {old_expression} = {result}")

            if isinstance(result, (int, float)):
                st.metric("Numerical result", f"{result:.10g}")


# =========================================================
# OHM'S LAW
# =========================================================

elif section == "⚡ Ohm's Law":

    st.header("⚡ Ohm's Law Simulator")

    st.latex(r"V = I \times R")

    st.write(
        "Voltage equals current multiplied by resistance."
    )

    col1, col2 = st.columns(2)

    with col1:
        current = st.number_input(
            "Current (amperes)",
            min_value=0.0,
            max_value=1_000_000.0,
            value=5.0,
            step=0.5,
        )

    with col2:
        resistance = st.number_input(
            "Resistance (ohms)",
            min_value=0.0,
            max_value=1_000_000.0,
            value=10.0,
            step=1.0,
        )

    voltage = current * resistance

    st.metric("Calculated voltage", f"{voltage:g} V")

    chart_data = pd.DataFrame(
        {
            "Current (A)": [
                current * fraction / 10
                for fraction in range(11)
            ]
        }
    )

    chart_data["Voltage (V)"] = (
        chart_data["Current (A)"] * resistance
    )

    st.markdown("### 📊 Voltage versus current")

    st.line_chart(
        chart_data.set_index("Current (A)")["Voltage (V)"]
    )

    st.caption(
        "The graph assumes constant resistance and an ideal "
        "ohmic component."
    )

    st.markdown("### 🔍 Calculation details")

    st.write(f"Current: {current:g} A")
    st.write(f"Resistance: {resistance:g} Ω")
    st.write(f"Voltage: {current:g} × {resistance:g} = {voltage:g} V")


# =========================================================
# POKÉMON LAB
# =========================================================

elif section == "🎮 Pokémon Lab":

    st.header("🎮 Pokémon Type-Effectiveness Lab")

    st.write(
        "This demonstration covers only four types and selected "
        "interactions. It is not a complete Pokémon type chart."
    )

    types = ["Electric", "Water", "Fire", "Grass"]

    col1, col2 = st.columns(2)

    with col1:
        attacker = st.selectbox(
            "Attacking type",
            types,
            key="attacker_type",
        )

    with col2:
        defender = st.selectbox(
            "Defending type",
            types,
            key="defender_type",
        )

    # Selected interactions from the standard type chart.
    # All other interactions in this limited model are neutral.
    effectiveness = {
        ("Electric", "Water"): 2.0,
        ("Electric", "Grass"): 0.5,
        ("Water", "Fire"): 2.0,
        ("Water", "Grass"): 0.5,
        ("Fire", "Grass"): 2.0,
        ("Fire", "Water"): 0.5,
        ("Grass", "Water"): 2.0,
        ("Grass", "Fire"): 0.5,
        ("Electric", "Electric"): 0.5,
        ("Water", "Electric"): 1.0,
        ("Fire", "Electric"): 1.0,
        ("Grass", "Electric"): 1.0,
    }

    multiplier = effectiveness.get((attacker, defender), 1.0)

    st.markdown("### 🔬 Analysis")

    st.metric("Effectiveness multiplier", f"{multiplier:g}×")

    if multiplier > 1:
        st.success("Super effective in this simplified model!")
    elif multiplier < 1:
        st.warning("Not very effective in this simplified model.")
    else:
        st.info("Neutral damage in this simplified model.")

    st.caption(
        "The full game includes additional types, immunities, "
        "dual-type interactions and other battle mechanics."
    )

    st.divider()

    st.markdown("### 📋 Selected matchup table")

    table = pd.DataFrame(
        [
            {
                "Attacking type": a,
                "Defending type": d,
                "Multiplier": effectiveness.get((a, d), 1.0),
            }
            for a in types
            for d in types
        ]
    )

    st.dataframe(table, use_container_width=True, hide_index=True)


# =========================================================
# CATCH PROBABILITY
# =========================================================

elif section == "🎯 Catch Probability":

    st.header("🎯 Educational Catch-Probability Simulator")

    st.warning(
        "This is a hypothetical classroom model, not the official "
        "Pokémon GO or main-series catch-rate formula."
    )

    level = st.slider(
        "Illustrative difficulty level",
        min_value=1,
        max_value=100,
        value=40,
    )

    ball = st.selectbox(
        "Hypothetical ball multiplier",
        [
            "Standard Ball",
            "Great Ball",
            "Ultra Ball",
            "Master Ball",
        ],
    )

    multipliers = {
        "Standard Ball": 1.0,
        "Great Ball": 1.5,
        "Ultra Ball": 2.0,
        "Master Ball": 100.0,
    }

    if st.button("🎲 Run simulation"):

        if ball == "Master Ball":
            probability = 100.0
        else:
            probability = min(
                100.0,
                max(
                    1.0,
                    (100.0 / (level * 0.4)) * multipliers[ball] * 10,
                ),
            )

        st.session_state.catch_result = probability

    if st.session_state.catch_result is not None:
        st.metric(
            "Model output",
            f"{st.session_state.catch_result:.2f}%",
        )

        st.progress(
            int(round(st.session_state.catch_result))
        )

        st.caption(
            "This percentage is generated by the illustrative formula "
            "in this application and is not a prediction of actual "
            "in-game outcomes."
        )


# =========================================================
# CHALLENGES
# =========================================================

elif section == "🧠 Challenges":

    st.header("🧠 Scientific Challenge Generator")

    challenges = [
        {
            "question": (
                "A circuit has a voltage of 100 V and a resistance "
                "of 20 Ω. What is the current?"
            ),
            "hint": "Use Ohm's law: I = V / R.",
            "solution": "I = 100 / 20 = 5 A.",
            "answer": 5.0,
        },
        {
            "question": (
                "What is the volume of a sphere with radius 5 units?"
            ),
            "hint": "Use V = (4/3)πr³.",
            "solution": (
                "V = (4/3) × π × 5³ = (500/3)π ≈ 523.60 cubic units."
            ),
            "answer": (4 / 3) * math.pi * 125,
        },
        {
            "question": (
                "Evaluate sin(π/2) + sqrt(81). "
                "Remember that trigonometric functions use radians."
            ),
            "hint": "sin(π/2) = 1 and sqrt(81) = 9.",
            "solution": "1 + 9 = 10.",
            "answer": 10.0,
        },
    ]

    if st.button("🎲 Generate a challenge") or (
        st.session_state.challenge is None
    ):
        st.session_state.challenge = random.choice(challenges)
        st.session_state.challenge_answer = None

    challenge = st.session_state.challenge

    st.markdown("### 🧪 Your question")

    st.write(challenge["question"])

    if st.button("💡 Show hint"):
        st.info(challenge["hint"])

    user_answer = st.text_input(
        "Your numerical answer",
        key="challenge_user_answer",
    )

    if st.button("✅ Check answer"):
        try:
            submitted = safe_calculate(user_answer.strip())

            if math.isclose(
                float(submitted),
                float(challenge["answer"]),
                rel_tol=1e-3,
                abs_tol=1e-3,
            ):
                st.success("Correct! Excellent scientific reasoning.")
            else:
                st.warning(
                    "Not quite. Try again or reveal the worked solution."
                )
        except Exception:
            st.error(
                "Enter a valid numerical expression, such as 5 or 2*pi."
            )

    if st.button("📖 Reveal worked solution"):
        st.info(challenge["solution"])


# =========================================================
# MATHEMATICAL CONSTANTS
# =========================================================

elif section == "📐 Constants":

    st.header("📐 Mathematical Constants Dictionary")

    constants = {
        "Pi (π)": (
            math.pi,
            "The ratio of a circle's circumference to its diameter.",
        ),
        "Euler's number (e)": (
            math.e,
            "A fundamental constant in exponential growth and calculus.",
        ),
        "Golden ratio (φ)": (
            (1 + math.sqrt(5)) / 2,
            "A mathematical ratio found in several geometric contexts.",
        ),
        "Square root of 2": (
            math.sqrt(2),
            "The diagonal of a unit square.",
        ),
        "Square root of 3": (
            math.sqrt(3),
            "Appears in equilateral-triangle geometry.",
        ),
    }

    selected_constant = st.selectbox(
        "Select a constant",
        list(constants.keys()),
    )

    value, description = constants[selected_constant]

    st.metric("Numerical value", f"{value:.12f}")
    st.write(description)

    st.caption(
        "Mathematical constants have precise definitions; the displayed "
        "decimal values are rounded approximations."
    )


# =========================================================
# RESEARCH NOTEBOOK
# =========================================================

elif section == "📝 Research Notebook":

    st.header("📝 Researcher's Notebook")

    st.write(
        "Write observations, ideas, calculations or future experiments."
    )

    note_title = st.text_input(
        "Note title",
        placeholder="e.g. Ideas for the next experiment",
    )

    note_text = st.text_area(
        "Research notes",
        height=180,
        placeholder="Record your observations here...",
    )

    if st.button("💾 Save note"):

        if not note_title.strip() or not note_text.strip():
            st.warning("Please provide both a title and note content.")
        else:
            st.session_state.notes.append(
                {
                    "title": note_title.strip(),
                    "content": note_text.strip(),
                }
            )

            st.success("Note saved for this session.")

    st.divider()

    st.markdown("### 📚 Saved notes")

    if st.session_state.notes:

        for index, note in enumerate(
            st.session_state.notes,
            start=1,
        ):
            with st.expander(f"{index}. {note['title']}"):
                st.write(note["content"])

        export_text = "\n\n".join(
            [
                f"TITLE: {note['title']}\n{note['content']}"
                for note in st.session_state.notes
            ]
        )

        st.download_button(
            label="⬇️ Download notes as TXT",
            data=export_text,
            file_name="tom_lab_research_notes.txt",
            mime="text/plain",
        )

        if st.button("🗑️ Clear all notes"):
            st.session_state.notes = []
            st.success("Session notes cleared.")
            st.rerun()

    else:
        st.info(
            "No notes saved yet. Add your first research observation above."
        )

    st.caption(
        "Notes are stored in the current Streamlit session, not in a "
        "permanent database. Download them before ending the session."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94a3b8;">
        <p>⚡ TOM LAB | Mathematics • Physics • Pokémon</p>
        <p>Independent educational project • Built with Python and Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True,
)
