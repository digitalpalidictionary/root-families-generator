#!/usr/bin/env python3.10
# coding: utf-8

import pandas as pd
import re
from datetime import date
import warnings
from datetime import datetime

def timeis():
	global blue
	global yellow
	global green
	global red
	global white

	blue = "\033[38;5;33m" #blue
	green = "\033[38;5;34m" #green
	red= "\033[38;5;160m" #red
	yellow = "\033[38;5;220m" #yellow
	white = "\033[38;5;251m" #white
	now = datetime.now()
	current_time = now.strftime("%Y-%m-%d %H:%M:%S")
	return (f"{blue}{current_time}{white}")

print(f"{timeis()} {yellow}root families generator")
print(f"{timeis()} ----------------------------------------")

today = date.today()
date = today.strftime("%d")

warnings.simplefilter(action='ignore', category=FutureWarning)

def sort_key(word):

    pāli_alphabet = [
        "√", "a", "ā", "i", "ī", "u", "ū", "e", "o", "k", "kh", "g", "gh", "ṅ",
        "c", "ch", "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍḥ", "ṇ", "t", "th", "d",
        "dh", "n", "p", "ph", "b", "bh", "m", "y", "r", "l", "s", "v", "h",
        "ḷ", "ṃ", " ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
	]

    #comp iteration condition
    dl = [i for i in pāli_alphabet if len(i) > 1]

    for i in dl:
        word = word.replace(i, '/{}'.format(i))

    wordVe = []

    k = -3

    for j in range(len(word)):
        if word[j] == '/':
            k = j
            wordVe.append(word[j + 1:j + 3])
        if j > k + 2:
            wordVe.append(word[j])

    word = wordVe

    pāli_alphabet_string = '-'.join(pāli_alphabet)
    return [pāli_alphabet_string.find('-' + x + '-') for x in wordVe]

def setup_roots_df():
	print(f"{timeis()} {green}setting up roots dataframe") 

	global roots_df
	global roots_df_count

	roots_df = pd.read_csv("../csvs/roots.csv", sep="\t", dtype=str)
	roots_df.fillna("", inplace=True)

	roots_df = roots_df[roots_df["Count"] != "0"] # remove roots with no examples
	roots_df = roots_df[roots_df["Fin"] != ""] # remove extra iines
	roots_df.sort_values(by = ["Root"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key)) #sort
	roots_df["Dhātupātha"] = roots_df["Dhātupātha"].str.replace("-", "")
	roots_df["Kaccāyana Dhātu Mañjūsā"] = roots_df["Kaccāyana Dhātu Mañjūsā"].str.replace("-", "")

	roots_df_count = roots_df.shape[0]


def setup_dpd_df():
	print(f"{timeis()} {green}setting up dpd dataframe") 

	global dpd_df

	dpd_df = pd.read_csv("../csvs/dpd-full.csv", sep="\t", dtype=str)
	dpd_df.fillna("", inplace=True)
	dpd_df.loc[dpd_df["Meaning IN CONTEXT"] == "", "Meaning IN CONTEXT"] = dpd_df["Buddhadatta"] + "*"

def setup_root_families_df():
	print(f"{timeis()} {green}setting up root families dataframe") 

	global root_families_df
	global root_families_df_count
	 
	test1 = dpd_df["Family"] != ""
	test2 = dpd_df["Metadata"] == ""
	filter = test1 & test2
	root_families_df = dpd_df.loc[filter, ["Pāli Root", "Grp", "Root Meaning", "Family"]]

	root_families_df = root_families_df.drop_duplicates(subset=["Pāli Root", "Grp", "Root Meaning", "Family"])
	root_families_df.sort_values(["Pāli Root", "Grp", "Root Meaning", "Family"], ascending = (True, True, True, True), inplace=True)
	root_families_df.sort_values(by = ["Family"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key)) #sort
	root_families_df = root_families_df.reset_index(drop=True)

	root_families_df_count = root_families_df.shape[0]

