import streamlit as st
import math
import random

st.set_page_config(page_title="Professor Tom Crawford Lab", page_icon="⚡", layout="wide")

st.title("⚡ Professor Tom Crawford | Advanced Math & Pokémon Research Lab ⚡")
st.markdown("### *Interactive Academic Simulation Center: 'Volts, Voltorbs & Variables'*")
st.markdown("---")

# Access & Security Protocol
st.sidebar.header("🔬 Access & Security")
researcher_name = st.sidebar.text_input("Researcher Name / Title:", placeholder="e.g. Researcher Şeyma")
agree_terms = st.sidebar.checkbox("I agree to the Professor Tom Crawford lab safety protocols.")

if not researcher_name or not agree_terms:
    st.warning("⚠️ Please enter your name and agree to the safety protocol in the sidebar!")
    st.stop()
else:
    st.success(f"🎉 Welcome, {researcher_name}. Systems are online!")

st.markdown("---")

# Module 1: Universal Mathematics Calculation Engine
st.header("🧮 1. Universal Mathematics Calculation Engine")
math_input = st.text_input("Mathematical Expression / Equation", value="50 * 3 + sqrt(400)")
if st.button("⚡ Calculate Expression"):
    try:
        safe_dict = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e,
            "factorial": math.factorial, "abs": abs, "round": round,
            "pow": pow, "floor": math.floor, "ceil": math.ceil,
        }
        result = eval(math_input.strip(), {"__builtins__": {}}, safe_dict)
        st.success(f"🌐 [Universal Math Result]:\n{math_input} = {result}")
    except Exception as e:
        st.error(f"⚠️ Expression Error: Enter a valid format. Error: {str(e)}")

st.markdown("---")

# Module 2: Pokémon Type Effectiveness & Damage Matrix
st.header("🧪 2. Pokémon Type Effectiveness & Damage Matrix")
col1, col2 = st.columns(2)
with col1:
    attacker_type = st.selectbox("Attacker Type", ["Electric", "Water", "Fire", "Grass"])
with col2:
    defender_type = st.selectbox("Defender Type", ["Electric", "Water", "Fire", "Grass"])

if st.button("🔍 Calculate Type Interaction"):
    chart = {
        ("Electric", "Water"): 2.0, ("Electric", "Grass"): 0.5, ("Electric", "Fire"): 1.0,
        ("Water", "Fire"): 2.0, ("Water", "Electric"): 1.0, ("Water", "Grass"): 0.5,
        ("Fire", "Grass"): 2.0, ("Fire", "Water"): 0.5, ("Fire", "Electric"): 1.0,
        ("Grass", "Water"): 2.0, ("Grass", "Fire"): 0.5, ("Grass", "Electric"): 1.0
    }
    multiplier = chart.get((attacker_type, defender_type), 1.0)
    text = "Normal Damage (1x)"
    if multiplier > 1.0: text = "Super Effective! (Advantage 💥)"
    elif multiplier < 1.0: text = "Not Very Effective... (Disadvantage 🛡️)"
    st.info(f"🧪 [Type Analysis]: {attacker_type} -> {defender_type} | Multiplier: {multiplier}x ({text})")

st.markdown("---")

# Module 3: Voltorb Physics & Ohm's Law
st.header("⚡ 3. Voltorb Physics & Ohm's Law Simulator (V = I * R)")
c_in = st.text_input("Current (Amperes - I)", value="5")
r_in = st.text_input("Resistance (Ohms - R)", value="10")
if st.button("🔋 Calculate Voltage Output"):
    try:
        v = float(c_in) * float(r_in)
        st.success(f"⚡ [Voltorb Simulation]: Generated Voltage (V) = {v} Volts!")
    except ValueError:
        st.error("⚠️ Please enter valid numerical values!")

st.markdown("---")

# Module 4: Laboratory Challenge
st.header("🧠 4. Laboratory Challenge & Question Generator")
if st.button("🎲 Generate Random Scientific Challenge"):
    challenges = [
        "Challenge: If a Level 50 Pikachu hits with a Thunderbolt attack scaled by sin(pi/2), what is the damage coefficient? (Hint: 1)",
        "Challenge: Can you calculate the volume of a Poké Ball with a radius of 5?",
        "Challenge: What is the current in Amperes for a circuit with 100 Volts and 20 Ohms of resistance?"
    ]
    st.info(random.choice(challenges))

st.markdown("---")

# Module 5: Catch Probability
st.header("🎯 5. Legendary Pokémon Catch Probability Simulator")
poke_lvl = st.text_input("Pokémon Level", value="40")
ball_type = st.selectbox("Poké Ball Type", ["Standard Poké Ball", "Great Ball", "Ultra Ball", "Master Ball"])
if st.button("🎲 Calculate Catch Rate"):
    try:
        lvl = float(poke_lvl)
        mods = {"Standard Poké Ball": 1.0, "Great Ball": 1.5, "Ultra Ball": 2.0, "Master Ball": 100.0}
        mod = mods.get(ball_type, 1.0)
        if mod == 100.0:
            st.success("🎯 Master Ball selected! Catch Probability: 100% Guaranteed Success! 🚀")
        else:
            prob = max(1.0, min(100.0, (100 / (lvl * 0.4)) * mod * 10))
            st.success(f"🎯 Catch Probability: %{prob:.2f}")
    except ValueError:
        st.error("⚠️ Please enter a valid level!")

st.markdown("---")

# Module 6: Mathematical Constants
st.header("📐 6. Mathematical Constants Dictionary")
const_choice = st.selectbox("Select Mathematical Constant", ["Pi (π)", "Euler's Number (e)", "Golden Ratio (φ)"])
if st.button("📖 Show Constant Details"):
    constants = {
        "Pi (π)": "Value: ~3.14159 | The foundation of Poké Ball volume and perimeter calculations.",
        "Euler's Number (e)": "Value: ~2.71828 | Exponential growth curves and XP gain rate.",
        "Golden Ratio (φ)": "Value: ~1.61803 | Aesthetic body ratios of Legendary Pokémon."
    }
    st.info(constants.get(const_choice, ""))

st.markdown("---")

# Module 7: Evolution Module
st.header("📈 7. Pokémon Evolution & Combat Power (CP) Estimator")
cp_in = st.text_input("Current Combat Power (CP)", value="1200")
candy_in = st.text_input("Candies to Use", value="50")
if st.button("🚀 Calculate Evolution Power"):
    try:
        res = float(cp_in) * 1.8 + (int(candy_in) * 0.5)
        st.success(f"📈 Estimated Post-Evolution CP: {res:.2f}")
    except ValueError:
        st.error("⚠️ Please enter numeric values!")

st.markdown("---")

# Module 8 & 9: Notepad and Quote of the Day
col_n1, col_n2 = st.columns(2)
with col_n1:
    st.header("📝 8. Researcher Notepad")
    note = st.text_input("Write down your notes...")
    if st.button("💾 Save Note"):
        if note: st.success(f"Saved: {note}")
        else: st.warning("Note cannot be empty.")

with col_n2:
    st.header("✨ 9. Quote of the Day")
    if st.button("💡 Generate Quote"):
        quotes = [
            "💡 'Mathematics is the language with which God has written the universe.' - Galileo & Prof. Tom Crawford",
            "⚡ 'Volts, Voltorbs & Variables: Numbers govern the universe!'",
            "🔬 'Curiosity is the greatest catalyst for scientific discovery.'"
        ]
        st.info(random.choice(quotes))
