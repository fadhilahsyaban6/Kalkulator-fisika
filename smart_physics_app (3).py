
import streamlit as st
import math
import random

# Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Physics Calculator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk tampilan menarik
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .formula-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .step-box {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #2ca02c;
    }
    .quiz-correct {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        color: #155724;
    }
    .quiz-wrong {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        color: #721c24;
    }
    .constant-box {
        background-color: #fff3cd;
        padding: 8px;
        border-radius: 5px;
        margin: 3px 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .hero-text {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin: 20px 0;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA & KONSTANTA ====================
PHYSICS_CONSTANTS = {
    "Kecepatan cahaya (c)": {"nilai": 2.998e8, "satuan": "m/s"},
    "Konstanta gravitasi (G)": {"nilai": 6.674e-11, "satuan": "N·m²/kg²"},
    "Konstanta Planck (h)": {"nilai": 6.626e-34, "satuan": "J·s"},
    "Muatan elektron (e)": {"nilai": 1.602e-19, "satuan": "C"},
    "Massa elektron (mₑ)": {"nilai": 9.109e-31, "satuan": "kg"},
    "Massa proton (mₚ)": {"nilai": 1.673e-27, "satuan": "kg"},
    "Massa neutron (mₙ)": {"nilai": 1.675e-27, "satuan": "kg"},
    "Konstanta Boltzmann (k)": {"nilai": 1.381e-23, "satuan": "J/K"},
    "Konstanta Avogadro (Nₐ)": {"nilai": 6.022e23, "satuan": "mol⁻¹"},
    "Permeabilitas vakum (μ₀)": {"nilai": 4*math.pi*1e-7, "satuan": "N/A²"},
    "Permitivitas vakum (ε₀)": {"nilai": 8.854e-12, "satuan": "F/m"},
    "Percepatan gravitasi bumi (g)": {"nilai": 9.81, "satuan": "m/s²"},
    "Tekanan atmosfer standar (atm)": {"nilai": 1.013e5, "satuan": "Pa"},
    "Suhu triple point air": {"nilai": 273.16, "satuan": "K"},
}

UNIT_TABLE = {
    "Panjang": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "μm": 1e-6, "nm": 1e-9, "ft": 0.3048, "in": 0.0254, "mi": 1609.34},
    "Massa": {"kg": 1, "g": 0.001, "mg": 1e-6, "ton": 1000, "lb": 0.4536, "oz": 0.02835},
    "Waktu": {"s": 1, "min": 60, "hr": 3600, "day": 86400, "ms": 0.001},
    "Suhu": {"C": "special", "K": "special", "F": "special", "R": "special"},
    "Tekanan": {"Pa": 1, "kPa": 1000, "MPa": 1e6, "bar": 1e5, "atm": 101325, "mmHg": 133.322, "psi": 6894.76},
    "Energi": {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184, "Wh": 3600, "kWh": 3.6e6, "eV": 1.602e-19},
    "Daya": {"W": 1, "kW": 1000, "MW": 1e6, "hp": 745.7},
    "Kerapatan": {"kg/m³": 1, "g/cm³": 1000, "kg/L": 1000, "g/mL": 1000, "lb/ft³": 16.018},
    "Viskositas": {"Pa·s": 1, "Poise": 0.1, "cP": 0.001, "mPa·s": 0.001},
    "Gaya": {"N": 1, "kN": 1000, "dyne": 1e-5, "kgf": 9.81, "lbf": 4.448},
}

# ==================== FUNGSI KONVERSI ====================
def convert_temperature(val, from_unit, to_unit):
    if from_unit == to_unit:
        return val
    # Konversi ke Celsius dulu
    if from_unit == "C":
        c = val
    elif from_unit == "K":
        c = val - 273.15
    elif from_unit == "F":
        c = (val - 32) * 5/9
    elif from_unit == "R":
        c = val * 5/9 - 273.15
    else:
        return None
    # Konversi dari Celsius ke target
    if to_unit == "C":
        return c
    elif to_unit == "K":
        return c + 273.15
    elif to_unit == "F":
        return c * 9/5 + 32
    elif to_unit == "R":
        return (c + 273.15) * 9/5
    return None

def auto_convert(value, from_unit, to_unit, category):
    if category == "Suhu":
        return convert_temperature(value, from_unit, to_unit)

    units = UNIT_TABLE.get(category, {})
    if from_unit not in units or to_unit not in units:
        return None

    # Konversi ke unit dasar, lalu ke target
    base_value = value * units[from_unit]
    return base_value / units[to_unit]

# ==================== KALKULATOR KERAPATAN ====================
def calc_density(mass, volume, mass_unit, vol_unit):
    # Konversi ke kg dan m³
    mass_kg = auto_convert(mass, mass_unit, "kg", "Massa")
    vol_m3 = auto_convert(volume, vol_unit, "m", "Panjang")**3 if vol_unit in UNIT_TABLE["Panjang"] else None

    if vol_unit == "L" or vol_unit == "dm³":
        vol_m3 = volume * 0.001
    elif vol_unit == "mL" or vol_unit == "cm³":
        vol_m3 = volume * 1e-6
    elif vol_unit == "ft³":
        vol_m3 = volume * 0.0283
    elif vol_unit == "in³":
        vol_m3 = volume * 1.639e-5
    else:
        # Coba konversi dari tabel panjang
        try:
            vol_m3 = auto_convert(volume, vol_unit, "m", "Panjang")**3
        except:
            vol_m3 = volume * 1e-3  # default L

    density = mass_kg / vol_m3 if vol_m3 else 0
    return density, mass_kg, vol_m3

# ==================== KALKULATOR VISKOSITAS ====================
def calc_viscosity(force, area, velocity, gradient, f_unit, a_unit, v_unit, g_unit):
    # η = (F/A) / (dv/dy) = shear stress / shear rate
    # Konversi satuan ke SI
    f_si = auto_convert(force, f_unit, "N", "Gaya") if f_unit != "N" else force
    a_si = auto_convert(area, a_unit, "m", "Panjang")**2 if a_unit in UNIT_TABLE["Panjang"] else area

    if a_unit == "cm²":
        a_si = area * 1e-4
    elif a_unit == "mm²":
        a_si = area * 1e-6
    elif a_unit == "ft²":
        a_si = area * 0.0929
    elif a_unit == "in²":
        a_si = area * 0.000645

    v_si = auto_convert(velocity, v_unit, "m", "Panjang") if v_unit in UNIT_TABLE["Panjang"] else velocity

    if g_unit in UNIT_TABLE["Panjang"]:
        g_si = auto_convert(gradient, g_unit, "m", "Panjang")
    else:
        g_si = gradient

    shear_stress = f_si / a_si if a_si else 0
    shear_rate = v_si / g_si if g_si else 0
    viscosity = shear_stress / shear_rate if shear_rate else 0

    return viscosity, shear_stress, shear_rate, f_si, a_si, v_si, g_si

# ==================== KALKULATOR SUDUT REPOSISI ====================
def calc_repose_angle(mu_s):
    # θ = arctan(μs)
    theta_rad = math.atan(mu_s)
    theta_deg = math.degrees(theta_rad)
    return theta_deg, theta_rad

# ==================== DATA QUIZ ====================
QUIZ_QUESTIONS = [
    {
        "type": "pilihan_ganda",
        "soal": "Sebuah balok bermassa 5 kg dikenai gaya 20 N. Berapa percepatan balok tersebut?",
        "pilihan": ["2 m/s²", "4 m/s²", "5 m/s²", "0.25 m/s²"],
        "jawaban": "4 m/s²",
        "pembahasan": "Menggunakan Hukum II Newton: F = m × a → a = F/m = 20 N / 5 kg = 4 m/s²"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Berapa kerapatan air pada suhu 4°C?",
        "pilihan": ["1000 kg/m³", "1 kg/m³", "100 kg/m³", "10 kg/m³"],
        "jawaban": "1000 kg/m³",
        "pembahasan": "Air pada suhu 4°C memiliki kerapatan maksimum sebesar 1000 kg/m³ atau 1 g/cm³."
    },
    {
        "type": "isian",
        "soal": "Sebuah benda jatuh bebas dari ketinggian 20 m. Berapa kecepatan benda saat menyentuh tanah? (g = 10 m/s², tulis angka saja)",
        "jawaban": "20",
        "pembahasan": "Menggunakan v² = 2gh → v = √(2×10×20) = √400 = 20 m/s"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Satuan viskositas dinamis dalam SI adalah...",
        "pilihan": ["Poise", "Stokes", "Pa·s", "N/m²"],
        "jawaban": "Pa·s",
        "pembahasan": "Satuan viskositas dinamis dalam SI adalah Pa·s (Pascal-second). 1 Pa·s = 10 Poise."
    },
    {
        "type": "pilihan_ganda",
        "soal": "Jika koefisien gesek statis μₛ = 0.5, berapa sudut reposisi maksimum?",
        "pilihan": ["26.6°", "30°", "45°", "60°"],
        "jawaban": "26.6°",
        "pembahasan": "θ = arctan(μₛ) = arctan(0.5) ≈ 26.565° ≈ 26.6°"
    },
    {
        "type": "isian",
        "soal": "Konversikan 25°C ke Kelvin! (tulis angka saja)",
        "jawaban": "298.15",
        "pembahasan": "K = C + 273.15 = 25 + 273.15 = 298.15 K"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Tekanan hidrostatik di kedalaman 10 m dalam air (ρ = 1000 kg/m³) adalah...",
        "pilihan": ["98000 Pa", "100000 Pa", "101325 Pa", "50000 Pa"],
        "jawaban": "98000 Pa",
        "pembahasan": "P = ρgh = 1000 × 9.8 × 10 = 98000 Pa"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Energi kinetik sebuah benda bermassa 2 kg yang bergerak dengan kecepatan 10 m/s adalah...",
        "pilihan": ["10 J", "100 J", "200 J", "50 J"],
        "jawaban": "100 J",
        "pembahasan": "Ek = ½mv² = ½ × 2 × 10² = 100 J"
    },
    {
        "type": "isian",
        "soal": "Berapa gaya gravitasi antara dua benda bermassa 1000 kg dan 2000 kg yang berjarak 10 m? (G = 6.67×10⁻¹¹, tulis dalam bentuk desimal dengan 4 angka di belakang koma)",
        "jawaban": "0.0013",
        "pembahasan": "F = G(m₁m₂)/r² = 6.67×10⁻¹¹ × (1000×2000)/100 = 1.334×10⁻⁶ N. Jika dibulatkan: 0.0000013 N"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Hukum Archimedes berlaku untuk...",
        "pilihan": ["Benda yang tenggelam", "Benda yang mengapung", "Benda dalam fluida", "Semua benar"],
        "jawaban": "Semua benar",
        "pembahasan": "Hukum Archimedes berlaku untuk semua benda yang berada dalam fluida, baik tenggelam, mengapung, atau melayang."
    },
]

# ==================== SIDEBAR NAVIGASI ====================
st.sidebar.markdown("<h1 style='text-align:center;'>⚛️ Smart Physics</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📋 Menu Navigasi",
    ["🏠 Beranda", "📚 Rumus & Cheat Sheet", "🧮 Kalkulator", "🔄 Unit Converter", "📝 Quiz Fisika"]
)

# ==================== HALAMAN BERANDA ====================
if menu == "🏠 Beranda":
    st.markdown("<div class='main-header'>⚛️ Smart Physics Calculator</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-text'>Aplikasi kalkulator fisika cerdas dengan langkah pengerjaan, konversi satuan otomatis, dan latihan soal interaktif untuk mahasiswa fisika dasar.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧮</div>
            <h3>Kalkulator Cerdas</h3>
            <p>Kerapatan, Viskositas, Sudut Reposisi dengan langkah pengerjaan lengkap dan penjelasan rumus.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔄</div>
            <h3>Auto Converter</h3>
            <p>Konversi satuan otomatis untuk berbagai besaran fisika: panjang, massa, suhu, tekanan, energi, dan lainnya.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📝</div>
            <h3>Quiz Interaktif</h3>
            <p>Latihan soal pilihan ganda dan isian dengan pembahasan otomatis untuk persiapan ujian fisika dasar.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='sub-header'>🔬 Pengenalan Materi Fisika Dasar</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📐 Mekanika", "🌡️ Termodinamika", "⚡ Listrik & Magnet", "🔊 Gelombang"])

    with tab1:
        st.markdown("""
        ### Mekanika Klasik
        Mekanika adalah cabang fisika yang mempelajari gerak benda dan gaya yang menyebabkannya. 

        **Topik Utama:**
        - **Kinematika**: Gerak lurus, gerak parabola, gerak melingkar
        - **Dinamika**: Hukum Newton, gaya gesek, momentum
        - **Energi**: Energi kinetik, energi potensial, usaha
        - **Fluida**: Tekanan, hukum Pascal, hukum Archimedes, viskositas

        **Aplikasi Praktis:**
        - Perancangan jembatan dan bangunan
        - Aerodinamika kendaraan
        - Sistem hidrolik
        """)

    with tab2:
        st.markdown("""
        ### Termodinamika
        Mempelajari hubungan antara panas, kerja, energi, dan sifat materi.

        **Topik Utama:**
        - **Suhu dan Kalor**: Konduksi, konveksi, radiasi
        - **Hukum Termodinamika 0-3**: Kesetimbangan, kekekalan, entropi
        - **Gas Ideal**: Persamaan keadaan, teori kinetik gas
        - **Perubahan Fase**: Kalor laten, diagram fase

        **Konsep Kunci:**
        - Entropi mengukur ketidakteraturan sistem
        - Efisiensi mesin Carnot adalah batas teoritis
        """)

    with tab3:
        st.markdown("""
        ### Listrik & Magnet
        Mempelajari muatan listrik, medan listrik, dan medan magnet.

        **Topik Utama:**
        - **Elektrostatika**: Hukum Coulomb, medan listrik, potensial
        - **Arus Listrik**: Hukum Ohm, rangkaian DC, daya listrik
        - **Magnetostatika**: Gaya Lorentz, medan magnet, induksi
        - **Induksi Elektromagnetik**: Hukum Faraday, hamburan gelombang EM

        **Aplikasi:**
        - Generator dan motor listrik
        - Transformator
        - Gelombang radio dan komunikasi
        """)

    with tab4:
        st.markdown("""
        ### Gelombang & Optika
        Mempelajari perambatan gangguan melalui medium dan zat.

        **Topik Utama:**
        - **Gelombang Mekanik**: Gelombang tali, gelombang suara
        - **Gelombang EM**: Spektrum elektromagnetik, polarisasi
        - **Optika Geometris**: Pembiasan, pemantulan, lensa, cermin
        - **Optika Fisis**: Interferensi, difraksi, polarisasi

        **Fenomena Menarik:**
        - Efek Doppler pada gelombang suara
        - Interferensi Young (celah ganda)
        - Prisma dan dispersi cahaya
        """)

    st.markdown("---")
    st.info("💡 **Tips**: Gunakan menu di sidebar untuk mengakses fitur kalkulator, konverter, dan quiz!")

# ==================== HALAMAN RUMUS & CHEAT SHEET ====================
elif menu == "📚 Rumus & Cheat Sheet":
    st.markdown("<div class='main-header'>📚 Rumus & Cheat Sheet Fisika</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Tabel Satuan", "🔢 Konstanta Fisika", "📖 Rumus Penting"])

    with tab1:
        st.markdown("<div class='sub-header'>📋 Tabel Satuan SI dan Konversi</div>", unsafe_allow_html=True)

        satuan_data = {
            "Besaran Pokok": [
                ["Panjang", "meter", "m"],
                ["Massa", "kilogram", "kg"],
                ["Waktu", "second", "s"],
                ["Arus listrik", "ampere", "A"],
                ["Suhu", "kelvin", "K"],
                ["Jumlah zat", "mole", "mol"],
                ["Intensitas cahaya", "candela", "cd"]
            ],
            "Besaran Turunan": [
                ["Kecepatan", "m/s"],
                ["Percepatan", "m/s²"],
                ["Gaya", "Newton (N = kg·m/s²)"],
                ["Energi", "Joule (J = N·m)"],
                ["Daya", "Watt (W = J/s)"],
                ["Tekanan", "Pascal (Pa = N/m²)"],
                ["Muatan listrik", "Coulomb (C = A·s)"],
                ["Potensial listrik", "Volt (V = W/A)"],
                ["Resistansi", "Ohm (Ω = V/A)"],
                ["Kapasitansi", "Farad (F = C/V)"],
                ["Frekuensi", "Hertz (Hz = s⁻¹)"],
                ["Kerapatan", "kg/m³"],
                ["Viskositas", "Pa·s (Pascal-second)"]
            ]
        }

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Besaran Pokok SI**")
            st.table(satuan_data["Besaran Pokok"])
        with col_b:
            st.markdown("**Besaran Turunan SI**")
            st.table(satuan_data["Besaran Turunan"])

        st.markdown("---")
        st.markdown("**Prefix Metric (Awalan SI)**")
        prefix_data = [
            ["Tera (T)", "10¹²", "1.000.000.000.000"],
            ["Giga (G)", "10⁹", "1.000.000.000"],
            ["Mega (M)", "10⁶", "1.000.000"],
            ["Kilo (k)", "10³", "1.000"],
            ["Hekto (h)", "10²", "100"],
            ["Deka (da)", "10¹", "10"],
            ["Desi (d)", "10⁻¹", "0,1"],
            ["Senti (c)", "10⁻²", "0,01"],
            ["Mili (m)", "10⁻³", "0,001"],
            ["Mikro (μ)", "10⁻⁶", "0,000001"],
            ["Nano (n)", "10⁻⁹", "0,000000001"],
            ["Piko (p)", "10⁻¹²", "0,000000000001"]
        ]
        st.table(prefix_data)

    with tab2:
        st.markdown("<div class='sub-header'>🔢 Konstanta Fisika Fundamental</div>", unsafe_allow_html=True)
        st.markdown("Konstanta-konstanta ini digunakan secara universal dalam perhitungan fisika.")

        for name, data in PHYSICS_CONSTANTS.items():
            st.markdown(f"""
            <div class='constant-box'>
                <b>{name}</b> = {data['nilai']:.4e} {data['satuan']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Catatan Penting:**")
        st.markdown("""
        - Kecepatan cahaya **c** adalah batas kecepatan maksimum di alam semesta
        - Konstanta Planck **h** menghubungkan energi dengan frekuensi (E = hf)
        - Konstanta gravitasi **G** digunakan dalam hukum gravitasi universal Newton
        - Konstanta Boltzmann **k** menghubungkan energi dengan suhu untuk partikel individual
        """)

    with tab3:
        st.markdown("<div class='sub-header'>📖 Rumus-Rumus Penting Fisika Dasar</div>", unsafe_allow_html=True)

        rumus_categories = {
            "Mekanika": [
                ("Hukum II Newton", "F = m · a", "Gaya = massa × percepatan"),
                ("Energi Kinetik", "Ek = ½ m v²", "Energi gerak = ½ × massa × kecepatan²"),
                ("Energi Potensial Gravitasi", "Ep = m g h", "Energi posisi = massa × gravitasi × ketinggian"),
                ("Momentum", "p = m v", "Momentum = massa × kecepatan"),
                ("Gerak Jatuh Bebas", "h = ½ g t²", "Ketinggian = ½ × gravitasi × waktu²"),
                ("Gerak Lurus Berubah Beraturan", "v = v₀ + a t", "Kecepatan akhir = awal + percepatan × waktu"),
                ("Gaya Gesek", "f = μ N", "Gaya gesek = koefisien gesek × gaya normal"),
            ],
            "Fluida": [
                ("Tekanan Hidrostatik", "P = ρ g h", "Tekanan = kerapatan × gravitasi × kedalaman"),
                ("Hukum Archimedes", "Fa = ρf V g", "Gaya apung = kerapatan fluida × volume × gravitasi"),
                ("Debit (Aliran)", "Q = A v", "Debit = luas penampang × kecepatan aliran"),
                ("Hukum Bernoulli", "P + ½ρv² + ρgh = konstan", "Energi per satuan volume konstan sepanjang aliran"),
                ("Viskositas (Newton)", "η = τ / (dv/dy)", "Viskositas = tegangan geser / laju regangan"),
                ("Kerapatan", "ρ = m / V", "Kerapatan = massa / volume"),
            ],
            "Termodinamika": [
                ("Persamaan Gas Ideal", "PV = nRT", "Tekanan×Volume = mol×konstanta gas×Suhu"),
                ("Kalor", "Q = m c ΔT", "Kalor = massa × kalor jenis × perubahan suhu"),
                ("Kalor Laten", "Q = m L", "Kalor = massa × kalor laten"),
                ("Efisiensi Carnot", "η = 1 - T₂/T₁", "Efisiensi = 1 - (suhu rendah/suhu tinggi) dalam Kelvin"),
                ("Energi Kinetik Gas", "Ek = 3/2 kT", "Energi rata-rata = 3/2 × konstanta Boltzmann × suhu"),
            ],
            "Listrik & Magnet": [
                ("Hukum Ohm", "V = I R", "Tegangan = arus × resistansi"),
                ("Daya Listrik", "P = V I = I²R = V²/R", "Daya = tegangan × arus"),
                ("Hukum Coulomb", "F = k q₁q₂/r²", "Gaya elektrostatik = konstanta × muatan²/jarak²"),
                ("Medan Listrik", "E = F/q = kQ/r²", "Medan = gaya/muatan uji"),
                ("Gaya Lorentz", "F = q(v × B)", "Gaya = muatan × (kecepatan × medan magnet)"),
                ("Induksi Faraday", "ε = -dΦ/dt", "GGL induksi = -laju perubahan fluks magnet"),
            ],
            "Gelombang & Optika": [
                ("Kecepatan Gelombang", "v = f λ", "Kecepatan = frekuensi × panjang gelombang"),
                ("Energi Foton", "E = h f", "Energi = konstanta Planck × frekuensi"),
                ("Hukum Snellius", "n₁ sin θ₁ = n₂ sin θ₂", "Indeks bias × sin sudut = konstan"),
                ("Pembesaran Lensa", "M = -s'/s = h'/h", "Pembesaran = -jarak bayangan/jarak benda"),
                ("Persamaan Lensa", "1/f = 1/s + 1/s'", "1/fokus = 1/jarak benda + 1/jarak bayangan"),
            ]
        }

        for category, formulas in rumus_categories.items():
            with st.expander(f"📌 {category}"):
                for name, formula, desc in formulas:
                    st.markdown(f"""
                    <div class='formula-box'>
                        <b>{name}</b><br>
                        <span style='font-size:1.3em; color:#1f77b4;'>{formula}</span><br>
                        <span style='color:#666; font-size:0.9em;'>{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== HALAMAN KALKULATOR ====================
elif menu == "🧮 Kalkulator":
    st.markdown("<div class='main-header'>🧮 Smart Physics Calculator</div>", unsafe_allow_html=True)
    st.markdown("Isi nilai yang diketahui, sistem akan menghitung secara otomatis dengan langkah pengerjaan lengkap!")

    calc_type = st.selectbox(
        "Pilih Kalkulator:",
        ["📊 Kerapatan (Density)", "🍯 Viskositas (Kekentalan)", "📐 Sudut Reposisi", "⚡ Persamaan Gas Ideal", "🔄 Konversi Satuan"]
    )

    # --- KALKULATOR KERAPATAN ---
    if calc_type == "📊 Kerapatan (Density)":
        st.markdown("<div class='sub-header'>📊 Kalkulator Kerapatan (ρ = m/V)</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            mass = st.number_input("Massa (m):", min_value=0.0, value=1.0, step=0.1)
            mass_unit = st.selectbox("Satuan Massa:", ["kg", "g", "mg", "ton", "lb"])
        with col2:
            volume = st.number_input("Volume (V):", min_value=0.0, value=1.0, step=0.1)
            vol_unit = st.selectbox("Satuan Volume:", ["m³", "L", "cm³", "mL", "ft³", "mm³"])

        if st.button("🔍 Hitung Kerapatan", type="primary"):
            if mass <= 0 or volume <= 0:
                st.error("❌ Massa dan volume harus lebih besar dari 0!")
            else:
                # Konversi ke SI
                mass_kg = auto_convert(mass, mass_unit, "kg", "Massa")

                # Konversi volume
                vol_conversions = {
                    "m³": mass, "L": 0.001, "cm³": 1e-6, "mL": 1e-6, 
                    "ft³": 0.0283168, "mm³": 1e-9
                }
                vol_m3 = volume * vol_conversions.get(vol_unit, 1)

                density = mass_kg / vol_m3

                st.success("✅ Perhitungan Berhasil!")

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class='step-box'>
                    <b>Langkah 1:</b> Konversi satuan ke SI<br>
                    Massa = {mass} {mass_unit} = {mass_kg:.6f} kg<br>
                    Volume = {volume} {vol_unit} = {vol_m3:.6e} m³
                </div>
                <div class='step-box'>
                    <b>Langkah 2:</b> Masukkan ke rumus kerapatan<br>
                    ρ = m / V = {mass_kg:.6f} / {vol_m3:.6e}
                </div>
                <div class='step-box'>
                    <b>Langkah 3:</b> Hasil akhir<br>
                    <span style='font-size:1.5em; color:#1f77b4;'><b>ρ = {density:.4f} kg/m³</b></span><br>
                    = {density/1000:.4f} g/cm³<br>
                    = {density*0.001:.4f} kg/L
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                st.info("""
                **Kerapatan (ρ)** adalah ukuran massa per satuan volume suatu zat. 
                Rumus: **ρ = m/V**

                - **ρ** (rho) = kerapatan (kg/m³)
                - **m** = massa benda (kg)
                - **V** = volume benda (m³)

                **Interpretasi Fisika:**
                - Air murni: ρ ≈ 1000 kg/m³ (pada 4°C)
                - Udara: ρ ≈ 1.225 kg/m³ (pada 15°C, 1 atm)
                - Besi: ρ ≈ 7870 kg/m³
                - Kerapatan relatif (specific gravity) = ρ_zat / ρ_air
                """)

    # --- KALKULATOR VISKOSITAS (METODE OSWALD) ---
    elif calc_type == "🍯 Viskositas (Kekentalan)":
        st.markdown("<div class='sub-header'>🍯 Kalkulator Viskositas Metode Oswald</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='formula-box' style='text-align:center;'>
            <h3>📐 Rumus Viskositas Metode Oswald</h3>
            <p style='font-size:1.3em;'>
                η<sub>uji</sub> = 
                <span style='display:inline-block; text-align:center; vertical-align:middle;'>
                    <span style='border-bottom:2px solid black; padding:0 10px;'>t<sub>uji</sub> × ρ<sub>uji</sub> × η<sub>ref</sub></span><br>
                    <span style='padding:0 10px;'>t<sub>ref</sub> × ρ<sub>ref</sub></span>
                </span>
            </p>
            <p style='color:#666;'>
                η = viskositas | t = waktu alir | ρ = densitas/kerapatan
            </p>
        </div>
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='color:#1f77b4;'>🧴 Fluida Uji (misal: Air Sabun)</h4>", unsafe_allow_html=True)
            t_uji = st.number_input("Waktu alir fluida uji (t₂) dalam detik:", min_value=0.0, value=45.0, step=0.1, format="%.2f")
            rho_uji = st.number_input("Densitas fluida uji (ρ₂) dalam kg/m³:", min_value=0.0, value=1020.0, step=1.0, format="%.2f")

        with col2:
            st.markdown("<h4 style='color:#ff7f0e;'>💧 Fluida Referensi (misal: Air Suling)</h4>", unsafe_allow_html=True)
            t_ref = st.number_input("Waktu alir fluida referensi (t₁) dalam detik:", min_value=0.0, value=30.0, step=0.1, format="%.2f")
            rho_ref = st.number_input("Densitas fluida referensi (ρ₁) dalam kg/m³:", min_value=0.0, value=1000.0, step=1.0, format="%.2f")
            eta_ref = st.number_input("Viskositas fluida referensi (η₁) dalam Pa·s:", min_value=0.0, value=0.001002, step=0.0001, format="%.6f", help="Air suling 20°C = 0.001002 Pa·s")

        if st.button("🔍 Hitung Viskositas", type="primary"):
            if t_ref <= 0 or rho_ref <= 0:
                st.error("❌ Waktu alir dan densitas referensi harus lebih besar dari 0!")
            else:
                # Rumus Oswald: η₂ = (t₂ × ρ₂ × η₁) / (t₁ × ρ₁)
                eta_uji = (t_uji * rho_uji * eta_ref) / (t_ref * rho_ref)
                eta_cp = eta_uji * 1000
                eta_poise = eta_uji * 10

                st.success("✅ Perhitungan Berhasil!")

                st.markdown(f"""
                <div style='background-color:#fff3cd; padding:20px; border-radius:12px; text-align:center; margin:20px 0;'>
                    <h2 style='color:#ff7f0e; margin:0;'>🍯 Viskositas Fluida Uji</h2>
                    <h1 style='color:#1f77b4; margin:10px 0;'>η₂ = {eta_uji:.6f} Pa·s</h1>
                    <p style='font-size:1.2em; margin:0;'>
                        = {eta_cp:.3f} cP (centiPoise)<br>
                        = {eta_poise:.4f} Poise
                    </p>
                </div>
                """)

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class='step-box'>
                    <b>Langkah 1:</b> Identifikasi variabel dari pengukuran<br>
                    • t₂ (waktu alir uji) = {t_uji:.2f} detik<br>
                    • ρ₂ (densitas uji) = {rho_uji:.2f} kg/m³<br>
                    • t₁ (waktu alir referensi) = {t_ref:.2f} detik<br>
                    • ρ₁ (densitas referensi) = {rho_ref:.2f} kg/m³<br>
                    • η₁ (viskositas referensi) = {eta_ref:.6f} Pa·s
                </div>
                <div class='step-box'>
                    <b>Langkah 2:</b> Masukkan ke rumus Oswald<br>
                    η₂ = (t₂ × ρ₂ × η₁) / (t₁ × ρ₁)<br>
                    η₂ = ({t_uji:.2f} × {rho_uji:.2f} × {eta_ref:.6f}) / ({t_ref:.2f} × {rho_ref:.2f})
                </div>
                <div class='step-box'>
                    <b>Langkah 3:</b> Hitung pembilang (atas)<br>
                    {t_uji:.2f} × {rho_uji:.2f} × {eta_ref:.6f} = <b>{t_uji * rho_uji * eta_ref:.6e}</b>
                </div>
                <div class='step-box'>
                    <b>Langkah 4:</b> Hitung penyebut (bawah)<br>
                    {t_ref:.2f} × {rho_ref:.2f} = <b>{t_ref * rho_ref:.2f}</b>
                </div>
                <div class='step-box'>
                    <b>Langkah 5:</b> Bagi pembilang dengan penyebut<br>
                    η₂ = {t_uji * rho_uji * eta_ref:.6e} / {t_ref * rho_ref:.2f} = <b>{eta_uji:.6f} Pa·s</b>
                </div>
                """)

                st.markdown("<div class='sub-header'>📖 Penjelasan Teori & Rumus:</div>", unsafe_allow_html=True)
                st.info("""
                **Metode Oswald (Viskometer Kapiler)**

                Rumus ini didasarkan pada Hukum Poiseuille untuk aliran laminar melalui pipa kapiler:

                Ketika volume fluida yang sama dialirkan melalui viskometer, waktu alir bergantung pada viskositas dan densitas:

                t ∝ η / ρ  →  η ∝ t × ρ

                Sehingga perbandingan dua fluida:
                η₂/η₁ = (t₂ × ρ₂) / (t₁ × ρ₁)

                **Syarat pengukuran:**
                • Aliran harus laminar (tidak turbulen)
                • Suhu konstan (viskositas sangat sensitif terhadap suhu)
                • Volume fluida yang dialirkan sama untuk uji dan referensi
                • Viskometer dalam posisi vertikal yang sama

                **Referensi:**
                • Air suling 20°C: η = 0.001002 Pa·s, ρ = 1000 kg/m³
                • Air suling 25°C: η = 0.00089 Pa·s, ρ = 997 kg/m³
                """)

                st.markdown("<h4>📊 Referensi Viskositas & Densitas Beberapa Zat</h4>", unsafe_allow_html=True)
                ref_data = {
                    "Zat": ["Air suling (20°C)", "Air suling (25°C)", "Air sabun", "Madu", "Oli SAE 30", "Glikol", "Glycerin", "Bensin", "Alkohol"],
                    "η (Pa·s)": [0.001002, 0.00089, 0.0015, 0.002, 0.1, 0.016, 1.41, 0.00029, 0.0012],
                    "ρ (kg/m³)": [1000, 997, 1020, 1420, 890, 1110, 1260, 750, 789]
                }
                st.table(ref_data)
                st.caption("*Nilai bersifat perkiraan, dapat bervariasi menurut komposisi dan suhu")

    # --- KALKULATOR SUDUT REPOSISI ---
    elif calc_type == "📐 Sudut Reposisi":
        st.markdown("<div class='sub-header'>📐 Kalkulator Sudut Reposisi (θ = arctan h/r)</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='formula-box' style='text-align:center;'>
            <h3>📐 Rumus Sudut Reposisi dari Geometri Tumpukan</h3>
            <p style='font-size:1.4em; color:#1f77b4;'><b>tan θ = h / r</b></p>
            <p style='font-size:1.2em; color:#ff7f0e;'><b>θ = arctan (h / r)</b></p>
            <p style='color:#666;'>
                θ = sudut reposisi | h = tinggi sampel tumpukan | r = jari-jari dasar tumpukan
            </p>
        </div>
        """)

        col1, col2 = st.columns(2)
        with col1:
            h = st.number_input("Tinggi sampel tumpukan (h):", min_value=0.0, value=5.0, step=0.1, format="%.2f")
            h_unit = st.selectbox("Satuan tinggi:", ["m", "cm", "mm", "ft", "in"])
        with col2:
            r = st.number_input("Jari-jari dasar tumpukan (r):", min_value=0.0, value=10.0, step=0.1, format="%.2f")
            r_unit = st.selectbox("Satuan jari-jari:", ["m", "cm", "mm", "ft", "in"])

        if st.button("🔍 Hitung Sudut Reposisi", type="primary"):
            if h <= 0 or r <= 0:
                st.error("❌ Tinggi (h) dan jari-jari (r) harus lebih besar dari 0!")
            else:
                # Konversi ke satuan yang sama (m)
                unit_to_m = {"m": 1, "cm": 0.01, "mm": 0.001, "ft": 0.3048, "in": 0.0254}
                h_m = h * unit_to_m[h_unit]
                r_m = r * unit_to_m[r_unit]

                # Hitung sudut reposisi
                tan_theta = h_m / r_m
                theta_rad = math.atan(tan_theta)
                theta_deg = math.degrees(theta_rad)

                # Hitung koefisien gesek statis (μs) dari sudut reposisi
                mu_s = tan_theta

                st.success("✅ Perhitungan Berhasil!")

                st.markdown(f"""
                <div style='background-color:#e8f4f8; padding:20px; border-radius:12px; text-align:center; margin:20px 0; border-left:5px solid #1f77b4;'>
                    <h2 style='color:#1f77b4; margin:0;'>📐 Sudut Reposisi (θ)</h2>
                    <h1 style='color:#ff7f0e; margin:10px 0;'>θ = {theta_deg:.2f}°</h1>
                    <p style='font-size:1.2em; margin:0;'>= {theta_rad:.4f} radian</p>
                    <p style='font-size:1.1em; color:#666; margin-top:10px;'>
                        tan θ = {tan_theta:.4f} | Koefisien gesek statis μₛ ≈ {mu_s:.4f}
                    </p>
                </div>
                """)

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class='step-box'>
                    <b>Langkah 1:</b> Identifikasi variabel pengukuran<br>
                    • h (tinggi tumpukan) = {h} {h_unit} = {h_m:.4f} m<br>
                    • r (jari-jari dasar) = {r} {r_unit} = {r_m:.4f} m
                </div>
                <div class='step-box'>
                    <b>Langkah 2:</b> Pastikan satuan sama (konversi ke meter)<br>
                    • h = {h} × {unit_to_m[h_unit]} = {h_m:.4f} m<br>
                    • r = {r} × {unit_to_m[r_unit]} = {r_m:.4f} m
                </div>
                <div class='step-box'>
                    <b>Langkah 3:</b> Hitung tan θ<br>
                    tan θ = h / r = {h_m:.4f} / {r_m:.4f} = <b>{tan_theta:.4f}</b>
                </div>
                <div class='step-box'>
                    <b>Langkah 4:</b> Hitung sudut θ dalam radian<br>
                    θ = arctan({tan_theta:.4f}) = <b>{theta_rad:.4f} rad</b>
                </div>
                <div class='step-box'>
                    <b>Langkah 5:</b> Konversi ke derajat<br>
                    θ = {theta_rad:.4f} × (180/π) = <b>{theta_deg:.2f}°</b>
                </div>
                <div class='step-box'>
                    <b>Bonus:</b> Estimasi koefisien gesek statis<br>
                    μₛ = tan θ = <b>{mu_s:.4f}</b><br>
                    <i>(Hanya valid untuk permukaan kasar dan partikel seragam)</i>
                </div>
                """)

                st.markdown("<div class='sub-header'>📖 Penjelasan Teori & Rumus:</div>", unsafe_allow_html=True)
                st.info("""
                **Sudut Reposisi (Angle of Repose)** adalah sudut maksimum suatu permukaan tumpukan material 
                relatif terhadap horizontal di mana material masih dapat bertahan tanpa meluncur.

                **Rumus dari Geometri:**
                Untuk tumpukan material berbentuk kerucut:
                **tan θ = h / r**

                Dimana:
                • θ = sudut reposisi (° atau rad)
                • h = tinggi tumpukan material (sampel)
                • r = jari-jari dasar tumpukan

                **Hubungan dengan Koefisien Gesek:**
                Pada kondisi kritis (akan meluncur):
                • Komponen gaya gravitasi sejajar bidang: mg sin(θ)
                • Gaya gesek maksimum: fₘₐₓ = μₛ mg cos(θ)
                • Saat kritis: mg sin(θ) = μₛ mg cos(θ)
                • **μₛ = tan(θ) = h/r**

                **Aplikasi Praktis:**
                • Desain tangki silo, hopper, dan conveyor
                • Teknik pertambangan (stabilitas lereng tambang)
                • Farmasi (aliran serbuk obat)
                • Teknik sipil (stabilitas lereng tanah)
                • Industri pangan (aliran gula, tepung, biji)

                **Referensi Sudut Reposisi:**
                • Pasir kering: 30°-35° (h/r ≈ 0.58-0.70)
                • Tepung gandum: 45°-55° (h/r ≈ 1.0-1.43)
                • Batu bara: 35°-45° (h/r ≈ 0.70-1.0)
                • Semen: 40°-50° (h/r ≈ 0.84-1.19)
                """)

    # --- KALKULATOR PERSAMAAN GAS IDEAL ---
    elif calc_type == "⚡ Persamaan Gas Ideal":
        st.markdown("<div class='sub-header'>⚡ Kalkulator Persamaan Gas Ideal (PV = nRT)</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='formula-box' style='text-align:center;'>
            <h3>📐 Persamaan Gas Ideal</h3>
            <p style='font-size:1.4em; color:#1f77b4;'><b>PV = nRT</b></p>
            <p style='color:#666;'>
                P = tekanan | V = volume | n = jumlah mol | R = konstanta gas | T = suhu (Kelvin)
            </p>
        </div>
        """)

        # Pilih variabel yang dicari
        cari = st.selectbox(
            "🎯 Pilih yang ingin dicari:",
            ["🔵 Tekanan (P)", "🟢 Volume (V)", "🟡 Jumlah Mol (n)", "🔴 Suhu (T)"]
        )

        st.markdown("---")

        # Konstanta R dalam berbagai satuan
        R_SI = 8.314  # Pa·m³/(mol·K) = J/(mol·K)

        # ==================== CARI TEKANAN (P) ====================
        if cari == "🔵 Tekanan (P)":
            st.markdown("<h4 style='color:#1f77b4;'>🔵 Mencari Tekanan (P = nRT/V)</h4>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")
            with col2:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=300.0, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", "°C (Celcius)"])
            with col3:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])

            P_unit_out = st.selectbox("Satuan hasil tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])

            if st.button("🔍 Hitung Tekanan", type="primary"):
                if n_val <= 0 or V_val <= 0:
                    st.error("❌ n dan V harus lebih besar dari 0!")
                else:
                    # Konversi suhu ke Kelvin
                    if T_unit == "°C (Celcius)":
                        T_k = T_val + 273.15
                    else:
                        T_k = T_val

                    # Konversi volume ke m³
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]

                    # Hitung P dalam Pa (SI)
                    P_pa = (n_val * R_SI * T_k) / V_m3

                    # Konversi hasil ke satuan yang diminta
                    P_conv = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_hasil = P_pa / P_conv[P_unit_out]

                    st.success("✅ Perhitungan Berhasil!")

                    st.markdown(f"""
                    <div style='background-color:#e8f4f8; padding:20px; border-radius:12px; text-align:center; margin:20px 0; border-left:5px solid #1f77b4;'>
                        <h2 style='color:#1f77b4; margin:0;'>🔵 Tekanan (P)</h2>
                        <h1 style='color:#ff7f0e; margin:10px 0;'>P = {P_hasil:.4f} {P_unit_out}</h1>
                        <p style='font-size:1.1em;'>= {P_pa:.4f} Pa = {P_pa/1000:.4f} kPa = {P_pa/101325:.6f} atm</p>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Identifikasi variabel yang diketahui<br>
                        • n = {n_val} mol<br>
                        • T = {T_val} {T_unit.split()[0]} = {T_k:.2f} K<br>
                        • V = {V_val} {V_unit} = {V_m3:.6e} m³<br>
                        • R = {R_SI} J/(mol·K)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Pilih rumus sesuai yang dicari<br>
                        Karena yang dicari adalah <b>Tekanan (P)</b>, gunakan:<br>
                        <b>P = nRT / V</b>
                    </div>
                    <div class='step-box'>
                        <b>Langkah 3:</b> Pastikan semua satuan dalam SI<br>
                        • n sudah dalam mol ✓<br>
                        • T dikonversi ke Kelvin: {T_val} {T_unit.split()[0]} → {T_k:.2f} K<br>
                        • V dikonversi ke m³: {V_val} {V_unit} → {V_m3:.6e} m³
                    </div>
                    <div class='step-box'>
                        <b>Langkah 4:</b> Substitusi nilai ke rumus<br>
                        P = ({n_val} × {R_SI} × {T_k:.2f}) / {V_m3:.6e}<br>
                        P = {n_val * R_SI * T_k:.6e} / {V_m3:.6e}
                    </div>
                    <div class='step-box'>
                        <b>Langkah 5:</b> Hitung dan konversi ke satuan yang diminta<br>
                        P = {P_pa:.4f} Pa<br>
                        Konversi ke {P_unit_out}: {P_pa:.4f} / {P_conv[P_unit_out]} = <b>{P_hasil:.4f} {P_unit_out}</b>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                    st.info("""
                    **Persamaan Gas Ideal: PV = nRT**

                    Untuk mencari Tekanan (P), rumus diubah menjadi:
                    **P = nRT / V**

                    Dimana:
                    • P = Tekanan (Pa)
                    • n = Jumlah mol (mol)
                    • R = Konstanta gas universal = 8.314 J/(mol·K)
                    • T = Suhu mutlak (Kelvin)
                    • V = Volume (m³)

                    **Catatan penting:**
                    • Suhu harus dalam Kelvin! Jika menggunakan Celcius, tambahkan 273.15.
                    • Volume harus dalam m³ untuk konsistensi dengan satuan R.
                    • Gas ideal adalah gas yang mengikuti hukum ini pada tekanan rendah & suhu tinggi.
                    """)

        # ==================== CARI VOLUME (V) ====================
        elif cari == "🟢 Volume (V)":
            st.markdown("<h4 style='color:#2ca02c;'>🟢 Mencari Volume (V = nRT/P)</h4>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")
            with col2:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=300.0, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", "°C (Celcius)"])
            with col3:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])

            V_unit_out = st.selectbox("Satuan hasil volume:", ["m³", "L", "cm³", "mL"])

            if st.button("🔍 Hitung Volume", type="primary"):
                if n_val <= 0 or P_val <= 0:
                    st.error("❌ n dan P harus lebih besar dari 0!")
                else:
                    # Konversi suhu ke Kelvin
                    if T_unit == "°C (Celcius)":
                        T_k = T_val + 273.15
                    else:
                        T_k = T_val

                    # Konversi tekanan ke Pa
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]

                    # Hitung V dalam m³ (SI)
                    V_m3 = (n_val * R_SI * T_k) / P_pa

                    # Konversi hasil ke satuan yang diminta
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_hasil = V_m3 / V_conv[V_unit_out]

                    st.success("✅ Perhitungan Berhasil!")

                    st.markdown(f"""
                    <div style='background-color:#e8f4f8; padding:20px; border-radius:12px; text-align:center; margin:20px 0; border-left:5px solid #2ca02c;'>
                        <h2 style='color:#2ca02c; margin:0;'>🟢 Volume (V)</h2>
                        <h1 style='color:#ff7f0e; margin:10px 0;'>V = {V_hasil:.4f} {V_unit_out}</h1>
                        <p style='font-size:1.1em;'>= {V_m3:.6e} m³ = {V_m3*1000:.4f} L = {V_m3*1e6:.2f} cm³</p>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Identifikasi variabel yang diketahui<br>
                        • n = {n_val} mol<br>
                        • T = {T_val} {T_unit.split()[0]} = {T_k:.2f} K<br>
                        • P = {P_val} {P_unit} = {P_pa:.2f} Pa<br>
                        • R = {R_SI} J/(mol·K)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Pilih rumus sesuai yang dicari<br>
                        Karena yang dicari adalah <b>Volume (V)</b>, gunakan:<br>
                        <b>V = nRT / P</b>
                    </div>
                    <div class='step-box'>
                        <b>Langkah 3:</b> Pastikan semua satuan dalam SI<br>
                        • n sudah dalam mol ✓<br>
                        • T dikonversi ke Kelvin: {T_val} {T_unit.split()[0]} → {T_k:.2f} K<br>
                        • P dikonversi ke Pa: {P_val} {P_unit} → {P_pa:.2f} Pa
                    </div>
                    <div class='step-box'>
                        <b>Langkah 4:</b> Substitusi nilai ke rumus<br>
                        V = ({n_val} × {R_SI} × {T_k:.2f}) / {P_pa:.2f}<br>
                        V = {n_val * R_SI * T_k:.6e} / {P_pa:.2f}
                    </div>
                    <div class='step-box'>
                        <b>Langkah 5:</b> Hitung dan konversi ke satuan yang diminta<br>
                        V = {V_m3:.6e} m³<br>
                        Konversi ke {V_unit_out}: {V_m3:.6e} / {V_conv[V_unit_out]} = <b>{V_hasil:.4f} {V_unit_out}</b>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                    st.info("""
                    **Persamaan Gas Ideal: PV = nRT**

                    Untuk mencari Volume (V), rumus diubah menjadi:
                    **V = nRT / P**

                    Dimana:
                    • V = Volume (m³)
                    • n = Jumlah mol (mol)
                    • R = Konstanta gas universal = 8.314 J/(mol·K)
                    • T = Suhu mutlak (Kelvin)
                    • P = Tekanan (Pa)

                    **Catatan penting:**
                    • Tekanan harus dikonversi ke Pascal (Pa) agar konsisten dengan R.
                    • 1 atm = 101325 Pa = 1.01325 bar.
                    • Pada STP (0°C, 1 atm), 1 mol gas ideal memiliki volume 22.4 L.
                    """)

        # ==================== CARI MOL (n) ====================
        elif cari == "🟡 Jumlah Mol (n)":
            st.markdown("<h4 style='color:#ff7f0e;'>🟡 Mencari Jumlah Mol (n = PV/RT)</h4>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])
            with col2:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])
            with col3:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=273.15, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", "°C (Celcius)"])

            if st.button("🔍 Hitung Jumlah Mol", type="primary"):
                if P_val <= 0 or V_val <= 0:
                    st.error("❌ P dan V harus lebih besar dari 0!")
                else:
                    # Konversi suhu ke Kelvin
                    if T_unit == "°C (Celcius)":
                        T_k = T_val + 273.15
                    else:
                        T_k = T_val

                    # Konversi tekanan ke Pa
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]

                    # Konversi volume ke m³
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]

                    # Hitung n dalam mol
                    n_hasil = (P_pa * V_m3) / (R_SI * T_k)

                    st.success("✅ Perhitungan Berhasil!")

                    st.markdown(f"""
                    <div style='background-color:#e8f4f8; padding:20px; border-radius:12px; text-align:center; margin:20px 0; border-left:5px solid #ff7f0e;'>
                        <h2 style='color:#ff7f0e; margin:0;'>🟡 Jumlah Mol (n)</h2>
                        <h1 style='color:#1f77b4; margin:10px 0;'>n = {n_hasil:.4f} mol</h1>
                        <p style='font-size:1.1em;'>= {n_hasil*1000:.2f} mmol = {n_hasil/1000:.6f} kmol</p>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Identifikasi variabel yang diketahui<br>
                        • P = {P_val} {P_unit} = {P_pa:.2f} Pa<br>
                        • V = {V_val} {V_unit} = {V_m3:.6e} m³<br>
                        • T = {T_val} {T_unit.split()[0]} = {T_k:.2f} K<br>
                        • R = {R_SI} J/(mol·K)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Pilih rumus sesuai yang dicari<br>
                        Karena yang dicari adalah <b>Jumlah Mol (n)</b>, gunakan:<br>
                        <b>n = PV / RT</b>
                    </div>
                    <div class='step-box'>
                        <b>Langkah 3:</b> Pastikan semua satuan dalam SI<br>
                        • P dikonversi ke Pa: {P_val} {P_unit} → {P_pa:.2f} Pa<br>
                        • V dikonversi ke m³: {V_val} {V_unit} → {V_m3:.6e} m³<br>
                        • T dikonversi ke Kelvin: {T_val} {T_unit.split()[0]} → {T_k:.2f} K
                    </div>
                    <div class='step-box'>
                        <b>Langkah 4:</b> Substitusi nilai ke rumus<br>
                        n = ({P_pa:.2f} × {V_m3:.6e}) / ({R_SI} × {T_k:.2f})<br>
                        n = {P_pa * V_m3:.6e} / {R_SI * T_k:.4f}
                    </div>
                    <div class='step-box'>
                        <b>Langkah 5:</b> Hitung hasil akhir<br>
                        n = <b>{n_hasil:.4f} mol</b>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                    st.info("""
                    **Persamaan Gas Ideal: PV = nRT**

                    Untuk mencari Jumlah Mol (n), rumus diubah menjadi:
                    **n = PV / RT**

                    Dimana:
                    • n = Jumlah mol (mol)
                    • P = Tekanan (Pa)
                    • V = Volume (m³)
                    • R = Konstanta gas universal = 8.314 J/(mol·K)
                    • T = Suhu mutlak (Kelvin)

                    **Catatan penting:**
                    • Hasil dalam mol dapat dikonversi ke gram dengan: massa = n × Mr (massa molekul relatif).
                    • 1 mol gas ideal pada STP (0°C, 1 atm) memiliki volume 22.4 L.
                    • Konstanta R = 8.314 J/(mol·K) = 0.0821 L·atm/(mol·K).
                    """)

        # ==================== CARI SUHU (T) ====================
        elif cari == "🔴 Suhu (T)":
            st.markdown("<h4 style='color:#d62728;'>🔴 Mencari Suhu (T = PV/nR)</h4>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])
            with col2:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])
            with col3:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")

            T_unit_out = st.selectbox("Satuan hasil suhu:", ["K (Kelvin)", "°C (Celcius)"])

            if st.button("🔍 Hitung Suhu", type="primary"):
                if n_val <= 0:
                    st.error("❌ n harus lebih besar dari 0!")
                else:
                    # Konversi tekanan ke Pa
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]

                    # Konversi volume ke m³
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]

                    # Hitung T dalam Kelvin (SI)
                    T_k = (P_pa * V_m3) / (n_val * R_SI)

                    # Konversi ke satuan yang diminta
                    if T_unit_out == "°C (Celcius)":
                        T_hasil = T_k - 273.15
                    else:
                        T_hasil = T_k

                    st.success("✅ Perhitungan Berhasil!")

                    st.markdown(f"""
                    <div style='background-color:#e8f4f8; padding:20px; border-radius:12px; text-align:center; margin:20px 0; border-left:5px solid #d62728;'>
                        <h2 style='color:#d62728; margin:0;'>🔴 Suhu (T)</h2>
                        <h1 style='color:#ff7f0e; margin:10px 0;'>T = {T_hasil:.2f} {T_unit_out.split()[0]}</h1>
                        <p style='font-size:1.1em;'>= {T_k:.2f} K = {T_k-273.15:.2f} °C = {T_k*9/5-459.67:.2f} °F</p>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Identifikasi variabel yang diketahui<br>
                        • P = {P_val} {P_unit} = {P_pa:.2f} Pa<br>
                        • V = {V_val} {V_unit} = {V_m3:.6e} m³<br>
                        • n = {n_val} mol<br>
                        • R = {R_SI} J/(mol·K)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Pilih rumus sesuai yang dicari<br>
                        Karena yang dicari adalah <b>Suhu (T)</b>, gunakan:<br>
                        <b>T = PV / nR</b>
                    </div>
                    <div class='step-box'>
                        <b>Langkah 3:</b> Pastikan semua satuan dalam SI<br>
                        • P dikonversi ke Pa: {P_val} {P_unit} → {P_pa:.2f} Pa<br>
                        • V dikonversi ke m³: {V_val} {V_unit} → {V_m3:.6e} m³<br>
                        • n sudah dalam mol ✓
                    </div>
                    <div class='step-box'>
                        <b>Langkah 4:</b> Substitusi nilai ke rumus<br>
                        T = ({P_pa:.2f} × {V_m3:.6e}) / ({n_val} × {R_SI})<br>
                        T = {P_pa * V_m3:.6e} / {n_val * R_SI:.4f}
                    </div>
                    <div class='step-box'>
                        <b>Langkah 5:</b> Hitung dan konversi ke satuan yang diminta<br>
                        T = {T_k:.2f} K<br>
                        Konversi ke {T_unit_out.split()[0]}: {T_k:.2f} - 273.15 = <b>{T_hasil:.2f} {T_unit_out.split()[0]}</b>
                    </div>
                    """)

                    st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                    st.info("""
                    **Persamaan Gas Ideal: PV = nRT**

                    Untuk mencari Suhu (T), rumus diubah menjadi:
                    **T = PV / nR**

                    Dimana:
                    • T = Suhu mutlak (Kelvin)
                    • P = Tekanan (Pa)
                    • V = Volume (m³)
                    • n = Jumlah mol (mol)
                    • R = Konstanta gas universal = 8.314 J/(mol·K)

                    **Catatan penting:**
                    • Hasil awal selalu dalam Kelvin (K), lalu dikonversi ke Celcius jika diminta.
                    • Suhu mutlak tidak bisa negatif! Jika hasil T < 0 K, berarti ada kesalahan input.
                    • 0 K = -273.15°C = titik nol mutlak (tidak ada energi kinetik).
                    • Suhu standar = 273.15 K = 0°C = 32°F.
                    """)

    # --- KONVERSI SATUAN ---
    elif calc_type == "🔄 Konversi Satuan":
        st.markdown("<div class='sub-header'>🔄 Kalkulator Konversi Satuan</div>", unsafe_allow_html=True)

        category = st.selectbox("Kategori Besaran:", list(UNIT_TABLE.keys()))

        col1, col2, col3 = st.columns([2, 1, 2])

        units = list(UNIT_TABLE[category].keys())

        with col1:
            from_unit = st.selectbox("Dari:", units)
            value = st.number_input("Nilai:", value=1.0, step=0.1)

        with col2:
            st.markdown("<br><br><h2 style='text-align:center;'>➡️</h2>", unsafe_allow_html=True)

        with col3:
            to_unit = st.selectbox("Ke:", units)

        if st.button("🔄 Konversi", type="primary"):
            result = auto_convert(value, from_unit, to_unit, category)

            if result is not None:
                st.success(f"✅ **{value} {from_unit} = {result:.6g} {to_unit}**")

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                if category == "Suhu":
                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Konversi Suhu:</b><br>
                        {value}°{from_unit} → {result:.4f}°{to_unit}<br>
                        <i>(Menggunakan rumus konversi suhu spesifik)</i>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    base = value * UNIT_TABLE[category][from_unit]
                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Konversi ke unit dasar SI<br>
                        {value} {from_unit} = {value} × {UNIT_TABLE[category][from_unit]} = {base:.6e} (unit dasar)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Konversi ke target<br>
                        {base:.6e} / {UNIT_TABLE[category][to_unit]} = {result:.6g} {to_unit}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Konversi tidak valid!")

# ==================== HALAMAN UNIT CONVERTER ====================
elif menu == "🔄 Unit Converter":
    st.markdown("<div class='main-header'>🔄 Auto Unit Converter</div>", unsafe_allow_html=True)
    st.markdown("Konversi satuan otomatis untuk berbagai besaran fisika dengan langkah pengerjaan.")

    converter_type = st.selectbox(
        "Pilih Kategori Konversi:",
        ["📏 Panjang", "⚖️ Massa", "⏱️ Waktu", "🌡️ Suhu", "💨 Tekanan", "⚡ Energi", "🔌 Daya", "📊 Kerapatan", "🍯 Viskositas", "💪 Gaya"]
    )

    category_map = {
        "📏 Panjang": "Panjang", "⚖️ Massa": "Massa", "⏱️ Waktu": "Waktu",
        "🌡️ Suhu": "Suhu", "💨 Tekanan": "Tekanan", "⚡ Energi": "Energi",
        "🔌 Daya": "Daya", "📊 Kerapatan": "Kerapatan", "🍯 Viskositas": "Viskositas", "💪 Gaya": "Gaya"
    }

    cat = category_map[converter_type]
    units = list(UNIT_TABLE[cat].keys())

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        from_u = st.selectbox("Dari Satuan:", units, key="from")
        val = st.number_input("Masukkan Nilai:", value=1.0, step=0.1)

    with col2:
        st.markdown("<br><br><h1 style='text-align:center;'>⇄</h1>", unsafe_allow_html=True)

    with col3:
        to_u = st.selectbox("Ke Satuan:", units, key="to")

    if st.button("🚀 Konversi Sekarang", type="primary", use_container_width=True):
        result = auto_convert(val, from_u, to_u, cat)

        if result is not None:
            st.balloons()
            st.markdown(f"""
            <div style='background-color:#e8f4f8; padding:20px; border-radius:15px; text-align:center; margin:20px 0;'>
                <h2 style='color:#1f77b4; margin:0;'>{val} {from_u}</h2>
                <h1 style='margin:10px 0;'>⬇️</h1>
                <h2 style='color:#ff7f0e; margin:0;'>= {result:.6g} {to_u}</h2>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📋 Lihat Langkah Pengerjaan"):
                if cat == "Suhu":
                    st.markdown(f"""
                    **Rumus Konversi Suhu:**
                    - Celcius → Kelvin: K = C + 273.15
                    - Celcius → Fahrenheit: F = C × 9/5 + 32
                    - Celcius → Rankine: R = (C + 273.15) × 9/5
                    - Fahrenheit → Celcius: C = (F - 32) × 5/9

                    **Hasil:** {val}°{from_u} = {result:.4f}°{to_u}
                    """)
                else:
                    base_val = val * UNIT_TABLE[cat][from_u]
                    st.markdown(f"""
                    **Langkah 1: Konversi ke Unit Dasar SI**

                    Faktor konversi {from_u} ke unit dasar = {UNIT_TABLE[cat][from_u]}

                    {val} {from_u} × {UNIT_TABLE[cat][from_u]} = {base_val:.6e} (unit dasar SI)

                    **Langkah 2: Konversi ke Satuan Target**

                    Faktor konversi unit dasar ke {to_u} = 1/{UNIT_TABLE[cat][to_u]}

                    {base_val:.6e} ÷ {UNIT_TABLE[cat][to_u]} = **{result:.6g} {to_u}**
                    """)
        else:
            st.error("❌ Konversi gagal. Periksa satuan yang dipilih.")

    st.markdown("---")
    st.markdown("<div class='sub-header'>📊 Tabel Konversi Cepat</div>", unsafe_allow_html=True)

    quick_conversions = {
        "Panjang": [("1 m", "100 cm", "3.281 ft", "39.37 in"), ("1 km", "0.621 mi", "3281 ft", "100000 cm")],
        "Massa": [("1 kg", "1000 g", "2.205 lb", "35.27 oz"), ("1 ton", "1000 kg", "2205 lb", "1e6 g")],
        "Suhu": [("0°C", "32°F", "273.15 K", "491.67°R"), ("100°C", "212°F", "373.15 K", "671.67°R")],
        "Tekanan": [("1 atm", "101325 Pa", "1.013 bar", "760 mmHg"), ("1 bar", "100000 Pa", "0.987 atm", "750 mmHg")],
        "Energi": [("1 J", "0.239 cal", "0.000278 Wh", "6.24e18 eV"), ("1 kWh", "3.6e6 J", "860 kcal", "3.6e9 mJ")],
        "Kerapatan": [("1 g/cm³", "1000 kg/m³", "1 kg/L", "62.43 lb/ft³"), ("1 kg/m³", "0.001 g/cm³", "0.001 kg/L", "0.062 lb/ft³")],
    }

    if cat in quick_conversions:
        for row in quick_conversions[cat]:
            cols = st.columns(len(row))
            for i, val_str in enumerate(row):
                with cols[i]:
                    st.metric(label="", value=val_str)

# ==================== HALAMAN QUIZ ====================
elif menu == "📝 Quiz Fisika":
    st.markdown("<div class='main-header'>📝 Quiz Fisika Dasar</div>", unsafe_allow_html=True)
    st.markdown("Latihan soal pilihan ganda dan isian singkat dengan pembahasan otomatis. Kategori: **Kuliah Dasar**")

    # Inisialisasi state
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = set()
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:15px; border-radius:10px; text-align:center;'>
            <h3>🏆 Skor: {st.session_state.quiz_score} / {len(QUIZ_QUESTIONS)}</h3>
            <progress value={st.session_state.quiz_score} max={len(QUIZ_QUESTIONS)} style='width:100%; height:20px;'></progress>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tampilkan semua soal
    for idx, q in enumerate(QUIZ_QUESTIONS):
        with st.container():
            st.markdown(f"<div class='sub-header'>Soal {idx+1} ({q['type'].replace('_', ' ').title()})</div>", unsafe_allow_html=True)
            st.markdown(f"**{q['soal']}**")

            answered = idx in st.session_state.quiz_answered

            if q['type'] == "pilihan_ganda":
                user_answer = st.radio(
                    f"Pilih jawaban (Soal {idx+1}):",
                    q['pilihan'],
                    key=f"pg_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx+1}", key=f"btn_pg_{idx}"):
                        st.session_state.quiz_answered.add(idx)
                        if user_answer == q['jawaban']:
                            st.session_state.quiz_score += 1
                            st.success("✅ Benar!")
                        else:
                            st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                        st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                        st.rerun()
                else:
                    # Tampilkan hasil yang tersimpan
                    # Cek apakah jawaban benar (perlu cek dari state, tapi simpelnya kita cek dari score logic)
                    # Untuk sederhana, tampilkan pembahasan saja
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

            else:  # isian
                user_answer = st.text_input(
                    f"Jawaban Anda (Soal {idx+1}):",
                    key=f"isian_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx+1}", key=f"btn_isian_{idx}"):
                        if user_answer.strip():
                            st.session_state.quiz_answered.add(idx)
                            # Cek jawaban (toleransi untuk angka)
                            try:
                                user_val = float(user_answer.strip().replace(',', '.'))
                                correct_val = float(q['jawaban'].replace(',', '.'))
                                if abs(user_val - correct_val) < 0.01 * max(abs(correct_val), 1):
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            except:
                                if user_answer.strip().lower() == q['jawaban'].strip().lower():
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                            st.rerun()
                        else:
                            st.warning("⚠️ Masukkan jawaban terlebih dahulu!")
                else:
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

            st.markdown("---")

    # Tombol reset
    if st.button("🔄 Reset Quiz", type="secondary"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = set()
        st.rerun()

    if st.session_state.quiz_score == len(QUIZ_QUESTIONS):
        st.balloons()
        st.markdown("""
        <div style='background-color:#d4edda; padding:20px; border-radius:15px; text-align:center; margin-top:20px;'>
            <h1 style='color:#155724;'>🎉 Selamat! 🎉</h1>
            <h2 style='color:#155724;'>Anda telah menjawab semua soal dengan benar!</h2>
            <p style='font-size:1.2em;'>Skor sempurna: {}/{}</p>
        </div>
        """.format(len(QUIZ_QUESTIONS), len(QUIZ_QUESTIONS)), unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align:center; color:#888;'>⚛️ Smart Physics Calculator v1.0<br>Built with Streamlit</p>", unsafe_allow_html=True)
