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
        user_ebitda = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="k_ebitda")
        user_noshow = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="k_noshow")
        user_ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="k_ins")
        user_hire_wks = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="k_hire")
    with col2:
        user_hyg_prod = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="k_hprod")
        user_hyg_perio = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="k_hperio")
        user_np_count = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="k_npcount")
        user_conv_pct = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="k_conv")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. THE MATH ENGINE (Strict Variable Naming)
        ANNUAL_REV = 1200000
        final_cats = {}

        # EBITDA Calculation (Isolated)
        eb_val = user_ebitda if user_ebitda is not None else 22
        eb_loss_amt = max(0.0, (22 - eb_val) / 100 * ANNUAL_REV)
        final_cats['EBITDA'] = {'loss': eb_loss_amt, 'color': "green" if eb_val >= 22 else "red" if user_ebitda is not None else "white"}

        # No Shows (Isolated)
        ns_val = user_noshow if user_noshow is not None else 5
        ns_loss_amt = max(0.0, (ns_val - 5) / 100 * ANNUAL_REV)
        final_cats['No Shows'] = {'loss': ns_loss_amt, 'color': "green" if ns_val <= 5 else "red" if user_noshow is not None else "white"}

        # Insurance (Isolated)
        ins_val = user_ins_days if user_ins_days is not None else 25
        ins_loss_amt = max(0.0, (ins_val - 25) / 365 * 0.07 * ANNUAL_REV)
        final_cats['Insurance'] = {'loss': ins_loss_amt, 'color': "green" if ins_val <= 25 else "red" if user_ins_days is not None else "white"}

        # Hiring (Isolated)
        hr_val = user_hire_wks if user_hire_wks is not None else 4
        hr_loss_amt = max(0.0, (hr_val - 4) * 5120 - 10000)
        final_cats['Hiring'] = {'loss': hr_loss_amt, 'color': "green" if hr_val <= 4 else "red" if user_hire_wks is not None else "white"}

        # NP Conversion (Isolated)
        conv_val = user_conv_pct if user_conv_pct is not None else 80
        pat_val = user_np_count if user_np_count is not None else 0
        np_loss_amt = max(0.0, (80 - conv_val) / 100 * pat_val * 1000 * 12)
        final_cats['Patient Conversion'] = {'loss': np_loss_amt, 'color': "green" if conv_val >= 80 else "red" if user_conv_pct is not None else "white"}

        # HYGIENE CALCULATION (Independent Logic)
        if user_hyg_prod is not None:
            # 5. Hygiene Production Loss
            calc_hp_loss = max(0.0, (30 - user_hyg_prod) / 100 * ANNUAL_REV)
            final_cats['Hygiene Production'] = {'loss': calc_hp_loss, 'color': "green" if user_hyg_prod >= 30 else "red"}
            
            # 6. Hygiene Perio Loss
            if user_hyg_perio is not None:
                perio_diff = (40 - user_hyg_perio) / 100
                if user_hyg_prod >= 30:
                    perio_math = perio_diff * (user_hyg_prod / 100) * ANNUAL_REV
                else:
                    perio_math = (perio_diff * 0.30 * ANNUAL_REV) + calc_hp_loss
                final_cats['Hygiene Perio'] = {'loss': max(0.0, perio_math), 'color': "green" if user_hyg_perio >= 40 else "red"}
        else:
            final_cats['Hygiene System'] = {'loss': 0.0, 'color': 'white', 'msg': 'Hygiene Production % Needed'}

        # Summary
        fruit_name = max(final_cats, key=lambda x: final_cats[x]['loss'])
        total_sum = sum(v['loss'] for v in final_cats.values())

        # 4. RENDERING
        missing_fields = any(v is None for v in [user_ebitda, user_noshow, user_ins_days, user_hire_wks, user_hyg_prod, user_hyg_perio, user_np_count, user_conv_pct])
        
        skip_alert = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if missing_fields else ''
        
        st.markdown(f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
            <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{fruit_name}</b></p>
            <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_sum:,.0f}</b> on the table annually.</p>
            {skip_alert}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for label, obj in final_cats.items():
            st.markdown(f'<div class="status-box status-{obj["color"]}">{obj.get("msg", label)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. TEXT BLOCKS
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
