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
        
        active_metrics = {}
        REV_BASE = 1200000

        # EBITDA: Bench 22%
        if in_eb is not None:
            gap = max(0.0, 22.0 - in_eb)
            # If EBITDA is 15%, loss is calculated. If 60%, loss is 0.
            loss = (gap / 100) * REV_BASE if in_eb < 22 else 0.0
            active_metrics['EBITDA'] = {'gap': gap, 'loss': loss, 'status': "red" if in_eb < 22 else "green"}

        # No Shows: Bench 5%
        if in_ns is not None:
            gap = max(0.0, in_ns - 5.0)
            loss = (gap / 100) * REV_BASE if in_ns > 5 else 0.0
            active_metrics['No Shows'] = {'gap': gap, 'loss': loss, 'status': "red" if in_ns > 5 else "green"}

        # Insurance: Bench 25 days
        if in_id is not None:
            gap = max(0.0, in_id - 25.0)
            loss = (gap / 365) * 0.07 * REV_BASE if in_id > 25 else 0.0
            active_metrics['Insurance'] = {'gap': gap, 'loss': loss, 'status': "red" if in_id > 25 else "green"}

        # Hiring: Bench 4 weeks
        if in_hw is not None:
            gap = max(0.0, in_hw - 4.0)
            loss = (gap * 5120) - 10000 if in_hw > 4 else 0.0
            active_metrics['Hiring'] = {'gap': gap, 'loss': max(0.0, loss), 'status': "red" if in_hw > 4 else "green"}

        # NP Conversion: DEPENDENCY (Calls + NP Count)
        if in_cp is not None and in_np is not None:
            gap = max(0.0, 80.0 - in_cp)
            loss = (gap / 100) * in_np * 1000 * 12 if in_cp < 80 else 0.0
            active_metrics['Patient Conversion'] = {'gap': gap, 'loss': loss, 'status': "red" if in_cp < 80 else "green"}

        # Hygiene System: DEPENDENCY (Prod + Perio)
        if in_hp is not None:
            hp_gap = max(0.0, 30.0 - in_hp)
            hp_loss = (hp_gap / 100) * REV_BASE if in_hp < 30 else 0.0
            active_metrics['Hygiene Production'] = {'gap': hp_gap, 'loss': hp_loss, 'status': "red" if in_hp < 30 else "green"}
            
            if in_per is not None:
                per_gap = max(0.0, 40.0 - in_per)
                # Math dependency on production level
                h_base = (in_hp / 100) * REV_BASE if in_hp >= 30 else (0.30 * REV_BASE)
                per_loss = (per_gap / 100) * h_base if in_per < 40 else 0.0
                active_metrics['Hygiene Perio'] = {'gap': per_gap, 'loss': per_loss, 'status': "red" if in_per < 40 else "green"}

        # 4. FINAL VERDICT LOGIC
        if active_metrics:
            # Low Hanging Fruit = The entry with the largest 'gap'
            winner = max(active_metrics, key=lambda k: active_metrics[k]['gap'])
            
            # TOTAL LEAKAGE = Only sum areas that are actually failing (Status RED)
            # This prevents a "Green" EBITDA from adding noise to the total number.
            total_leakage = sum(m['loss'] for m in active_metrics.values() if m['status'] == "red")

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">Your furthest variance from benchmark is <b>{winner}</b>.</p>
                <p style="font-size: 1.1rem;">Your estimated annual revenue leakage is <b>${total_leakage:,.0f}</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, d in active_metrics.items():
                st.markdown(f'<div class="status-box status-{d["status"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. GHL FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
