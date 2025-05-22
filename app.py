import streamlit as st
import openai

st.title("Certificazione Team Work")
st.subheader("Simulazione con un collega virtuale")

openai.api_key = st.secrets["OPENAI_API_KEY"]

user_input = st.text_input("Il tuo collega non consegna in tempo un lavoro. Cosa gli dici?")

if user_input:
    # Risposta del collega virtuale
    chat_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un collega stressato da una scadenza mancata. Rispondi in modo realistico."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = chat_response.choices[0].message.content

    # Valutazione della risposta dell'utente
    scoring_prompt = f"""Analizza questa frase di un candidato nel contesto di collaborazione in un team:
'{user_input}'
Dai un punteggio da 0 a 100 sulla capacità di collaborazione (team work), spiegando brevemente perché.
Rispondi nel formato:
Punteggio: XX
Motivazione: ..."""

    scoring_response = openai.chat.completions.create(
        model="gpt-4",
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
