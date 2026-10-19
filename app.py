import ast
import math
import operator
import random

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(page_title="Tom Lab | Maths, Science & Pokémon", page_icon="⚡", layout="wide")

# Independent fan-made educational project. Pokémon artwork is loaded from PokeAPI's public sprite repository.
POKEMON = {
    "Pikachu": (25, "Electric mascot", "A friendly guide for power, ratios and modelling."),
    "Magnemite": (81, "Electricity", "A visual companion for voltage, current and resistance."),
    "Voltorb": (100, "Probability", "A round companion for random sampling and Monte Carlo experiments."),
    "Porygon": (137, "Dimensions", "A digital companion for coordinates and higher-dimensional geometry."),
    "Eevee": (133, "Functions", "A companion for exploring how inputs map to outputs."),
    "Bulbasaur": (1, "Algebra", "A companion for variables, equations and patterns."),
    "Squirtle": (7, "Geometry", "A companion for shapes, measurement and spatial reasoning."),
    "Gastly": (92, "Complex numbers", "A themed guide to the number system and the imaginary unit."),
    "Abra": (63, "Calculus", "A companion for limits, gradients and rates of change."),
    "Metang": (375, "Vectors", "A companion for direction, magnitude and coordinates."),
    "Meowth": (52, "Statistics", "A companion for averages, spread and data interpretation."),
    "Rotom": (479, "Logic & computing", "A companion for algorithms and safe calculations."),
}

def sprite_url(name):
    number = POKEMON[name][0]
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{number}.png"

def pokemon_card(name, width=105):
    number, theme, description = POKEMON[name]
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(sprite_url(name), width=width)
    with col2:
        st.markdown(f"**{name} · {theme}**")
        st.caption(description)

def section_intro(title, pokemon, question, theory, why, formula=None):
    st.title(title)
    pokemon_card(pokemon, 115)
    st.subheader("🔎 Research question")
    st.write(question)
    with st.expander("📚 Learn the theory first", expanded=True):
        st.markdown(theory)
        if formula:
            st.latex(formula)
        st.markdown(f"**Why it matters:** {why}")

def safe_calculate(expression):
    binary = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
    unary = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 12:
                raise ValueError("Exponent too large")
            result = binary[type(node.op)](left, right)
            if not math.isfinite(float(result)) or abs(result) > 1e100:
                raise ValueError("Result outside allowed range")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary:
            return unary[type(node.op)](visit(node.operand))
        raise ValueError("Use numbers and +, -, *, /, %, **, parentheses only.")
    return visit(ast.parse(expression, mode="eval"))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');
