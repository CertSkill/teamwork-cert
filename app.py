import streamlit as st
import openai

st.title("Certificazione Team Work")
st.subheader("Simulazione con un collega virtuale")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Input dell'utente
user_input = st.text_input("Il tuo collega non consegna in tempo un lavoro. Cosa gli dici?")

# Invio a GPT
if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un collega stressato da una scadenza mancata. Rispondi in modo realistico."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    st.markdown("**Risposta del collega:**")
    st.write(reply)
