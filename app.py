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

# 2. INPUT SECTION - Hard Coded Keys for Isolation
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        u_ebitda = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="unique_ebitda")
        u_noshow = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="unique_noshow")
        u_ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="unique_ins")
        u_hire_wks = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="unique_hire")
    with col2:
        u_hyg_prod = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="unique_hprod")
        u_hyg_perio = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="unique_hperio")
        u_np_count = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="unique_npcount")
        u_conv_pct = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="unique_conv")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. THE QUARANTINED MATH ENGINE
        FIXED_REVENUE = 1200000
        final_results = {}

        # EBITDA - Isolated
        val_eb = u_ebitda if u_ebitda is not None else 22
        loss_eb = max(0.0, (22 - val_eb) / 100 * FIXED_REVENUE)
        final_results['EBITDA'] = {'loss': loss_eb, 'color': "green" if val_eb >= 22 else "red" if u_ebitda is not None else "white"}

        # No Shows - Isolated
        val_ns = u_noshow if u_noshow is not None else 5
        loss_ns = max(0.0, (val_ns - 5) / 100 * FIXED_REVENUE)
        final_results['No Shows'] = {'loss': loss_ns, 'color': "green" if val_ns <= 5 else "red" if u_noshow is not None else "white"}

        # Insurance - Isolated
        val_ins = u_ins_days if u_ins_days is not None else 25
        loss_ins = max(0.0, (val_ins - 25) / 365 * 0.07 * FIXED_REVENUE)
        final_results['Insurance'] = {'loss': loss_ins, 'color': "green" if val_ins <= 25 else "red" if u_ins_days is not None else "white"}

        # Hiring - Isolated
        val_hw = u_hire_wks if u_hire_wks is not None else 4
        loss_hw = max(0.0, (val_hw - 4) * 5120 - 10000)
        final_results['Hiring'] = {'loss': loss_hw, 'color': "green" if val_hw <= 4 else "red" if u_hire_wks is not None else "white"}

        # Patient Conversion - Isolated
        val_cp = u_conv_pct if u_conv_pct is not None else 80
        val_np = u_np_count if u_np_count is not None else 0
        loss_np = max(0.0, (80 - val_cp) / 100 * val_np * 1000 * 12)
        final_results['Patient Conversion'] = {'loss': loss_np, 'color': "green" if val_cp >= 80 else "red" if u_conv_pct is not None else "white"}

        # HYGIENE PRODUCTION - Isolated
        loss_h_prod = 0.0
        if u_hyg_prod is not None:
            loss_h_prod = max(0.0, (30 - u_hyg_prod) / 100 * FIXED_REVENUE)
            final_results['Hygiene Production'] = {'loss': loss_h_prod, 'color': "green" if u_hyg_prod >= 30 else "red"}
        else:
            final_results['Hygiene Production'] = {'loss': 0.0, 'color': 'white'}

        # HYGIENE PERIO - Isolated (Only looks at u_hyg_perio and u_hyg_prod)
        loss_h_perio = 0.0
        if u_hyg_perio is not None:
            p_diff = (40 - u_hyg_perio) / 100
            # Determination of base for math
            if u_hyg_prod is not None and u_hyg_prod >= 30:
                base_val = (u_hyg_prod / 100) * FIXED_REVENUE
                loss_h_perio = max(0.0, p_diff * base_val)
            else:
                # If prod is low or missing, use benchmark 30% revenue base
                base_val = 0.30 * FIXED_REVENUE
                # Strictly using only the perio diff + the calculated prod loss (if any)
                loss_h_perio = max(0.0, (p_diff * base_val) + loss_h_prod)
            
            final_results['Hygiene Perio'] = {'loss': loss_h_perio, 'color': "green" if u_hyg_perio >= 40 else "red"}
        else:
            final_results['Hygiene Perio'] = {'loss': 0.0, 'color': 'white'}

        # Summary Generation
        fruit_key = max(final_results, key=lambda x: final_results[x]['loss'])
        total_practice_loss = sum(v['loss'] for v in final_results.values())

        # 4. RENDERING THE RESULTS
        has_skips = any(v is None for v in [u_ebitda, u_noshow, u_ins_days, u_hire_wks, u_hyg_prod, u_hyg_perio, u_np_count, u_conv_pct])
        
        skip_notice = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if has_skips else ''
        
        st.markdown(f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
            <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{fruit_key}</b></p>
            <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_practice_loss:,.0f}</b> on the table annually.</p>
            {skip_notice}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for label, data in final_results.items():
            if data['color'] != 'white' or label in ['Hygiene Production', 'Hygiene Perio']:
                st.markdown(f'<div class="status-box status-{data["color"]}">{label}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. CTA & DISCLAIMER
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px; padding: 10px;">
                <p style="font-size: 1.2rem; color: #ff8c00; font-weight: 700; margin-bottom: 10px;">“You just got a glimpse.”</p>
                <p style="font-size: 1.1rem; color: #ffffff; font-family: sans-serif; line-height: 1.5;">
                    Now let’s find what you’re actually missing. Fill out the form below to unlock your full Practice Autopsy—breaking down exactly where revenue is leaking across all 6 categories.<br><br>
                    <b>Because if this much showed up from a few inputs… what do you think happens when you’re tracking 140+ metrics in real time?</b>
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #ff4500;">
                <p style="font-size: 0.85rem; color: #cccccc; font-style: italic; font-family: sans-serif; margin: 0;">
                    <b>Disclaimer:</b> These results aren’t meant to be perfect—they’re meant to be revealing. We’ve taken your inputs and applied industry benchmarks to surface likely gaps. But without real-time data integration, there are variables we simply can’t see. Pronto doesn’t guess. It knows. This is the preview… not the movie.
                </p>
            </div>
        """, unsafe_allow_html=True)

        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:650px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=700)
