import streamlit as st
import streamlit.components.v1 as components
import time

# Setup Page Config
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

# Custom CSS for Pronto Branding and Status Blocks
st.markdown("""
    <style>
    .stApp { background-color: #001e36; color: #ffffff; }
    .stNumberInput label { color: #ffffff !important; font-weight: 600; }
    
    /* Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }

    /* Verdict Card */
    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 30px; border-radius: 15px; 
        border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px;
    }

    /* Color Blocks */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .status-box { padding: 20px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.9rem; border: 2px solid transparent; text-transform: uppercase; }
    .status-green { border-color: #28a745; background: rgba(40, 167, 69, 0.1); color: #28a745; }
    .status-yellow { border-color: #ffc107; background: rgba(255, 193, 7, 0.1); color: #ffc107; }
    .status-red { border-color: #dc3545; background: rgba(220, 53, 69, 0.1); color: #dc3545; }
    .status-white { border-color: #ffffff; background: rgba(255, 255, 255, 0.1); color: #ffffff; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# Inputs Container
with st.container():
    # 6 Metrics First
    col1, col2 = st.columns(2)
    with col1:
        ebitda_val = st.number_input("Current EBITDA %", min_value=0.0, max_value=100.0, value=None)
        hygiene_val = st.number_input("Hygiene Department %", min_value=0.0, max_value=100.0, value=None)
        case_val = st.number_input("Case Acceptance %", min_value=0.0, max_value=100.0, value=None)
    with col2:
        missed_calls = st.number_input("Missed Calls %", min_value=0.0, max_value=100.0, value=None)
        no_shows = st.number_input("No Shows %", min_value=0.0, max_value=100.0, value=None)
        ins_days = st.number_input("Insurance Collection Days", min_value=0, value=None)

    # Annual Gross Collections moved to the bottom of the list
    user_revenue = st.number_input("Annual Gross Collections ($) if you would like a more accurate depiction of the office autopsy", min_value=0, value=None)
    
    # Use 1.2M for calculations as per instruction, or user input if provided
    calc_revenue = user_revenue if user_revenue else 1200000

    # Action Button
    if st.button("Generate Autopsy Results"):
        # THINKING ANIMATION
        with st.empty():
            for i in range(7):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                time.sleep(1)
            st.write("")

        # CALCULATIONS & BENCHMARKS
        results = {}
        fields = {
            'EBITDA %': (ebitda_val, 30, 'higher'),
            'Hygiene Department': (hygiene_val, 32, 'higher'),
            'Case Acceptance': (case_val, 95, 'higher'),
            'Missed Calls': (missed_calls, 7, 'lower'),
            'No Shows': (no_shows, 5, 'lower'),
            'Insurance Collections': (ins_days, 60, 'lower')
        }

        any_empty = False
        
        for name, (val, bench, direction) in fields.items():
            if val is None:
                results[name] = {'loss': 0, 'color': 'white'}
                any_empty = True
            else:
                if direction == 'higher':
                    diff = (bench / 100) - (val / 100)
                    loss = max(0, diff * calc_revenue)
                    if val >= bench: color = "green"
                    elif val >= (bench * 0.9): color = "yellow"
                    else: color = "red"
                else: # lower is better
                    if name == 'Insurance Collections':
                        days_diff = max(0, val - bench)
                        loss = (days_diff / 365) * 0.07 * calc_revenue
                        if val <= bench: color = "green"
                        elif val <= (bench * 1.1): color = "yellow"
                        else: color = "red"
                    else:
                        diff = (val / 100) - (bench / 100)
                        loss = max(0, diff * calc_revenue)
                        if val <= bench: color = "green"
                        elif val <= (bench * 1.1): color = "yellow"
                        else: color = "red"
                
                results[name] = {'loss': loss, 'color': color}

        # FIND HIGHEST LOSS FOR VERDICT
        low_hanging_fruit = max(results, key=lambda x: results[x]['loss'])
        total_loss = sum(item['loss'] for item in results.values())

        # VERDICT SECTION
        st.markdown(f"""
        <div class="report-card">
            <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
            <p style="font-size: 1.2rem;">Pronto discovered that your low hanging fruit is in <b>{low_hanging_fruit}</b></p>
            <p style="font-size: 1.1rem;">Based on {calc_revenue/1000000:.1f} million in production, your practice is leaving <b>${total_loss:,.0f}</b> on the table annually.</p>
            {f'<p style="font-size: 1rem; color: #00d2ff; font-weight: bold; margin-top: 10px;">I see that you left one or more fields. With Pronto, you will have access to all of these numbers at your fingertips each and every day.</p>' if any_empty else ''}
            <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 20px;">
                To get a more detailed analysis and autopsy of your personal results, please fill out the following and we will elaborate on the {low_hanging_fruit} results as well as the others and let you know what can be done about it.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # STATUS BLOCKS
        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        for name, data in results.items():
            st.markdown(f'<div class="status-box status-{data["color"]}">{name}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # GHL FORM
        components.html(f"""
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:500px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh" title="Form 0"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=520)
