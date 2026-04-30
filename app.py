import streamlit as st
import streamlit.components.v1 as components
import time

# 1. SETUP
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001e36; color: #ffffff; }
    .stNumberInput label { color: #ffffff !important; font-weight: 600; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .report-card { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 15px; border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .status-box { padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.8rem; border: 2px solid transparent; text-transform: uppercase; }
    .status-green { border-color: #28a745; background: rgba(40, 167, 69, 0.1); color: #28a745; }
    .status-red { border-color: #dc3545; background: rgba(220, 53, 69, 0.1); color: #dc3545; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# 2. INPUTS
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        in_eb = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="f_eb")
        in_ns = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="f_ns")
        in_id = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="f_id")
        in_hw = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="f_hw")
    with c2:
        in_hp = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="f_hp")
        in_per = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="f_per")
        in_np = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="f_np")
        in_cp = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="f_cp")

    if st.button("Generate Autopsy Results"):
        # 3. THE VARIANCE ENGINE
        # We track 'variance' (how far from goal) and 'loss' (dollar impact)
        # The Verdict will be chosen by the HIGHEST VARIANCE.
        
        data_pool = {}
        REV = 1200000

        # EBITDA (Goal: 22%)
        if in_eb is not None:
            var = max(0, 22 - in_eb)
            data_pool['EBITDA'] = {'var': var, 'loss': (var/100)*REV, 'color': "green" if in_eb >= 22 else "red"}

        # No Shows (Goal: 5%)
        if in_ns is not None:
            var = max(0, in_ns - 5)
            data_pool['No Shows'] = {'var': var, 'loss': (var/100)*REV, 'color': "green" if in_ns <= 5 else "red"}

        # Insurance (Goal: 25 days)
        if in_id is not None:
            var = max(0, in_id - 25)
            # Normalizing variance for days (treating 10 days over as a "10 point" gap)
            data_pool['Insurance'] = {'var': var, 'loss': (var/365)*0.07*REV, 'color': "green" if in_id <= 25 else "red"}

        # Hiring (Goal: 4 weeks)
        if in_hw is not None:
            var = max(0, in_hw - 4)
            data_pool['Hiring'] = {'var': var, 'loss': (var*5120)-10000 if var > 0 else 0, 'color': "green" if in_hw <= 4 else "red"}

        # NP CONVERSION (DEPENDENCY 1: Calls + NP Count)
        if in_cp is not None and in_np is not None:
            var = max(0, 80 - in_cp)
            data_pool['Patient Conversion'] = {'var': var, 'loss': (var/100)*in_np*1000*12, 'color': "green" if in_cp >= 80 else "red"}

        # HYGIENE SYSTEM (DEPENDENCY 2: Prod + Perio)
        if in_hp is not None:
            prod_var = max(0, 30 - in_hp)
            data_pool['Hygiene Production'] = {'var': prod_var, 'loss': (prod_var/100)*REV, 'color': "green" if in_hp >= 30 else "red"}
            
            if in_per is not None:
                per_var = max(0, 40 - in_per)
                # Perio base depends on Prod %
                hyg_base = (in_hp/100)*REV if in_hp >= 30 else (0.30*REV)
                data_pool['Hygiene Perio'] = {'var': per_var, 'loss': (per_var/100)*hyg_base, 'color': "green" if in_per >= 40 else "red"}

        # 4. THE VERDICT ( Furthest from benchmark )
        if data_pool:
            # Find the key with the largest 'var' (variance)
            winner_key = max(data_pool, key=lambda x: data_pool[x]['var'])
            total_money = sum(v['loss'] for v in data_pool.values())

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">Your practice is furthest from industry benchmarks in <b>{winner_key}</b>.</p>
                <p style="font-size: 1.1rem;">This variance, combined with other gaps, is costing you roughly <b>${total_money:,.0f}</b> per year.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, d in data_pool.items():
                st.markdown(f'<div class="status-box status-{d["color"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
