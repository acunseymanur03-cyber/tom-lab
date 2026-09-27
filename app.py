import streamlit as st
import math
import random

st.set_page_config(page_title="Professor Tom Crawford Laboratuvarı", page_icon="⚡", layout="wide")

st.title("⚡ Professor Tom Crawford | Gelişmiş Matematik & Pokémon Araştırma Üssü ⚡")
st.markdown("### *İnteraktif Akademik Simülasyon Merkezi: 'Volt, Voltorb ve Değişkenler'*")
st.markdown("---")

# Giriş ve Güvenlik Protokolü
st.sidebar.header("🔬 Erişim ve Güvenlik")
researcher_name = st.sidebar.text_input("Araştırmacı Adı / Unvanı:", placeholder="Örn: Araştırmacı Şeyma")
agree_terms = st.sidebar.checkbox("Professor Tom Crawford laboratuvar güvenlik kurallarını onaylıyorum.")

if not researcher_name or not agree_terms:
    st.warning("⚠️ Lütfen sol menüden adınızı girin ve laboratuvar güvenlik protokolünü onaylayın!")
    st.stop()
else:
    st.success(f"🎉 Hoş geldiniz, {researcher_name}. Sistemler aktif!")

st.markdown("---")

# Modül 1: Evrensel Matematik Hesap Motoru
st.header("🧮 1. Evrensel Matematik Hesap Motoru")
math_input = st.text_input("Matematiksel İfade / Denklem", value="50 * 3 + sqrt(400)")
if st.button("⚡ Matematiksel İşlemi Hesapla"):
    try:
        safe_dict = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e,
            "factorial": math.factorial, "abs": abs, "round": round,
            "pow": pow, "floor": math.floor, "ceil": math.ceil,
        }
        result = eval(math_input.strip(), {"__builtins__": {}}, safe_dict)
        st.success(f"🌐 [Evrensel Matematik Sonucu]:\n{math_input} = {result}")
    except Exception as e:
        st.error(f"⚠️ İfade Hatası: Geçerli bir format girin. Hata: {str(e)}")

st.markdown("---")

# Modül 2: Pokémon Tür Etkileşim Matrisi
st.header("🧪 2. Pokémon Tür Etkileşim ve Hasar Matrisi")
col1, col2 = st.columns(2)
with col1:
    attacker_type = st.selectbox("Saldırı Türü", ["Elektrik", "Su", "Ateş", "Çimen"])
with col2:
    defender_type = st.selectbox("Savunma Türü", ["Elektrik", "Su", "Ateş", "Çimen"])

if st.button("🔍 Tür Etkileşimini Hesapla"):
    chart = {
        ("Elektrik", "Su"): 2.0, ("Elektrik", "Çimen"): 0.5, ("Elektrik", "Ateş"): 1.0,
        ("Su", "Ateş"): 2.0, ("Su", "Elektrik"): 1.0, ("Su", "Çimen"): 0.5,
        ("Ateş", "Çimen"): 2.0, ("Ateş", "Su"): 0.5, ("Ateş", "Elektrik"): 1.0,
        ("Çimen", "Su"): 2.0, ("Çimen", "Ateş"): 0.5, ("Çimen", "Elektrik"): 1.0
    }
    multiplier = chart.get((attacker_type, defender_type), 1.0)
    text = "Normal Hasar (1x)"
    if multiplier > 1.0: text = "Süper Etkili! (Avantajlı 💥)"
    elif multiplier < 1.0: text = "Pek Etkili Değil... (Dezavantajlı 🛡️)"
    st.info(f"🧪 [Tür Analizi]: {attacker_type} -> {defender_type} | Çarpan: {multiplier}x ({text})")

st.markdown("---")

# Modül 3: Voltorb Fizik & Ohm Kanunu
st.header("⚡ 3. Voltorb Fizik & Ohm Kanunu Simülatörü (V = I * R)")
c_in = st.text_input("Akım (Amper - I)", value="5")
r_in = st.text_input("Direnç (Ohm - R)", value="10")
if st.button("🔋 Voltaj Üretimini Hesapla"):
    try:
        v = float(c_in) * float(r_in)
        st.success(f"⚡ [Voltorb Simülasyonu]: Üretilen Voltaj (V) = {v} Volt!")
    except ValueError:
        st.error("⚠️ Lütfen geçerli sayısal değerler girin!")

