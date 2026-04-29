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
        ebitda_val = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        no_shows = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        hire_weeks = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with col2:
        hyg_prod_pct = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        hyg_perio_pct = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1)
        new_patients = st.number_input("# New Patients per Month", min_value=0, value=None, step=1)
        call_conv_pct = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. CALCULATIONS
        rev = 1200000
        results = {}
        
        # Helper for color logic
        def get_color(val, bench, higher_is_better):
            if val is None: return "white"
            if higher_is_better:
                return "green" if val >= bench else ("yellow" if val >= (bench * 0.9) else "red")
            else:
                return "green" if val <= bench else ("yellow" if val <= (bench * 1.1) else "red")

        # Basic Stats
        results['EBITDA'] = {'loss': max(0, (22 - (ebitda_val or 22))/100 * rev), 'color': get_color(ebitda_val, 22, True)}
        results['No Shows'] = {'loss': max(0, ((no_shows or 5) - 5)/100 * rev), 'color': get_color(no_shows, 5, False)}
        results['Insurance'] = {'loss': max(0, ((ins_days or 25) - 25)/365 * 0.07 * rev), 'color': get_color(ins_days, 25, False)}
        
        # Hiring Logic
        hiring_loss = max(0, ((hire_weeks or 4) - 4) * 5120 - 10000)
        results['Hiring'] = {'loss': hiring_loss, 'color': get_color(hire_weeks, 4, False)}

        # New Patient Logic
        np_loss = max(0, (80 - (call_conv_pct or 80))/100 * (new_patients or 0) * 1000 * 12)
        results['New Patients'] = {'loss': np_loss, 'color': get_color(call_conv_pct, 80, True)}

        # Hygiene Tricky Logic
        if hyg_prod_pct is not None:
            # Calculation #5: Hygiene Production
            hyg_prod_loss = max(0, (30 - hyg_prod_pct)/100 * rev)
            
            # Calculation #6: Hygiene Perio %
            if hyg_perio_pct is not None:
                bench_perio = 40
                diff_perio_pct = (bench_perio - hyg_perio_pct) / 100
                
                if hyg_prod_pct >= 30:
                    perio_loss = max(0, diff_perio_pct * (hyg_prod_pct/100) * rev)
                else:
                    perio_loss = max(0, (diff_perio_pct * 0.30 * rev) + hyg_prod_loss)
                
                results['Hygiene System'] = {'loss': perio_loss, 'color': get_color(hyg_perio_pct, 40, True)}
            else:
                results['Hygiene System'] = {'loss': hyg_prod_loss, 'color': 'white'}
        else:
            results['Hygiene System'] = {'loss': 0, 'color': 'white', 'msg': "Hygiene production % needed for calculation"}

        low_hanging_fruit = max(results, key=lambda x: results[x]['loss'])
        total_loss = sum(item['loss'] for item in results.values())

        # 4. VERDICT RENDERING
        any_empty = any(v is None for v in [ebitda_val, no_shows, ins_days, hire_weeks, hyg_prod_pct, hyg_perio_pct, new_patients, call_conv_pct])
        
        empty_msg = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if any_empty else ''
        
        verdict_html = f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
            <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{low_hanging_fruit}</b></p>
            <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_loss:,.0f}</b> on the table annually.</p>
            {empty_msg}
        </div>
        """
        st.markdown(verdict_html, unsafe_allow_html=True)

        # 5. STATUS BLOCKS
        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for name, data in results.items():
            display_name = data.get('msg', name)
            st.markdown(f'<div class="status-box status-{data["color"]}">{display_name}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. UPDATED CTA TEXT
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

        # 7. LEAD FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:650px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=700)
