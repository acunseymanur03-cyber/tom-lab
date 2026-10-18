import ast
import math
import operator
import random
import io

import numpy as np
import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Tom Lab | Interactive STEM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #0b1020, #111b31);
    }

    h1, h2, h3 {
        color: #67e8f9 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid #22d3ee;
    }

    .lab-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 18px;
        border: 1px solid #334155;
        border-radius: 14px;
        margin-bottom: 10px;
    }

    .muted {
        color: #cbd5e1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "notes": [],
    "math_result": None,
    "challenge_index": None,
    "monte_carlo_result": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SAFE MATHEMATICS ENGINE
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

FUNCTIONS = {
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
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def safe_calculate(expression):
    """Evaluate a restricted arithmetic expression without eval()."""

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    tree = ast.parse(expression, mode="eval")

    def visit(node, depth=0):
        if depth > 30:
            raise ValueError("Expression is too complex.")

        if isinstance(node, ast.Expression):
            return visit(node.body, depth + 1)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numeric values are allowed.")

            if abs(node.value) > 1e100:
                raise ValueError("Number is too large.")

            return node.value

        if isinstance(node, ast.Name):
            if node.id in CONSTANTS:
                return CONSTANTS[node.id]

            raise ValueError("Unknown constant.")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in UNARY_OPERATORS:
                raise ValueError("Unsupported unary operator.")

            return UNARY_OPERATORS[op_type](
                visit(node.operand, depth + 1)
            )

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in BINARY_OPERATORS:
                raise ValueError("Unsupported operator.")

            left = visit(node.left, depth + 1)
            right = visit(node.right, depth + 1)

            if op_type is ast.Pow:
                if abs(right) > 100:
                    raise ValueError("Exponent is too large.")

                if abs(left) > 1e50:
                    raise ValueError("Base is too large.")

            result = BINARY_OPERATORS[op_type](left, right)

            if isinstance(result, complex):
                raise ValueError("Complex numbers are not supported.")

            if not math.isfinite(float(result)):
                raise ValueError("Result is not finite.")

            if abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only approved functions are allowed.")

            name = node.func.id

            if name not in FUNCTIONS:
                raise ValueError("Function is not allowed.")

            if node.keywords or len(node.args) > 5:
                raise ValueError("Invalid function arguments.")

            args = [
                visit(arg, depth + 1)
                for arg in node.args
            ]

            result = FUNCTIONS[name](*args)

            if not math.isfinite(float(result)):
                raise ValueError("Result is not finite.")

            return result

        raise ValueError("Unsupported mathematical expression.")

    return visit(tree)


# =========================================================
# HEADER
# =========================================================

st.title("⚡ TOM LAB")
st.subheader("Mathematics • Physics • Pokémon • Scientific Discovery")

st.markdown(
    """
    An interactive environment for exploring mathematical ideas,
    visualising scientific relationships and experimenting with models.
    """
)

st.info(
    "Independent educational project. Not affiliated with or endorsed "
    "by Professor Tom Crawford, Pokémon or their publishers."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔬 Research Console")

researcher = st.sidebar.text_input(
    "Researcher name",
    placeholder="Your name",
)

page = st.sidebar.radio(
    "Choose a laboratory",
    [
        "🏠 Dashboard",
        "🧮 Mathematics Engine",
        "📈 Function Explorer",
        "⚡ Physics Lab",
        "🎮 Pokémon Lab",
        "🎯 Probability Lab",
        "🧠 Challenge Studio",
        "📐 Constants Library",
        "📝 Research Notebook",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Educational simulations. Check assumptions and verify results."
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.success(
        f"Welcome, {researcher.strip() or 'Researcher'}! "
        "Your laboratory is ready."
    )

    st.markdown("## Explore the laboratory")

    c1, c2, c3 = st.columns(3)

    c1.metric("Scientific areas", "4")
    c2.metric("Math functions", len(FUNCTIONS))
    c3.metric("Saved notes", len(st.session_state.notes))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="lab-card">
            <h3>🧮 Mathematics Engine</h3>
            Evaluate mathematical expressions using a restricted,
            safer calculation engine.
            </div>
            <div class="lab-card">
            <h3>📈 Function Explorer</h3>
            Visualise functions and investigate the effects of parameters.
            </div>
            <div class="lab-card">
            <h3>⚡ Physics Lab</h3>
            Explore electrical circuits and Ohm's law.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="lab-card">
            <h3>🎮 Pokémon Lab</h3>
            Investigate selected type interactions and simplified models.
            </div>
            <div class="lab-card">
            <h3>🎯 Probability Lab</h3>
            Explore probability using random experiments.
            </div>
            <div class="lab-card">
            <h3>📝 Research Notebook</h3>
            Record observations and export your notes.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Research principle")

    st.write(
        "A useful scientific model explains its assumptions, "
        "shows its calculations and makes its limitations visible."
    )


# =========================================================
# MATHEMATICS ENGINE
# =========================================================

elif page == "🧮 Mathematics Engine":

    st.header("🧮 Mathematics Engine")

    st.write(
        "Examples: `sqrt(144) + 2*pi`, `sin(pi/2)`, `factorial(5)`"
    )

    st.caption("Trigonometric functions use radians.")

    expression = st.text_input(
        "Mathematical expression",
        value="50 * 3 + sqrt(400)",
        key="expression",
    )

    if st.button("Calculate", key="calculate_math"):

        try:
            result = safe_calculate(expression.strip())

            st.session_state.math_result = {
                "expression": expression,
                "result": result,
                "error": None,
            }

        except Exception as error:
            st.session_state.math_result = {
                "expression": expression,
                "result": None,
                "error": str(error),
            }

    if st.session_state.math_result is not None:

        data = st.session_state.math_result

        if data["error"]:
            st.error(data["error"])
        else:
            st.success(
                f'{data["expression"]} = {data["result"]}'
            )

            st.metric(
                "Numerical result",
                f'{data["result"]:.10g}',
            )


# =========================================================
# FUNCTION EXPLORER
# =========================================================

elif page == "📈 Function Explorer":

    st.header("📈 Interactive Function Explorer")

    st.write(
        "Explore how changing a function parameter affects its graph."
    )

    function_name = st.selectbox(
        "Select a function",
        [
            "Linear: y = ax + b",
            "Quadratic: y = ax² + b",
            "Sine: y = a sin(bx)",
            "Exponential: y = a e^(bx)",
        ],
    )

    a = st.slider("Parameter a", -5.0, 5.0, 1.0, 0.5)
    b = st.slider("Parameter b", -5.0, 5.0, 1.0, 0.5)

    x_min, x_max = st.slider(
        "Horizontal range",
        -20,
        20,
        (-10, 10),
    )

    x = np.linspace(x_min, x_max, 400)

    if function_name == "Linear: y = ax + b":
        y = a * x + b

    elif function_name == "Quadratic: y = ax² + b":
        y = a * x**2 + b

    elif function_name == "Sine: y = a sin(bx)":
        y = a * np.sin(b * x)

    else:
        exponent = np.clip(b * x, -50, 50)
        y = a * np.exp(exponent)

    graph_data = pd.DataFrame(
        {
            "x": x,
            "y": y,
        }
    ).set_index("x")

    st.line_chart(graph_data)

    st.markdown("### What are you seeing?")

    if function_name == "Linear: y = ax + b":
        st.write(
            "`a` controls the slope and `b` controls the vertical intercept."
        )

    elif function_name == "Quadratic: y = ax² + b":
        st.write(
            "`a` controls the opening direction and vertical stretch. "
            "`b` shifts the graph vertically."
        )

    elif function_name == "Sine: y = a sin(bx)":
        st.write(
            "`a` controls amplitude. When `b` is nonzero, the period "
            "is 2π/|b|."
        )

    else:
        st.write(
            "`a` controls vertical scaling. `b` controls exponential "
            "growth or decay."
        )

    st.caption(
        "The graph is sampled numerically over the selected interval."
    )


# =========================================================
# PHYSICS LAB
# =========================================================

elif page == "⚡ Physics Lab":

    st.header("⚡ Electrical Physics Lab")

    st.latex(r"V = I R")

    st.write(
        "Ohm's law relates voltage, current and resistance for an "
        "ohmic component under suitable conditions."
    )

    mode = st.radio(
        "Calculate",
        [
            "Voltage",
            "Current",
            "Resistance",
        ],
        horizontal=True,
    )

    if mode == "Voltage":

        current = st.number_input(
            "Current (A)",
            min_value=0.0,
            value=2.0,
        )

        resistance = st.number_input(
            "Resistance (Ω)",
            min_value=0.0,
            value=10.0,
        )

        if st.button("Calculate voltage"):
            voltage = current * resistance

            st.metric("Voltage", f"{voltage:.4g} V")

            st.write(
                f"V = I × R = {current:g} × "
                f"{resistance:g} = {voltage:g} V"
            )

    elif mode == "Current":

        voltage = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            value=12.0,
        )

        resistance = st.number_input(
            "Resistance (Ω)",
            min_value=0.000001,
            value=4.0,
        )

        if st.button("Calculate current"):
            current = voltage / resistance

            st.metric("Current", f"{current:.4g} A")

            st.write(
                f"I = V / R = {voltage:g} / "
                f"{resistance:g} = {current:g} A"
            )

    else:

        voltage = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            value=12.0,
        )

        current = st.number_input(
            "Current (A)",
            min_value=0.000001,
            value=3.0,
        )

        if st.button("Calculate resistance"):
            resistance = voltage / current

            st.metric("Resistance", f"{resistance:.4g} Ω")

            st.write(
                f"R = V / I = {voltage:g} / "
                f"{current:g} = {resistance:g} Ω"
            )

    st.divider()

    st.markdown("### 📊 Voltage-current relationship")

    resistance_graph = st.slider(
        "Fixed resistance (Ω)",
        1,
        100,
        10,
    )

    currents = np.linspace(0, 10, 101)

    graph = pd.DataFrame(
        {
            "Current (A)": currents,
            "Voltage (V)": currents * resistance_graph,
        }
    ).set_index("Current (A)")

    st.line_chart(graph)


# =========================================================
# POKÉMON LAB
# =========================================================

elif page == "🎮 Pokémon Lab":

    st.header("🎮 Pokémon Mathematics Lab")

    st.write(
        "Use familiar fictional examples to explore mathematical models."
    )

    st.warning(
        "The matchup table below is intentionally limited to four types. "
        "Unlisted interactions default to neutral and may not reflect "
        "the full rules of any Pokémon game."
    )

    types = [
        "Electric",
        "Water",
        "Fire",
        "Grass",
    ]

    chart = {
        ("Electric", "Water"): 2.0,
        ("Electric", "Grass"): 0.5,
        ("Electric", "Electric"): 0.5,
        ("Water", "Fire"): 2.0,
        ("Water", "Grass"): 0.5,
        ("Fire", "Grass"): 2.0,
        ("Fire", "Water"): 0.5,
        ("Grass", "Water"): 2.0,
        ("Grass", "Fire"): 0.5,
    }

    col1, col2 = st.columns(2)

    with col1:
        attacker = st.selectbox(
            "Attacking type",
            types,
        )

    with col2:
        defender = st.selectbox(
            "Defending type",
            types,
        )

    multiplier = chart.get(
        (attacker, defender),
        1.0,
    )

    st.metric(
        "Modelled effectiveness",
        f"{multiplier:g}×",
    )

    if multiplier > 1:
        st.success("Super effective in this limited model!")

    elif multiplier < 1:
        st.warning("Not very effective in this limited model.")

    else:
        st.info("Neutral in this limited model.")

    st.divider()

    st.markdown("### 🧪 Illustrative CP model")

    st.caption(
        "This is an invented educational model, not an official game formula."
    )

    initial_cp = st.number_input(
        "Initial CP (arbitrary units)",
        min_value=0.0,
        value=1200.0,
    )

    growth_factor = st.slider(
        "Illustrative growth factor",
        1.0,
        3.0,
        1.8,
        0.1,
    )

    bonus = st.number_input(
        "Additional bonus (arbitrary units)",
        min_value=0.0,
        value=25.0,
    )

    estimated_cp = initial_cp * growth_factor + bonus

    st.metric(
        "Model output",
        f"{estimated_cp:.2f}",
    )


# =========================================================
# PROBABILITY LAB
# =========================================================

elif page == "🎯 Probability Lab":

    st.header("🎯 Probability & Monte Carlo Lab")

    st.write(
        "Monte Carlo simulation estimates mathematical quantities "
        "using repeated random experiments."
    )

    st.markdown("### 🟣 Estimate π")

    st.write(
        "Random points are sampled in a square surrounding a quarter "
        "circle. The proportion inside the circle estimates π/4."
    )

    trials = st.select_slider(
        "Number of random points",
        options=[
            100,
            500,
            1000,
            5000,
            10000,
            50000,
        ],
        value=5000,
    )

    if st.button("Run Monte Carlo experiment"):

        rng = np.random.default_rng()

        x = rng.random(trials)
        y = rng.random(trials)

        inside = (x**2 + y**2) <= 1

        estimate = 4 * np.mean(inside)

        st.session_state.monte_carlo_result = {
            "trials": trials,
            "estimate": float(estimate),
            "inside": int(np.sum(inside)),
        }

    if st.session_state.monte_carlo_result:

        result = st.session_state.monte_carlo_result

        st.metric(
            "Estimated π",
            f'{result["estimate"]:.6f}',
        )

        st.metric(
            "Actual π",
            f"{math.pi:.6f}",
        )

        st.metric(
            "Absolute error",
            f"{abs(result['estimate'] - math.pi):.6f}",
        )

        st.write(
            f'Points inside quarter circle: {result["inside"]} '
            f'of {result["trials"]}.'
        )

        st.caption(
            "The estimate varies between runs. More samples often "
            "improve accuracy, but do not guarantee a closer estimate "
            "in every individual run."
        )


# =========================================================
# CHALLENGE STUDIO
# =========================================================

elif page == "🧠 Challenge Studio":

    st.header("🧠 Scientific Challenge Studio")

    questions = [
        {
            "question": (
                "A circuit has a voltage of 100 V and resistance of "
                "20 Ω. What is its current?"
            ),
            "hint": "Use I = V/R.",
            "answer": 5.0,
            "solution": "I = 100/20 = 5 A.",
        },
        {
            "question": (
                "What is the volume of a sphere with radius 3 units?"
            ),
            "hint": "Use V = (4/3)πr³.",
            "answer": (4 / 3) * math.pi * 27,
            "solution": (
                "V = (4/3) × π × 3³ = 36π ≈ 113.097 cubic units."
            ),
        },
        {
            "question": "Evaluate sin(π/2) + sqrt(81).",
            "hint": "sin(π/2) = 1 and sqrt(81) = 9.",
            "answer": 10.0,
            "solution": "1 + 9 = 10.",
        },
    ]

    if st.button("🎲 Generate new challenge"):
        st.session_state.challenge_index = random.randrange(
            len(questions)
        )

    if st.session_state.challenge_index is None:
        st.session_state.challenge_index = 0

    question = questions[st.session_state.challenge_index]

    st.markdown("### Problem")

    st.write(question["question"])

    if st.button("💡 Reveal hint"):
        st.info(question["hint"])

    answer_text = st.text_input(
        "Your answer",
        key="answer_text",
    )

    if st.button("Check answer"):

        try:
            submitted = safe_calculate(answer_text.strip())

            if math.isclose(
                float(submitted),
                question["answer"],
                rel_tol=1e-3,
                abs_tol=1e-3,
            ):
                st.success("Correct! Great work.")
            else:
                st.warning(
                    "Not quite. Try again or inspect the solution."
                )

        except Exception:
            st.error(
                "Please enter a valid numerical expression."
            )

    if st.button("📖 Show worked solution"):
        st.info(question["solution"])


# =========================================================
# CONSTANTS LIBRARY
# =========================================================

elif page == "📐 Constants Library":

    st.header("📐 Mathematical Constants Library")

    constants = {
        "Pi (π)": (
            math.pi,
            "Circumference divided by diameter for a circle.",
        ),
        "Euler's number (e)": (
            math.e,
            "A central constant in exponential growth and calculus.",
        ),
        "Golden ratio (φ)": (
            (1 + math.sqrt(5)) / 2,
            "A ratio appearing in several geometric constructions.",
        ),
        "Square root of 2": (
            math.sqrt(2),
            "The diagonal length of a unit square.",
        ),
    }

    selected = st.selectbox(
        "Choose a constant",
        list(constants.keys()),
    )

    value, description = constants[selected]

    st.metric(
        "Approximate value",
        f"{value:.12f}",
    )

    st.write(description)

    st.caption(
        "Displayed decimal values are approximations."
    )


# =========================================================
# RESEARCH NOTEBOOK
# =========================================================

elif page == "📝 Research Notebook":

    st.header("📝 Research Notebook")

    st.write(
        "Record observations, hypotheses, calculations and ideas."
    )

    title = st.text_input(
        "Note title",
        placeholder="Experiment 01",
    )

    content = st.text_area(
        "Your notes",
        height=180,
        placeholder="Write your observations...",
    )

    if st.button("💾 Save note"):

        if not title.strip() or not content.strip():

            st.warning(
                "Enter both a title and note content."
            )

        else:

            st.session_state.notes.append(
                {
                    "title": title.strip(),
                    "content": content.strip(),
                }
            )

            st.success("Note saved for this session.")

    st.divider()

    if st.session_state.notes:

        for index, note in enumerate(
            st.session_state.notes,
            start=1,
        ):

            with st.expander(
                f'{index}. {note["title"]}'
            ):

                st.write(note["content"])

        export_content = "\n\n".join(
            [
                f'TITLE: {note["title"]}\n{note["content"]}'
                for note in st.session_state.notes
            ]
        )

        st.download_button(
            "⬇️ Download notebook (.txt)",
            data=export_content,
            file_name="tom_lab_notebook.txt",
            mime="text/plain",
        )

        if st.button("🗑️ Clear notebook"):

            st.session_state.notes = []

            st.success("Notebook cleared.")

            st.rerun()

    else:

        st.info(
            "Your notebook is empty. Save your first observation above."
        )

    st.caption(
        "Notes remain in the current session. Download them to keep "
        "a permanent copy."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#94a3b8;">
        <p>⚡ TOM LAB</p>
        <p>Independent educational project built with Python and Streamlit</p>
        <p>Mathematics • Physics • Probability • Scientific Exploration</p>
    </div>
    """,
    unsafe_allow_html=True,
)
