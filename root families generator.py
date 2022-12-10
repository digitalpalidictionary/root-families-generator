#!/usr/bin/env python3.10
# coding: utf-8

from rootmatrix import generate_root_matrix
import pandas as pd
import re
from datetime import date
import warnings
import os
import json

from timeis import timeis, yellow, line, white, green, red, blue, tic, toc
from sorter import sort_key
from delete_unused_files import del_unused_files

print(f"{timeis()} {yellow}root families generator")
print(f"{timeis()} {line}")

today = date.today()
date = today.strftime("%d")

warnings.simplefilter(action='ignore', category=FutureWarning)

def setup_roots_df():
	print(f"{timeis()} {green}setting up roots dataframe") 

	roots_df = pd.read_csv("../csvs/roots.csv", sep="\t", dtype=str)
	roots_df.fillna("", inplace=True)

	roots_df = roots_df[roots_df["Count"] != "0"] # remove roots with no examples
	roots_df = roots_df[roots_df["Fin"] != ""] # remove extra iines
	roots_df.sort_values(by = ["Root"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key)) #sort
	roots_df["Dhātupātha"] = roots_df["Dhātupātha"].str.replace("-", "")
	roots_df["Kaccāyana Dhātu Mañjūsā"] = roots_df["Kaccāyana Dhātu Mañjūsā"].str.replace("-", "")

	roots_df_count = roots_df.shape[0]

	print(f"{timeis()} {green}setting up roots matrix checklist")

	root_matrix_checklist = []

	for row in range(roots_df_count):
		count = roots_df.loc[row, 'Count']
		root = roots_df.loc[row, 'Root']
		group = roots_df.loc[row, 'Group']
		meaning = roots_df.loc[row, 'Meaning']
		matrix = roots_df.loc[row, 'matrix test']
		root_info = f"{root} {group} {meaning}"
		
		if matrix == "√": 
			root_matrix_checklist.append(root_info)
	
	# print(root_matrix_checklist)

	return roots_df, roots_df_count, root_matrix_checklist


def setup_dpd_df():
	print(f"{timeis()} {green}setting up dpd dataframe") 

	global dpd_df
	global dpd_df2

	dpd_df = pd.read_csv("../csvs/dpd-full.csv", sep="\t", dtype=str)
	dpd_df.fillna("", inplace=True)
	dpd_df2 = dpd_df.copy()

	for row in range (len(dpd_df)):
		root = dpd_df.loc[row, "Pāli Root"]
		meaning = dpd_df.loc[row, "Meaning IN CONTEXT"]
		literal = dpd_df.loc[row, "Literal Meaning"]
		source = dpd_df.loc[row, "Source1"]
		buddhadatta = dpd_df.loc[row, "Buddhadatta"]

		# add literal meaning
		if meaning != "" and literal != "":
			meaning += f"; lit. {literal}"
		
		# add word information degree of completion
		if meaning != "" and source != "":
			meaning += " <span class='g1'>●</span>"
		elif meaning != "" and source == "":
			meaning += " <span class='g2'>●</span>"
		elif meaning == "":
			meaning = buddhadatta + " <span class='g3'>●</span>"
		dpd_df.loc[row, "Meaning IN CONTEXT"] = meaning


def setup_root_families_df():
	print(f"{timeis()} {green}setting up root families dataframe") 

	global root_families_df
	global root_families_df_count
	 
	test1 = dpd_df["Family"] != ""
	root_families_df = dpd_df.loc[test1, [
		"Pāli Root", "Grp", "Root Meaning", "Family"]]

	root_families_df = root_families_df.drop_duplicates(subset=["Pāli Root", "Grp", "Root Meaning", "Family"])
	root_families_df.sort_values(["Pāli Root", "Grp", "Root Meaning", "Family"], ascending = (True, True, True, True), inplace=True)
	root_families_df.sort_values(by = ["Family"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key)) #sort
	root_families_df = root_families_df.reset_index(drop=True)
	root_families_df_count = root_families_df.shape[0]


def generate_root_subfamily_html():
	print(f"{timeis()} {green}generating html for each root subfamily")
	global subfamily_list
	subfamily_list = []
	root_subfamiles_dict = {}

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
		subfamily_df = dpd_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT"]]
		subfamily_df_length = subfamily_df.shape[0]

		html_string = """<table class="table1"><tbody>"""
			
		for row_sf in range(subfamily_df_length):
			sf_pali = subfamily_df.iloc[row_sf, 0]
			sf_pos = subfamily_df.iloc[row_sf, 1]
			sf_english = subfamily_df.iloc[row_sf, 2]

			html_string += f"<tr><th>{sf_pali}</th>"
			html_string += f"<td><b>{sf_pos}</b></td>"
			html_string += f"<td>{sf_english}</td></tr>"

		html_string += f"""</tbody></table>"""
		html_string += f"{subfamily_df_length}"
		
		try:
			with open(f"output/subfamily html/{root} {root_group} {root_meaning} {subfamily}.html", "w") as output_file:
				output_file.write(html_string)
		except:
			print(f"{timeis()} {red}error writing 'output/subfamily html/{root} {root_group} {root_meaning} {subfamily}.html'")
		
		subfamily_string = f"{root} {root_group} {root_meaning} {subfamily}"	
		subfamily_list.append(subfamily_string)

		html_string_json = re.sub("table1", "root-families", html_string)
		root_subfamiles_dict[subfamily_string] = html_string_json
	
	root_subfamiles_json = json.dumps(root_subfamiles_dict, ensure_ascii=False, indent=4)
	with open ("../dpd-app/data/root-subfamilies.json", "w") as f:
		f.write(root_subfamiles_json)



