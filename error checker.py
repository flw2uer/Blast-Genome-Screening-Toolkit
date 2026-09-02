import os
import streamlit as st
import pandas as pd

genome_files = os.listdir()
positive = 0
error_data = []

st.title ("error checker")

for genome_file in genome_files:
        if genome_file.endswith(".fna") and genome_file != "gene.fna":
            results = genome_file.split(".")[0] + "_results.txt" 

            if os.path.exists(results) != True:
             Status = "error"
             error_data.append({"genome failed": genome_file, "Status": Status})


            elif os.path.exists(results) == True:
                positive += 1


st.subheader (f"Successul queries - {positive}")
if error_data == {}:
            st.write (f"No failed searches - every genome has a result file.")


else: 
    ed = pd.DataFrame(error_data)
    st.dataframe (ed)