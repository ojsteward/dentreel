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
        ebitda_in = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="eb1")
        no_shows_in = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="ns1")
        ins_days_in = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="id1")
        hire_weeks_in = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="hw1")
    with col2:
        hyg_prod_in = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="hp1")
        hyg_perio_in = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="hper1")
        new_pat_in = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="np1")
        conv_pct_in = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="cp1")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. INDEPENDENT MATH ENGINE
        REV = 1200000
        cats = {}

        # EBITDA
        v_eb = ebitda_in if ebitda_in is not None else 22
        loss_eb = max(0, (22 - v_eb)/100 * REV)
        cats['EBITDA'] = {'loss': loss_eb, 'color': "green" if v_eb >= 22 else ("yellow" if v_eb >= 20 else "red") if ebitda_in is not None else "white"}

        # No Shows
        v_ns = no_shows_in if no_shows_in is not None else 5
        loss_ns = max(0, (v_ns - 5)/100 * REV)
        cats['No Shows'] = {'loss': loss_ns, 'color': "green" if v_ns <= 5 else "red" if no_shows_in is not None else "white"}

        # Insurance
        v_id = ins_days_in if ins_days_in is not None else 25
        loss_id = max(0, (v_id - 25)/365 * 0.07 * REV)
        cats['Insurance'] = {'loss': loss_id, 'color': "green" if v_id <= 25 else "red" if ins_days_in is not None else "white"}

        # Hiring
        v_hw = hire_weeks_in if hire_weeks_in is not None else 4
        loss_hw = max(0, (v_hw - 4) * 5120 - 10000)
        cats['Hiring'] = {'loss': loss_hw, 'color': "green" if v_hw <= 4 else "red" if hire_weeks_in is not None else "white"}

        # NP Conversion
        v_cp = conv_pct_in if conv_pct_in is not None else 80
        v_np = new_pat_in if new_pat_in is not None else 0
        loss_np = max(0, (80 - v_cp)/100 * v_np * 1000 * 12)
        cats['Patient Conversion'] = {'loss': loss_np, 'color': "green" if v_cp >= 80 else "red" if conv_pct_in is not None else "white"}

        # Hygiene Logic (Strictly Isolated)
        if hyg_prod_in is not None:
            # 5. Hygiene Production
            hp_loss = max(0, (30 - hyg_prod_in)/100 * REV)
            cats['Hygiene Production'] = {'loss': hp_loss, 'color': "green" if hyg_prod_in >= 30 else "red"}
            
            # 6. Hygiene Perio
            if hyg_perio_in is not None:
                p_diff = (40 - hyg_perio_in)/100
                if hyg_prod_in >= 30:
                    perio_val = p_diff * (hyg_prod_in/100) * REV
                else:
                    perio_val = (p_diff * 0.30 * REV) + hp_loss
                cats['Hygiene Perio'] = {'loss': max(0, perio_val), 'color': "green" if hyg_perio_in >= 40 else "red"}
        else:
            cats['Hygiene'] = {'loss': 0, 'color': 'white', 'msg': 'Hygiene Production % Needed'}

        # Summary
        fruit = max(cats, key=lambda x: cats[x]['loss'])
        total_lost = sum(c['loss'] for c in cats.values())

        # 4. RENDERING
        any_empty = any(v is None for v in [ebitda_in, no_shows_in, ins_days_in, hire_weeks_in, hyg_prod_in, hyg_perio_in, new_pat_in, conv_pct_in])
        
        skip_txt = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if any_empty else ''
        
        st.markdown(f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
            <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{fruit}</b></p>
            <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_lost:,.0f}</b> on the table annually.</p>
            {skip_txt}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for n, d in cats.items():
            st.markdown(f'<div class="status-box status-{d["color"]}">{d.get("msg", n)}</div>', unsafe_allow_html=True)
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
