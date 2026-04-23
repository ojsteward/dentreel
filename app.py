import streamlit as st
import requests

# Setup Page Config
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

# Pronto Branding CSS (Matching prontobymaeva.com)
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* Input Labels */
    .stNumberInput label { color: #ffffff !important; font-weight: 500; font-size: 1rem; }
    
    /* Button Styling - Pronto Gradient/Blue */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #1e90ff 0%, #00bfff 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(30, 144, 255, 0.3); border: none; color: white; }

    /* Results Card */
    .report-card { 
        background: rgba(255,255,255,0.03); 
        padding: 30px; 
        border-radius: 12px; 
        border: 1px solid rgba(255,255,255,0.1); 
        margin-top: 25px; 
        text-align: center;
    }
    .metric-title { color: #1e90ff; font-weight: bold; text-transform: uppercase; font-size: 0.9rem; }
    .metric-value { font-size: 2.2rem; font-weight: 900; margin-bottom: 10px; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Logo
st.image("https://storage.googleapis.com/msgsndr/MgimDtWvlYqx8IwO2yH8/media/694bebdbe889d39cb8476f9a.png", width=180)

st.title("Practice Revenue Autopsy™")
st.write("Enter your office metrics below to identify production gaps and overhead leaks.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input("Annual Gross Collections ($)", min_value=0, value=1200000, step=100000)
        ops = st.number_input("Number of Operatories", min_value=1, value=5)
    with col2:
        ebitda = st.number_input("Annual EBITDA ($)", min_value=0, value=200000, step=25000)
        practice_name = st.text_input("Practice Name", placeholder="e.g. Sunset Dental")

    if st.button("Generate Autopsy Results"):
        # PRONTO BENCHMARKS
        # Pronto targets high efficiency: $300k+ per op/year
        target_revenue_per_op = 300000 
        target_revenue = ops * target_revenue_per_op
        target_ebitda_pct = 0.22 
        
        current_ebitda_pct = ebitda / revenue if revenue > 0 else 0
        revenue_gap = max(0, target_revenue - revenue)
        profit_leak = max(0, (revenue * target_ebitda_pct) - ebitda)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Display
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f'<p class="metric-title">Annual Production Gap</p>', unsafe_allow_html=True)
            if revenue_gap > 0:
                st.markdown(f'<p class="metric-value" style="color: #ff4b4b;">${revenue_gap:,.0f}</p>', unsafe_allow_html=True)
                st.caption(f"Your facility is currently performing at {revenue/target_revenue:.1%} of its potential.")
            else:
                st.markdown(f'<p class="metric-value" style="color: #00ffcc;">$0</p>', unsafe_allow_html=True)
                st.caption("Elite efficiency levels.")

        with c2:
            st.markdown(f'<p class="metric-title">Operational Profit Leak</p>', unsafe_allow_html=True)
            if profit_leak > 0:
                st.markdown(f'<p class="metric-value" style="color: #fca311;">${profit_leak:,.0f}</p>', unsafe_allow_html=True)
                st.caption(f"Targeting a 22% EBITDA margin for {practice_name if practice_name else 'your practice'}.")
            else:
                st.markdown(f'<p class="metric-value" style="color: #00ffcc;">Optimal</p>', unsafe_allow_html=True)
                st.caption("Margins are within healthy Pronto benchmarks.")

        # FINAL VERDICT
        st.markdown(f"""
        <div class="report-card">
            <h2 style="margin-top:0;">The Verdict</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Based on Pronto’s evaluation, your practice has a combined 
                <b style="color: #1e90ff; font-size: 1.3rem;">${revenue_gap + profit_leak:,.0f}</b> 
                opportunity currently left on the table.
            </p>
            <p>Ready to close the gap? Reach out to the <b>Pronto</b> team to turn these metrics into a clinical and operational reality.</p>
            <a href="https://prontobymaeva.com/#contact" target="_blank">
                <button style="background: #ffffff; color: #0d1117; border: none; padding: 12px 25px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                    CONTACT PRONTO
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
