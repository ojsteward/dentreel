import streamlit as st
import streamlit.components.v1 as components
import time

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

    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 30px; border-radius: 15px; 
        border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px;
    }

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

# 2. INPUT SECTION
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        v_ebitda = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="v_eb")
        v_noshow = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="v_ns")
        v_ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="v_id")
        v_hire_wks = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="v_hw")
    with col2:
        v_hyg_prod = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="v_hp")
        v_hyg_perio = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="v_hper")
        v_np_count = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="v_npc")
        v_conv_pct = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="v_cp")

    if st.button("Generate Autopsy Results"):
        # Local variable reset at button click to prevent sum-leakage
        FINAL_RESULTS = {}
        REV_ANCHOR = 1200000

        # --- INDEPENDENT MATH BLOCKS ---
        
        # 1. EBITDA
        if v_ebitda is not None:
            eb_diff = max(0, 22 - v_ebitda)
            FINAL_RESULTS['EBITDA'] = {
                'loss': (eb_diff / 100) * REV_ANCHOR,
                'color': "green" if v_ebitda >= 22 else "red"
            }

        # 2. NO SHOWS
        if v_noshow is not None:
            ns_diff = max(0, v_noshow - 5)
            FINAL_RESULTS['No Shows'] = {
                'loss': (ns_diff / 100) * REV_ANCHOR,
                'color': "green" if v_noshow <= 5 else "red"
            }

        # 3. INSURANCE
        if v_ins_days is not None:
            ins_diff = max(0, v_ins_days - 25)
            FINAL_RESULTS['Insurance'] = {
                'loss': (ins_diff / 365) * 0.07 * REV_ANCHOR,
                'color': "green" if v_ins_days <= 25 else "red"
            }

        # 4. HIRING
        if v_hire_wks is not None:
            hr_diff = max(0, v_hire_wks - 4)
            FINAL_RESULTS['Hiring'] = {
                'loss': (hr_diff * 5120) - 10000 if hr_diff > 0 else 0,
                'color': "green" if v_hire_wks <= 4 else "red"
            }

        # 5. CONVERSION
        if v_conv_pct is not None and v_np_count is not None:
            conv_diff = max(0, 80 - v_conv_pct)
            FINAL_RESULTS['Patient Conversion'] = {
                'loss': (conv_diff / 100) * v_np_count * 1000 * 12,
                'color': "green" if v_conv_pct >= 80 else "red"
            }

        # 6. HYGIENE PRODUCTION
        if v_hyg_prod is not None:
            hp_diff = max(0, 30 - v_hyg_prod)
            FINAL_RESULTS['Hygiene Production'] = {
                'loss': (hp_diff / 100) * REV_ANCHOR,
                'color': "green" if v_hyg_prod >= 30 else "red"
            }

        # 7. HYGIENE PERIO (Strictly uses its own inputs)
        if v_hyg_perio is not None:
            per_diff = max(0, 40 - v_hyg_perio)
            # Use benchmark 30% revenue as base for perio calculation
            FINAL_RESULTS['Hygiene Perio'] = {
                'loss': (per_diff / 100) * (0.30 * REV_ANCHOR),
                'color': "green" if v_hyg_perio >= 40 else "red"
            }

        # --- THE VERDICT CALCULATION (Cleaned) ---
        if FINAL_RESULTS:
            # Only pull keys that actually exist in this specific run
            total_leakage = sum(item['loss'] for item in FINAL_RESULTS.values())
            fruit_key = max(FINAL_RESULTS, key=lambda k: FINAL_RESULTS[k]['loss'])

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
                <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{fruit_key}</b></p>
                <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_leakage:,.0f}</b> on the table annually.</p>
            </div>
            """, unsafe_allow_html=True)

            # --- GRID DISPLAY ---
            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in FINAL_RESULTS.items():
                st.markdown(f'<div class="status-box status-{data["color"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. GHL FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
