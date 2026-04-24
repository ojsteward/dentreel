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
        hygiene_val = st.number_input("Hyg Perio %", min_value=0, max_value=100, value=None, step=1)
        case_val = st.number_input("Case Acceptance %", min_value=0, max_value=100, value=None, step=1)
    with col2:
        missed_calls = st.number_input("% of Missed Calls", min_value=0, max_value=100, value=None, step=1)
        no_shows = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        ins_days = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # 3. CALCULATIONS
        revenue = 1200000
        results = {}
        fields = {
            'EBITDA %': (ebitda_val, 22, 'higher'),
            'Hyg Perio': (hygiene_val, 40, 'higher'),
            'Case Acceptance': (case_val, 95, 'higher'),
            'Missed Calls': (missed_calls, 7, 'lower'),
            'No Shows': (no_shows, 5, 'lower'),
            'Insurance Collections': (ins_days, 25, 'lower')
        }

        any_empty = any(v is None for v, b, d in fields.values())
        
        for name, (val, bench, direction) in fields.items():
            if val is None:
                results[name] = {'loss': 0, 'color': 'white'}
            else:
                if direction == 'higher':
                    diff = (bench / 100) - (val / 100)
                    loss = max(0, diff * revenue)
                    color = "green" if val >= bench else ("yellow" if val >= (bench * 0.9) else "red")
                else:
                    if name == 'Insurance Collections':
                        ddd = max(0, val - bench)
                        loss = (ddd / 365) * 0.07 * revenue
                        color = "green" if val <= bench else ("yellow" if val <= (bench * 1.1) else "red")
                    else:
                        diff = (val / 100) - (bench / 100)
                        loss = max(0, diff * revenue)
                        color = "green" if val <= bench else ("yellow" if val <= (bench * 1.1) else "red")
                results[name] = {'loss': loss, 'color': color}

        low_hanging_fruit = max(results, key=lambda x: results[x]['loss'])
        total_loss = sum(item['loss'] for item in results.values())

        # 4. VERDICT RENDERING
        empty_msg = f'<p style="color: #00d2ff; font-weight: bold; margin-top: 10px; font-family: sans-serif;">I see that you left out one or more fields. With Pronto, you will have access to all of these numbers at your fingertips each and every day.</p>' if any_empty else ''
        
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
            st.markdown(f'<div class="status-box status-{data["color"]}">{name}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. CALL TO ACTION TEXT (With orange header restored)
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px; padding: 10px;">
                <p style="font-size: 1.1rem; color: #ff8c00; font-weight: 700; margin-bottom: 5px;">Ready to examine your office further?</p>
                <p style="font-size: 1.1rem; color: #ffffff; font-family: sans-serif; line-height: 1.5;">
                    Fill out the form below to get your complete Autopsy with opportunities for each of these 6 categories. 
                    <b>Now imagine if you had 140 of these at your finger tips each and every day.</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 7. LEAD FORM
        components.html("""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:650px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=700)
