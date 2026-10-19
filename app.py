import ast
import math
import operator
import random

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tom Lab | Mathematics & Physics",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Tom Lab")
st.subheader(
    "An Interactive Mathematics, Physics & Pokémon Playground"
)

st.markdown(
    """
    Explore mathematics through experiments, simulations and
    interactive visualisations.

    Inspired by the idea that mathematics can be discovered
    through curiosity, science and playful questions.
    """
)

st.caption(
    "Independent educational project. Not affiliated with "
    "Professor Tom Crawford or any university."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔬 Tom Lab")

page = st.sidebar.radio(
    "Choose your laboratory",
    [
        "🏠 Dashboard",
        "🧮 Mathematics Engine",
        "📈 Function Explorer",
        "⚡ Physics Lab",
        "⚡ Pokémon Lab",
        "🎲 Monte Carlo Lab",
        "🧠 Challenge Studio",
        "📚 Constants Library",
        "📝 Research Notebook"
    ]
)


# ============================================================
# SAFE MATHEMATICS ENGINE
# ============================================================

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
    "factorial": math.factorial,
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def safe_calculate(expression):
    """Evaluate a restricted mathematical expression."""

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("Boolean values are not allowed.")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > 100:
                    raise ValueError("Exponent must be between -100 and 100.")

                if abs(left) > 1e100:
                    raise ValueError("Base is too large.")

            result = ALLOWED_OPERATORS[op_type](left, right)

            if not math.isfinite(float(result)):
                raise ValueError("Result is not finite.")

            if abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Unsupported unary operator.")

            return ALLOWED_OPERATORS[op_type](evaluate(node.operand))

        if isinstance(node, ast.Name):
            if node.id in ALLOWED_CONSTANTS:
                return ALLOWED_CONSTANTS[node.id]

            raise ValueError(f"Unknown constant: {node.id}")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call.")

            name = node.func.id

            if name not in ALLOWED_FUNCTIONS:
                raise ValueError(f"Function not allowed: {name}")

            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")

            args = [evaluate(arg) for arg in node.args]

            if len(args) != 1:
                raise ValueError(
                    "These functions require exactly one argument."
                )

            if name == "factorial":
                value = args[0]

                if (
                    not isinstance(value, int)
                    and not float(value).is_integer()
                ):
                    raise ValueError("Factorial requires an integer.")

                if value < 0 or value > 170:
                    raise ValueError(
                        "Factorial input must be between 0 and 170."
                    )

                args[0] = int(value)

            result = ALLOWED_FUNCTIONS[name](*args)

            if not math.isfinite(float(result)):
                raise ValueError("Result is not finite.")

            return result

        raise ValueError("Unsupported mathematical expression.")

    return evaluate(tree)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("Welcome to Tom Lab! ⚡")

    st.write(
        """
        This laboratory brings together mathematics, physics,
        probability, programming and Pokémon-inspired experiments.

        Choose a section from the sidebar to begin exploring.
        """
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Mathematics", "Explore", "Equations & functions")
    col2.metric("Physics", "Experiment", "Electrical circuits")
    col3.metric("Probability", "Simulate", "Monte Carlo methods")

    st.divider()

    st.subheader("🔍 Featured experiment")

    st.markdown(
        """
        **Can randomness help us estimate π?**

        Monte Carlo methods use random samples to estimate
        mathematical quantities.

        In the Monte Carlo Lab, you can watch random points
        appear inside a square and estimate π by measuring
        how many fall inside a quarter-circle.
        """
    )

    st.info(
        "New challenge: use the same principle to estimate "
        "the volume of a four-dimensional sphere!"
    )


# ============================================================
# MATHEMATICS ENGINE
# ============================================================

elif page == "🧮 Mathematics Engine":

    st.header("🧮 Mathematics Calculation Engine")

    st.write(
        "Calculate expressions using arithmetic and selected "
        "mathematical functions."
    )

    expression = st.text_input(
        "Enter an expression",
        value="50 * 3 + sqrt(400)",
        help="Examples: 2*pi, sqrt(144), sin(pi/2), log10(100)"
    )

    if st.button("Calculate", type="primary"):

        try:
            result = safe_calculate(expression)

            st.success(f"Result: {result}")

        except Exception as error:
            st.error(f"Could not calculate expression: {error}")

    with st.expander("Available operations and functions"):

        st.markdown(
            """
            - Arithmetic: `+`, `-`, `*`, `/`, `**`, `%`
            - Functions: `sqrt`, `sin`, `cos`, `tan`
            - Logarithms: `log`, `log10`
            - Other functions: `exp`, `abs`, `factorial`
            - Constants: `pi`, `e`

            Trigonometric functions use radians.
            """
        )


# ============================================================
# FUNCTION EXPLORER
# ============================================================

elif page == "📈 Function Explorer":

    st.header("📈 Function Explorer")

    function_type = st.selectbox(
        "Choose a function",
        [
            "Linear: ax + b",
            "Quadratic: ax² + bx + c",
            "Sine: a sin(bx)",
            "Exponential: a × exp(bx)"
        ]
    )

    col1, col2, col3 = st.columns(3)

    a = col1.slider("Parameter a", -5.0, 5.0, 1.0, 0.5)
    b = col2.slider("Parameter b", -5.0, 5.0, 1.0, 0.5)
    c = col3.slider("Parameter c", -5.0, 5.0, 0.0, 0.5)

    x = np.linspace(-10, 10, 500)

    if function_type == "Linear: ax + b":
        y = a * x + b
        formula = f"y = {a}x + {b}"

    elif function_type == "Quadratic: ax² + bx + c":
        y = a * x**2 + b * x + c
        formula = f"y = {a}x² + {b}x + {c}"

    elif function_type == "Sine: a sin(bx)":
        y = a * np.sin(b * x)
        formula = f"y = {a} sin({b}x)"

    else:
        y = a * np.exp(np.clip(b * x, -50, 50))
        formula = f"y = {a} exp({b}x)"

    fig, ax = plt.subplots()

    ax.plot(x, y, label=formula)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(formula)
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Change the parameters to explore how the graph changes."
    )


# ============================================================
# PHYSICS LAB
# ============================================================

elif page == "⚡ Physics Lab":

    st.header("⚡ Ohm's Law Laboratory")

    st.latex(r"V = IR")

    st.write(
        "Ohm's law relates voltage, current and resistance."
    )

    mode = st.radio(
        "What would you like to calculate?",
        ["Voltage", "Current", "Resistance"],
        horizontal=True
    )

    if mode == "Voltage":

        current = st.number_input(
            "Current (A)", min_value=0.0, value=2.0
        )

        resistance = st.number_input(
            "Resistance (Ω)", min_value=0.0, value=5.0
        )

        voltage = current * resistance

        st.metric("Voltage", f"{voltage:.4g} V")

    elif mode == "Current":

        voltage = st.number_input(
            "Voltage (V)", min_value=0.0, value=12.0
        )

        resistance = st.number_input(
            "Resistance (Ω)", min_value=0.0, value=4.0
        )

        if resistance > 0:
            current = voltage / resistance
            st.metric("Current", f"{current:.4g} A")
        else:
            st.warning("Resistance must be greater than zero.")

    else:

        voltage = st.number_input(
            "Voltage (V)", min_value=0.0, value=12.0
        )

        current = st.number_input(
            "Current (A)", min_value=0.0, value=3.0
        )

        if current > 0:
            resistance = voltage / current
            st.metric("Resistance", f"{resistance:.4g} Ω")
        else:
            st.warning("Current must be greater than zero.")

    st.divider()

    st.subheader("Explore the voltage-current relationship")

    resistance_graph = st.slider(
        "Resistance (Ω)", 1.0, 100.0, 10.0
    )

    currents = np.linspace(0, 5, 100)
    voltages = resistance_graph * currents

    fig, ax = plt.subplots()

    ax.plot(currents, voltages)
    ax.set_xlabel("Current (A)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(
        f"Ohm's Law: V = {resistance_graph:g}I"
    )
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# POKÉMON LAB
# ============================================================

elif page == "⚡ Pokémon Lab":

    st.header("⚡ Pokémon-Inspired Mathematics Lab")

    st.write(
        """
        Explore mathematical ideas through Pokémon-inspired
        examples. The simplified models below are educational
        illustrations, not official Pokémon game calculations.
        """
    )

    st.subheader("⚡ Illustrative power model")

    voltage = st.slider(
        "Voltage (V)", 1, 240, 12
    )

    current = st.slider(
        "Current (A)", 1, 100, 5
    )

    power = voltage * current

    st.metric("Electrical power", f"{power} W")

    st.latex(r"P = VI")

    st.caption(
        "This is a physics calculation, not a measurement of "
        "an actual Pokémon's electrical output."
    )

    st.divider()

    st.subheader("🎮 Illustrative catch-probability model")

    base_probability = st.slider(
        "Base probability (%)", 1, 100, 30
    )

    ball_multiplier = st.slider(
        "Illustrative ball multiplier", 1.0, 3.0, 1.5
    )

    status_multiplier = st.slider(
        "Illustrative status multiplier", 1.0, 2.0, 1.2
    )

    probability = min(
        100.0,
        base_probability * ball_multiplier * status_multiplier
    )

    st.metric(
        "Model probability",
        f"{probability:.1f}%"
    )

    st.caption(
        "This is a made-up teaching model, not the official "
        "catch-rate formula from any Pokémon game."
    )


# ============================================================
# MONTE CARLO LAB
# ============================================================

elif page == "🎲 Monte Carlo Lab":

    st.header("🎲 Monte Carlo Mathematics Laboratory")

    st.markdown(
        """
        **What is the Monte Carlo method?**

        Monte Carlo methods use random samples to estimate
        mathematical quantities. Instead of calculating an
        answer directly, we simulate many random outcomes
        and use their statistical properties.

        In this laboratory, you can estimate π and the volume
        of a four-dimensional unit sphere.
        """
    )

    experiment = st.radio(
        "Choose an experiment",
        [
            "Estimate π",
            "Estimate the volume of a 4D sphere"
        ],
        horizontal=True
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: ESTIMATE PI
    # --------------------------------------------------------

    if experiment == "Estimate π":

        st.subheader("🥧 Estimating π with random points")

        st.latex(r"\pi \approx 4 \times \frac{N_{\text{inside}}}{N_{\text{total}}}")

        st.markdown(
            """
            Imagine a square with side length 2 and a circle
            of radius 1 centred inside it.

            The square has area 4, while the circle has area π.
            The fraction of random points inside the circle
            therefore approximates π / 4.

            Multiplying that fraction by 4 gives an estimate
            of π.
            """
        )

        n_points = st.slider(
            "Number of random points",
            min_value=100,
            max_value=100000,
            value=5000,
            step=100
        )

        seed = st.number_input(
            "Random seed (use the same value to reproduce results)",
            min_value=0,
            max_value=999999,
            value=42
        )

        if st.button("Run π experiment", type="primary"):

            rng = np.random.default_rng(int(seed))

            points = rng.uniform(
                -1, 1, size=(n_points, 2)
            )

            x = points[:, 0]
            y = points[:, 1]

            inside = x**2 + y**2 <= 1

            estimate = 4 * np.mean(inside)

            absolute_error = abs(estimate - math.pi)

            st.session_state["mc_pi_result"] = {
                "points": points,
                "inside": inside,
                "estimate": estimate,
                "n_points": n_points,
                "seed": int(seed)
            }

        result = st.session_state.get("mc_pi_result")

        if result is not None:

            points = result["points"]
            inside = result["inside"]
            estimate = result["estimate"]
            n_points = result["n_points"]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Estimated π",
                f"{estimate:.6f}"
            )

            col2.metric(
                "Actual π",
                f"{math.pi:.6f}"
            )

            col3.metric(
                "Absolute error",
                f"{abs(estimate - math.pi):.6f}"
            )

            st.subheader("🔵 Visualisation of random points")

            st.write(
                """
                Each point is sampled uniformly from the square.
                Points inside the unit circle are shown separately
                from points outside it.
                """
            )

            # Display only a subset if the experiment is large.
            display_count = min(8000, len(points))

            display_points = points[:display_count]
            display_inside = inside[:display_count]

            fig, ax = plt.subplots()

            ax.scatter(
                display_points[~display_inside, 0],
                display_points[~display_inside, 1],
                s=8,
                alpha=0.55,
                label="Outside circle"
            )

            ax.scatter(
                display_points[display_inside, 0],
                display_points[display_inside, 1],
                s=8,
                alpha=0.55,
                label="Inside circle"
            )

            circle = plt.Circle(
                (0, 0),
                1,
                fill=False,
                linewidth=2,
                label="Unit circle"
            )

            ax.add_patch(circle)

            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(
                f"Monte Carlo π experiment: "
                f"{display_count} displayed points"
            )
            ax.grid(True, alpha=0.25)
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            st.caption(
                f"The chart displays {display_count:,} points. "
                f"The estimate uses all {n_points:,} points."
            )

            st.subheader("📈 How does the estimate converge?")

            cumulative_inside = np.cumsum(inside)
            sample_numbers = np.arange(
                1, len(inside) + 1
            )

            cumulative_estimates = (
                4 * cumulative_inside / sample_numbers
            )

            # Limit the number of plotted points for readability.
            plot_indices = np.unique(
                np.linspace(
                    0,
                    len(sample_numbers) - 1,
                    min(2000, len(sample_numbers)),
                    dtype=int
                )
            )

            fig, ax = plt.subplots()

            ax.plot(
                sample_numbers[plot_indices],
                cumulative_estimates[plot_indices],
                label="Running estimate"
            )

            ax.axhline(
                math.pi,
                linestyle="--",
                label="Actual π"
            )

            ax.set_xlabel("Number of samples")
            ax.set_ylabel("Estimated π")
            ax.set_title("Convergence of the Monte Carlo estimate")
            ax.grid(True, alpha=0.25)
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            st.info(
                """
                **How to interpret the graph**

                The estimate usually fluctuates as more points
                are sampled. With more samples, it often becomes
                more stable, but it is not guaranteed to move
                closer to π after every new point.
                """
            )

            with st.expander("Why does this method work?"):

                st.markdown(
                    """
                    The unit circle has area π, and the surrounding
                    square has area 4.

                    If points are sampled uniformly, the proportion
                    that falls inside the circle estimates the ratio
                    of their areas:

                    π / 4 ≈ points inside / total points.

                    Rearranging gives the Monte Carlo estimate
                    of π.

                    This is a statistical estimate, so different
                    random samples can produce different results.
                    """
                )

    # --------------------------------------------------------
    # EXPERIMENT 2: FOUR-DIMENSIONAL UNIT SPHERE
    # --------------------------------------------------------

    else:

        st.subheader("🌌 The volume of a four-dimensional sphere")

        st.markdown(
            """
            In two dimensions, a circle is the set of points
            satisfying x² + y² ≤ 1.

            In three dimensions, a sphere is described by
            x² + y² + z² ≤ 1.

            In four dimensions, the unit sphere is defined by:

            **x₁² + x₂² + x₃² + x₄² ≤ 1**

            We cannot directly draw a four-dimensional sphere
            in ordinary three-dimensional space. However,
            we can sample random points in a four-dimensional
            box and estimate the fraction that lies inside it.
            """
        )

        st.latex(
            r"V \approx 16 \times "
            r"\frac{N_{\text{inside}}}{N_{\text{total}}}"
        )

        st.markdown(
            """
            Each coordinate is sampled uniformly from [-1, 1].
            The four-dimensional box has volume 2⁴ = 16.

            The proportion of points inside the unit sphere
            estimates the fraction of the box occupied by
            the sphere. Multiplying that fraction by 16
            gives an estimate of the sphere's volume.
            """
        )

        n_4d = st.slider(
            "Number of 4D samples",
            min_value=1000,
            max_value=200000,
            value=20000,
            step=1000
        )

        seed_4d = st.number_input(
            "4D experiment random seed",
            min_value=0,
            max_value=999999,
            value=123,
            key="seed_4d"
        )

        if st.button(
            "Estimate 4D sphere volume",
            type="primary"
        ):

            rng = np.random.default_rng(int(seed_4d))

            samples = rng.uniform(
                -1,
                1,
                size=(n_4d, 4)
            )

            squared_radius = np.sum(samples**2, axis=1)

            inside_4d = squared_radius <= 1

            volume_estimate = (
                16 * np.mean(inside_4d)
            )

            # The exact volume of the 4D unit ball is π² / 2.
            exact_volume = math.pi**2 / 2

            st.session_state["mc_4d_result"] = {
                "samples": samples,
                "inside": inside_4d,
                "estimate": volume_estimate,
                "n_samples": n_4d,
                "seed": int(seed_4d)
            }

        result_4d = st.session_state.get("mc_4d_result")

        if result_4d is not None:

            samples = result_4d["samples"]
            inside_4d = result_4d["inside"]
            volume_estimate = result_4d["estimate"]
            n_4d_actual = result_4d["n_samples"]

            exact_volume = math.pi**2 / 2

            absolute_error = abs(
                volume_estimate - exact_volume
            )

            percentage_error = (
                100 * absolute_error / exact_volume
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Estimated volume",
                f"{volume_estimate:.6f}"
            )

            col2.metric(
                "Exact volume",
                f"{exact_volume:.6f}"
            )

            col3.metric(
                "Absolute error",
                f"{absolute_error:.6f}"
            )

            st.caption(
                f"Relative error: {percentage_error:.3f}%"
            )

            st.latex(
                r"V_{\text{exact}} = \frac{\pi^2}{2}"
            )

            st.success(
                f"{int(np.sum(inside_4d)):,} of "
                f"{n_4d_actual:,} sampled points fell "
                f"inside the 4D unit sphere."
            )

            st.subheader("🔎 A 2D projection of the 4D samples")

            st.markdown(
                """
                The chart below displays only the first two
                coordinates of each four-dimensional sample.

                **Important:** this is a projection, not a
                picture of the complete 4D sphere.

                A point's classification depends on all four
                coordinates. Consequently, a point can appear
                inside the circle in this projection but still
                be outside the 4D sphere because its third and
                fourth coordinates are also part of the distance.
                """
            )

            display_count_4d = min(
                8000,
                len(samples)
            )

            projected = samples[:display_count_4d]
            projected_inside = inside_4d[:display_count_4d]

            fig, ax = plt.subplots()

            ax.scatter(
                projected[~projected_inside, 0],
                projected[~projected_inside, 1],
                s=8,
                alpha=0.45,
                label="Outside 4D sphere"
            )

            ax.scatter(
                projected[projected_inside, 0],
                projected[projected_inside, 1],
                s=8,
                alpha=0.55,
                label="Inside 4D sphere"
            )

            circle = plt.Circle(
                (0, 0),
                1,
                fill=False,
                linewidth=2,
                label="Unit circle in projection"
            )

            ax.add_patch(circle)

            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("First coordinate")
            ax.set_ylabel("Second coordinate")
            ax.set_title("Projection of 4D Monte Carlo samples")
            ax.grid(True, alpha=0.25)
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            st.caption(
                f"The projection shows at most "
                f"{display_count_4d:,} points; the volume "
                f"estimate uses all {n_4d_actual:,} samples."
            )

            st.subheader("📈 Convergence of the 4D volume estimate")

            cumulative_inside_4d = np.cumsum(
                inside_4d
            )

            sample_numbers_4d = np.arange(
                1,
                len(inside_4d) + 1
            )

            cumulative_volumes = (
                16
                * cumulative_inside_4d
                / sample_numbers_4d
            )

            plot_indices_4d = np.unique(
                np.linspace(
                    0,
                    len(sample_numbers_4d) - 1,
                    min(2000, len(sample_numbers_4d)),
                    dtype=int
                )
            )

            fig, ax = plt.subplots()

            ax.plot(
                sample_numbers_4d[plot_indices_4d],
                cumulative_volumes[plot_indices_4d],
                label="Running volume estimate"
            )

            ax.axhline(
                exact_volume,
                linestyle="--",
                label="Exact volume: π² / 2"
            )

            ax.set_xlabel("Number of samples")
            ax.set_ylabel("Estimated volume")
            ax.set_title(
                "Monte Carlo estimation of the 4D sphere"
            )
            ax.grid(True, alpha=0.25)
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            with st.expander("The mathematics behind the result"):

                st.markdown(
                    """
                    The four-dimensional unit sphere is the set

                    x₁² + x₂² + x₃² + x₄² ≤ 1.

                    The surrounding box is [-1, 1]⁴ and has
                    volume 16.

                    If N points are sampled uniformly and
                    N_inside points fall inside the sphere,
                    the Monte Carlo estimate is

                    V ≈ 16 × N_inside / N.

                    The exact volume of a four-dimensional
                    unit sphere is π² / 2, approximately 4.9348.

                    Monte Carlo results vary from run to run.
                    Increasing the number of samples usually
                    improves the estimate statistically, but
                    it does not guarantee a smaller error
                    after every experiment.
                    """
                )

            st.info(
                "Challenge: change the random seed or increase "
                "the sample count. How does the estimate change?"
            )


# ============================================================
# CHALLENGE STUDIO
# ============================================================

elif page == "🧠 Challenge Studio":

    st.header("🧠 Mathematics Challenge Studio")

    challenge = st.selectbox(
        "Choose a challenge",
        [
            "The Square Mystery",
            "The Probability Puzzle",
            "The Fourth Dimension"
        ]
    )

    if challenge == "The Square Mystery":

        st.write(
            "A square has side length 8. What is its area?"
        )

        answer = st.number_input(
            "Your answer",
            value=0,
            step=1,
            key="square_answer"
        )

        if st.button("Check answer"):

            if answer == 64:
                st.success("Correct! Area = 8 × 8 = 64.")
            else:
                st.warning("Try again. Multiply the side by itself.")

    elif challenge == "The Probability Puzzle":

        st.write(
            "A fair six-sided die is rolled. "
            "What is the probability of rolling a 6?"
        )

        answer = st.selectbox(
            "Choose an answer",
            ["1/2", "1/3", "1/6", "1/12"]
        )

        if st.button("Check probability"):

            if answer == "1/6":
                st.success("Correct! One of six outcomes is a 6.")
            else:
                st.warning("A fair die has six equally likely outcomes.")

    else:

        st.write(
            "The exact volume of a four-dimensional unit sphere "
            "is π² / 2. What is its approximate value?"
        )

        st.write(
            f"π² / 2 ≈ {math.pi**2 / 2:.4f}"
        )

        st.info(
            "Try to estimate this value yourself using the "
            "Monte Carlo Lab."
        )


# ============================================================
# CONSTANTS LIBRARY
# ============================================================

elif page == "📚 Constants Library":

    st.header("📚 Mathematical & Physical Constants")

    constants = pd.DataFrame(
        [
            ["π", math.pi, "Circle circumference / diameter"],
            ["e", math.e, "Base of natural logarithms"],
            ["Speed of light", 299792458, "m/s in vacuum"],
            ["Gravitational constant", 6.67430e-11, "m³ kg⁻¹ s⁻²"],
            ["Elementary charge", 1.602176634e-19, "C"],
            ["Planck constant", 6.62607015e-34, "J s"],
        ],
        columns=[
            "Constant",
            "Value",
            "Description"
        ]
    )

    st.dataframe(
        constants,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Physical constants are presented for educational use."
    )


# ============================================================
# RESEARCH NOTEBOOK
# ============================================================

elif page == "📝 Research Notebook":

    st.header("📝 Research Notebook")

    st.write(
        "Record your observations, calculations and ideas."
    )

    notes = st.text_area(
        "Your research notes",
        height=250,
        placeholder=(
            "What did you discover today?\n"
            "Which experiment surprised you?\n"
            "What would you like to test next?"
        )
    )

    if notes.strip():

        st.download_button(
            "Download notes as TXT",
            data=notes,
            file_name="tom_lab_research_notes.txt",
            mime="text/plain"
        )

    else:

        st.caption(
            "Write something above to enable the download."
        )

    st.info(
        "Notes are kept in this page during your current "
        "interaction. Download them if you want to keep a copy."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Tom Lab | An independent educational coding project"
)

st.caption(
    "Mathematical models are provided for learning and "
    "experimentation. Results from random simulations "
    "may vary between runs."
)
