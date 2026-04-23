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
    .status-box { padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.85rem; border: 2px solid transparent; }
    .status-green { border-color: #28a745; background: rgba(40, 167, 69, 0.1); color: #28a745; }
    .status-yellow { border-color: #ffc107; background: rgba(255, 193, 7, 0.1); color: #ffc107; }
    .status-red { border-color: #dc3545; background: rgba(220, 53, 69, 0.1); color: #dc3545; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# Inputs (NO PRE-FILLED NUMBERS)
with st.container():
    revenue = st.number_input("Annual Gross Collections ($)", min_value=0, value=None, placeholder="e.g. 1200000")
    
    col1, col2 = st.columns(2)
    with col1:
        ebitda_val = st.number_input("Current EBITDA %", min_value=0.0, max_value=100.0, value=None, placeholder="e.g. 25")
        hygiene_val = st.number_input("Hygiene Department %", min_value=0.0, max_value=100.0, value=None, placeholder="e.g. 28")
        case_val = st.number_input("Case Acceptance %", min_value=0.0, max_value=100.0, value=None, placeholder="e.g. 80")
    with col2:
        missed_calls = st.number_input("Missed Calls %", min_value=0.0, max_value=100.0, value=None, placeholder="e.g. 12")
        no_shows = st.number_input("No Shows %", min_value=0.0, max_value=100.0, value=None, placeholder="e.g. 10")
        ins_days = st.number_input("Insurance Collection Days", min_value=0, value=None, placeholder="e.g. 75")

    if st.button("Generate Autopsy Results"):
        if any(v is None for v in [revenue, ebitda_val, hygiene_val, case_val, missed_calls, no_shows, ins_days]):
            st.error("Please fill in all fields.")
            st.info("I see that you left one or more numbers. With Pronto, you will have access to all of these numbers at your fingertips each and every day.")
        else:
            # THINKING ANIMATION
            with st.empty():
                for i in range(7):
                    st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {7-i}s")
                    time.sleep(1)
                st.write("")

            # CALCULATIONS & BENCHMARKS
            results = {}
            
            # 1. EBITDA (Benchmark 30%)
            diff = 0.30 - (ebitda_val / 100)
            results['EBITDA %'] = {
                'loss': max(0, diff * revenue),
                'val': ebitda_val,
                'bench': 30,
                'type': 'higher_is_better'
            }

            # 2. HYGIENE (Benchmark 32%)
            diff = 0.32 - (hygiene_val / 100)
            results['Hygiene Department'] = {
                'loss': max(0, diff * revenue),
                'val': hygiene_val,
                'bench': 32,
                'type': 'higher_is_better'
            }

            # 3. CASE ACCEPTANCE (Benchmark 95%)
            diff = 0.95 - (case_val / 100)
            results['Case Acceptance'] = {
                'loss': max(0, diff * revenue),
                'val': case_val,
                'bench': 95,
                'type': 'higher_is_better'
            }

            # 4. MISSED CALLS (Benchmark 7%)
            diff = (missed_calls / 100) - 0.07
            results['Missed Calls'] = {
                'loss': max(0, diff * revenue),
                'val': missed_calls,
                'bench': 7,
                'type': 'lower_is_better'
            }

            # 5. NO SHOWS (Benchmark 5%)
            diff = (no_shows / 100) - 0.05
            results['No Shows'] = {
                'loss': max(0, diff * revenue),
                'val': no_shows,
                'bench': 5,
                'type': 'lower_is_better'
            }

            # 6. INSURANCE DAYS (Benchmark 60 Days)
            days_diff = max(0, ins_days - 60)
            # Calculation: DDD / 365 * 7% Cost of Capital * Revenue
            ins_loss = (days_diff / 365) * 0.07 * revenue
            results['Insurance Collections'] = {
                'loss': ins_loss,
                'val': ins_days,
                'bench': 60,
                'type': 'lower_is_better'
            }

            # FIND HIGHEST LOSS
            low_hanging_fruit = max(results, key=lambda x: results[x]['loss'])
            total_loss = sum(item['loss'] for item in results.values())

            # VERDICT SECTION
            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0;">The Verdict</h1>
                <p style="font-size: 1.2rem;">Pronto discovered that your low hanging fruit is in <b>"{low_hanging_fruit}"</b></p>
                <p style="font-size: 1.1rem;">Based on {revenue/1000000:.1f} million in production, your practice is leaving <b>"${total_loss:,.0f}"</b> on the table annually.</p>
                <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 20px;">
                    To get a more detailed analysis and autopsy of your personal results, please fill out the following and we will elaborate on the "{low_hanging_fruit}" results as well as the others and let you know what can be done about it.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # STATUS BLOCKS
            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for name, data in results.items():
                val, bench = data['val'], data['bench']
                
                # Logic for Red/Yellow/Green
                if data['type'] == 'higher_is_better':
                    if val >= bench: color = "green"
                    elif val >= (bench * 0.9): color = "yellow"
                    else: color = "red"
                else: # lower is better
                    if val <= bench: color = "green"
                    elif val <= (bench * 1.1): color = "yellow"
                    else: color = "red"
                
                st.markdown(f'<div class="status-box status-{color}">{name.upper()}<br>${data["loss"]:,.0f} Opportunity</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # GHL FORM
            components.html("""
                <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:500px;border:none;border-radius:8px" id="inline-iVFg0wteKeXMSEXviPvh" data-form-id="iVFg0wteKeXMSEXviPvh" title="Form 0"></iframe>
                <script src="https://link.msgsndr.com/js/form_embed.js"></script>
            """, height=520)
