import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import copy

# Configurazione pagina
st.set_page_config(
    page_title="F1 Database Manager",
    page_icon="🏎️",
    layout="wide"
)

# Titolo dell'app
st.title("🏎️ F1 Database Manager")
st.markdown("Gestisci e aggiorna i tuoi file JSON della Formula 1")

# Directory per i file JSON
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Schema dei file
SCHEMAS = {
    "f1db-drivers.json": {
        "fields": [
            {"name": "id", "type": "text", "required": True},
            {"name": "name", "type": "text", "required": True},
            {"name": "firstName", "type": "text", "required": True},
            {"name": "lastName", "type": "text", "required": True},
            {"name": "fullName", "type": "text", "required": True},
            {"name": "abbreviation", "type": "text", "required": True},
            {"name": "permanentNumber", "type": "text", "required": True},
            {"name": "gender", "type": "select", "options": ["MALE", "FEMALE", "OTHER"], "required": True},
            {"name": "dateOfBirth", "type": "date", "required": True},
            {"name": "dateOfDeath", "type": "date", "required": False},
            {"name": "placeOfBirth", "type": "text", "required": True},
            {"name": "countryOfBirthCountryId", "type": "text", "required": True},
            {"name": "nationalityCountryId", "type": "text", "required": True},
            {"name": "secondNationalityCountryId", "type": "text", "required": False},
            {"name": "bestChampionshipPosition", "type": "number", "required": True},
            {"name": "bestStartingGridPosition", "type": "number", "required": True},
            {"name": "bestRaceResult", "type": "number", "required": True},
            {"name": "bestSprintRaceResult", "type": "number", "required": False},
            {"name": "totalChampionshipWins", "type": "number", "required": True},
            {"name": "totalRaceEntries", "type": "number", "required": True},
            {"name": "totalRaceStarts", "type": "number", "required": True},
            {"name": "totalRaceWins", "type": "number", "required": True},
            {"name": "totalRaceLaps", "type": "number", "required": True},
            {"name": "totalPodiums", "type": "number", "required": True},
            {"name": "totalPoints", "type": "number", "required": True},
            {"name": "totalChampionshipPoints", "type": "number", "required": True},
            {"name": "totalPolePositions", "type": "number", "required": True},
            {"name": "totalFastestLaps", "type": "number", "required": True},
            {"name": "totalSprintRaceStarts", "type": "number", "required": True},
            {"name": "totalSprintRaceWins", "type": "number", "required": True},
            {"name": "totalDriverOfTheDay", "type": "number", "required": True},
            {"name": "totalGrandSlams", "type": "number", "required": True}
        ]
    },
    "f1db-constructors.json": {
        "fields": [
            {"name": "id", "type": "text", "required": True},
            {"name": "name", "type": "text", "required": True},
            {"name": "fullName", "type": "text", "required": True},
            {"name": "countryId", "type": "text", "required": True},
            {"name": "bestChampionshipPosition", "type": "number", "required": True},
            {"name": "bestStartingGridPosition", "type": "number", "required": True},
            {"name": "bestRaceResult", "type": "number", "required": True},
            {"name": "bestSprintRaceResult", "type": "number", "required": False},
            {"name": "totalChampionshipWins", "type": "number", "required": True},
            {"name": "totalRaceEntries", "type": "number", "required": True},
            {"name": "totalRaceStarts", "type": "number", "required": True},
            {"name": "totalRaceWins", "type": "number", "required": True},
            {"name": "total1And2Finishes", "type": "number", "required": True},
            {"name": "totalRaceLaps", "type": "number", "required": True},
            {"name": "totalPodiums", "type": "number", "required": True},
            {"name": "totalPodiumRaces", "type": "number", "required": True},
            {"name": "totalPoints", "type": "number", "required": True},
            {"name": "totalChampionshipPoints", "type": "number", "required": True},
            {"name": "totalPolePositions", "type": "number", "required": True},
            {"name": "totalFastestLaps", "type": "number", "required": True},
            {"name": "totalSprintRaceStarts", "type": "number", "required": True},
            {"name": "totalSprintRaceWins", "type": "number", "required": True}
        ]
    },
    "f1db-races-race-results.json": {
        "fields": [
            {"name": "raceId", "type": "number", "required": True},
            {"name": "year", "type": "number", "required": True},
            {"name": "round", "type": "number", "required": True},
            {"name": "positionDisplayOrder", "type": "number", "required": True},
            {"name": "positionNumber", "type": "number", "required": True},
            {"name": "positionText", "type": "text", "required": True},
            {"name": "driverNumber", "type": "text", "required": True},
            {"name": "driverId", "type": "text", "required": True},
            {"name": "constructorId", "type": "text", "required": True},
            {"name": "engineManufacturerId", "type": "text", "required": True},
            {"name": "tyreManufacturerId", "type": "text", "required": True},
            {"name": "sharedCar", "type": "checkbox", "required": True},
            {"name": "laps", "type": "number", "required": True},
            {"name": "time", "type": "text", "required": False},
            {"name": "timeMillis", "type": "number", "required": False},
            {"name": "timePenalty", "type": "text", "required": False},
            {"name": "timePenaltyMillis", "type": "number", "required": False},
            {"name": "gap", "type": "text", "required": True},
            {"name": "gapMillis", "type": "number", "required": False},
            {"name": "gapLaps", "type": "number", "required": True},
            {"name": "interval", "type": "text", "required": False},
            {"name": "intervalMillis", "type": "number", "required": False},
            {"name": "reasonRetired", "type": "text", "required": False},
            {"name": "points", "type": "number", "required": False},
            {"name": "polePosition", "type": "checkbox", "required": True},
            {"name": "qualificationPositionNumber", "type": "number", "required": True},
            {"name": "qualificationPositionText", "type": "text", "required": True},
            {"name": "gridPositionNumber", "type": "number", "required": True},
            {"name": "gridPositionText", "type": "text", "required": True},
            {"name": "positionsGained", "type": "number", "required": True},
            {"name": "pitStops", "type": "number", "required": True},
            {"name": "fastestLap", "type": "checkbox", "required": True},
            {"name": "driverOfTheDay", "type": "checkbox", "required": True},
            {"name": "grandSlam", "type": "checkbox", "required": True}
        ]
    }
}