def extract_bases():
	print(f"{timeis()} {green}extracting bases")
	
	bases_dict = {}

	for row in range(len(dpd_df)):
		root = dpd_df.loc[row, "Pāli Root"]
		root_group = dpd_df.loc[row, "Grp"]
		root_meaning = dpd_df.loc[row, "Root Meaning"]
		base = dpd_df.loc[row, "Base"]
		base = re.sub("^.+ > ", "", base)
		root_fam = f"{root} {root_group} {root_meaning}"

		if root != "":
			if root_fam not in bases_dict:
				bases_dict[root_fam] = {base}
			else:
				bases_dict[root_fam].add(base)
	
	for root_fam, bases in bases_dict.items():
		bases.discard("")
		bases = sorted(bases, key=lambda x: len(x))

		if len(bases) == 0:
			bases_dict[root_fam] = "-"
		else:
			bases_string = ""
			for base in bases:
				if base != bases[-1]:
					bases_string += f"{base}, "
				else:
					bases_string += f"{base}"
			
			bases_dict[root_fam] = bases_string

	return bases_dict


def generate_root_families_csvs():
	print(f"{timeis()} {green}generating root families csvs")
	global root_family_csv_list
	root_family_csv_list = []

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
		root_family_csv_string = root + " " + root_group + " " + root_meaning
		root_family_csv_list.append(root_family_csv_string)

def generate_root_info_html():

	print(f"{timeis()} {green}writing root info")
	global root_families_list
	root_families_list = []
	
	for row in range(roots_df_count):
		root = roots_df.iloc[row, 2]
		root_in_comps = roots_df.iloc[row, 3]
		root_has_verb = roots_df.iloc[row, 4]
		root_group = roots_df.iloc[row, 5]
		root_sign = roots_df.iloc[row, 6]
		root_meaning = roots_df.iloc[row, 8]
		root_fam = f"{root} {root_group} {root_meaning}"
		base = bases_dict[root_fam]

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
		html_string += f"""<tr><th>Pāḷi Root:</th><td>{root}<sup>{root_has_verb}</sup>{root_group} {root_group_pali} + {root_sign} ({root_meaning})</td></tr>"""
		if re.findall(",", base):
			html_string += f"""<tr><th>Bases:</th><td>{base}</td></tr>"""
		else:
			html_string += f"""<tr><th>Base:</th><td>{base}</td></tr>"""

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
		root_families_string = f"{root} {root_group} {root_meaning}"
		root_families_list.append(root_families_string)

def generate_root_families_csv_for_anki():

	print(f"{timeis()} {green}generating root families csv for anki")

	#combine meaning and buddhadatta columns
	anki_df = dpd_df
	anki_df["Buddhadatta"] = anki_df["Buddhadatta"].str.replace("(.+)", "<div style='color: #AA4400'>\\1<div>")
	anki_df.loc[anki_df["Meaning IN CONTEXT"].isnull(), "Meaning IN CONTEXT"] = anki_df["Buddhadatta"]
	anki_df["Construction"] = anki_df["Construction"].str.replace("(.+)\n.+", "\\1")

    #writing root families for anki.csv
	anki_file = open ("../csvs for anki/root families.csv", 'w', encoding= "'utf-8")
	csv_file = open ("output/root families.csv", 'w', encoding= "'utf-8")

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

		csv_file = open ("output/root families.csv", 'a', encoding= "'utf-8")
		anki_file = open("../csvs for anki/root families.csv", 'a')
		anki_file.write(f"<b>{root_family}</b> {root_group} ({root_meaning})\t")
		anki_file.write(f"<table><tbody>")

		for row in range(filtered_df.shape[0]):
			pāli = filtered_df.iloc[row, 0]
			pos = filtered_df.iloc[row, 1]
			meaning = filtered_df.iloc[row, 2]
			construction = filtered_df.iloc[row, 3]
			construction = re.sub(f"<br/>.+",  "", construction) #remove 2nd line
			anki_file.write(f"<tr valign='top'><div style='color: #FFB380'><td>{pāli}</td><td><div style='color: #FF6600'>{pos}</div></td><td><div style='color: #FFB380'>{meaning}</td><td><div style='color: #AA4400'>{construction}</div></td></tr>")
			csv_file.write(f"{root_family}\t{root_group}\t{root_meaning}\t{pāli}\t{pos}\t{meaning}")
			csv_file.write(f"\t{construction}\n")

		anki_file.write(f"</tbody></table>")
		anki_file.write(f"\t{date}")
		anki_file.write(f"\n")
		csv_file.write(f"\n")

	anki_file.close()
	csv_file.close()

def delete_unused_subfamily_files():

	file_dir = "output/subfamily html/"
	file_ext = ".html"
	del_unused_files(subfamily_list, file_dir, file_ext)


def delete_unused_root_info_files():
	
	file_dir = "output/root info/"
	file_ext = ".html"
	del_unused_files(root_families_list, file_dir, file_ext)


def delete_unused_root_family_csv_files():
	
	file_dir = "output/families/"
	file_ext = ".csv"
	del_unused_files(root_family_csv_list, file_dir, file_ext)


def delete_unused_root_matrix_files():

	file_dir = "output/matrix/"
	file_ext = ".html"
	del_unused_files(root_families_list, file_dir, file_ext)




tic()
roots_df, roots_df_count, root_matrix_checklist = setup_roots_df()
setup_dpd_df()
setup_root_families_df()
generate_root_subfamily_html()
bases_dict = extract_bases()
generate_root_families_csvs()
generate_root_info_html()
generate_root_families_csv_for_anki()
delete_unused_subfamily_files()
delete_unused_root_info_files()
delete_unused_root_family_csv_files()
generate_root_matrix(dpd_df2, date, root_matrix_checklist)
delete_unused_root_matrix_files()
toc()
