import time
start = time.time()
import os
import subprocess
import pandas as pd
import streamlit as st

st.title ("BLAST Gene Presence Screener")

placeholder = st.empty()
uploaded = placeholder.file_uploader ("Upload query gene here")

if uploaded is not None:
    placeholder.empty()
    with st.spinner("Running BLAST..."):
        with open ("gene.fna", "wb") as w:
            w.write(uploaded.getvalue())

        def get_gc_content(filename):
            with open(filename , "r") as f:
                d = {}

                for line in f:
                    if line[0] == ">":
                        current_title = line.strip()[1:]
                        d[current_title] = []

                    
                    else:
                        DNA = line.strip()
                        d[current_title].append(DNA) # we stored DNA, in the dictrionary key

            for key in d:
                d[key] = "".join(d[key])

                L = len(d[key])
                count = d[key].count("G") + d[key].count("C")
                gc = count/L *100
                d[key] = gc
                    
            return d


        gc_content = {}
        genome_files = os.listdir()
        for genome_file in genome_files:
            if genome_file.endswith(".fna") and genome_file != "gene.fna":
                gc_content[genome_file] = get_gc_content(genome_file)

        def blastnquery():
            for genome_file in genome_files:
                if genome_file.endswith(".fna") and genome_file != "gene.fna":
                    db = genome_file.split(".")[0] + "_db"
                    results = genome_file.split(".")[0] + "_results.txt"

                    if os.path.exists(db + ".nhr") and os.path.getmtime (genome_file) < os.path.getmtime (db + ".nhr"):
                        pass

                    else: 
                        subprocess.run (["makeblastdb", "-in", genome_file, "-dbtype", "nucl", "-out", db])

                    subprocess.run (["blastn", "-query", "gene.fna", "-db", db ,"-outfmt", "6", "-out", results])

        blastnquery()

        def build_tally():
            tally = {}
            identity = {}
            for genome_file in genome_files:
                if genome_file.endswith(".fna") and genome_file != "gene.fna":
                    results = genome_file.split(".")[0] + "_results.txt"
                    with open (results, "r") as f: 
                        lines = f.readlines()
                        hit_count = len(lines)

                        if hit_count >= 1:
                            firstline = lines[0].split("\t")
                            identity[firstline[1]] = firstline[2]
                            for line in lines:
                                field = line.split("\t")
                                tally[field[1]] = tally.get(field [1], 0) + 1
                            
            return tally, identity


        def results_reading():
            table = {}
            tally, identity = build_tally()

            for genome_file in genome_files: 
                if genome_file.endswith(".fna") and genome_file != "gene.fna":
                        for headers, gc in gc_content[genome_file].items():
                            replicon = headers.split(" ")[0]
                            hits = tally.get(replicon, 0)
                            best_identity = identity.get(replicon, "n/a")

                            if "plasmid" in headers.lower():
                                rep = "plasmid"
                            elif "chromosome" in headers.lower() or "complete genome" in headers.lower():
                                rep = "chromosome"
                            else: 
                                rep = "contig/unkown"
                            table[replicon] = {"replicon type": rep, "GC%": gc, "hitcount": hits, "best identity%": best_identity}

            return table
        table = results_reading()
        pf = pd.DataFrame.from_dict (table, orient="index")
        pf.index.name = "replicon"
        st.dataframe (pf)
        print(time.time() - start)