# Funzioni di utilità
def load_json_file(filename):
    """Carica un file JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json_file(filename, data):
    """Salva dati in un file JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def convert_date_to_string(date_obj):
    """Converte un oggetto date in stringa ISO"""
    if date_obj:
        return date_obj.isoformat()
    return None

def convert_string_to_date(date_str):
    """Converte una stringa ISO in oggetto date"""
    if date_str:
        return datetime.fromisoformat(date_str).date()
    return None

# Sidebar per la navigazione
st.sidebar.title("Navigazione")

# Seleziona tipo di file
file_type = st.sidebar.selectbox(
    "Seleziona tipo di dati",
    ["Piloti", "Costruttori", "Risultati Gare"],
    index=0
)

# Mappatura tipo di file
FILE_MAPPING = {
    "Piloti": "f1db-drivers.json",
    "Costruttori": "f1db-constructors.json",
    "Risultati Gare": "f1db-races-race-results.json"
}

selected_file = FILE_MAPPING[file_type]
schema = SCHEMAS[selected_file]

# Carica i dati esistenti
data = load_json_file(selected_file)

# Layout principale
tab1, tab2, tab3 = st.tabs(["Visualizza", "Aggiungi", "Modifica"])

with tab1:
    st.header(f"📊 Visualizza {file_type}")
    
    if data:
        # Converti in DataFrame per una visualizzazione migliore
        df = pd.DataFrame(data)
        
        # Mostra statistiche
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Numero record", len(data))
        with col2:
            if file_type == "Piloti":
                st.metric("Piloti attivi", len([d for d in data if not d.get('dateOfDeath')]))
            elif file_type == "Costruttori":
                st.metric("Costruttori", len(data))
            else:
                st.metric("Gare registrate", df['raceId'].nunique())
        
        # Filtri
        st.subheader("Filtri")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'name' in df.columns:
                search_name = st.text_input("Cerca per nome")
                if search_name:
                    df = df[df['name'].str.contains(search_name, case=False, na=False)]
        
        with col2:
            if 'year' in df.columns:
                years = sorted(df['year'].unique())
                selected_year = st.selectbox("Filtra per anno", ["Tutti"] + list(years))
                if selected_year != "Tutti":
                    df = df[df['year'] == selected_year]
        
        # Mostra dati
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Opzione per scaricare i dati
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Scarica come CSV",
            data=csv,
            file_name=f"{selected_file.replace('.json', '')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nessun dato disponibile. Usa la tab 'Aggiungi' per inserire nuovi record.")

