""" This file is part of the XTProject software
    File author(s): Sierra Dean <ccnd@live.com>
    source: https://github.com/SierraD/XTProject
    Last Updated: February 02 2025

    Added the ability to search TWs with commas included
"""

import pandas as pd
import streamlit as st

# Configure the page, with headings and layout columns
st.set_page_config(layout="wide")
st.header(":cyclone: XTP Search Application")
st.markdown(":floppy_disk: Last updated 2025-02-02, SDean")
col1, col2 = st.columns(2)
col3, col4 = col2.columns(2)

# Add a toggle for the help walktrhough and interactive table formatting
col1.success("A TRIUMF DCR XT Search")
opt = col3.toggle("Change table formatting")
sidebar = col4.toggle("Need help?")

# Display the help walkthrough
if sidebar == True:
    st.sidebar.info("This application is available to search all X data with various parameters, allowing for a large degree of freedom for your search. Please note that letter casing is arbitrary.")
    st.sidebar.subheader("Lets try it:")
    st.sidebar.write("Type the following XT Page number into the search bar to see all the unique thumbwheels on that page. This search will also show other pages the thumbwheel is on, and any associated scans.")
    st.sidebar.button("Type: 2P")
    st.sidebar.write("On that XT Page we can see the Aluminum Active LCW tank level. Try to search for that thumbwheel to get more information.")
    st.sidebar.button("Type: MS 232 MUX")
    st.sidebar.write("If you want to search a Scan, Scan Element, or Scan Variable output from the message reader, type SCAN before your search. This will open two new prompts next to the search bar, ELEMENT and VARIABLE. The ELEMENT option will show you the info only for that element. If the element is unknown, the variable printed before the scan name on the message reader can also be searched. ")
    st.sidebar.button("Type: SCAN MS")
    st.sidebar.button("Enter ELEMENT: 46")
    st.sidebar.warning("Reset the ELEMENT or the VARIABLE to 0 to perform the alternate search.")
    st.sidebar.button("Enter VARIABLE: 75120")
    st.sidebar.write("Lastly, if you dont know the page, thumbwheel, or scan for your search, just type associated words to find all associated information.")
    st.sidebar.button("Type: LCW")

# Add a user-defined text search
User_Input = col1.text_input("Please enter your search here :pencil:", value="", key="A")

# Open and read the XTP data
url = "https://raw.githubusercontent.com/SierraD/XTProject/refs/heads/main/XTP_2025.csv"
XTP_df = pd.read_csv(url)
XTP_df["Scan Element"] = XTP_df["Scan Element"].fillna("[]").apply(lambda x: eval(x))
XTP_df["Scan Element"] = XTP_df["Scan Element"].tolist()
# XTP_df has Scan Elements as a list to be used in the search, XTP_readable has them as a string for easier visibility 
XTP_readable = pd.DataFrame(XTP_df)
XTP_readable["Scan Element"] = XTP_df["Scan Element"]
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].astype(str)
XTP_readable["XT Page"] = XTP_df["XT Page"]
XTP_df["XT Page"] = XTP_df["XT Page"].str.replace(" ", "")
XTP_df["XT Page"] = XTP_df["XT Page"].str.split(",")

# Open and read the Scan data
url2 = "https://raw.githubusercontent.com/SierraD/XTProject/refs/heads/main/SCNS_2025.csv"
SCNS_df = pd.read_csv(url2, usecols=["Scan", "Element", "On Action", "DO MESSAGE", "DO OFF Command", "DO WRITE Command", "DO INSERT Command", 
                                     "DO CALC Command", "DO LOG Command", "I/L Statement", "CCS Message"])
All_Scans = ["None"]
All_Scans = All_Scans + (SCNS_df["Scan"].unique().tolist())

# Format XTP_readable for visibility
XTP_readable["Scan"] = XTP_readable["Scan"].str.replace("[", "")
XTP_readable["Scan"] = XTP_readable["Scan"].str.replace("]", "")
XTP_readable["Scan"] = XTP_readable["Scan"].str.replace("'", "")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("[['", "")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("['", "")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("',", ":")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("]]", "")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("]", "")
XTP_readable["Scan Element"] = XTP_readable["Scan Element"].str.replace("[", "N/A")
XTP_readable = XTP_readable.fillna('N/A')

# SCNS_df has Scan Elements as a list to be used in the search, SCNS_readable has them as a string for easier visibility
SCNS_readable = SCNS_df
SCNS_readable = SCNS_readable.fillna('N/A')
SCNS_readable["CCS Message"] = SCNS_readable["CCS Message"].str.replace("-", "N/A")

