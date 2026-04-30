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
    .status-white { border-color: #ffffff; background: rgba(255, 255, 255, 0.1); color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# 2. THE INPUTS
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        eb_val = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="input_ebitda")
        ns_val = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="input_noshow")
        id_val = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="input_ins")
        hw_val = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="input_hire")
    with c2:
        hp_val = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="input_hprod")
        hper_val = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="input_hperio")
        np_val = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="input_np")
        cp_val = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="input_conv")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(3):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {3-i}s")
                time.sleep(1)
        
        # 3. ABSOLUTE ISOLATION MATH ENGINE
        # Each category is calculated with ZERO reference to other category variables.
        REV_BASE = 1200000
        
        results = {}

        # 1. EBITDA Logic
        if eb_val is not None:
            results['EBITDA'] = {
                'loss': max(0.0, (22 - eb_val) / 100 * REV_BASE),
                'color': "green" if eb_val >= 22 else "red"
            }

        # 2. No Shows Logic
        if ns_val is not None:
            results['No Shows'] = {
                'loss': max(0.0, (ns_val - 5) / 100 * REV_BASE),
                'color': "green" if ns_val <= 5 else "red"
            }

        # 3. Insurance Logic
        if id_val is not None:
            results['Insurance'] = {
                'loss': max(0.0, (id_val - 25) / 365 * 0.07 * REV_BASE),
                'color': "green" if id_val <= 25 else "red"
            }

        # 4. Hiring Logic
        if hw_val is not None:
            results['Hiring'] = {
                'loss': max(0.0, (hw_val - 4) * 5120 - 10000),
                'color': "green" if hw_val <= 4 else "red"
            }

        # 5. Patient Conversion Logic
        if cp_val is not None and np_val is not None:
            results['Patient Conversion'] = {
                'loss': max(0.0, (80 - cp_val) / 100 * np_val * 1000 * 12),
                'color': "green" if cp_val >= 80 else "red"
            }

        # 6. Hygiene Production Logic
        if hp_val is not None:
            results['Hygiene Production'] = {
                'loss': max(0.0, (30 - hp_val) / 100 * REV_BASE),
                'color': "green" if hp_val >= 30 else "red"
            }

        # 7. Hygiene Perio Logic (CRITICAL FIX: NO CROSS-DEPENDENCY)
        if hper_val is not None:
            # We use a static 30% revenue benchmark for hygiene as the base for perio.
            # This ensures Perio ONLY changes when Perio % or Hygiene Prod % change.
            # It is now physically impossible for EBITDA to affect this.
            hyg_revenue_base = (hp_val / 100 * REV_BASE) if hp_val is not None else (0.30 * REV_BASE)
            perio_gap = (40 - hper_val) / 100
            results['Hygiene Perio'] = {
                'loss': max(0.0, perio_gap * hyg_revenue_base),
                'color': "green" if hper_val >= 40 else "red"
            }

        # 4. FINAL DISPLAY
        if results:
            top_loss_key = max(results, key=lambda x: results[x]['loss'])
            total_loss_val = sum(v['loss'] for v in results.values())
            
            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
                <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{top_loss_key}</b></p>
                <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_loss_val:,.0f}</b> on the table annually.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in results.items():
                st.markdown(f'<div class="status-box status-{data["color"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
