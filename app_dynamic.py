
import streamlit as st
import openai

st.set_page_config(page_title="Certificazione Team Work", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Certificazione Team Work")
st.subheader("Valutazione guidata da esperti: 5 domande statiche, 15 adattive")

# Domande statiche (fisse)
domande_statiche = [
    "Un collega non rispetta una scadenza. Come ti comporti?",
    "Durante una riunione un collega ti interrompe più volte. Come reagisci?",
    "Il team ha preso una decisione che non condividi. Cosa fai?",
    "Ti viene chiesto di coordinare un progetto. Come ti organizzi?",
    "Ricevi un feedback negativo dal team. Come reagisci?"
]

# Sessione
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.risposte = []
    st.session_state.punteggi = []
    st.session_state.profilo = {
        "Collaborazione": [],
        "Comunicazione": [],
        "Leadership": [],
        "Problem solving": [],
        "Empatia": []
    }

# Numero totale (5 statiche + 15 dinamiche)
totale_domande = 20

# Funzione per generare domanda dinamica
def genera_domanda_dinamica(storia_utente):
    prompt = f"""Agisci come un team composto da:
- uno psicologo comportamentale aziendale,
- un HR manager esperto in selezione,
- un project manager operativo,
- un data analyst HR tech,
- un formatore aziendale,
- un esperto UX e digital assessment.

In base a questa risposta data dal candidato:
{storia_utente}

Genera una domanda successiva che permetta di approfondire la valutazione della soft skill teamwork. Sii specifico e contestuale. Scrivi solo la domanda."""
    risposta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return risposta.choices[0].message.content.strip()

# Logica test
if st.session_state.indice < totale_domande:
    if st.session_state.indice < 5:
        domanda = domande_statiche[st.session_state.indice]
    else:
        # Domande dinamiche in base alla risposta precedente
        ultima = st.session_state.risposte[-1] if st.session_state.risposte else ""
        domanda = genera_domanda_dinamica(ultima)

    st.markdown(f"### Domanda {st.session_state.indice + 1} di {totale_domande}")
    st.markdown(f"**{domanda}**")
    risposta = st.text_area("La tua risposta")

    if st.button("Invia risposta"):
        with st.spinner("Analisi della risposta..."):
            valutazione = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Valuta questa risposta in merito alla capacità di lavorare in team:
Risposta: {risposta}
Assegna un punteggio da 0 a 100 per ciascuna delle seguenti dimensioni:
1. Collaborazione
2. Comunicazione
3. Leadership
4. Problem solving
5. Empatia

Rispondi nel formato:
Collaborazione: XX
Comunicazione: XX
Leadership: XX
Problem solving: XX
Empatia: XX

Spiega brevemente ogni punteggio.
"""
                    }
                ]
            )

            output = valutazione.choices[0].message.content
            st.session_state.risposte.append(risposta)
            st.session_state.punteggi.append(output)

            for riga in output.splitlines():
                for chiave in st.session_state.profilo:
                    if riga.startswith(chiave):
                        numero = ''.join(filter(str.isdigit, riga))
                        if numero:
                            st.session_state.profilo[chiave].append(int(numero))

            st.session_state.indice += 1
            st.rerun()

else:
    st.success("✅ Test completato!")
    st.markdown("---")

    punteggi_finali = {
        k: round(sum(v)/len(v), 2) if v else 0 for k, v in st.session_state.profilo.items()
    }
    media_totale = round(sum(punteggi_finali.values()) / len(punteggi_finali), 2)

    st.markdown("### 📊 Profilo del candidato")
    for k, v in punteggi_finali.items():
        st.markdown(f"**{k}:** {v}/100")

    punti_forti = [k for k, v in punteggi_finali.items() if v >= 80]
    punti_deboli = [k for k, v in punteggi_finali.items() if v < 60]
    miglioramento = [k for k in punteggi_finali if 60 <= punteggi_finali[k] < 80]

    st.markdown("### ✅ Punti di forza")
    st.markdown(", ".join(punti_forti) if punti_forti else "_Nessun punto forte evidente._")

    st.markdown("### 🧩 Aree di miglioramento")
    st.markdown(", ".join(miglioramento) if miglioramento else "_Non ci sono aree intermedie._")

    st.markdown("### ⚠️ Punti deboli")
    st.markdown(", ".join(punti_deboli) if punti_deboli else "_Nessun punto critico identificato._")

    if media_totale >= 70:
        st.success("🎖 Hai ottenuto la certificazione Team Work!")
        st.image("https://raw.githubusercontent.com/CertSkill/teamwork-cert/main/badge.png", width=300)
    else:
        st.info("🧠 Continua ad allenarti per ottenere la certificazione.")

    if st.button("🔄 Ricomincia il test"):
        st.session_state.clear()
        st.rerun()