with tab2:
    st.header(f"➕ Aggiungi nuovo {file_type[:-1].replace('f1db-', '').replace('.json', '')}")
    
    with st.form("add_form"):
        form_data = {}
        
        # Crea campi del form dinamicamente basandosi sullo schema
        cols = st.columns(2)
        col_idx = 0
        
        for field in schema["fields"]:
            with cols[col_idx]:
                field_name = field["name"]
                field_type = field["type"]
                required = field.get("required", False)
                
                label = f"{field_name}{' *' if required else ''}"
                
                if field_type == "text":
                    form_data[field_name] = st.text_input(label, value="")
                
                elif field_type == "number":
                    form_data[field_name] = st.number_input(
                        label,
                        value=0,
                        step=1 if field_name in ["raceId", "year", "round"] else 0.1
                    )
                
                elif field_type == "date":
                    form_data[field_name] = st.date_input(label)
                
                elif field_type == "select":
                    options = field.get("options", [])
                    form_data[field_name] = st.selectbox(
                        label,
                        options=options
                    )
                
                elif field_type == "checkbox":
                    form_data[field_name] = st.checkbox(label, value=False)
            
            col_idx = (col_idx + 1) % 2
        
        # Bottone per submit
        submitted = st.form_submit_button("Salva nuovo record")
        
        if submitted:
            # Validazione campi obbligatori
            missing_fields = []
            for field in schema["fields"]:
                if field.get("required", False):
                    field_name = field["name"]
                    if field_name not in form_data or form_data[field_name] == "":
                        missing_fields.append(field_name)
            
            if missing_fields:
                st.error(f"Campi obbligatori mancanti: {', '.join(missing_fields)}")
            else:
                # Converti date in stringhe
                for field in schema["fields"]:
                    if field["type"] == "date":
                        field_name = field["name"]
                        if form_data[field_name]:
                            form_data[field_name] = convert_date_to_string(form_data[field_name])
                
                # Aggiungi nuovo record ai dati
                data.append(form_data)
                
                # Salva nel file
                if save_json_file(selected_file, data):
                    st.success("Record salvato con successo!")
                    st.rerun()
                else:
                    st.error("Errore nel salvataggio del record")

