import streamlit as st
import openai

st.set_page_config(page_title="Certificazione Team Work", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Certificazione Team Work")
st.subheader("30 domande: 10 adattive + 20 personalizzate in base al profilo")

# Inizializza sessione
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
    st.session_state.domande_fase_b = []

NUM_DOMANDE_A = 10
NUM_DOMANDE_TOTALI = 30

# Flusso A: genera la prossima domanda in base alla risposta precedente
def genera_domanda_flusso_a(risposta_precedente):
    prompt = f"""Come un team composto da uno psicologo del lavoro, un HR senior, un project manager, un data analyst HR, un formatore aziendale e un esperto UX, genera una nuova domanda per valutare meglio il teamwork sulla base di questa risposta:
\"{risposta_precedente}\"
Scrivi solo la domanda."""
    out = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return out.choices[0].message.content.strip()

# Flusso B: genera 20 domande personalizzate a partire dal profilo
def genera_domande_flusso_b(profilo):
    profilo_descrizione = ", ".join([f"{k}: {round(sum(v)/len(v), 2) if v else 0}" for k, v in profilo.items()])
    prompt = f"""Sei un team di esperti HR. Genera 20 domande personalizzate per valutare il teamwork di un candidato con questo profilo: {profilo_descrizione}. Scrivi solo 1 domanda per riga."""
    out = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return [r.strip() for r in out.choices[0].message.content.strip().split("\n") if r.strip()]

# Domande
if st.session_state.indice < NUM_DOMANDE_TOTALI:
    if st.session_state.indice == 0:
        domanda = "Un collega non rispetta una scadenza. Come ti comporti?"
    elif st.session_state.indice < NUM_DOMANDE_A:
        domanda = genera_domanda_flusso_a(st.session_state.risposte[-1])
    elif st.session_state.indice == NUM_DOMANDE_A:
        st.session_state.domande_fase_b = genera_domande_flusso_b(st.session_state.profilo)
        domanda = st.session_state.domande_fase_b[0]
    else:
        domanda = st.session_state.domande_fase_b[st.session_state.indice - NUM_DOMANDE_A]

    st.markdown(f"### Domanda {st.session_state.indice + 1} di {NUM_DOMANDE_TOTALI}")
    st.markdown(f"**{domanda}**")
    risposta = st.text_area("La tua risposta", value="", key=f"risposta_{st.session_state.indice}")

    if st.button("Invia risposta", key=f"btn_{st.session_state.indice}"):
        with st.spinner("Analisi della risposta..."):
            valutazione = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
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

Spiega brevemente ogni punteggio."""
                }]
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

# Fase finale: profilo + badge
else:
    st.success("✅ Test completato!")
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