# Output the search outcomes depending on the user input
if User_Input != "":
    if "," in User_Input:
        User_Input = User_Input.replace(",", " ")
    TW_Result = XTP_df[XTP_df["Thumbwheel"]==(User_Input.upper())].index
    XT_Result = XTP_df[[User_Input.upper() in x for x in XTP_df["XT Page"]]].index
    Scan_Result = False
    # Determing if the user wants to search for a scan
    if "SCAN" in User_Input.upper():
        Scan_Result = True
    # Determine if the user wants to search for an XT Page 
    if len(XT_Result) > 0:
        st.success("Showing results for XT Page "+User_Input)
        # Display all results for that XT Page
        XT_df = XTP_readable.iloc[XT_Result]
        if opt == True:
            st.dataframe(XT_df, hide_index=True, width=8000)
        else:
            st.table(XT_df)
    # Determine if the user wants to search for a Thumbwheel
    elif len(TW_Result) == 1:
        st.success("Showing results for Thumbwheel "+User_Input)
        TW_df = XTP_readable.iloc[TW_Result]
        # Display all XT Page results for the Thumbwheel
        if opt == True:
            st.dataframe(TW_df, hide_index=True, width=8000)
        else:
            st.table(TW_df)
        TW_df["XT Page"] = TW_df["XT Page"].astype(str)
        st.success("Showing results for Scan Elements for "+User_Input)
        # Obtain all scan results for the thumbwheel
        Scan_Inf = pd.DataFrame()
        for i in range(0, len(XTP_df["Scan Element"][TW_df.index[0]])):
            for j in range (1, len(XTP_df["Scan Element"][TW_df.index[0]][i])):
                scan_ind = SCNS_readable[SCNS_readable["Scan"]==XTP_df["Scan Element"][TW_df.index[0]][i][0]].index
                el_ind = SCNS_readable[SCNS_readable["Element"]==XTP_df["Scan Element"][TW_df.index[0]][i][j]].index
                scan_info = list(set(scan_ind).intersection(set(el_ind)))
                if len(scan_info) != 0:
                    Scan_Inf = pd.concat([Scan_Inf, SCNS_readable[scan_info[0]:scan_info[0]+1]])                    
        # Display all scan results for the thumbwheel
        if opt == True:
            st.dataframe(Scan_Inf, hide_index=True, width=8000)
        else:
            st.table(Scan_Inf)
    # If it has been determined that the user wants to search for a scan
    elif Scan_Result == True:
        st.success("Showing results for "+User_Input)
        # Include the option for the user to add a scan element or variable
        element = col3.number_input("Insert an element", value=0)
        scan_num = col4.number_input("Insert a scan variable", value=0)
        a = User_Input.upper().replace("SCAN ", "")
        # Obtain all scan results
        Scan_Result = SCNS_readable[SCNS_readable["Scan"]==(a)].index
        SC_df = SCNS_readable.iloc[Scan_Result]
        # Obtain all element results
        if element != 0:
            Element_Result = SC_df[SC_df["Element"]==(element)].index
            # Display all element results
            if opt == True:
                st.dataframe(SCNS_readable[Element_Result[0]:Element_Result[0]+1], hide_index=True, width=8000)
            else:
                st.table(SCNS_readable[Element_Result[0]:Element_Result[0]+1])
        # Obtain all variable results
        elif scan_num!= 0:
            Scan_Vars = pd.DataFrame()
            Num_Result = SCNS_readable[SCNS_readable["DO MESSAGE"].str.contains(str(scan_num))].index
            scan_indexes = list(set(Scan_Result).intersection(set(Num_Result)))
            for k in scan_indexes:
                Scan_Vars = pd.concat([Scan_Vars, SCNS_readable[k:k+1]])
            # Display all variable results
            if opt == True:
                st.dataframe(Scan_Vars, hide_index=True, width=8000)
            else:
                st.table(Scan_Vars)
        else:
            # Display all scan results if element and variable not specified
            if opt == True:
                st.dataframe(SC_df, hide_index=True, width=8000)
            else:
                st.table(SC_df)
    # Determine if the user wants to search for associated text
    else:
        Title_Result = XTP_df[XTP_df["Text"].str.contains(User_Input.upper())].index
        Title_df = XTP_readable.iloc[Title_Result]
        # Display all associated results
        if opt == True:
            st.dataframe(Title_df, hide_index=True, width=8000)
        else:
            st.table(Title_df)
