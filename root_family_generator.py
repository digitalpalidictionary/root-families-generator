#!/usr/bin/env python3.10
# coding: utf-8

import logging
import pandas as pd

#setup logger
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')

#import dpd csv as dataframe
logging.warning(f"opening Pāli English Dictionary.csv as data frame")
csv_file = "/home/bhikkhu/Bodhirasa/Dropbox/Pāli English Dictionary/Pāli English Dictionary.csv"
df = pd.read_csv (csv_file, sep="\t")

#combine meaning and buddhadatta columns
df.loc[df["Meaning IN CONTEXT"].isnull(), "Meaning IN CONTEXT"] = "*" + df["Buddhadatta"]

# extract root families
logging.warning("extracting root family names")

root_family_list = df[~df["Family"].isnull()]
root_family_list = root_family_list[~root_family_list["Pāli1"].str.contains("Help", "Abbreviations")]
root_family_list = root_family_list[["Pāli Root", "Grp", "Root Meaning", "Family"]]
root_family_list = root_family_list.drop_duplicates(subset=["Pāli Root", "Grp", "Root Meaning", "Family"])
root_family_list.sort_values(["Pāli Root", "Grp", "Root Meaning", "Family"], ascending = (True, True, True, True), inplace=True)
root_family_list = root_family_list.reset_index(drop=True)

# write families
logging.warning(f"writing root_families_list.csv")
root_family_list.to_csv("root_families_list.csv", sep="\t")

# row count
root_families_count = root_family_list.shape[0]
logging.warning(f"root_families_count = {root_families_count}")

yn = input("for (s)tudents of (d)pd? ")
if yn == "s":

    #writing root_families_study.csv
    logging.warning ("writing root_families_study.csv")
    txt_file = open ("root_families_study.csv", 'w', encoding= "'utf-8")
    txt_file.write(f"Family\tGrp\tRoot Meaning\tPāli\tConstruction\tPOS\tMeaning\n")

    logging.warning ("~" *40)
    row =0

    for row in range (0, root_families_count):
        root = root_family_list.iloc[row, 0]
        root_group = (root_family_list.iloc[row, 1]).astype(int)
        root_meaning = root_family_list.iloc[row, 2]
        root_family = root_family_list.iloc[row, 3]

        if row % 100 == 0:
            logging.warning (f"{row} {root} {root_group} {root_meaning} {root_family}")

        test1 = ~df["Pāli Root"].isnull()
        test2 = df["Pāli Root"] == (root)
        test3 = df["Grp"] == (root_group).astype(int)
        test4 = df["Root Meaning"] == (root_meaning)
        test5 = df["Family"] == (root_family)

        filter = test1 & test2 & test3 & test4 & test5
        filtered_df = df.loc[filter, ["Family", "Grp", "Root Meaning", "Pāli1", "Construction", "POS", "Meaning IN CONTEXT"]]

        with open("root_families_study.csv", 'a') as txt_file:
            txt_file.write (f"~~~~~~~~~~\n")
            # txt_file.write (f"{root_family}\n")
            filtered_df.to_csv(txt_file, header=False, index=False, sep="\t")

if yn == "d":
    #writing root_families_dpd.csv
    logging.warning ("writing root_families_dpd.csv")
    txt_file = open ("root_families_dpd.csv", 'w', encoding= "'utf-8")

    logging.warning ("~" *40)
    row =0

    for row in range (0, root_families_count):
        root = root_family_list.iloc[row, 0]
        root_group = (root_family_list.iloc[row, 1]).astype(int)
        root_meaning = root_family_list.iloc[row, 2]
        root_family = root_family_list.iloc[row, 3]

        if row % 100 == 0:
            logging.warning (f"{row} {root} {root_group} {root_meaning} {root_family}")
        
        test1 = ~df["Pāli Root"].isnull()
        test2 = df["Pāli Root"] == (root)
        test3 = df["Grp"] == (root_group).astype(int)
        test4 = df["Root Meaning"] == (root_meaning)
        test5 = df["Family"] == (root_family)

        filter = test1 & test2 & test3 & test4 & test5
        filtered_df = df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT"]]

        with open("root_families_dpd.csv", 'a') as txt_file:
            txt_file.write(f"{root_family}\t({root} {root_group} {root_meaning})\n")
            filtered_df.to_csv(txt_file, header=False, index=False, sep="\t")
            txt_file.write(f"\n")


logging.warning(f"fin")