def generate_root_subfamily_html():
	print(f"{timeis()} {green}generating html for each root subfamily")

	for row in range(root_families_df_count):

		root = root_families_df.loc[row, "Pāli Root"]
		root_group = root_families_df.loc[row, "Grp"]
		root_meaning = root_families_df.loc[row, "Root Meaning"]
		subfamily = root_families_df.loc[row, "Family"]

		if row % 500 == 0 or row /  root_families_df_count == 1:
			print(f"{timeis()} {row}/{root_families_df_count}\t{subfamily} {root_group} {root_meaning}")

		# dpd_df.columns
		test1 = dpd_df["Pāli Root"] == root
		test2 = dpd_df["Grp"] == root_group
		test3 = dpd_df["Root Meaning"] == root_meaning
		test4 = dpd_df["Family"] == subfamily
		filter = test1 & test2 & test3 & test4
		subfamily_df = dpd_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT", "Literal Meaning"]]
		subfamily_df_length = subfamily_df.shape[0]

		html_string = ""
		html_string += """<tbody>"""
			
		for row_sf in range(subfamily_df_length):
			sf_pali = subfamily_df.iloc[row_sf, 0]
			sf_pos = subfamily_df.iloc[row_sf, 1]
			sf_english = subfamily_df.iloc[row_sf, 2]
			sf_literal = subfamily_df.iloc[row_sf, 3]

			html_string += f"<tr><th>{sf_pali}</th>"
			html_string += f"<td>{sf_pos}</td>"
			html_string += f"<td>{sf_english}"
			
			if sf_literal == "":
				html_string +=  f"</td></tr>"
			if sf_literal != "":
				html_string += f"; lit. {sf_literal}</td></tr>"

		html_string += f"""</tbody>"""

		with open(f"output/subfamily html/{root} {root_group} {root_meaning} {subfamily}.html", "w") as output_file:
			output_file.write(html_string)

def extract_bases():

	print(f"{timeis()} {green}extracting bases")

	bases_df = dpd_df
	bases_dict = {}

	for row in range(roots_df_count):
		root = roots_df.iloc[row, 2]
		root_group = roots_df.iloc[row, 5]
		root_meaning = roots_df.iloc[row, 8]

		test1 = bases_df["Pāli Root"] == root
		test2 = bases_df["Grp"] == root_group
		test3 = bases_df["Root Meaning"] == root_meaning
		test4 = bases_df["Base"].str.contains(fr">")
		filter = test1 & test2 & test3 & test4
		bases_filtered = bases_df.loc[filter, ["Base"]]

		bases_filtered = bases_filtered.dropna()
		bases_filtered = bases_filtered.sort_values(by="Base", key=lambda x: x.str.len())
		bases_filtered = bases_filtered["Base"].str.replace("^.+ > ", "")
		bases_filtered.drop_duplicates(inplace=True, keep="first")
		
		bases_filtered_size = bases_filtered.shape[0]

		if row % 100 == 0:
			print(f"{timeis()} {row}/{roots_df_count}\t{root} {root_group} {root_meaning}")

		with open(f"output/bases/{root} {root_group} {root_meaning}.csv", "w") as output_file:
			bases_filtered_size = bases_filtered.shape[0]

			if bases_filtered_size == 0:
				output_file.write(f"-")
			if bases_filtered_size > 0:
				bases_filtered.to_csv(output_file, header=False, index=False, sep="\t")

def generate_root_families_csvs():
	print(f"{timeis()} {green}generating root families csvs")

	root_families_df = dpd_df

	for row in range(roots_df_count):
		root = roots_df.iloc[row, 2]
		root_group = roots_df.iloc[row, 5]
		root_meaning = roots_df.iloc[row, 8]

		test1 = root_families_df["Pāli Root"] == root
		test2 = root_families_df["Root Meaning"] == root_meaning
		test3 = root_families_df["Grp"] == root_group
		filter = test1 & test2 & test3
		root_families_filtered = root_families_df.loc[filter, ["Family"]]
		root_families_filtered.drop_duplicates("Family", inplace=True, keep='first')

		root_families_filtered.sort_values(by = ["Family"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key)) #sort

		with open(f"output/families/{root} {root_group} {root_meaning}.csv", "w") as output_file:
			root_families_filtered.to_csv(output_file, header=False, index=False, sep="\t")

