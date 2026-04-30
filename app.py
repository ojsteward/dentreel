import streamlit as st
import streamlit.components.v1 as components
import time

# 1. SETUP
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
    .report-card { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 15px; border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px; }
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

# 2. ISOLATED INPUTS
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        # We use strict session keys to prevent cross-talk
        eb_in = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1, key="eb_val")
        ns_in = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1, key="ns_val")
        id_in = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1, key="id_val")
        hw_in = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1, key="hw_val")
    with c2:
        hp_in = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1, key="hp_val")
        hper_in = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1, key="hper_val")
        np_in = st.number_input("# New Patients per Month", min_value=0, value=None, step=1, key="np_val")
        cp_in = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1, key="cp_val")

    if st.button("Generate Autopsy Results"):
        with st.empty():
            for i in range(5):
                st.markdown(f"### 🧪 Pronto AI is conducting autopsy... {5-i}s")
                time.sleep(1)
        
        # 3. QUARANTINED MATH ENGINE (Variables defined only inside this scope)
        BASE_REV = 1200000
        output = {}

        # EBITDA
        if eb_in is not None:
            eb_loss = max(0.0, (22 - eb_in) / 100 * BASE_REV)
            output['EBITDA'] = {'loss': eb_loss, 'color': "green" if eb_in >= 22 else "red"}

        # No Shows
        if ns_in is not None:
            ns_loss = max(0.0, (ns_in - 5) / 100 * BASE_REV)
            output['No Shows'] = {'loss': ns_loss, 'color': "green" if ns_in <= 5 else "red"}

        # Insurance
        if id_in is not None:
            ins_loss = max(0.0, (id_in - 25) / 365 * 0.07 * BASE_REV)
            output['Insurance'] = {'loss': ins_loss, 'color': "green" if id_in <= 25 else "red"}

        # Hiring
        if hw_in is not None:
            hr_loss = max(0.0, (hw_in - 4) * 5120 - 10000)
            output['Hiring'] = {'loss': hr_loss, 'color': "green" if hw_in <= 4 else "red"}

        # New Patients
        if cp_in is not None and np_in is not None:
            np_loss = max(0.0, (80 - cp_in) / 100 * np_in * 1000 * 12)
            output['New Patients'] = {'loss': np_loss, 'color': "green" if cp_in >= 80 else "red"}

        # HYGIENE PRODUCTION (Calculation #5)
        loss_5 = 0.0
        if hp_in is not None:
            loss_5 = max(0.0, (30 - hp_in) / 100 * BASE_REV)
            output['Hygiene Production'] = {'loss': loss_5, 'color': "green" if hp_in >= 30 else "red"}

        # HYGIENE PERIO (Calculation #6 - THE LEAK STOPPER)
        if hper_in is not None:
            p_diff = (40 - hper_in) / 100
            
            # Here is the fix: We use the literal input values ONLY.
            # No reference to the EBITDA variable or any other category result.
            if hp_in is not None and hp_in >= 30:
                # Use their actual hygiene production
                perio_math = p_diff * (hp_in / 100) * BASE_REV
            else:
                # Use the benchmark 30% and add the production gap
                # loss_5 is defined locally right above, it cannot see EBITDA.
                perio_math = (p_diff * 0.30 * BASE_REV) + loss_5
            
            output['Hygiene Perio'] = {'loss': max(0.0, perio_math), 'color': "green" if hper_in >= 40 else "red"}

        # 4. RESULTS DISPLAY
        if output:
            fruit = max(output, key=lambda x: output[x]['loss'])
            total_sum = sum(v['loss'] for v in output.values())
            
            any_skipped = any(v is None for v in [eb_in, ns_in, id_in, hw_in, hp_in, hper_in, np_in, cp_in])
            skip_msg = f'<p style="color: #00d2ff; font-weight: bold; font-family: sans-serif;">Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>' if any_skipped else ''

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-family: sans-serif;">The Verdict</h1>
                <p style="font-size: 1.2rem; font-family: sans-serif;">Pronto discovered that your low hanging fruit is in <b>{fruit}</b></p>
                <p style="font-size: 1.1rem; font-family: sans-serif;">Based on 1.2 million in production, your practice is leaving <b>${total_sum:,.0f}</b> on the table annually.</p>
                {skip_msg}
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for k, v in output.items():
                st.markdown(f'<div class="status-box status-{v["color"]}">{k}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. CTA & DISCLAIMER
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px; padding: 10px;">
                <p style="font-size: 1.2rem; color: #ff8c00; font-weight: 700;">“You just got a glimpse.”</p>
                <p style="font-size: 1.1rem; color: #ffffff; font-family: sans-serif;">
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
            <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
            <script src="https://link.msgsndr.com/js/form_embed.js"></script>
        """, height=650)
