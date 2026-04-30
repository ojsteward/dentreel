import streamlit as st
import streamlit.components.v1 as components
import time

# 1. STYLE & BRANDING
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
        in_eb = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        in_ns = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        in_id = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        in_hw = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with c2:
        in_hp = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        in_per = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1)
        in_np = st.number_input("# New Patients per Month", min_value=0, value=None, step=1)
        in_cp = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        
        leaks = {}
        REV_BASE = 1200000

        # --- INDEPENDENT LOSS CALCULATIONS ---
        
        # EBITDA (Goal: 22%)
        if in_eb is not None:
            loss = ((22 - in_eb) / 100 * REV_BASE) if in_eb < 22 else 0
            leaks['EBITDA'] = {'loss': loss, 'status': "red" if in_eb < 22 else "green"}

        # No Shows (Goal: 5%)
        if in_ns is not None:
            loss = ((in_ns - 5) / 100 * REV_BASE) if in_ns > 5 else 0
            leaks['No Shows'] = {'loss': loss, 'status': "red" if in_ns > 5 else "green"}

        # Insurance (Goal: 25 Days)
        if in_id is not None:
            loss = ((in_id - 25) / 365 * 0.07 * REV_BASE) if in_id > 25 else 0
            leaks['Insurance'] = {'loss': loss, 'status': "red" if in_id > 25 else "green"}

        # Hiring (Goal: 4 Weeks)
        if in_hw is not None:
            loss = max(0, ((in_hw - 4) * 5120) - 10000) if in_hw > 4 else 0
            leaks['Hiring'] = {'loss': loss, 'status': "red" if in_hw > 4 else "green"}

        # Patient Conversion (Goal: 80%) - DEPENDENCY: NP Count
        if in_cp is not None and in_np is not None:
            loss = ((80 - in_cp) / 100 * in_np * 1000 * 12) if in_cp < 80 else 0
            leaks['Patient Conversion'] = {'loss': loss, 'status': "red" if in_cp < 80 else "green"}

        # Hygiene Production (Goal: 30%)
        if in_hp is not None:
            hp_loss = ((30 - in_hp) / 100 * REV_BASE) if in_hp < 30 else 0
            leaks['Hygiene Production'] = {'loss': hp_loss, 'status': "red" if in_hp < 30 else "green"}
            
            # Hygiene Perio (Goal: 40%) - DEPENDENCY: Hygiene Prod %
            if in_per is not None:
                h_base = (in_hp / 100 * REV_BASE) if in_hp >= 30 else (0.30 * REV_BASE)
                per_loss = ((40 - in_per) / 100 * h_base) if in_per < 40 else 0
                leaks['Hygiene Perio'] = {'loss': per_loss, 'status': "red" if in_per < 40 else "green"}

        # --- THE VERDICT: GREATEST NEGATIVE IMPACT ---
        if leaks:
            # Filter for only those with a "red" status (failing benchmarks)
            failing_metrics = {k: v for k, v in leaks.items() if v['status'] == "red"}
            
            if failing_metrics:
                # Primary Leak = The specific variable losing the most money
                primary_leak_key = max(failing_metrics, key=lambda k: failing_metrics[k]['loss'])
                primary_leak_value = failing_metrics[primary_leak_key]['loss']
                
                # Total Leakage = Sum of all negative impacts
                total_annual_leakage = sum(m['loss'] for m in failing_metrics.values())
            else:
                primary_leak_key = "None (Practice is Optimized)"
                primary_leak_value = 0
                total_annual_leakage = 0

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">The variable losing your office the most money is <b>{primary_leak_key}</b>.</p>
                <p style="font-size: 1.1rem;">Your total annual revenue leakage across all failing metrics is <b>${total_annual_leakage:,.0f}</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            # Display Status Grid
            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in leaks.items():
                st.markdown(f'<div class="status-box status-{data["status"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. GHL FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
