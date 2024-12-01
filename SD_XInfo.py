import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

url = "https://raw.githubusercontent.com/SierraD/XTProject/refs/heads/main/SD_XInfo.csv"
df = pd.read_csv(url, usecols=range(1,5))

st.header(":cyclone: XTP Search Application")
st.markdown(":floppy_disk: Last updated 2024-12-01, SDean")

col1, col2 = st.columns(2)

Search_Options = col1.radio("Choose your search parameter", ("Text", "XT Page", "Keyword", "Thumbwheel"))
Activated = col2.toggle("Show help?")
if Activated == True:
    st.sidebar.subheader("Help")
    Opt = st.sidebar.radio("Please select what you would like help with:", ("Everything", "Text", "XT Page", "Keyword", "Thumbwheel"))
    
    if Opt == "Everything":
        st.sidebar.success("This application is available to quickly search all active XT pages using the search parameters: :green[Text], :green[XT Page], :green[Keyword], or :green[Thumbwheel].")
        st.sidebar.write("Each XT Page contains a list of items which are displayed, each with associated text and thumbwheels. Items may appear on multiple XT Pages, and with different text on each page. This application uses user input to search the XT Page database and return all of the information related to the search. As each thumbwheel exists within a certain system, known keywords can also be used to search for a list of all items associated with that system. Please select another help parameter for more information.")

    elif Opt == "Text":
        st.sidebar.success("Each unqiue thumbwheel has associated text within the XT Page database. The :green[Text] option takes user input and searches the database for the given text.")
        st.sidebar.write("Each XT Page reads the thumbwheels and associated text from a database, and prints the information to the page. The thumbwheel text is not always exactly written on the XT Page due to space contstraints. For example, on XT Page :blue[02], the thumbwheel text :blue[BL1A Time of Flight] appears as :blue[TOF]. As this application uses the thumbwheel text, not the display text, the input text may need to be altered depending on the item. Correct capitalization is not necessary, but attempting various text configurations is sometimes needed to find the expected result, such as :blue[Cyc] instead of :blue[Cyclotron], and :blue[AirMonitor] instead of :blue[Air Monitor].")

    elif Opt == "XT Page":
        st.sidebar.success("The :green[XT Page] option takes user input and displays all unique thumbwheels and associated text found on the specified page.")
        st.sidebar.write("Each XT Page reads the thumbwheels and associated text from a database, and prints the information to the page. Several XT Page names contain symbols, such as :blue[.], :blue[-], and :blue[/]. These can be searched as :blue[DT], :blue[MN], and :blue[SL] respectively.")

    elif Opt == "Keyword":
        st.sidebar.success("The :green[Keyword] option supplies a drop down list of all thumbwheel systems contained within the XT Page database. Each system can be selected to display a list of all thumbwheels contained within the system.")
        st.sidebar.write("The thumbwheels use shorthand notation for different systems, such as :blue[TG] for :blue[Targets], and :blue[MG] for :blue[Magnets]. All thumbwheels in the system across all XT Pages can be viewed by selecting the system of interest.")

    elif Opt == "Thumbwheel":
        st.sidebar.success("The :green[Thumbwheel] option takes user input and displays all associated information for the thumbwheel specified.")
        st.sidebar.write("To read the thumbwheel properly, the user input must include the entire thumbwheel, such as :blue[TK 733 MUX], :blue[B1 3 DIGI], etc. The information displayed includes all XT Pages on which the thumbwheel appears, as well as the keyword system, and all associated text.")

if Search_Options == "Text":
    User_Input = col1.text_input("Please enter your search here :pencil:")
    if User_Input == "":
        st.write("")
    else:
        Title_Indexes = df[df["Text"].str.contains(User_Input.upper())].index
        st.dataframe(df.loc[Title_Indexes.tolist()], width=8000)
        
elif Search_Options == "XT Page":
    User_Input = col1.text_input("Please enter your search here :pencil:")
    if User_Input == "":
        st.write("")
    else:
        XTP_Indexes = df[df["XT Page"].str.contains(User_Input.upper())].index
        st.dataframe(df.loc[XTP_Indexes.tolist()], width=8000)
        
elif Search_Options == "Keyword":
    Keys = col1.selectbox("Please choose a keyword search :books:", ("None", "Beamline 1", "Beamline 1 Vacuum", "Beamline 2A", "Beamline 2A Vacuum", "Beamline 2C", 
                                                         "Beamline 4","Beamline 4 Vacuum", "CAMAC Design", "Diagnostics", "Extra Thumbwheels", 
                                                         "Ion Source 1", "Ion Source 2", "Ion Source 2 Vacuum", "Ion Source 3", "Ion Source 3 Vacuum", 
                                                         "Ion Source 4", "Ion Source 4 Vacuum", "Ion Source 4 Laser", "ISIS Beamline", "ISIS Beamline Vacuum", 
                                                         "Magnets", "Miscellanious", "Proton Therapy", "Radio Frequency", "Secondary Beamlines", "Safety", 
                                                         "Targets", "Tank", "Tank Vacuum"))
    if Keys == "None":
        st.write("")
    else:
        Key_Indexes = df[df["Keyword"]==(Keys)].index
        st.dataframe(df.loc[Key_Indexes.tolist()], width=8000)

elif Search_Options == "Thumbwheel":
    User_Input = col1.text_input("Please enter your search here :pencil:")
    if User_Input == "":
        st.write("")
    else:
        TW_Indexes = df[df["Thumbwheel"].str.contains(User_Input.upper())].index
        st.dataframe(df.loc[TW_Indexes.tolist()], width=8000)
