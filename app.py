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

# 2. INPUT SECTION (EBITDA REMOVED)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        u_noshow = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="ui_noshow")
        u_ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="ui_ins")
        u_hire_wks = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="ui_hire")
    with col2:
        u_hyg_prod = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="ui_hprod")
        u_hyg_perio = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="ui_hperio")
        u_np_count = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="ui_npcount")
        u_conv_pct = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="ui_conv")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(3):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {3-i}s")
                time.sleep(1)
            st.write("")

        # 3. CLEAN MATH ENGINE
        FIXED_REV = 1200000
        final_stats = {}

        # No Shows
        if u_noshow is not None:
            final_stats['No Shows'] = {
                'loss': max(0.0, (u_noshow - 5) / 100 * FIXED_REV),
                'color': "green" if u_noshow <= 5 else "red"
            }

        # Insurance
        if u_ins_days is not None:
            final_stats['Insurance'] = {
                'loss': max(0.0, (u_ins_days - 25) / 365 * 0.07 * FIXED_REV),
                'color': "green" if u_ins_days <= 25 else "red"
            }

        # Hiring
        if u_hire_wks is not None:
            final_stats['Hiring'] = {
                'loss': max(0.0, (u_hire_wks - 4) * 5120 - 10000),
                'color': "green" if u_hire_wks <= 4 else "red"
            }

        # Patient Conversion
        if u_conv_pct is not None and u_np_count is not None:
            final_stats['Patient Conversion'] = {
                'loss': max(0.0, (80 - u_conv_pct) / 100 * u_np_count * 1000 * 12),
                'color': "green" if u_conv_pct >= 80 else "red"
            }

        # Hygiene Production
        if u_hyg_prod is not None:
            final_stats['Hygiene Production'] = {
                'loss': max(0.0, (30 - u_hyg_prod) / 100 * FIXED_REV),
                'color': "green" if u_hyg_prod >= 30 else "red"
            }

        # Hygiene Perio (Using a Static Benchmark to avoid leaks)
        if u_hyg_perio is not None:
            # Perio is calculated based on a 30% hygiene production benchmark
            perio_base = (u_hyg_prod / 100 * FIXED_REV) if u_hyg_prod is not None else (0.30 * FIXED_REV)
            final_stats['Hygiene Perio'] = {
                'loss': max(0.0, (40 - u_hyg_perio) / 100 * perio_base),
                'color': "green" if u_hyg_perio >= 40 else "red"
            }

        # 4. RENDERING
        if final_stats:
            top_fruit = max(final_stats, key=lambda x: final_stats[x]['loss'])
            grand_total = sum(v['loss'] for v in final_stats.values())
            
            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
                <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{top_fruit}</b></p>
                <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${grand_total:,.0f}</b> on the table annually.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in final_stats.items():
                st.markdown(f'<div class="status-box status-{data["color"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. FOOTER & CTA
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #ffffff; font-family: sans-serif;">Complete the form below to unlock your full detailed report.</p>
            </div>
        """, unsafe_allow_html=True)

        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
