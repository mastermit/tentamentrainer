import streamlit as st
import random
import re

# Markdown-bestand inlezen en verwerken
def load_questions(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    questions = []
    raw_questions = re.split(r"## Vraag \d+", content)[1:]
    
    for raw in raw_questions:
        lines = raw.strip().split("\n")
        vraag = next((line for line in lines if line.startswith("Vraagstelling:")), "").replace("Vraagstelling:", "").strip()
        opties = [line.strip("* []") for line in lines if line.startswith("* ")]
        correct = next((line.strip("* []") for line in lines if "[x]" in line), None)
        
        if vraag and opties and correct:
            questions.append({"vraag": vraag, "opties": opties, "correct": correct})
    
    return questions

# Vragen inladen uit bestand
vraag_data = load_questions("TT_vragen_Eindtoets.md")
random.shuffle(vraag_data)

# State om voortgang bij te houden
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.fouten = []

st.title("Tentamentrainer")

if st.session_state.index < len(vraag_data):
    vraag = vraag_data[st.session_state.index]
    st.subheader(f"Vraag {st.session_state.index + 1}: {vraag['vraag']}")
    keuze = st.radio("Kies het juiste antwoord:", vraag["opties"], index=None)
    
    if st.button("Controleer antwoord"):
        if keuze:
            if keuze == vraag["correct"]:
                st.success("✅ Correct!")
                st.session_state.correct += 1
            else:
                st.error(f"❌ Fout! Het juiste antwoord is: {vraag['correct']}")
                st.session_state.wrong += 1
                st.session_state.fouten.append(vraag)
            
            st.session_state.index += 1
            st.experimental_rerun()
        else:
            st.warning("Selecteer een antwoord voordat je verder gaat.")
else:
    st.write("### Overzicht van je resultaten")
    st.write(f"✅ Correcte antwoorden: {st.session_state.correct}")
    st.write(f"❌ Foute antwoorden: {st.session_state.wrong}")
    
    if st.session_state.fouten:
        st.write("#### Fout beantwoorde vragen:")
        for f in st.session_state.fouten:
            st.write(f"- {f['vraag']} (Juiste antwoord: {f['correct']})")
    
    if st.button("Opnieuw beginnen"):
        st.session_state.index = 0
        st.session_state.correct = 0
        st.session_state.wrong = 0
        st.session_state.fouten = []
        st.experimental_rerun()
