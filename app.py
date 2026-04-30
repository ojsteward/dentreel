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
    .status-yellow { border-color: #ffc107; background: rgba(255, 193, 7, 0.1); color: #ffc107; }
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
        ebitda_input = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        no_shows_input = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        ins_days_input = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        hire_weeks_input = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with col2:
        hyg_prod_input = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        hyg_perio_input = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1)
        np_input = st.number_input("# New Patients per Month", min_value=0, value=None, step=1)
        conv_input = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. FIXED CALCULATIONS (Isolated Constants)
        REV_BASELINE = 1200000
        category_results = {}

        # EBITDA Calculation
        eb_loss = max(0, (22 - (ebitda_input or 22)) / 100 * REV_BASELINE)
        eb_color = "green" if (ebitda_input or 0) >= 22 else ("yellow" if (ebitda_input or 0) >= 20 else "red")
        category_results['EBITDA'] = {'loss': eb_loss, 'color': eb_color if ebitda_input is not None else 'white'}

        # No Shows Calculation
        ns_loss = max(0, ((no_shows_input or 5) - 5) / 100 * REV_BASELINE)
        ns_color = "green" if (no_shows_input or 0) <= 5 else ("yellow" if (no_shows_input or 0) <= 6 else "red")
        category_results['No Shows'] = {'loss': ns_loss, 'color': ns_color if no_shows_input is not None else 'white'}

        # Insurance Days Calculation
        ins_loss = max(0, ((ins_days_input or 25) - 25) / 365 * 0.07 * REV_BASELINE)
        ins_color = "green" if (ins_days_input or 0) <= 25 else ("yellow" if (ins_days_input or 0) <= 28 else "red")
        category_results['Insurance'] = {'loss': ins_loss, 'color': ins_color if ins_days_input is not None else 'white'}

        # Hiring Calculation
        hi_loss = max(0, ((hire_weeks_input or 4) - 4) * 5120 - 10000)
        hi_color = "green" if (hire_weeks_input or 0) <= 4 else ("yellow" if (hire_weeks_input or 0) <= 6 else "red")
        category_results['Hiring'] = {'loss': hi_loss, 'color': hi_color if hire_weeks_input is not None else 'white'}

        # New Patient Conversion Calculation
        np_loss = max(0, (80 - (conv_input or 80)) / 100 * (np_input or 0) * 1000 * 12)
        np_color = "green" if (conv_input or 0) >= 80 else ("yellow" if (conv_input or 0) >= 75 else "red")
        category_results['Patient Conversion'] = {'loss': np_loss, 'color': np_color if conv_input is not None else 'white'}

        # HYGIENE SYSTEM MATH (Isolated from EBITDA)
        h_prod_loss = 0
        h_perio_loss = 0
        
        if hyg_prod_input is not None:
            h_prod_loss = max(0, (30 - hyg_prod_input) / 100 * REV_BASELINE)
            
            if hyg_perio_input is not None:
                diff_perio = (40 - hyg_perio_input) / 100
                if hyg_prod_input >= 30:
                    h_perio_loss = max(0, diff_perio * (hyg_prod_input / 100) * REV_BASELINE)
                else:
                    # Use the special additive formula for low production
                    h_perio_loss = max(0, (diff_perio * 0.30 * REV_BASELINE) + h_prod_loss)
            
            category_results['Hygiene Production'] = {'loss': h_prod_loss, 'color': "green" if hyg_prod_input >= 30 else "red"}
            category_results['Hygiene Perio'] = {'loss': h_perio_loss, 'color': "green" if (hyg_perio_input or 0) >= 40 else "red"}
        else:
            category_results['Hygiene System'] = {'loss': 0, 'color': 'white', 'msg': 'Hygiene Production % Needed'}

        # Determine Low Hanging Fruit and Total
        low_hanging_fruit = max(category_results, key=lambda x: category_results[x]['loss'])
        total_loss_final = sum(item['loss'] for item in category_results.values())

        # 4. VERDICT RENDERING
        any_skipped = any(v is None for v in [ebitda_input, no_shows_input, ins_days_input, hire_weeks_input, hyg_prod_input, hyg_perio_input, np_input, conv_input])
        
        skip_msg = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if any_skipped else ''
        
        st.markdown(f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
            <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{low_hanging_fruit}</b></p>
            <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_loss_final:,.0f}</b> on the table annually.</p>
            {skip_msg}
        </div>
        """, unsafe_allow_html=True)

        # 5. STATUS BLOCKS
        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for name, data in category_results.items():
            label = data.get('msg', name)
            st.markdown(f'<div class="status-box status-{data["color"]}">{label}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. CTA & DISCLAIMER
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

        # 7. FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:650px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=700)
