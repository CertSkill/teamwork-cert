import streamlit as st
import openai

st.title("Certificazione Team Work")
st.subheader("Simulazione con un collega virtuale")

# Chiave segreta da Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Input dell'utente
user_input = st.text_input("Il tuo collega non consegna in tempo un lavoro. Cosa gli dici?")

if user_input:
    # Risposta del collega virtuale
    chat_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un collega stressato da una scadenza mancata. Rispondi in modo realistico."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = chat_response.choices[0].message.content

    # Valutazione della risposta dell’utente
    scoring_prompt = f"""Analizza questa frase di un candidato nel contesto di collaborazione in un team:
'{user_input}'
Dai un punteggio da 0 a 100 sulla capacità di collaborazione (team work), spiegando brevemente perché.
Rispondi nel formato:
Punteggio: XX
Motivazione: ..."""

    scoring_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": scoring_prompt}
        ]
    )
    scoring_result = scoring_response.choices[0].message.content

    # Output
    st.markdown("**Risposta del collega:**")
    st.write(reply)

    st.markdown("**Valutazione della tua risposta:**")
    st.write(scoring_result)
    # Badge finale (se supera soglia)
try:
    score_line = scoring_result.split("\n")[0]
    score = int("".join(filter(str.isdigit, score_line)))

    if score >= 70:
        st.success("🎖 Hai ottenuto la certificazione Team Work!")
        st.image("https://raw.githubusercontent.com/CertSkill/teamwork-cert/main/badge.png", width=300)
    else:
        st.info("🧠 Continua ad allenarti per ottenere la certificazione.")
except:
    st.warning("⚠️ Impossibile determinare il punteggio in automatico.")