def generate_root_info_html():

	print(f"{timeis()} {green}writing root info")

	for row in range(roots_df_count):
		root = roots_df.iloc[row, 2]
		root_in_comps = roots_df.iloc[row, 3]
		root_has_verb = roots_df.iloc[row, 4]
		root_group = roots_df.iloc[row, 5]
		root_sign = roots_df.iloc[row, 6]
		root_meaning = roots_df.iloc[row, 8]

		base_file = open(f"output/bases/{root} {root_group} {root_meaning}.csv")
		base = base_file.read()
		base_file.close()
		base = re.sub("\n", ", ", base)
		base = re.sub(", $", "", base)

		sk_root = roots_df.iloc[row, 9]
		sk_root_meaning = roots_df.iloc[row, 10]
		sk_root_class = roots_df.iloc[row, 11]
		example = roots_df.iloc[row, 12]
		dhp_no = roots_df.iloc[row, 13]
		dhp_root = roots_df.iloc[row, 14]
		dhp_meaning = roots_df.iloc[row, 15]
		dhp_english = roots_df.iloc[row, 16]
		dhm_no = roots_df.iloc[row, 17]
		dhm_root = roots_df.iloc[row, 18]
		dhm_meaning = roots_df.iloc[row, 19]
		dhm_english = roots_df.iloc[row, 20]
		sdn_root = roots_df.iloc[row, 21]
		sdn_meaning = roots_df.iloc[row, 22]
		sdn_english = roots_df.iloc[row, 23]
		pdp_root = roots_df.iloc[row, 24]
		pdp_meaning = roots_df.iloc[row, 25]
		pdp_english = roots_df.iloc[row, 26]
		notes = roots_df.iloc[row, 27]

		if str(root_group) == "1":
			root_group_pali = "bhūvādigaṇa"
		if str(root_group) == "2":
			root_group_pali = "rudhādigaṇa"
		if str(root_group) == "3":
			root_group_pali = "divādigaṇa"
		if str(root_group) == "4":
			root_group_pali = "svādigaṇa"
		if str(root_group) == "5":
			root_group_pali = "kiyādigaṇa"
		if str(root_group) == "6":
			root_group_pali = "gahādigaṇa"
		if str(root_group) == "7":
			root_group_pali = "tanādigaṇa"
		if str(root_group) == "8":
			root_group_pali = "curādigaṇa"

		html_string = ""
		html_string += f"""<tbody>"""
		html_string += f"""<tr><th>Pāḷi Root:</th><td>{root}<sup>{root_has_verb}</sup>{root_group} {root_group_pali} +{root_sign} ({root_meaning})</td></tr>"""
		html_string += f"""<tr><th>Base(s):</th><td>{base}</td></tr>"""

		# Root in comps
		if root_in_comps != "":
			html_string += f"""<tr><th>Root in Compounds:</th><td>{root_in_comps}</td></tr>"""
		else:
			pass

		# Dhātupātha
		if dhp_root != "-":
			html_string += f"""<tr><th>Dhātupātha:</th><td>{dhp_root} <i>{dhp_meaning}</i> ({dhp_english}) #{dhp_no}</td></tr>"""
		else:
			html_string += f"""<tr><th>Dhātupātha:</th><td>-</td></tr>"""

		# Dhātumañjūsa
		if dhm_root != "-":
			html_string += f"""<tr><th>Dhātumañjūsa:</th><td>{dhm_root} <i>{dhm_meaning}</i> ({dhm_english}) #{dhm_no}</td></tr>"""
		else:
			html_string += f"""<tr><th>Dhātumañjūsa:</th><td>-</td></tr>"""

		# Saddanīti
		if sdn_root != "-":
			html_string += f"""<tr><th>Saddanīti:</th><td>{sdn_root} <i>{sdn_meaning}</i> ({sdn_english})</td></tr>"""
		else:
			html_string += f"""<tr><th>Saddanīti:</th><td>-</td></tr>"""

		# Sanskrit
		html_string += f"""<tr><th>Sanskrit Root:</th><td style = 'color:gray'>{sk_root} {sk_root_class} ({sk_root_meaning})</td></tr>"""

		# Pāṇinīya Dhātupāṭha
		if pdp_root != "-":
			html_string += f"""<tr><th>Pāṇinīya Dhātupāṭha:</th><td style = 'color:gray'>{pdp_root} <i>{pdp_meaning}</i> ({pdp_english})</td></tr>"""
		else:
			html_string += f"""<tr><th>Pāṇinīya Dhātupāṭha:</th><td>-</td></tr>"""

		html_string += f"""</tbody>"""

		with open(f"output/root info/{root} {root_group} {root_meaning}.html", "w") as output_file:
			output_file.write(html_string)

