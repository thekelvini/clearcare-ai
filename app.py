import streamlit as st
import requests

st.set_page_config(
    page_title="ClearCare AI",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f7fbff;
}
.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.hero {
    background: linear-gradient(90deg, rgba(0,76,140,0.98), rgba(0,118,190,0.70)),
    url("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d");
    background-size: cover;
    background-position: center;
    border-radius: 16px;
    padding: 42px;
    color: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}
.hero h1 {
    font-size: 52px;
    margin-bottom: 0;
    font-weight: 800;
}
.hero h2 {
    font-size: 28px;
    color: #d7ecff;
    margin-top: 5px;
}
.hero p {
    font-size: 20px;
    max-width: 620px;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 18px;
}
.feature-card {
    background: white;
    border: 1px solid #dbe7f1;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.05);
}
.feature-card h3 {
    color: #0b1f3a;
    font-size: 22px;
    margin-bottom: 6px;
}
.feature-card p {
    color: #4b5563;
    font-size: 16px;
}
.notice {
    background: #fff7e6;
    border: 1px solid #f3c979;
    border-radius: 14px;
    padding: 20px;
    color: #3f2d00;
    font-size: 17px;
    margin-top: 18px;
}
.work-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 18px;
}
.work-card {
    background: white;
    border: 1px solid #dbe7f1;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.05);
}
.work-card h2 {
    color: #0b1f3a;
    font-size: 25px;
    margin-bottom: 16px;
}
.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #cfdce8;
    font-size: 16px;
}
.stButton button {
    background: #006dcc;
    color: white;
    border: none;
    border-radius: 10px;
    height: 55px;
    font-size: 18px;
    font-weight: 700;
}
.stButton button:hover {
    background: #004f99;
    color: white;
}
.footer {
    text-align: center;
    color: #475569;
    font-size: 14px;
    margin-top: 22px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🛡️ ClearCare AI</h1>
    <h2>Discharge Instruction Simplifier</h2>
    <p>Turning complex discharge instructions into clear, friendly language.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>👩‍⚕️ Nurse Reviewed</h3>
        <p>All outputs require licensed healthcare professional review.</p>
    </div>
    <div class="feature-card">
        <h3>🛡️ Safety First</h3>
        <p>Doses and warning signs are never changed.</p>
    </div>
    <div class="feature-card">
        <h3>📄 Plain Language</h3>
        <p>Complex medical terms are simplified for patients.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
<strong>Clinical Safety Notice:</strong> This tool simplifies discharge instructions only.
It does not diagnose, prescribe, or replace medical judgment.
A licensed healthcare professional must review all outputs before patient use.
</div>
# """, unsafe_allow_html=True)

# st.markdown('<div class="work-grid">', unsafe_allow_html=True)

# st.markdown('<div class="work-card">', unsafe_allow_html=True)
# st.markdown("<h2>📋 Paste Discharge Instructions</h2>", unsafe_allow_html=True)

user_input = st.text_area(
    "Paste de-identified discharge instructions here",
    height=260,
    label_visibility="collapsed",
    placeholder="Paste de-identified discharge instructions here..."
)

simplify_button = st.button(
    "✨ Simplify Instructions",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="work-card">', unsafe_allow_html=True)
st.markdown("<h2>💬 Patient-Friendly Version</h2>", unsafe_allow_html=True)

output_placeholder = st.empty()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if simplify_button:
    if user_input.strip() == "":
        st.error("Please paste discharge instructions.")
    else:
        try:
            with st.spinner("Simplifying instructions..."):
                prompt = f"""
You are ClearCare AI.

Rewrite the discharge instructions in clear patient-friendly language.

Rules:
- Do not add medical advice.
- Do not remove safety instructions.
- Do not change medication doses.
- Keep the meaning medically accurate.
- Use simple patient-friendly language.
- Use short headings.
- Keep the answer brief.
- End with: Nurse review required before patient delivery.

Discharge Instructions:
{user_input}
"""

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3.2:1b",
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_predict": 250,
                            "temperature": 0.2
                        }
                    },
                    timeout=90
                )

                if response.status_code != 200:
                    st.error("Ollama did not respond correctly. Make sure Ollama is running.")
                else:
                    result = response.json()
                    simplified_text = result.get("response", "")

                    if simplified_text.strip() == "":
                        st.error("No output was generated. Try a shorter discharge note.")
                    else:
                        output_placeholder.text_area(
                            "Simplified output",
                            simplified_text,
                            height=260,
                            label_visibility="collapsed"
                        )

                        st.success("Simplification complete. Nurse review is required.")

        except requests.exceptions.ConnectionError:
            st.error("Ollama is not running. Open Ollama and run: ollama run llama3.2:1b")

        except requests.exceptions.Timeout:
            st.error("The model took too long. Try a shorter note or restart Ollama.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("""
<div class="footer">
🛡️ ClearCare AI Prototype | Local AI Model | Educational Demonstration Only
</div>
""", unsafe_allow_html=True)