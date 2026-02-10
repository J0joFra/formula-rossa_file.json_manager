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
tab1, tab2, tab3, tab4 = st.tabs(["Visualizza", "Aggiungi singolo", "Aggiungi multipli", "Modifica"])

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
    st.header(f"📝 Aggiungi più {file_type[:-1].replace('f1db-', '').replace('.json', '')}")
    
    st.markdown("""
    **Incolla qui sotto i nuovi record in formato JSON.**
    
    Puoi incollare:
    - Un singolo oggetto JSON: `{...}`
    - Un array di oggetti JSON: `[{...}, {...}, ...]`
    
    Esempio per un pilota:
    ```json
    {
        "id": "nuovo-pilota",
        "name": "Nuovo Pilota",
        "firstName": "Nuovo",
        "lastName": "Pilota",
        "fullName": "Nuovo Pilota",
        "abbreviation": "NUP",
        "permanentNumber": "99",
        "gender": "MALE",
        "dateOfBirth": "2000-01-01",
        "dateOfDeath": null,
        "placeOfBirth": "Città",
        "countryOfBirthCountryId": "italy",
        "nationalityCountryId": "italy",
        "secondNationalityCountryId": null,
        "bestChampionshipPosition": 0,
        "bestStartingGridPosition": 0,
        "bestRaceResult": 0,
        "bestSprintRaceResult": null,
        "totalChampionshipWins": 0,
        "totalRaceEntries": 0,
        "totalRaceStarts": 0,
        "totalRaceWins": 0,
        "totalRaceLaps": 0,
        "totalPodiums": 0,
        "totalPoints": 0,
        "totalChampionshipPoints": 0,
        "totalPolePositions": 0,
        "totalFastestLaps": 0,
        "totalSprintRaceStarts": 0,
        "totalSprintRaceWins": 0,
        "totalDriverOfTheDay": 0,
        "totalGrandSlams": 0
    }
    ```
    """)
    
    # Area di testo per incollare JSON
    json_input = st.text_area(
        "Incolla i dati JSON qui:",
        height=300,
        placeholder='{"id": "example", "name": "Example Name", ...} oppure [{"id": "example1", ...}, {"id": "example2", ...}]'
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Carica da esempio", use_container_width=True):
            # Mostra un esempio basato sul tipo di file
            if file_type == "Piloti":
                example = {
                    "id": f"nuovo-pilota-{len(data)+1}",
                    "name": f"Nuovo Pilota {len(data)+1}",
                    "firstName": "Nuovo",
                    "lastName": f"Pilota {len(data)+1}",
                    "fullName": f"Nuovo Pilota {len(data)+1}",
                    "abbreviation": "NUP",
                    "permanentNumber": str(90 + len(data)),
                    "gender": "MALE",
                    "dateOfBirth": "2000-01-01",
                    "dateOfDeath": None,
                    "placeOfBirth": "Città",
                    "countryOfBirthCountryId": "italy",
                    "nationalityCountryId": "italy",
                    "secondNationalityCountryId": None,
                    "bestChampionshipPosition": 0,
                    "bestStartingGridPosition": 0,
                    "bestRaceResult": 0,
                    "bestSprintRaceResult": None,
                    "totalChampionshipWins": 0,
                    "totalRaceEntries": 0,
                    "totalRaceStarts": 0,
                    "totalRaceWins": 0,
                    "totalRaceLaps": 0,
                    "totalPodiums": 0,
                    "totalPoints": 0,
                    "totalChampionshipPoints": 0,
                    "totalPolePositions": 0,
                    "totalFastestLaps": 0,
                    "totalSprintRaceStarts": 0,
                    "totalSprintRaceWins": 0,
                    "totalDriverOfTheDay": 0,
                    "totalGrandSlams": 0
                }
            elif file_type == "Costruttori":
                example = {
                    "id": f"nuovo-costruttore-{len(data)+1}",
                    "name": f"Nuovo Costruttore {len(data)+1}",
                    "fullName": f"Nuovo Costruttore Racing {len(data)+1}",
                    "countryId": "italy",
                    "bestChampionshipPosition": 0,
                    "bestStartingGridPosition": 0,
                    "bestRaceResult": 0,
                    "bestSprintRaceResult": None,
                    "totalChampionshipWins": 0,
                    "totalRaceEntries": 0,
                    "totalRaceStarts": 0,
                    "totalRaceWins": 0,
                    "total1And2Finishes": 0,
                    "totalRaceLaps": 0,
                    "totalPodiums": 0,
                    "totalPodiumRaces": 0,
                    "totalPoints": 0,
                    "totalChampionshipPoints": 0,
                    "totalPolePositions": 0,
                    "totalFastestLaps": 0,
                    "totalSprintRaceStarts": 0,
                    "totalSprintRaceWins": 0
                }
            else:  # Risultati Gare
                example = {
                    "raceId": 1150,
                    "year": 2026,
                    "round": 25,
                    "positionDisplayOrder": 1,
                    "positionNumber": 1,
                    "positionText": "1",
                    "driverNumber": "1",
                    "driverId": "max-verstappen",
                    "constructorId": "red-bull",
                    "engineManufacturerId": "honda",
                    "tyreManufacturerId": "pirelli",
                    "sharedCar": False,
                    "laps": 58,
                    "time": "1:30:00.000",
                    "timeMillis": 5400000,
                    "timePenalty": None,
                    "timePenaltyMillis": None,
                    "gap": "0",
                    "gapMillis": 0,
                    "gapLaps": 0,
                    "interval": None,
                    "intervalMillis": None,
                    "reasonRetired": None,
                    "points": 25,
                    "polePosition": True,
                    "qualificationPositionNumber": 1,
                    "qualificationPositionText": "1",
                    "gridPositionNumber": 1,
                    "gridPositionText": "1",
                    "positionsGained": 0,
                    "pitStops": 2,
                    "fastestLap": True,
                    "driverOfTheDay": True,
                    "grandSlam": True
                }
            
            st.session_state.example_json = json.dumps(example, indent=2, ensure_ascii=False)
            st.rerun()
    
    with col2:
        add_records = st.button("➕ Aggiungi record", type="primary", use_container_width=True)
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.example_json = ""
            st.rerun()
    
    # Usa l'esempio se presente in session_state
    if 'example_json' in st.session_state:
        json_input = st.text_area(
            "Incolla i dati JSON qui:",
            value=st.session_state.example_json,
            height=300
        )
    
    if add_records and json_input:
        try:
            # Prova a parsare il JSON
            new_data = json.loads(json_input)
            
            # Controlla se è un singolo oggetto o un array
            if isinstance(new_data, dict):
                new_records = [new_data]
            elif isinstance(new_data, list):
                new_records = new_data
            else:
                st.error("Il JSON deve essere un oggetto o un array di oggetti")
                new_records = []
            
            if new_records:
                # Validazione dei campi obbligatori
                invalid_records = []
                valid_records = []
                
                for i, record in enumerate(new_records):
                    missing_fields = []
                    for field in schema["fields"]:
                        if field.get("required", False):
                            field_name = field["name"]
                            if field_name not in record or record[field_name] == "":
                                missing_fields.append(field_name)
                    
                    if missing_fields:
                        invalid_records.append({
                            "index": i,
                            "record": record,
                            "missing_fields": missing_fields
                        })
                    else:
                        valid_records.append(record)
                
                if invalid_records:
                    st.error(f"{len(invalid_records)} record hanno campi obbligatori mancanti:")
                    for invalid in invalid_records:
                        st.write(f"Record {invalid['index']}: Mancano {', '.join(invalid['missing_fields'])}")
                
                if valid_records:
                    # Aggiungi i record validi
                    old_count = len(data)
                    data.extend(valid_records)
                    
                    # Salva nel file
                    if save_json_file(selected_file, data):
                        st.success(f"Aggiunti {len(valid_records)} nuovi record! Totale: {old_count} → {len(data)}")
                        
                        # Mostra anteprima dei record aggiunti
                        with st.expander("Anteprima dei record aggiunti"):
                            df_new = pd.DataFrame(valid_records)
                            st.dataframe(df_new, use_container_width=True)
                        
                        st.rerun()
        
        except json.JSONDecodeError as e:
            st.error(f"Errore nel parsing JSON: {str(e)}")
        except Exception as e:
            st.error(f"Errore: {str(e)}")

with tab4:
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
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    update_clicked = st.form_submit_button("Aggiorna record", use_container_width=True)
                with col2:
                    delete_clicked = st.form_submit_button("Elimina record", type="secondary", use_container_width=True)
                with col3:
                    duplicate_clicked = st.form_submit_button("Duplica record", type="secondary", use_container_width=True)
                
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
                    # Rimuovi record
                    deleted_record = data.pop(record_idx)
                    
                    if save_json_file(selected_file, data):
                        st.success("Record eliminato con successo!")
                        with st.expander("Record eliminato"):
                            st.json(deleted_record)
                        st.rerun()
                
                if duplicate_clicked:
                    # Duplica il record
                    duplicated_record = copy.deepcopy(record)
                    
                    # Modifica l'ID per evitare duplicati
                    if 'id' in duplicated_record:
                        duplicated_record['id'] = f"{duplicated_record['id']}-copy"
                    
                    if 'name' in duplicated_record:
                        duplicated_record['name'] = f"{duplicated_record['name']} (Copia)"
                    
                    # Aggiungi alla lista
                    data.append(duplicated_record)
                    
                    if save_json_file(selected_file, data):
                        st.success("Record duplicato con successo!")
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
    3. Aggiungi singoli record nella tab 'Aggiungi singolo'
    4. Aggiungi più record insieme nella tab 'Aggiungi multipli'
    5. Modifica o elimina record nella tab 'Modifica'
    
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

# Bottone per upload file JSON
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "Carica file JSON",
    type=['json'],
    help="Carica un file JSON per sostituire i dati attuali"
)

if uploaded_file is not None:
    try:
        new_data = json.load(uploaded_file)
        if st.sidebar.button(f"Sostituisci {file_type} con file caricato", type="primary"):
            # Sostituisci i dati
            data = new_data if isinstance(new_data, list) else [new_data]
            if save_json_file(selected_file, data):
                st.sidebar.success(f"Dati di {file_type} aggiornati dal file!")
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Errore nel caricamento del file: {str(e)}")
