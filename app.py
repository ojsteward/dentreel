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
        
        # 3. THE SILO MATH
        # We calculate each loss independently. 
        # Loss is only calculated if the metric is WORSE than the benchmark.
        RESULTS = {}
        REV_BASE = 1200000

        # EBITDA: 22% Bench
        if v_eb is not None:
            RESULTS['EBITDA'] = {
                'loss': ((22 - v_eb) / 100 * REV_BASE) if v_eb < 22 else 0,
                'status': "red" if v_eb < 22 else "green"
            }

        # No Shows: 5% Bench
        if v_ns is not None:
            RESULTS['No Shows'] = {
                'loss': ((v_ns - 5) / 100 * REV_BASE) if v_ns > 5 else 0,
                'status': "red" if v_ns > 5 else "green"
            }

        # Insurance: 25 Days Bench
        if v_id is not None:
            RESULTS['Insurance'] = {
                'loss': ((v_id - 25) / 365 * 0.07 * REV_BASE) if v_id > 25 else 0,
                'status': "red" if v_id > 25 else "green"
            }

        # Hiring: 4 Weeks Bench
        if v_hw is not None:
            raw_loss = ((v_hw - 4) * 5120) - 10000 if v_hw > 4 else 0
            RESULTS['Hiring'] = {
                'loss': max(0, raw_loss),
                'status': "red" if v_hw > 4 else "green"
            }

        # NP Conv: 80% Bench (Calls + NP Count dependency)
        if v_cp is not None and v_np is not None:
            RESULTS['Patient Conversion'] = {
                'loss': ((80 - v_cp) / 100 * v_np * 1000 * 12) if v_cp < 80 else 0,
                'status': "red" if v_cp < 80 else "green"
            }

        # Hygiene Prod: 30% Bench
        if v_hp is not None:
            RESULTS['Hygiene Production'] = {
                'loss': ((30 - v_hp) / 100 * REV_BASE) if v_hp < 30 else 0,
                'status': "red" if v_hp < 30 else "green"
            }
            
            # Hygiene Perio: 40% Bench (Depends on Prod for base)
            if v_per is not None:
                h_base = (v_hp / 100 * REV_BASE) if v_hp >= 30 else (0.30 * REV_BASE)
                RESULTS['Hygiene Perio'] = {
                    'loss': ((40 - v_per) / 100 * h_base) if v_per < 40 else 0,
                    'status': "red" if v_per < 40 else "green"
                }

        # 4. THE VERDICT (SINGLE VARIABLE FOCUS)
        if RESULTS:
            # Filter for failing categories
            red_items = {k: v for k, v in RESULTS.items() if v['status'] == "red"}
            
            if red_items:
                # Identify the "Winner" (the specific variable losing the most money)
                winner_key = max(red_items, key=lambda k: red_items[k]['loss'])
                winner_loss = red_items[winner_key]['loss']
            else:
                winner_key = "Performance Benchmarks Met"
                winner_loss = 0

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">Your single greatest financial leak is <b>{winner_key}</b>.</p>
                <p style="font-size: 1.1rem;">This specific area is costing your office <b>${winner_loss:,.0f}</b> annually.</p>
                <p style="font-size: 0.8rem; color: #00d2ff; margin-top:10px;">*Only the primary leak is calculated in this total.</p>
            </div>
            """, unsafe_allow_html=True)

            # Display Grid
            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in RESULTS.items():
                st.markdown(f'<div class="status-box status-{data["status"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