st.markdown("---")

# Modül 4: Laboratuvar Bulmacası
st.header("🧠 4. Laboratuvar Bulmaca ve Soru Üreteci")
if st.button("🎲 Rastgele Bilimsel Soru Üret"):
    challenges = [
        "Soru: Seviye 50 bir Pikachu'nun Thunderbolt saldırısının sin(pi/2) açısıyla vurduğunu varsayarsak hasar katsayısı kaç olur? (İpucu: 1)",
        "Soru: Yarıçapı 5 olan bir Poké Topu'nun hacmini hesaplayabilir misin?",
        "Soru: 100 Volt ve 20 Ohm dirence sahip bir devrede akım kaç Amperdir?"
    ]
    st.info(random.choice(challenges))

st.markdown("---")

# Modül 5: Yakalama Olasılığı
st.header("🎯 5. Efsanevi Pokémon Yakalama Olasılığı Simülatörü")
poke_lvl = st.text_input("Pokémon Seviyesi", value="40")
ball_type = st.selectbox("Top Türü", ["Standard Pokéball", "Great Ball", "Ultra Ball", "Master Ball"])
if st.button("🎲 Yakalama Şansını Hesapla"):
    try:
        lvl = float(poke_lvl)
        mods = {"Standard Pokéball": 1.0, "Great Ball": 1.5, "Ultra Ball": 2.0, "Master Ball": 100.0}
        mod = mods.get(ball_type, 1.0)
        if mod == 100.0:
            st.success("🎯 Master Ball seçildi! Yakalama Olasılığı: %100 Kesin Başarı! 🚀")
        else:
            prob = max(1.0, min(100.0, (100 / (lvl * 0.4)) * mod * 10))
            st.success(f"🎯 Yakalama Şansı: %{prob:.2f}")
    except ValueError:
        st.error("⚠️ Lütfen geçerli bir seviye girin!")

st.markdown("---")

# Modül 6: Matematiksel Sabitler
st.header("📐 6. Matematiksel Sabitler Sözlüğü")
const_choice = st.selectbox("Matematiksel Sabit Seçin", ["Pi (π)", "Euler Sayısı (e)", "Altın Oran (φ)"])
if st.button("📖 Sabit Detayını Göster"):
    constants = {
        "Pi (π)": "Değer: ~3.14159 | Poké Toplarının hacim ve çevre hesaplamalarının temel taşı.",
        "Euler Sayısı (e)": "Değer: ~2.71828 | Üstel büyüme eğrileri ve XP artış hızı.",
        "Altın Oran (φ)": "Değer: ~1.61803 | Efsanevi Pokémon'ların estetik vücut oranları."
    }
    st.info(constants.get(const_choice, ""))

st.markdown("---")

# Modül 7: Evrim Modülü
st.header("📈 7. Pokémon Evrim ve Güç Tahmin Modülü")
cp_in = st.text_input("Mevcut Savaş Gücü (CP)", value="1200")
candy_in = st.text_input("Kullanılacak Şeker Miktarı", value="50")
if st.button("🚀 Evrim Gücünü Hesapla"):
    try:
        res = float(cp_in) * 1.8 + (int(candy_in) * 0.5)
        st.success(f"📈 Tahmini Evrim Sonrası Güç (CP): {res:.2f}")
    except ValueError:
        st.error("⚠️ Lütfen sayısal değerler girin!")

st.markdown("---")

# Modül 8 & 9: Not Defteri ve Günün Sözü
col_n1, col_n2 = st.columns(2)
with col_n1:
    st.header("📝 8. Not Defteri")
    note = st.text_input("Notunuzu yazın...")
    if st.button("💾 Kaydet"):
        if note: st.success(f"Kaydedildi: {note}")
        else: st.warning("Boş olamaz.")

with col_n2:
    st.header("✨ 9. Günün Sözü")
    if st.button("💡 Söz Üret"):
        quotes = [
            "💡 'Matematik evrenin yazıldığı dildir.' - Galileo & Prof. Tom Crawford",
            "⚡ 'Volts, Voltorbs & Variables: Sayılar evreni yönetir!'",
            "🔬 'Merak, bilimsel keşfin en büyük katalizörüdür.'"
        ]
        st.info(random.choice(quotes))

