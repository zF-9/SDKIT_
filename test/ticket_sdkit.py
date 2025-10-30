import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("test ticket")
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="TICKET", usecols=list(range(5)), ttl=5) 
existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)

# List Sections
SECTIONS = [
    "BPA",
    "DGD",
    "BSP",
    "BPO",
    "Pej.D",
    "BKNS",
    "GNK",
    "BKP",
    "INSAN",
]

SEVERITY = [
    "BREAKDOWN",
    "MAINTENANCE",
    "REPAIR", ""
    "SUPPORT",
]

with st.form(key="ticket_form"):
    name = st.text_input(label="NAME")
    section = st.selectbox("SECTION", options=SECTIONS, index=None)
    date = st.date_input(label="DATE")
    ticket = st.text_area(label="TICKET")
    level = st.multiselect("TYPE", options=SEVERITY)

    st.markdown("**Required**")

    submit_button = st.form_submit_button(label="SUBMIT")

    if submit_button:
        #st.write("submit pressed")
        if not name or not section:
            st.warning("Please fill in the required")
            st.stop()
        #elif existing_data["STAFF"].str.contains(name).any():
        #    st.warning("name already exist")
        #    st.stop()
        else:
            #create new row data 
            new_ticket = pd.DataFrame([{
                "DATE": date.strftime("%d-%m-%Y"),
                "STAFF": name,
                "SECTION": section,
                "TICKET": ticket,
                "TYPE": ",".join(level),
            }])
            
            #appending new ticket to existing data 
            update_df = pd.concat([existing_data, new_ticket], ignore_index=True)

            #update the list in the googlesheet
            conn.update(worksheet="TICKET", data=update_df)
            st.success("Updated Successfully!")

