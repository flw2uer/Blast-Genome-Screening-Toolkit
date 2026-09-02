# Blast-Genome-Screening-Toolkit
A Streamlit web app for monitoring BLAST search results and tracking failed genome sequences.
Supported Files: This tool exclusively uses .fna (FASTA) files, but supports both GCA (GenBank) and GCF (RefSeq) assemblies.

## Requirements 
To run this this tool, you will need python installed on your computer, along with the following packages -  

**1. Install Homebrew (if you don't have it)**
Homebrew is a package manager that makes installing bioinformatics tools much easier.
Go to https://brew.sh/ and follow the instructions.

**2. Install the packages needed (if you don't have it)**

**To install Streamlit or Pandas**
type in the below command within terminal or command prompt.
pip install streamlit
pip install pandas

##if this doesn't work, try replacing pip with pip3.

**To install Blast**
type in the below command in the terminal or command prompt
brew install blast 

This script has been stress-tested locally using 1,171 complete genome .fna files in a single run. It successfully parsed the files, monitored the BLAST outputs, and generated the final error table without crashing or memory issues #(using about 12-19 gbs of ram), see the uploaded CSV for the exact output. 
<img width="1124" height="498" alt="Screenshot 2026-09-02 at 17 18 15" src="https://github.com/user-attachments/assets/e0ac869c-a49e-48cb-867b-6db434ab6b55" />