def generate_root_families_csv_for_anki():

	print(f"{timeis()} {green}generating root families csv for anki")

	#combine meaning and buddhadatta columns
    
	anki_df = dpd_df
	
	anki_df["Buddhadatta"] = anki_df["Buddhadatta"].str.replace("(.+)", "<div style='color: #AA4400'>\\1<div>")
	anki_df.loc[anki_df["Meaning IN CONTEXT"].isnull(), "Meaning IN CONTEXT"] = anki_df["Buddhadatta"]
	anki_df["Construction"] = anki_df["Construction"].str.replace("(.+)\n.+", "\\1")

    #writing root families for anki.csv
	txt_file = open ("../csvs for anki/root families.csv", 'w', encoding= "'utf-8")

	for row in range (0, root_families_df_count):
		root = root_families_df.iloc[row, 0]
		root_group = (root_families_df.iloc[row, 1])
		root_meaning = root_families_df.iloc[row, 2]
		root_family = root_families_df.iloc[row, 3]
		
		if row % 500 == 0:
			print(f"{timeis()} {row}/{root_families_df_count}\t{root} {root_group} {root_meaning} {root_family}")
        
		test1 = ~anki_df["Pāli Root"].isnull()
		test2 = anki_df["Pāli Root"] == (root)
		test3 = anki_df["Grp"] == (root_group)
		test4 = anki_df["Root Meaning"] == (root_meaning)
		test5 = anki_df["Family"] == (root_family)
		filter = test1 & test2 & test3 & test4 & test5
		filtered_df = anki_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT", "Construction"]]

		with open("../csvs for anki/root families.csv", 'a') as txt_file:
			txt_file.write(f"<b>{root_family}</b> {root_group} ({root_meaning})\t")
			txt_file.write(f"<table><tbody>")
			for row in range(filtered_df.shape[0]):
				pāli = filtered_df.iloc[row, 0]
				pos = filtered_df.iloc[row, 1]
				meaning = filtered_df.iloc[row, 2]
				construction = filtered_df.iloc[row, 3]
				construction = re.sub(f"<br/>.+",  "", construction) #remove 2nd line
				txt_file.write(f"<tr valign='top'><div style='color: #FFB380'><td>{pāli}</td><td><div style='color: #FF6600'>{pos}</div></td><td><div style='color: #FFB380'>{meaning}</td><td><div style='color: #AA4400'>{construction}</div></td></tr>")
			txt_file.write(f"</tbody></table>")
			txt_file.write(f"\t{date}")
			txt_file.write(f"\n")


setup_roots_df()
setup_dpd_df()
setup_root_families_df()
generate_root_subfamily_html()
extract_bases()
generate_root_families_csvs()
generate_root_info_html()
generate_root_families_csv_for_anki()

print(f"{timeis()} ----------------------------------------")