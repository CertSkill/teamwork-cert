import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# 📌 Lista delle domande fisse
domande_fisse = [
    "Un collega non rispetta una scadenza. Come ti comporti?",
    "Sei in ritardo e il tuo team aspetta una tua parte. Cosa fai?",
    "Hai un'opinione diversa dal gruppo. Come la esprimi?",
    "Un nuovo membro entra nel team. Come lo accogli?",
    "Un collega ti interrompe spesso. Come reagisci?",
    "Il tuo team non ha raggiunto l’obiettivo. Cosa dici alla fine?",
    "Un collega si prende il merito di un tuo lavoro. Cosa fai?",
    "Devi lavorare con una persona che ti è poco simpatica. Come ti comporti?",
    "Il team sta decidendo in fretta una soluzione sbagliata. Come reagisci?",
    "Hai un dubbio su una tua attività. Cosa fai prima di procedere?"
]

# 📌 Lista delle domande adattive
domande_adattive = [
    "Il tuo feedback costruttivo è stato ignorato. Come reagisci?",
    "Hai un collega molto insicuro nel team. Come lo supporti?",
    "Ti viene chiesto di sostituire un collega senza preavviso. Accetti?",
    "Noti un conflitto tra due colleghi. Intervieni? Come?",
    "Hai appena sbagliato, e il team si blocca. Come lo comunichi?",
    "Il tuo team riceve una critica pubblica. Cosa dici internamente?",
    "Hai raggiunto l’obiettivo, ma un collega no. Cosa fai?",
    "Il tuo capo assegna al team un task quasi impossibile. Come reagisci con il gruppo?",
    "Vedi che alcuni membri sono meno coinvolti. Come ti comporti?",
    "Il gruppo ti delega il ruolo di coordinatore. Qual è la tua prima azione?"
]

# 🔁 Unisci tutte le domande
domande = domande_fisse + domande_adattive
tot_domande = len(domande)

# 🧠 Session state per avanzamento
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.risposte = []
    st.session_state.punteggi = []

st.title("Certificazione Soft Skill – Team Work")
st.markdown("**Rispondi alle 20 domande per ottenere la tua certificazione personalizzata.**")

# ⚙️ Logica principale del test
if st.session_state.indice < tot_domande:
    domanda_corrente = domande[st.session_state.indice]
    st.markdown(f"**Domanda {st.session_state.indice + 1} di {tot_domande}:** {domanda_corrente}")
    risposta = st.text_area("La tua risposta")


    if st.button("Invia risposta"):
        with st.spinner("Analisi della risposta in corso..."):
            valutazione = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"""Valuta questa risposta in merito alla capacità di lavorare in team:
Risposta: {risposta}
Assegna un punteggio da 0 a 100 sulla base di collaborazione, comunicazione, iniziativa, ascolto, gestione del conflitto.
Formato risposta:
Punteggio: XX
Motivazione: ..."""}
                ]
            )

            output = valutazione.choices[0].message.content
            st.session_state.risposte.append(risposta)
            st.session_state.punteggi.append(output)
            st.session_state.indice += 1
            st.rerun()

# ✅ Fine del test – calcolo finale
else:
    st.success("Hai completato il test!")

    punteggi_numerici = []
    for p in st.session_state.punteggi:
        try:
            riga = p.split("\n")[0]
            numero = int("".join(filter(str.isdigit, riga)))
            punteggi_numerici.append(numero)
        except:
            continue

    punteggio_finale = int(sum(punteggi_numerici) / len(punteggi_numerici)) if punteggi_numerici else 0

    st.markdown(f"### 🧮 Punteggio medio: **{punteggio_finale}/100**")

    if punteggio_finale >= 70:
        st.success("🎖 Complimenti! Hai ottenuto la certificazione Team Work.")
        st.image("https://raw.githubusercontent.com/CertSkill/teamwork-cert/main/badge.png", width=300)
    else:
        st.info("🧠 Continua ad allenarti per ottenere la certificazione.")
    st.markdown("---")
       if st.button("🔄 Ricomincia il test"):
            st.session_state.clear()
            st.rerun()
