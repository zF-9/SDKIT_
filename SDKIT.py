import pandas as pd 
import numpy as np
import streamlit as st 
import plotly.express as px
import matplotlib.pyplot as plt
from numpy.random import default_rng as rng
from streamlit_gsheets import GSheetsConnection

# Page config
st.set_page_config(page_title='SDKIT', layout='wide')

# DB...ish
sql = '''
SELECT 
    "BRAND",
    "MODEL",
    "SERIAL NO",
    "ASSET NO",
    "SECTION",
    "STAFF"
FROM 
    CLP
'''
conn = st.connection("gsheets", type=GSheetsConnection)

# Webapp Header
st.title("SupportDesk IT")

# Sidebar Filters
st.sidebar.title('Sidebar Filters')

# Worksheet 1 
raw_clp = conn.read(usecols=[0, 3, 6, 7, 11, 10, 2], worksheet="CLP", header_rows=1)
data_clp = pd.DataFrame(raw_clp)

# Worksheet 2
raw_dsktp = conn.read(usecols=[0, 3, 6, 7, 11, 10, 2], worksheet="DSKTP", header_rows=1)
data_dsktp = pd.DataFrame(raw_dsktp)
#data_dsktp = _dsktp.reindex(_dsktp, axis=1)

with st.sidebar: 
    
    section_clp = data_clp['SECTION'].unique()
    model_clp = data_clp['MODEL'].unique()
            
    # Create a selectbox with these unique values as options
    selected_clpsec = st.selectbox(
        'Select a Section (Laptop)',
        options=section_clp
    )

    # Create a selectbox with these unique values as options
    selected_clpmod = st.selectbox(
        'Select a Model (Laptop)',
        options=model_clp
    )

    section_dsktp = data_dsktp['SECTION'].unique()
    model_dsktp = data_dsktp['MODEL'].unique()
        
    # Create a selectbox with these unique values as options
    selected_dsktpsec = st.selectbox(
        'Select a Section (Desktop)',
        options=section_dsktp
    )

    # Create a selectbox with these unique values as options
    selected_dsktpmod = st.selectbox(
        'Select a Model (Desktop)',
        options=model_dsktp
    )

tab1, tab2, tab3, tab4 = st.tabs(["OVERVIEW", "LAPTOPs", "DESKTOPs", "TICKETs"])

with tab1:

    #test_new df 
    fil_df_sec = data_clp[data_clp.SECTION == selected_clpsec] 
    fil_df_mod = data_clp[data_clp.MODEL == selected_clpmod]

    # Section filters Table 
    st.write(selected_clpsec +' Overview')
    #dsktp_dfs = fil_df_sec['STAFF'].value_counts()
    #st.bar_chart(dsktp_dfs)
    st.dataframe(fil_df_sec) 

    # Model filters Table
    st.write(selected_clpmod + ' Overview')
    st.dataframe(fil_df_mod)

with tab2:
    # Desktop Allocation
    st.write("Desktop(s) Allocations")
    dsktp_df = data_dsktp["SECTION"].value_counts().reset_index()
    dsktp_df.columns = ['SECTION', 'QUANTITY']
    st.bar_chart(dsktp_df, x='SECTION', y='QUANTITY', color='SECTION')
    st.dataframe(dsktp_df)
    #st.bar_chart(dsktp_df.set_index('SECTION'))

with tab3:
    # Laptop Allocation
    st.write("Laptop(s) Allocation")
    clp_df = data_clp["SECTION"].value_counts().reset_index()
    clp_df.columns = ['SECTION', 'QUANTITY']
    st.bar_chart(clp_df, x='SECTION', y='QUANTITY', color='SECTION')
    st.dataframe(dsktp_df)
    #st.bar_chart(clp_df.set_index('SECTION'))

with tab4:  
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

    TYPES = [
        "BREAKDOWN",
        "MAINTENANCE",
        "REPAIR", ""
        "SUPPORT",
    ]

    st.write("CREATE NEW TICKET")
    with st.form(key="ticket_form"):
        name = st.text_input(label="NAME")
        section = st.selectbox("SECTION", options=SECTIONS, index=None)
        date = st.date_input(label="DATE")
        ticket = st.text_area(label="TICKET")
        level = st.multiselect("TYPE", options=TYPES)

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


# Desktops_overview
with st.container():
    st.write("Desktop(s)")
    print(data_dsktp.head())
    st.dataframe(data_dsktp)

# Laptops_overview
with st.container():
    st.write("Laptop(s)")
    print(data_clp.head())
    #uniq = [data_clp['MODEL'].unique() for BRAND in data_clp.columns]
    #print(uniq)
    st.dataframe(raw_clp)    