with tab3:
    st.header(f"✏️ Modifica {file_type}")
    
    if data:
        # Seleziona record da modificare
        if file_type == "Piloti":
            options = {f"{d.get('name', '')} ({d.get('id', '')})": idx for idx, d in enumerate(data)}
        elif file_type == "Costruttori":
            options = {f"{d.get('name', '')} ({d.get('id', '')})": idx for idx, d in enumerate(data)}
        else:
            options = {f"Race {d.get('raceId', '')} - Driver {d.get('driverId', '')}": idx for idx, d in enumerate(data)}
        
        selected_key = st.selectbox(
            "Seleziona record da modificare",
            options=list(options.keys())
        )
        
        if selected_key:
            record_idx = options[selected_key]
            record = copy.deepcopy(data[record_idx])
            
            with st.form("edit_form"):
                # Crea campi del form con i valori esistenti
                edit_data = {}
                cols = st.columns(2)
                col_idx = 0
                
                for field in schema["fields"]:
                    with cols[col_idx]:
                        field_name = field["name"]
                        field_type = field["type"]
                        required = field.get("required", False)
                        
                        label = f"{field_name}{' *' if required else ''}"
                        current_value = record.get(field_name, "")
                        
                        # Converti stringhe date in oggetti date per il form
                        if field_type == "date" and current_value:
                            try:
                                current_value = convert_string_to_date(current_value)
                            except:
                                current_value = None
                        
                        if field_type == "text":
                            edit_data[field_name] = st.text_input(
                                label,
                                value=str(current_value) if current_value is not None else ""
                            )
                        
                        elif field_type == "number":
                            edit_data[field_name] = st.number_input(
                                label,
                                value=float(current_value) if current_value is not None else 0,
                                step=1 if field_name in ["raceId", "year", "round"] else 0.1
                            )
                        
                        elif field_type == "date":
                            edit_data[field_name] = st.date_input(
                                label,
                                value=current_value
                            )
                        
                        elif field_type == "select":
                            options = field.get("options", [])
                            edit_data[field_name] = st.selectbox(
                                label,
                                options=options,
                                index=options.index(current_value) if current_value in options else 0
                            )
                        
                        elif field_type == "checkbox":
                            edit_data[field_name] = st.checkbox(
                                label,
                                value=bool(current_value) if current_value is not None else False
                            )
                    
                    col_idx = (col_idx + 1) % 2
                
                col1, col2 = st.columns(2)
                with col1:
                    update_clicked = st.form_submit_button("Aggiorna record")
                with col2:
                    delete_clicked = st.form_submit_button("Elimina record", type="secondary")
                
                if update_clicked:
                    # Validazione
                    missing_fields = []
                    for field in schema["fields"]:
                        if field.get("required", False):
                            field_name = field["name"]
                            if field_name not in edit_data or edit_data[field_name] == "":
                                missing_fields.append(field_name)
                    
                    if missing_fields:
                        st.error(f"Campi obbligatori mancanti: {', '.join(missing_fields)}")
                    else:
                        # Converti date in stringhe
                        for field in schema["fields"]:
                            if field["type"] == "date":
                                field_name = field["name"]
                                edit_data[field_name] = convert_date_to_string(edit_data[field_name])
                        
                        # Aggiorna record
                        data[record_idx] = edit_data
                        
                        if save_json_file(selected_file, data):
                            st.success("Record aggiornato con successo!")
                            st.rerun()
                
                if delete_clicked:
                    # Conferma eliminazione
                    if st.warning("Sei sicuro di voler eliminare questo record?"):
                        # Rimuovi record
                        data.pop(record_idx)
                        
                        if save_json_file(selected_file, data):
                            st.success("Record eliminato con successo!")
                            st.rerun()
    else:
        st.info("Nessun dato disponibile da modificare.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Istruzioni:**
    1. Seleziona il tipo di dati dalla sidebar
    2. Visualizza i dati nella tab 'Visualizza'
    3. Aggiungi nuovi record nella tab 'Aggiungi'
    4. Modifica o elimina record nella tab 'Modifica'
    
    I dati vengono salvati automaticamente nei file JSON.
    """
)

# Bottone per scaricare tutti i dati
st.sidebar.markdown("---")
if st.sidebar.button("📥 Scarica tutti i dati"):
    # Crea un file ZIP con tutti i JSON
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename in FILE_MAPPING.values():
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                zip_file.write(filepath, filename)
    
    zip_buffer.seek(0)
    
    st.sidebar.download_button(
        label="Scarica ZIP",
        data=zip_buffer,
        file_name="f1db_data.zip",
        mime="application/zip"
    )
