import streamlit as st
import streamlit.components.v1 as components

# 1. SETUP & BRANDING
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

# 2. INPUT SECTION
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        v_eb = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        v_ns = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        v_id = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        v_hw = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with col2:
        v_hp = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        v_per = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1)
        v_np = st.number_input("# New Patients per Month", min_value=0, value=None, step=1)
        v_cp = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        
        # 3. THE SILO ENGINE
        FINAL_RESULTS = {}
        REV_BASE = 1200000

        # --- SILO 1: EBITDA ---
        if v_eb is not None:
            loss = ((22 - v_eb) / 100 * REV_BASE) if v_eb < 22 else 0
            FINAL_RESULTS['EBITDA'] = {'loss': loss, 'status': "red" if v_eb < 22 else "green"}

        # --- SILO 2: NO SHOWS ---
        if v_ns is not None:
            loss = ((v_ns - 5) / 100 * REV_BASE) if v_ns > 5 else 0
            FINAL_RESULTS['No Shows'] = {'loss': loss, 'status': "red" if v_ns > 5 else "green"}

        # --- SILO 3: INSURANCE ---
        if v_id is not None:
            loss = ((v_id - 25) / 365 * 0.07 * REV_BASE) if v_id > 25 else 0
            FINAL_RESULTS['Insurance'] = {'loss': loss, 'status': "red" if v_id > 25 else "green"}

        # --- SILO 4: HIRING ---
        if v_hw is not None:
            raw = ((v_hw - 4) * 5120) - 10000 if v_hw > 4 else 0
            FINAL_RESULTS['Hiring'] = {'loss': max(0, raw), 'status': "red" if v_hw > 4 else "green"}

        # --- SILO 5: PATIENT CONVERSION (COMBINED) ---
        # Calculation uses BOTH inputs to create ONE result
        if v_np is not None and v_cp is not None:
            loss = ((80 - v_cp) / 100 * v_np * 1000 * 12) if v_cp < 80 else 0
            FINAL_RESULTS['Patient Conversion'] = {'loss': loss, 'status': "red" if v_cp < 80 else "green"}

        # --- SILO 6: HYGIENE SYSTEM (COMBINED) ---
        # Calculation uses BOTH inputs to create ONE result
        if v_hp is not None and v_per is not None:
            prod_loss = ((30 - v_hp) / 100 * REV_BASE) if v_hp < 30 else 0
            h_base = (v_hp / 100 * REV_BASE) if v_hp >= 30 else (0.30 * REV_BASE)
            perio_loss = ((40 - v_per) / 100 * h_base) if v_per < 40 else 0
            
            total_h_loss = prod_loss + perio_loss
            FINAL_RESULTS['Hygiene System'] = {
                'loss': total_h_loss, 
                'status': "red" if (v_hp < 30 or v_per < 40) else "green"
            }

        # --- THE VERDICT (WINNER TAKE ALL) ---
        if FINAL_RESULTS:
            # Only look at the RED categories
            failing = {k: v for k, v in FINAL_RESULTS.items() if v['status'] == "red"}
            
            if failing:
                # The "Verdict" is strictly the category with the highest loss
                winner_key = max(failing, key=lambda k: failing[k]['loss'])
                winner_loss = failing[winner_key]['loss']
            else:
                winner_key = "Practice Optimized"
                winner_loss = 0

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">Your primary revenue leak is <b>{winner_key}</b>.</p>
                <p style="font-size: 1.1rem;">This specific area is costing your office <b>${winner_loss:,.0f}</b> annually.</p>
            </div>
            """, unsafe_allow_html=True)

            # Status Boxes
            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in FINAL_RESULTS.items():
                st.markdown(f'<div class="status-box status-{data["status"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