.stApp {background: radial-gradient(circle at top right,#17345b 0%,#0b1424 42%,#070b14 100%);}
h1,h2,h3 {font-family: Orbitron, sans-serif;}
[data-testid="stSidebar"] {background: #0a1220;}
.lab-banner {padding: 24px; border: 1px solid #3e8ac7; border-radius: 18px; background: linear-gradient(120deg,rgba(20,65,105,.8),rgba(40,24,80,.75));}
.small-note {padding: 12px 16px; border-left: 4px solid #55c7ff; background: rgba(45,100,150,.15); border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚡ TOM LAB")
st.sidebar.caption("Maths • Science • Pokémon-inspired experiments")
page = st.sidebar.radio("Choose a laboratory", [
    "Command Centre", "Mathematics Foundations", "Algebra & Equations", "Geometry & Trigonometry",
    "Functions & Graphs", "Calculus Explorer", "Probability & Statistics", "Monte Carlo π",
    "4D Sphere Lab", "Vectors & Coordinates", "Pokémon Power Lab", "Physics Lab",
    "Complex Numbers", "Safe Calculator", "Math Arcade", "Glossary & Study Map", "About & Credits"
])
st.sidebar.divider()
st.sidebar.caption("Independent educational fan project")

if page == "Command Centre":
    st.markdown("<div class='lab-banner'><h1>⚡ Welcome to Tom Lab</h1><p>Explore mathematics from first principles through guided lessons, interactive models, graphs and Pokémon-themed visual companions.</p></div>", unsafe_allow_html=True)
    st.write("This is a learning lab, not just a calculator: each topic includes a research question, theory, formulas, an experiment and an interpretation of results.")
    cols = st.columns(4)
    for col, name in zip(cols, ["Pikachu", "Eevee", "Voltorb", "Porygon"]):
        with col:
            st.image(sprite_url(name), width=95)
            st.markdown(f"**{name}**")
            st.caption(POKEMON[name][1])
    st.subheader("🧭 Suggested learning route")
    st.markdown("""
    1. **Foundations:** numbers, ratios, powers and scientific notation.
    2. **Algebra:** variables, expressions, equations and inequalities.
    3. **Geometry & trigonometry:** shapes, angles, area and sine/cosine.
    4. **Functions & calculus:** graphs, gradients, derivatives and accumulation.
    5. **Probability & statistics:** chance, distributions, averages and uncertainty.
    6. **Computational experiments:** estimate π and a four-dimensional sphere volume.
    7. **Applied science:** electrical power, vectors and mathematical modelling.
    """)
    st.info("Use the sidebar to open a lab. Start with the theory expander, then change the controls and interpret the result.")

elif page == "Mathematics Foundations":
    section_intro("🔢 Mathematics Foundations", "Bulbasaur",
        "How do we describe quantities, compare them and communicate very large or very small values?",
        """**Numbers:** natural numbers count objects; integers include negatives; rational numbers can be written as fractions; irrational numbers cannot be expressed as a ratio of integers (for example, √2); real numbers include rational and irrational values.

**Order of operations:** brackets first, then powers/roots, then multiplication/division, then addition/subtraction. For operations of equal priority, work left to right.

**Fractions and ratios:** a fraction a/b means a divided by b (b ≠ 0). A ratio compares quantities. Percent means “per hundred”.

**Powers:** aⁿ means multiplying a by itself n times for positive integer n. Scientific notation writes a number as a × 10ⁿ, with 1 ≤ |a| < 10.""",
        "These tools are the language used by algebra, physics, probability and almost every later topic.", r"\frac{a}{b},\quad p\%=\frac{p}{100},\quad a\times10^n")
    a, b = st.columns(2)
    with a:
        st.subheader("Ratio and percentage explorer")
        part = st.number_input("Part", 0.0, 1000000.0, 18.0, key="found_part")
        whole = st.number_input("Whole (must be positive)", 0.1, 1000000.0, 60.0, key="found_whole")
        st.metric("Part as a percentage", f"{100*part/whole:.2f}%")
        st.caption("Calculation: part ÷ whole × 100.")
    with b:
        st.subheader("Scientific notation")
        value = st.number_input("Enter a non-zero value", min_value=-1e100, max_value=1e100, value=123450.0, format="%.6g")
        if value != 0:
            st.metric("Scientific notation", f"{value:.6e}")
        else:
            st.info("Zero is written as 0; it has no non-zero scientific-notation coefficient.")
    st.subheader("Quick practice")
    st.write("If a research sample contains 15 successes from 50 trials, the observed success percentage is 15 ÷ 50 × 100 = 30%.")

elif page == "Algebra & Equations":
    section_intro("🌱 Algebra & Equations", "Bulbasaur",
        "How can a letter represent an unknown quantity, and how do we find its value?",
        """An **expression** combines numbers, variables and operations; an **equation** says two expressions are equal. A variable is a symbol whose value may be unknown or change.

To solve an equation, perform the same valid operation on both sides so equality is preserved. For a linear equation ax + b = c, with a ≠ 0, subtract b and divide by a.

An inequality (<, >, ≤, ≥) compares quantities. Multiplying or dividing an inequality by a negative number reverses its direction.""",
        "Algebra turns a specific calculation into a general method that works for many values.", r"ax+b=c\quad\Rightarrow\quad x=\frac{c-b}{a}")
    st.subheader("Solve a linear equation")
    a = st.number_input("Coefficient a (not zero)", min_value=-100.0, max_value=100.0, value=3.0, key="alg_a")
    b = st.number_input("Constant b", min_value=-1000.0, max_value=1000.0, value=5.0, key="alg_b")
    c = st.number_input("Right-hand side c", min_value=-1000.0, max_value=1000.0, value=20.0, key="alg_c")
    if a != 0:
        x = (c-b)/a
        st.success(f"Solution: x = {x:g}")
        st.write(f"1. Start with {a:g}x + ({b:g}) = {c:g}.")
        st.write(f"2. Subtract {b:g} from both sides: {a:g}x = {c-b:g}.")
        st.write(f"3. Divide both sides by {a:g}: x = {x:g}.")
        st.write(f"Check: left-hand side = {a*x+b:g}; right-hand side = {c:g}.")
    else:
        st.warning("The coefficient a must not be zero for this solver.")
    st.subheader("Quadratic equations")
    st.markdown("A quadratic has the form **ax² + bx + c = 0**. The discriminant Δ = b² − 4ac indicates the number of real roots: Δ > 0 gives two, Δ = 0 one repeated root, and Δ < 0 no real roots.")
    qa = st.number_input("Quadratic a", min_value=-100.0, max_value=100.0, value=1.0, key="quad_a")
    qb = st.number_input("Quadratic b", min_value=-1000.0, max_value=1000.0, value=-3.0, key="quad_b")
    qc = st.number_input("Quadratic c", min_value=-1000.0, max_value=1000.0, value=2.0, key="quad_c")
    if qa != 0:
        disc = qb*qb-4*qa*qc
        st.metric("Discriminant Δ", f"{disc:g}")
        if disc >= 0:
            r1=(-qb+math.sqrt(disc))/(2*qa); r2=(-qb-math.sqrt(disc))/(2*qa)
            st.write(f"Real roots: x₁ = {r1:.6g}, x₂ = {r2:.6g}")
        else:
            st.write("There are no real roots; the solutions are complex numbers.")

elif page == "Geometry & Trigonometry":
    section_intro("📐 Geometry & Trigonometry", "Squirtle",
        "How can lengths, areas, angles and periodic relationships be calculated?",
        """**Perimeter** is the distance around a 2D shape. **Area** measures the region inside it. **Volume** measures 3D space.

For a rectangle, A = length × width. For a triangle, A = ½ × base × height. For a circle, circumference C = 2πr and area A = πr².

In a right triangle, the Pythagorean theorem is a² + b² = c², where c is the hypotenuse. For an acute angle θ, sin θ = opposite/hypotenuse, cos θ = adjacent/hypotenuse and tan θ = opposite/adjacent.""",
        "Geometry connects visual shapes to exact measurements; trigonometry is used in navigation, waves, engineering and graphics.", r"a^2+b^2=c^2,\quad A_{\text{circle}}=\pi r^2")
    st.subheader("Shape calculator")
    shape = st.selectbox("Shape", ["Rectangle", "Triangle", "Circle", "Right triangle"])
    if shape == "Rectangle":
        length=st.number_input("Length", min_value=0.0, value=8.0, key="rect_l")
        width=st.number_input("Width", min_value=0.0, value=4.0, key="rect_w")
        st.metric("Area", f"{length*width:.4g} square units")
        st.metric("Perimeter", f"{2*(length+width):.4g} units")
    elif shape == "Triangle":
        base=st.number_input("Base", min_value=0.0, value=8.0, key="tri_b")
        height=st.number_input("Perpendicular height", min_value=0.0, value=5.0, key="tri_h")
        st.metric("Area", f"{0.5*base*height:.4g} square units")
    elif shape == "Circle":
        radius=st.number_input("Radius", min_value=0.0, value=3.0, key="circ_r")
        st.metric("Area", f"{math.pi*radius**2:.5g} square units")
        st.metric("Circumference", f"{2*math.pi*radius:.5g} units")
    else:
        side_a=st.number_input("Leg a", min_value=0.0, value=3.0, key="pyth_a")
        side_b=st.number_input("Leg b", min_value=0.0, value=4.0, key="pyth_b")
        st.metric("Hypotenuse c", f"{math.hypot(side_a,side_b):.5g} units")
    st.subheader("Trigonometry wave explorer")
    angle=st.slider("Angle θ (degrees)", 0, 360, 45)
    rad=math.radians(angle)
    c1,c2,c3=st.columns(3)
    c1.metric("sin θ", f"{math.sin(rad):.4f}")
    c2.metric("cos θ", f"{math.cos(rad):.4f}")
    c3.metric("tan θ", "undefined" if abs(math.cos(rad))<1e-9 else f"{math.tan(rad):.4f}")
    x=np.linspace(0, 2*np.pi, 500)
    fig,ax=plt.subplots(); ax.plot(x,np.sin(x),label="sin(x)"); ax.plot(x,np.cos(x),label="cos(x)"); ax.grid(True,alpha=.3); ax.legend(); ax.set_xlabel("Angle (radians)"); ax.set_ylabel("Value")
    st.pyplot(fig); plt.close(fig)

elif page == "Functions & Graphs":
    section_intro("📈 Functions & Graphs", "Eevee",
        "How does a function transform an input into an output, and what can its graph tell us?",
        """A **function** assigns each allowed input x exactly one output f(x). The **domain** is the set of allowed inputs; the **range** is the set of outputs produced.

The graph plots points (x, f(x)). A zero or root is an x-value where f(x) = 0. The y-intercept is f(0). A linear function has a constant gradient; a quadratic often makes a parabola. Sine and cosine are periodic functions.""",
        "Functions model relationships in motion, population growth, sound, finance and scientific measurements.", r"y=f(x),\quad m=\frac{\Delta y}{\Delta x}")
    choice=st.selectbox("Choose a function", ["x²", "x³", "2x + 1", "sin(x)", "cos(x)", "eˣ", "sqrt(|x|)"])
    low=st.slider("Minimum x", -20, -1, -10); high=st.slider("Maximum x", 1, 20, 10)
    x=np.linspace(low,high,600)
    if choice=="x²": y=x**2; formula=r"f(x)=x^2"
    elif choice=="x³": y=x**3; formula=r"f(x)=x^3"
    elif choice=="2x + 1": y=2*x+1; formula=r"f(x)=2x+1"
    elif choice=="sin(x)": y=np.sin(x); formula=r"f(x)=\sin(x)"
    elif choice=="cos(x)": y=np.cos(x); formula=r"f(x)=\cos(x)"
    elif choice=="eˣ": y=np.exp(np.clip(x,-50,50)); formula=r"f(x)=e^x"
    else: y=np.sqrt(np.abs(x)); formula=r"f(x)=\sqrt{|x|}"
    st.latex(formula)
    fig,ax=plt.subplots(); ax.plot(x,y); ax.axhline(0,linewidth=1); ax.axvline(0,linewidth=1); ax.grid(True,alpha=.3); ax.set_xlabel("x"); ax.set_ylabel("f(x)"); ax.set_title(f"Graph of {choice}")
    st.pyplot(fig); plt.close(fig)
    xv=st.number_input("Evaluate the function at x =", min_value=float(low), max_value=float(high), value=1.0)
    if choice=="x²": out=xv**2
    elif choice=="x³": out=xv**3
    elif choice=="2x + 1": out=2*xv+1
    elif choice=="sin(x)": out=math.sin(xv)
    elif choice=="cos(x)": out=math.cos(xv)
    elif choice=="eˣ": out=math.exp(max(-50,min(50,xv)))
    else: out=math.sqrt(abs(xv))
    st.success(f"f({xv:g}) = {out:.6g}")

elif page == "Calculus Explorer":
    section_intro("🧮 Calculus Explorer", "Abra",
        "How can mathematics describe instantaneous change and accumulated quantity?",
        """**Limits** describe what a function approaches as x approaches a value. A **derivative** measures instantaneous rate of change; geometrically, it is the gradient of the tangent line. An **integral** can represent accumulated quantity or area under a curve.

For powers, the power rule says d(xⁿ)/dx = n xⁿ⁻¹. Thus the derivative of x² is 2x. For a small change h, the difference quotient [f(x+h)−f(x)]/h approximates the derivative; as h approaches zero, it approaches the exact derivative when the derivative exists.""",
        "Calculus is central to motion, optimisation, growth, engineering and physical laws.", r"f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}")
    st.subheader("Derivative of f(x) = x²")
    x0=st.slider("Point x₀", -5.0, 5.0, 2.0, .25)
    h=st.select_slider("Step size h", options=[1.0,.5,.1,.01,.001], value=.1)
    f=lambda z:z*z
    estimate=(f(x0+h)-f(x0))/h
    exact=2*x0
    c1,c2=st.columns(2); c1.metric("Difference quotient", f"{estimate:.6f}"); c2.metric("Exact derivative 2x₀", f"{exact:.6f}")
    st.write("As h gets smaller, the secant-line gradient generally approaches the tangent-line gradient, here 2x₀.")
    xx=np.linspace(-5,5,300); yy=xx**2; tangent=exact*(xx-x0)+f(x0)
    fig,ax=plt.subplots(); ax.plot(xx,yy,label="f(x)=x²"); ax.plot(xx,tangent,label="Tangent at x₀"); ax.scatter([x0],[f(x0)]); ax.grid(True,alpha=.3); ax.legend(); st.pyplot(fig); plt.close(fig)
    st.subheader("Numerical area under x²")
    upper=st.slider("Upper integration limit", 1.0, 5.0, 3.0, .5)
    samples=st.slider("Rectangles for approximation", 10, 500, 100, 10)
    dx=upper/samples; xs=np.arange(samples)*dx; area=float(np.sum(xs**2)*dx); exact_area=upper**3/3
    c1,c2=st.columns(2); c1.metric("Rectangle estimate", f"{area:.5f}"); c2.metric("Exact integral", f"{exact_area:.5f}")
    st.caption("Left-endpoint rectangles approximate the area. Increasing the number of rectangles generally improves this approximation.")

elif page == "Probability & Statistics":
    section_intro("🎲 Probability & Statistics", "Meowth",
        "How do we describe uncertainty, summarise data and distinguish a pattern from random variation?",
        """**Probability** ranges from 0 (impossible) to 1 (certain). For equally likely outcomes, P(A) = favourable outcomes ÷ total outcomes.

**Mean** is the arithmetic average. **Median** is the middle value after sorting. **Range** is max − min. **Standard deviation** describes typical spread around the mean.

A sample is used to learn about a larger population. Random samples vary, so estimates have uncertainty. A larger sample often gives a more stable estimate, but does not automatically remove bias.""",
        "Statistics helps interpret experiments, polls, medicine, sports and scientific evidence.", r"P(A)=\frac{\text{favourable outcomes}}{\text{all equally likely outcomes}}")
    st.subheader("Roll a virtual die")
    rolls=st.slider("Number of rolls", 10, 5000, 500, 10)
    if st.button("Roll die"):
        results=np.random.randint(1,7,size=rolls)
        st.session_state["die_results"]=results
    if "die_results" in st.session_state:
        results=st.session_state["die_results"]
        counts=np.bincount(results,minlength=7)[1:]
        observed=counts/len(results)
        st.write(f"Observed rolls: {len(results)}")
        fig,ax=plt.subplots(); ax.bar(np.arange(1,7),observed); ax.axhline(1/6,linestyle="--",label="Theoretical probability 1/6"); ax.set_xlabel("Die face"); ax.set_ylabel("Observed proportion"); ax.legend(); st.pyplot(fig); plt.close(fig)
        st.caption("For a fair die, each face has probability 1/6. Random variation means observed proportions need not be exactly equal.")
    st.subheader("Enter data for summary statistics")
    raw=st.text_input("Comma-separated numbers", "4, 7, 7, 8, 9, 10, 15")
    try:
        vals=np.array([float(v.strip()) for v in raw.split(",") if v.strip()])
        if len(vals):
            c1,c2,c3,c4=st.columns(4); c1.metric("Count",str(len(vals))); c2.metric("Mean",f"{np.mean(vals):.4g}"); c3.metric("Median",f"{np.median(vals):.4g}"); c4.metric("Std. dev.",f"{np.std(vals):.4g}")
    except ValueError:
        st.error("Please enter only numbers separated by commas.")

elif page == "Monte Carlo π":
    section_intro("🎯 Monte Carlo π Laboratory", "Voltorb",
        "Can random points estimate π without measuring a circle's circumference?",
        """Imagine a unit square with corners (0,0) and (1,1), containing a quarter-circle of radius 1. The square's area is 1 and the quarter-circle's area is π/4. If points are uniformly random, the fraction that fall inside estimates the area ratio.

If N points are sampled and M fall inside, M/N ≈ (π/4)/1. Rearranging gives π ≈ 4M/N. This is a Monte Carlo method: a numerical estimate based on random sampling.""",
        "It demonstrates how geometry, probability and computation can work together. Estimates fluctuate and converge gradually, not perfectly at every run.", r"\pi\approx4\frac{M}{N}")
    trials=st.slider("Random points",100,20000,3000,100)
    if st.button("Run Monte Carlo π experiment"):
        x=np.random.random(trials); y=np.random.random(trials); inside=x*x+y*y<=1
        st.session_state["pi_data"]=(x,y,inside,trials)
    if "pi_data" in st.session_state:
        x,y,inside,n=st.session_state["pi_data"]; m=int(inside.sum()); estimate=4*m/n
        c1,c2,c3=st.columns(3); c1.metric("Estimated π",f"{estimate:.6f}"); c2.metric("True π",f"{math.pi:.6f}"); c3.metric("Absolute error",f"{abs(math.pi-estimate):.6f}")
        st.latex(rf"\pi\approx4\times\frac{{{m}}}{{{n}}}={estimate:.6f}")
        fig,ax=plt.subplots(); ax.scatter(x[inside],y[inside],s=5,label="Inside quarter-circle"); ax.scatter(x[~inside],y[~inside],s=5,label="Outside"); t=np.linspace(0,np.pi/2,300); ax.plot(np.cos(t),np.sin(t),linewidth=2); ax.set_aspect("equal"); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.legend(); ax.set_xlabel("x"); ax.set_ylabel("y"); st.pyplot(fig); plt.close(fig)
        st.markdown(f"**Interpretation:** {m} of {n} points landed inside. The observed fraction is {m/n:.4f}; multiplying it by 4 gives the estimate {estimate:.6f}.")
        st.warning("The result is an estimate, not an exact calculation. Re-running creates a new random sample.")

elif page == "4D Sphere Lab":
    section_intro("🧊 Four-Dimensional Sphere Laboratory", "Porygon",
        "How can Monte Carlo sampling estimate the volume of a shape in four dimensions?",
        """A 4D point has four coordinates (x₁,x₂,x₃,x₄). The unit 4D sphere consists of points whose squared coordinates sum to at most 1. It sits inside the 4D hypercube [-1,1]⁴, whose volume is 2⁴ = 16.

If N uniformly sampled points are in the hypercube and M are inside the sphere, then M/N estimates the fraction of hypercube volume occupied by the sphere. Therefore V₄ ≈ 16M/N. The exact unit 4-ball volume is π²/2 ≈ 4.9348.

A 2D scatter plot can only show a projection of the points; the inside/outside test must still use all four coordinates.""",
        "Higher-dimensional geometry appears in probability, data science, physics and optimisation; Monte Carlo gives a way to estimate volumes that are hard to visualise.", r"V_4\approx16\frac{M}{N},\qquad V_4=\frac{\pi^2}{2}")
    trials=st.slider("4D sample points",1000,50000,10000,1000)
    if st.button("Estimate 4D volume"):
        pts=np.random.uniform(-1,1,size=(trials,4)); inside=np.sum(pts**2,axis=1)<=1
        st.session_state["sphere_data"]=(pts,inside,trials)
    if "sphere_data" in st.session_state:
        pts,inside,n=st.session_state["sphere_data"]; m=int(inside.sum()); estimate=16*m/n; exact=math.pi**2/2
        c1,c2,c3=st.columns(3); c1.metric("Estimated volume",f"{estimate:.5f}"); c2.metric("Exact volume",f"{exact:.5f}"); c3.metric("Absolute error",f"{abs(estimate-exact):.5f}")
        st.latex(rf"V_4\approx16\times\frac{{{m}}}{{{n}}}={estimate:.5f}")
        fig,ax=plt.subplots(); ax.scatter(pts[inside,0],pts[inside,1],s=5,label="Inside (all 4 coordinates)"); ax.scatter(pts[~inside,0],pts[~inside,1],s=5,label="Outside"); ax.set_xlabel("Coordinate x₁"); ax.set_ylabel("Coordinate x₂"); ax.set_title("2D projection of 4D samples"); ax.legend(); st.pyplot(fig); plt.close(fig)
        st.info("This picture is only a 2D projection. A point is classified using x₁² + x₂² + x₃² + x₄² ≤ 1, not only the two plotted coordinates.")

elif page == "Vectors & Coordinates":
    section_intro("🧭 Vectors & Coordinates", "Metang",
        "How do we represent position, direction and magnitude mathematically?",
        """A coordinate such as (x,y) identifies a point in a 2D plane. A **vector** represents a directed quantity with magnitude and direction. In 2D, v = (a,b) has magnitude |v| = √(a²+b²).

Vectors can be added component-wise: (a,b)+(c,d)=(a+c,b+d). Scaling by k gives (ka,kb). The dot product (a,b)·(c,d)=ac+bd can help describe the angle between vectors.""",
        "Vectors model displacement, velocity, forces, graphics and movement in space.", r"\lVert(a,b)\rVert=\sqrt{a^2+b^2},\quad \mathbf{u}\cdot\mathbf{v}=u_xv_x+u_yv_y")
    c1,c2=st.columns(2)
    with c1:
        vx=st.number_input("Vector v x-component",-100.0,100.0,3.0,key="vx"); vy=st.number_input("Vector v y-component",-100.0,100.0,4.0,key="vy")
    with c2:
        wx=st.number_input("Vector w x-component",-100.0,100.0,1.0,key="wx"); wy=st.number_input("Vector w y-component",-100.0,100.0,2.0,key="wy")
    st.metric("Magnitude of v",f"{math.hypot(vx,vy):.5g}"); st.metric("Dot product v · w",f"{vx*wx+vy*wy:.5g}")
    fig,ax=plt.subplots(); ax.quiver(0,0,vx,vy,angles="xy",scale_units="xy",scale=1,label="v"); ax.quiver(0,0,wx,wy,angles="xy",scale_units="xy",scale=1,label="w"); lim=max(5,abs(vx),abs(vy),abs(wx),abs(wy))+1; ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.grid(True,alpha=.3); ax.set_aspect("equal"); ax.legend(); st.pyplot(fig); plt.close(fig)

elif page == "Pokémon Power Lab":
    section_intro("⚡ Pokémon Power Laboratory", "Pikachu",
        "Under a fictional model, how many Pokémon would be needed to power a lightbulb?",
        """Electrical power is the rate at which energy is transferred. It is measured in watts (W), where 1 W = 1 joule per second. If a device needs P watts and each Pokémon is assigned a fictional output p watts, a simple ideal model estimates P/p Pokémon.

Since we cannot use a fraction of a Pokémon, round upward: N = ceil(P/p). This model ignores conversion losses, storage, changing output and real-world safety; Pokémon power values here are fictional assumptions, not measured facts.""",
        "This is an example of mathematical modelling: state assumptions, calculate from them, then discuss how realistic the assumptions are.", r"N=\left\lceil\frac{P_{\text{bulb}}}{P_{\text{per Pokémon}}}\right\rceil")
    st.image(sprite_url("Pikachu"),width=150,caption="Pikachu — fictional model companion")
    bulb=st.number_input("Lightbulb power (W)",1.0,100000.0,60.0,step=1.0)
    per=st.number_input("Assumed output per Pokémon (W)",0.1,100000.0,10.0,step=1.0)
    number=math.ceil(bulb/per)
    st.metric("Pokémon needed in this model",str(number))
    st.latex(rf"N=\left\lceil\frac{{{bulb:g}}}{{{per:g}}}\right\rceil={number}")
    st.markdown(f"**Step 1:** The bulb requires {bulb:g} W. **Step 2:** The model assigns {per:g} W to each Pokémon. **Step 3:** {bulb:g} ÷ {per:g} = {bulb/per:.3f}. **Step 4:** Round up to {number} whole Pokémon.")
    st.warning("Educational fiction only: Pokémon do not have scientifically measured wattage, and this is not an engineering recommendation.")

elif page == "Physics Lab":
    section_intro("🔌 Physics Laboratory", "Magnemite",
        "How are voltage, current, resistance and electrical power related in a simple circuit?",
        """Voltage V is energy transferred per unit charge; current I is charge flow per second; resistance R describes opposition to current. For an ideal ohmic component, Ohm's law is V = IR.

Electrical power is P = VI. Combining this with Ohm's law gives P = I²R and P = V²/R for an ideal resistor. Units: voltage in volts (V), current in amperes (A), resistance in ohms (Ω), power in watts (W). Real circuits have limits and should be handled safely.""",
        "These relationships are foundational in electronics, energy use and electrical engineering.", r"V=IR,\qquad P=VI=I^2R=\frac{V^2}{R}")
    st.subheader("Ohm's law calculator")
    resistance=st.number_input("Resistance R (Ω)",0.1,100000.0,10.0)
    current=st.number_input("Current I (A)",0.0,10000.0,2.0)
    voltage=resistance*current; power=voltage*current
    c1,c2=st.columns(2); c1.metric("Voltage V = IR",f"{voltage:.4g} V"); c2.metric("Power P = VI",f"{power:.4g} W")
    st.write(f"Substitution: V = {resistance:g} × {current:g} = {voltage:g} V. Then P = {voltage:g} × {current:g} = {power:g} W.")
    st.warning("This is a simplified educational calculation, not a guide to building or modifying a real electrical circuit.")

elif page == "Complex Numbers":
    section_intro("🌀 Complex Numbers", "Gastly",
        "What happens when an equation has no real-number solution, such as x² = −1?",
        """The imaginary unit i is defined by i² = −1. A complex number has the form z = a + bi, where a is the real part and b is the imaginary part. Complex numbers can be represented as points (a,b) in a plane.

The modulus is |z| = √(a²+b²). Adding complex numbers adds their real and imaginary parts separately. Complex numbers are useful in electrical engineering, signal processing and many areas of mathematics.""",
        "They extend the real number system so polynomial equations can be solved more generally.", r"z=a+bi,\qquad |z|=\sqrt{a^2+b^2},\qquad i^2=-1")
    real=st.number_input("Real part a",-100.0,100.0,3.0,key="complex_a")
    imag=st.number_input("Imaginary part b",-100.0,100.0,4.0,key="complex_b")
    st.metric("Complex number",f"{real:g} {'+' if imag>=0 else '−'} {abs(imag):g}i")
    st.metric("Modulus",f"{math.hypot(real,imag):.5g}")
    fig,ax=plt.subplots(); ax.axhline(0,linewidth=1); ax.axvline(0,linewidth=1); ax.scatter([real],[imag]); ax.plot([0,real],[0,imag],linestyle="--"); ax.set_xlabel("Real axis"); ax.set_ylabel("Imaginary axis"); ax.grid(True,alpha=.3); ax.set_aspect("equal",adjustable="datalim"); st.pyplot(fig); plt.close(fig)

elif page == "Safe Calculator":
    section_intro("🧮 Safe Calculator", "Rotom",
        "How can we calculate arithmetic expressions while restricting the allowed operations?",
        """This calculator parses an expression and allows only numeric constants, parentheses, and basic arithmetic operators. It does not execute arbitrary Python code. Use ** for powers (for example, 2**5). Division by zero and invalid expressions will show an error.""",
        "Learning to separate data from executable code is a useful habit in programming and computational mathematics.")
    expr=st.text_input("Arithmetic expression", "50 * 3 + 20")
    if st.button("Calculate expression"):
        try: st.success(f"Result = {safe_calculate(expr)}")
        except Exception: st.error("Could not calculate this expression. Check the syntax and use only allowed arithmetic operations.")

elif page == "Math Arcade":
    section_intro("🧠 Math Arcade", "Eevee",
        "Can you apply a mathematical idea, then explain why the answer is correct?",
        """A useful problem-solving routine is: (1) identify what is known, (2) choose a rule or model, (3) calculate carefully, (4) check whether the result makes sense. A correct answer is stronger when you can explain the reasoning.""",
        "Retrieval practice helps you find which concepts you understand and which need more revision.")
    quiz=[
      ("12 × 8 = ?",["86","96","108","88"],"96","12 × 8 = 12 × (4 × 2) = 48 × 2 = 96."),
      ("Approximate π to 2 decimal places?",["2.71","3.14","1.41","4.00"],"3.14","π ≈ 3.14159, which rounds to 3.14."),
      ("Derivative of x²?",["x","2x","x³","2"],"2x","By the power rule, d(xⁿ)/dx = nxⁿ⁻¹, so d(x²)/dx = 2x."),
      ("A fair die: probability of rolling a 6?",["1/2","1/3","1/6","1/12"],"1/6","One of the six equally likely faces is a 6."),
      ("Right triangle legs are 3 and 4. Hypotenuse?",["5","6","7","12"],"5","Pythagoras: c = √(3²+4²) = √25 = 5."),
      ("If y = 2x + 1 and x = 4, y = ?",["7","8","9","10"],"9","Substitute x = 4: y = 2(4) + 1 = 9.")]
    if "quiz_index" not in st.session_state: st.session_state.quiz_index=0
    if "quiz_score" not in st.session_state: st.session_state.quiz_score=0
    idx=st.session_state.quiz_index
    if idx < len(quiz):
        q,opts,ans,explain=quiz[idx]; st.progress(idx/len(quiz)); st.markdown(f"**Question {idx+1} of {len(quiz)}**"); st.subheader(q)
        choice=st.radio("Choose one",opts,key=f"quiz_{idx}")
        if st.button("Submit answer",key=f"submit_{idx}"):
            if choice==ans: st.session_state.quiz_score+=1; st.success("Correct!")
            else: st.info(f"Correct answer: {ans}")
            st.write(explain); st.session_state.quiz_index+=1; st.rerun()
    else:
        st.success(f"Final score: {st.session_state.quiz_score}/{len(quiz)}")
        if st.button("Restart quiz"):
            st.session_state.quiz_index=0; st.session_state.quiz_score=0; st.rerun()

elif page == "Glossary & Study Map":
    st.title("📚 Glossary & Study Map")
    pokemon_card("Meowth",100)
    terms={
      "Algebra":"Using symbols and operations to represent quantities and relationships.",
      "Coefficient":"A number multiplying a variable, such as 3 in 3x.",
      "Domain":"The set of input values for which a function is defined.",
      "Derivative":"The instantaneous rate of change of a function, where it exists.",
      "Integral":"A mathematical tool for accumulation; definite integrals can represent signed area.",
      "Mean":"The sum of data values divided by the number of values.",
      "Median":"The middle value in sorted data (or the mean of the two middle values for an even count).",
      "Monte Carlo method":"A numerical method using random sampling to estimate a quantity.",
      "Probability":"A numerical measure of how likely an event is, between 0 and 1.",
      "Vector":"A quantity represented by components, with magnitude and direction.",
      "Volume":"A measure of three-dimensional or higher-dimensional space occupied by a region.",
      "Watt":"A unit of power equal to one joule per second.",
      "Standard deviation":"A measure of how spread out values are around their mean.",
      "Model assumption":"A simplifying statement used to make a mathematical model workable; assumptions limit conclusions."
    }
    for term,definition in terms.items():
        with st.expander(term): st.write(definition)
    st.subheader("Suggested revision order")
    st.markdown("Number skills → algebra → geometry and trigonometry → functions → calculus → probability and statistics → vectors and complex numbers → computational modelling.")

elif page == "About & Credits":
    st.title("ℹ️ About Tom Lab")
    pokemon_card("Pikachu",100)
    st.markdown("""Tom Lab is an independent, fan-made educational project that explores mathematics and science through interactive lessons and Pokémon-inspired visual themes. It is intended for learning, experimentation and mathematical discussion.""")
    st.subheader("Project principles")
    st.markdown("- Explain the theory before showing a result.\n- Make assumptions explicit.\n- Distinguish exact values from numerical estimates.\n- Explain uncertainty and limitations.\n- Use interactive controls to encourage exploration.")
    st.warning("This project is not an official Professor Tom Crawford project and is not affiliated with or endorsed by Professor Tom Crawford, Nintendo, The Pokémon Company, or their affiliates. Pokémon names and sprite artwork belong to their respective rights holders. The project uses sprites from the PokeAPI sprite repository and is intended as an independent educational fan project.")

st.sidebar.divider()
st.sidebar.caption("Tom Lab · Independent educational project")
