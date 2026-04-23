import streamlit as st

# Setup Page Config
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

# Pronto Blue & Orange Branding
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #001e36; color: #ffffff; }
    
    /* Input Labels */
    .stNumberInput label, .stTextInput label { color: #ffffff !important; font-weight: 600; }

    /* Button - Orange & Blue Gradient */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
        border: none;
    }
    div.stButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 10px 20px rgba(255, 140, 0, 0.4); 
        color: white;
        border: none;
    }

    /* Results Card */
    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #00d2ff; 
        margin-top: 25px; 
        text-align: center;
    }
    .metric-title { color: #ff8c00; font-weight: 800; text-transform: uppercase; font-size: 1rem; margin-bottom: 0px; }
    .metric-value { font-size: 2.5rem; font-weight: 900; color: #ffffff; margin-bottom: 5px; }
    
    /* Contact Button */
    .contact-btn {
        background-color: #00d2ff;
        color: #001e36 !important;
        padding: 12px 30px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 20px;
        transition: 0.3s;
    }
    .contact-btn:hover { background-color: #ffffff; transform: scale(1.05); }

    /* Clean up Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# White Logo
st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)

st.title("Practice Revenue Autopsy™")
st.write("Calculate your growth potential and operational efficiency.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input("Annual Gross Collections ($)", min_value=0, value=1200000, step=100000)
        ops = st.number_input("Number of Operatories", min_value=1, value=5)
    with col2:
        ebitda = st.number_input("Annual EBITDA ($)", min_value=0, value=200000, step=25000)
        practice_name = st.text_input("Practice Name", placeholder="e.g. Elite Dental")

    if st.button("Generate Autopsy Results"):
        # PRONTO BENCHMARKS
        target_rev_per_op = 300000 
        target_revenue = ops * target_rev_per_op
        target_ebitda_pct = 0.22 
        
        current_ebitda_pct = ebitda / revenue if revenue > 0 else 0
        revenue_gap = max(0, target_revenue - revenue)
        profit_leak = max(0, (revenue * target_ebitda_pct) - ebitda)
        total_opportunity = revenue_gap + profit_leak
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Display
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f'<p class="metric-title">Annual Production Gap</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">${revenue_gap:,.0f}</p>', unsafe_allow_html=True)
            st.caption(f"Target: ${target_revenue:,.0f}")

        with c2:
            st.markdown(f'<p class="metric-title">Operational Profit Leak</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">${profit_leak:,.0f}</p>', unsafe_allow_html=True)
            st.caption(f"Target Margin: {target_ebitda_pct:.0%}")

        # FINAL VERDICT
        st.markdown(f"""
        <div class="report-card">
            <h2 style="color: #ffffff; margin-top:0;">The Verdict</h2>
            <p style="font-size: 1.2rem; line-height: 1.6;">
                {practice_name if practice_name else 'Your practice'} is currently leaving 
                <b style="color: #ff8c00; font-size: 1.5rem;">${total_opportunity:,.0f}</b> 
                on the table annually.
            </p>
            <p style="color: rgba(255,255,255,0.7);">Pronto specializes in closing this gap through clinical optimization and cultural metrics.</p>
            <a href="https://prontobymaeva.com/#contact" class="contact-btn">REACH OUT TO PRONTO</a>
        </div>
        """, unsafe_allow_html=True)
