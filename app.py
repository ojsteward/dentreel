import streamlit as st

# Setup Page Config
st.set_page_config(page_title="Dentreel Revenue Autopsy", page_icon="🦷", layout="centered")

# Dentreel Branding CSS
st.markdown("""
    <style>
    .stApp { background-color: #001220; color: #ffffff; }
    .stNumberInput label, .stTextInput label { color: #00d2ff !important; font-weight: bold; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border: none; padding: 15px 30px; border-radius: 50px;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); }
    .report-card { background: rgba(255,255,255,0.05); padding: 25px; border-radius: 10px; border: 1px solid rgba(0,210,255,0.2); margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MgimDtWvlYqx8IwO2yH8/media/69d7ab0e019dc508d3bc2440.png", width=80)
st.title("Revenue Autopsy™")
st.write("Uncover exactly where your practice is leaking profit.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input("Annual Gross Collections ($)", min_value=0, value=1200000, step=50000)
        ops = st.number_input("Number of Operatories", min_value=1, value=5)
    with col2:
        ebitda = st.number_input("Current Annual EBITDA ($)", min_value=0, value=200000, step=10000)
        chair_days = st.number_input("Clinical Days per Week", min_value=1, value=4)

    if st.button("RUN AUTOPSY"):
        # BENCHMARKS (Logic for where they SHOULD be)
        # Healthy practices produce ~$25k-$30k per op/month
        target_revenue = ops * 30000 * 12 
        target_ebitda_pct = 0.22  # 22% is the "High Performance" sweet spot
        
        current_ebitda_pct = ebitda / revenue if revenue > 0 else 0
        revenue_gap = target_revenue - revenue
        
        st.markdown("---")
        st.subheader("Your Practice Analysis")
        
        # COLUMN 1: THE REVENUE GAP
        c1, c2 = st.columns(2)
        with c1:
            if revenue_gap > 0:
                st.error(f"**Annual Revenue Leak:**\n\n${revenue_gap:,.0f}")
                st.write(f"Based on your {ops} ops, you are under-utilizing your facility by {revenue_gap/target_revenue:.1%}.")
            else:
                st.success("**Revenue Performance:**\n\nElite Level")
                st.write("You are maximizing your square footage.")

        # COLUMN 2: THE PROFITABILITY
        with c2:
            if current_ebitda_pct < target_ebitda_pct:
                ebitda_gap = (revenue * target_ebitda_pct) - ebitda
                st.warning(f"**EBITDA Opportunity:**\n\n${ebitda_gap:,.0f}")
                st.write(f"Your margin is {current_ebitda_pct:.1%}. We aim for {target_ebitda_pct:.0%}.")
            else:
                st.success("**Profitability:**\n\nStrong")

        st.markdown(f"""
        <div class="report-card">
            <h3>The Verdict</h3>
            <p>Your practice should be producing <b>${target_revenue:,.0f}</b> per year. 
            By optimizing your clinical systems and cultural metrics, there is an immediate 
            <b>${max(0, revenue_gap) + max(0, (revenue * target_ebitda_pct) - ebitda):,.0f}</b> 
            improvement opportunity on the table.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Want the full clinical & cultural breakdown? Book your strategy call with The Marketeers.")
