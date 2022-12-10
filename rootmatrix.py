from os import times
from timeis import green, red, timeis, white
import re
import pandas as pd


def generate_root_matrix(dpd_df2, date, root_matrix_checklist):
	print(f"{timeis()} {green}generating root matrix")
	rootmx = {}
	counter=0
	counter_total = 0

	for row in range(len(dpd_df2)):
		headword = dpd_df2.loc[row, "Pāli1"]
		pos = dpd_df2.loc[row, "POS"]
		grammar = dpd_df2.loc[row, "Grammar"]
		meaning = dpd_df2.loc[row, "Meaning IN CONTEXT"]
		root = dpd_df2.loc[row, "Pāli Root"]
		root_group = dpd_df2.loc[row, "Grp"]
		root_meaning = dpd_df2.loc[row, "Root Meaning"]
		base = dpd_df2.loc[row, "Base"]
		pattern = dpd_df2.loc[row, "Pattern"]
		root_family = f"{root} {root_group} {root_meaning}"
		
		if row % 10000 == 0:
			print(f"{timeis()} {white}{row}/{len(dpd_df2)}\t{headword}")

		if root != "":
			if root_family not in rootmx:
				rootmx[root_family] = {
					'verbs':{
						'pr':[],
						'pr caus':[],
						'pr caus & pass': [],
						'pr pass':[],
						'pr desid':[],
						'pr desid & caus': [],
						'pr intens':[],
						'pr intens & caus': [],
						'pr deno':[],
						'pr deno & caus': [],
						'pr ●':[],

						'imp': [],
						'imp caus': [],
						'imp caus & pass': [],
						'imp pass': [],
						'imp desid': [],
						'imp desid & caus': [],
						'imp intens': [],
						'imp deno': [],
						'imp deno & caus': [],
						'imp ●': [],

						'opt':[],
						'opt caus': [],
						'opt caus & pass': [],
						'opt pass': [],
						'opt desid':[],
						'opt desid & caus': [],
						'opt intens':[],
						'opt deno':[],
						'opt deno & caus': [],
						'opt ●': [],

						'perf':[],
						'perf caus': [],
						'perf caus & pass': [],
						'perf pass': [],
						'perf desid': [],
						'perf desid & caus': [],
						'perf intens': [],
						'perf deno': [],
						'perf deno & caus': [],
						'perf ●': [],

						'imperf':[],
						'imperf caus': [],
						'imperf caus & pass': [],
						'imperf pass': [],
						'imperf desid': [],
						'imperf desid & caus': [],
						'imperf intens': [],
						'imperf deno': [],
						'imperf deno & caus': [],
						'imperf ●': [],

						'aor': [],
						'aor caus': [],
						'aor caus & pass': [],
						'aor pass': [],
						'aor desid': [],
						'aor desid & caus': [],
						'aor intens': [],
						'aor deno': [],
						'aor deno & caus': [],
						'aor ●': [],

						'fut':[],
						'fut caus': [],
						'fut caus & pass': [],
						'fut pass': [],
						'fut desid': [],
						'fut desid & caus': [],
						'fut intens': [],
						'fut deno': [],
						'fut deno & caus': [],
						'fut ●': [],

						'cond': [],
						'cond caus': [],
						'cond caus & pass': [],
						'cond pass': [],
						'cond desid': [],
						'cond desid & caus': [],
						'cond intens': [],
						'cond deno': [],
						'cond deno & caus': [],
						'cond ●': [],

						'abs': [],
						'abs caus': [],
						'abs caus & pass': [],
						'abs pass': [],
						'abs desid': [],
						'abs desid & caus': [],
						'abs intens': [],
						'abs deno': [],
						'abs deno & caus': [],
						'abs ●': [],

						'ger': [],
						'ger caus': [],
						'ger caus & pass': [],
						'ger pass': [],
						'ger desid': [],
						'ger desid & caus': [],
						'ger intens': [],
						'ger deno': [],
						'ger deno & caus': [],
						'ger ●': [],

						'inf': [],
						'inf caus': [],
						'inf caus & pass': [],
						'inf pass': [],
						'inf desid': [],
						'inf desid & caus': [],
						'inf intens': [],
						'inf deno': [],
						'inf deno & caus': [],
						'inf ●': [],
					},
					
					'participles':{
						'prp':[],
						'prp caus': [],
						'prp caus & pass': [],
						'prp pass': [],
						'prp desid': [],
						'prp desid & caus': [],
						'prp desid & pass': [],
						'prp intens': [],
						'prp deno': [],
						'prp deno & caus': [],
						'prp ●': [],

						'pp':[],
						'pp caus': [],
						'pp caus & pass': [],
						'pp pass': [],
						'pp desid': [],
						'pp desid & caus': [],
						'pp intens': [],
						'pp deno': [],
						'pp deno & caus': [],
						'pp ●': [],

						'app': [],
						'app ●': [],

						'ptp':[],
						'ptp caus': [],
						'ptp caus & pass': [],
						'ptp pass': [],
						'ptp desid': [],
						'ptp desid & caus': [],
						'ptp intens': [],
						'ptp deno': [],
						'ptp deno & caus': [],
						'ptp ●': [],

					},

					'nouns':{
						'masc':[],
						'masc caus': [],
						'masc caus & pass': [],
						'masc pass': [],
						'masc desid': [],
						'masc desid & caus': [],
						'masc intens': [],
						'masc deno': [],
						'masc deno & caus': [],
						'masc ●': [],

						'fem':[],
						'fem caus': [],
						'fem caus & pass': [],
						'fem pass': [],
						'fem desid': [],
						'fem desid & caus': [],
						'fem intens': [],
						'fem deno': [],
						'fem deno & caus': [],
						'fem ●': [],

						'nt': [],
						'nt caus': [],
						'nt caus & pass': [],
						'nt pass': [],
						'nt desid': [],
						'nt desid & caus': [],
						'nt intens': [],
						'nt deno': [],
						'nt deno & caus': [],
						'nt ●': [],
						},
					
					'adjectives':{
						'adj': [],
						'adj caus': [],
						'adj caus & pass': [],
						'adj pass': [],
						'adj desid': [],
						'adj desid & caus': [],
						'adj intens': [],
						'adj deno': [],
						'adj deno & caus': [],
						'adj ●': [],
					},

					'adverbs': {
					'ind': [],
					'ind caus': [],
					'ind caus & pass': [],
					'ind pass': [],
					'ind desid': [],
					'ind desid & caus': [],
                    'ind intens': [],
					'ind deno': [],
					'ind deno & caus': [],
					'ind ●': [],
					}
				}
			
			# assign words to dict categories
			if meaning != "" or \
			root_family in root_matrix_checklist:

				if pos == 'pr':
					# first caus & pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['pr caus & pass'] += [headword]
						counter += 1
					
					# desid & caus 
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdesid\b", base)):
						rootmx[root_family]['verbs']['pr desid & caus'] += [headword]
						counter += 1

					# intens & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bintens\b", base)):
						rootmx[root_family]['verbs']['pr intens & caus'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['pr deno & caus'] += [headword]
						counter += 1
					
					# caus 
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['pr caus'] += [headword]
						counter += 1
					
					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['pr pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['pr intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['pr desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['pr deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['pr'] += [headword]
						counter += 1				

				elif pos == 'imp':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['imp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['imp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['imp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['imp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['imp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['imp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['imp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['imp'] += [headword]
						counter += 1

				elif pos == 'opt':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['opt caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['opt deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['opt caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['opt pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['opt intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['opt desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['opt deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['opt'] += [headword]
						counter += 1

				elif pos == 'perf':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['perf caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['perf deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['perf caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['perf pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['perf intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['perf desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['perf deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['perf'] += [headword]
						counter += 1

				elif pos == 'imperf':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['imperf caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['imperf deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['imperf caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['imperf pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['imperf intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['imperf desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['imperf deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['imperf'] += [headword]
						counter += 1

				elif pos == 'aor':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['aor caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['aor deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['aor caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['aor pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['aor intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['aor desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['aor deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['aor'] += [headword]
						counter += 1

				elif pos == 'fut':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['fut caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['aor deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['fut caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['fut pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['fut intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['fut desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['fut deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['fut'] += [headword]
						counter += 1

				elif pos == 'cond':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['cond caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['cond deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['cond caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['cond pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['cond intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['cond desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['cond deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['cond'] += [headword]
						counter += 1

				elif pos == 'abs':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['abs caus & pass'] += [headword]
						counter += 1

					# desid & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdesid\b", base)):
						rootmx[root_family]['verbs']['abs desid & caus'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['abs deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['abs caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['abs pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['abs intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['abs desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['abs deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['abs'] += [headword]
						counter += 1

				elif pos == 'ger':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['ger caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['ger deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['ger caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['ger pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['ger intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['ger desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['ger deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['ger'] += [headword]
						counter += 1

				elif pos == 'inf':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['verbs']['inf caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['verbs']['inf deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['verbs']['inf caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['verbs']['inf pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['verbs']['inf intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['verbs']['inf desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['verbs']['inf deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['verbs']['inf'] += [headword]
						counter += 1

				elif pos == 'prp':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['prp caus & pass'] += [headword]
						counter += 1
					
					# desid and pass
					elif (re.findall(r"\bdesid\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['prp desid & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['prp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['prp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['prp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['prp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['prp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['prp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['prp'] += [headword]
						counter += 1

				elif pos == 'adj' and re.findall("prp", grammar):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['prp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['prp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['prp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['prp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['prp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['prp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['prp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['prp'] += [headword]
						counter += 1

				elif pos == 'pp':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['pp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['pp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['pp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['pp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['pp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['pp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['pp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['pp'] += [headword]
						counter += 1

				# adj and pp
				elif pos == 'adj' and re.findall(r"\bpp\b", grammar):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['pp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['pp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['pp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['pp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['pp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['pp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['pp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['pp'] += [headword]
						counter += 1

				# app
				elif re.findall(r"\bapp\b", grammar):
					rootmx[root_family]['participles']['app'] += [headword]
					counter += 1

				elif pos == 'ptp':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['ptp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['ptp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['ptp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['ptp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['ptp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['ptp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['ptp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['ptp'] += [headword]
						counter += 1

				elif pos == 'adj' and re.findall("ptp", grammar):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['participles']['ptp caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['participles']['ptp deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['participles']['ptp caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['participles']['ptp pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['participles']['ptp intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['participles']['ptp desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['participles']['ptp deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['participles']['ptp'] += [headword]
						counter += 1

				elif pos == 'masc':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['nouns']['masc caus & pass'] += [headword]
						counter += 1

					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['nouns']['masc deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['nouns']['masc caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['nouns']['masc pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['nouns']['masc intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['nouns']['masc desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['nouns']['masc deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['nouns']['masc'] += [headword]
						counter += 1

				elif pos == 'root' and re.findall('masc', grammar):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['nouns']['masc caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['nouns']['masc deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['nouns']['masc caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['nouns']['masc pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['nouns']['masc intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['nouns']['masc desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['nouns']['masc deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['nouns']['masc'] += [headword]
						counter += 1

				elif pos == 'fem':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['nouns']['fem caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['nouns']['fem deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['nouns']['fem caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['nouns']['fem pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['nouns']['fem intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['nouns']['fem desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['nouns']['fem deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['nouns']['fem'] += [headword]
						counter += 1

				elif pos == 'card' and re.findall("fem", grammar):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['nouns']['fem caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['nouns']['fem deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['nouns']['fem caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['nouns']['fem pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['nouns']['fem intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['nouns']['fem desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['nouns']['fem deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['nouns']['fem'] += [headword]
						counter += 1

				elif pos == 'nt':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['nouns']['nt caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['nouns']['nt deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['nouns']['nt caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['nouns']['nt pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['nouns']['nt intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['nouns']['nt desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['nouns']['nt deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['nouns']['nt'] += [headword]
						counter += 1
				
				# special case
				elif headword == 'sogandhika 3':
					rootmx[root_family]['nouns']['nt'] += [headword]
					counter += 1


				elif pos == 'adj':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['adjectives']['adj caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['adjectives']['adj deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['adjectives']['adj caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['adjectives']['adj pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['adjectives']['adj intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['adjectives']['adj desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['adjectives']['adj deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['adjectives']['adj'] += [headword]
						counter += 1

				elif pos == 'suffix' and re.findall('adj', base):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['adjectives']['adj caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['adjectives']['adj deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['adjectives']['adj caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['adjectives']['adj pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['adjectives']['adj intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['adjectives']['adj desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['adjectives']['adj deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['adjectives']['adj'] += [headword]
						counter += 1
				
				elif pos == 'ind':
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['adverbs']['ind caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['adverbs']['ind deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['adverbs']['ind caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['adverbs']['ind pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['adverbs']['ind intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['adverbs']['ind desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['adverbs']['ind deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['adverbs']['ind'] += [headword]
						counter += 1
		
				elif pos == 'suffix': # and re.findall('ind', 'base'):
					# first caus and pass
					if (re.findall(r"\bcaus\b", base) and re.findall(r"\bpass\b", base)):
						rootmx[root_family]['adverbs']['ind caus & pass'] += [headword]
						counter += 1
					
					# deno & caus
					elif (re.findall(r"\bcaus\b", base) and re.findall(r"\bdeno\b", base)):
						rootmx[root_family]['adverbs']['ind deno & caus'] += [headword]
						counter += 1

					# caus
					elif re.findall(r"\bcaus\b", base):
						rootmx[root_family]['adverbs']['ind caus'] += [headword]
						counter += 1

					# pass
					elif re.findall(r"\bpass\b", base):
						rootmx[root_family]['adverbs']['ind pass'] += [headword]
						counter += 1

					# intens
					elif re.findall(r"\bintens\b", base):
						rootmx[root_family]['adverbs']['ind intens'] += [headword]
						counter += 1

					# desid
					elif re.findall(r"\bdesid\b", base):
						rootmx[root_family]['adverbs']['ind desid'] += [headword]
						counter += 1

					# deno
					elif re.findall(r"\bdeno\b", base):
						rootmx[root_family]['adverbs']['ind deno'] += [headword]
						counter += 1

					# normal
					else:
						rootmx[root_family]['adverbs']['ind'] += [headword]
						counter += 1

				else:
					print(f"{timeis()} {red}{headword}{white}")
			
			elif meaning == "":

				if pos == 'pr':
					rootmx[root_family]['verbs']['pr ●'] += [headword]
					counter += 1

				elif pos == 'imp':
					rootmx[root_family]['verbs']['imp ●'] += [headword]
					counter += 1

				elif pos == 'opt':
					rootmx[root_family]['verbs']['opt ●'] += [headword]
					counter += 1

				elif pos == 'perf':
					rootmx[root_family]['verbs']['perf ●'] += [headword]
					counter += 1

				elif pos == 'imperf':
					rootmx[root_family]['verbs']['imperf ●'] += [headword]
					counter += 1

				elif pos == 'aor':
					rootmx[root_family]['verbs']['aor ●'] += [headword]
					counter += 1

				elif pos == 'fut':
					rootmx[root_family]['verbs']['fut ●'] += [headword]
					counter += 1

				elif pos == 'cond':
					rootmx[root_family]['verbs']['cond ●'] += [headword]
					counter += 1

				elif pos == 'abs':
					rootmx[root_family]['verbs']['abs ●'] += [headword]
					counter += 1

				elif pos == 'ger':
					rootmx[root_family]['verbs']['ger ●'] += [headword]
					counter += 1

				elif pos == 'inf':
					rootmx[root_family]['verbs']['inf ●'] += [headword]
					counter += 1

				elif pos == 'prp':
					rootmx[root_family]['participles']['prp ●'] += [headword]
					counter += 1

				elif pos == 'pp':
					rootmx[root_family]['participles']['pp ●'] += [headword]
					counter += 1

				elif re.findall(r"\bapp\b", grammar):
					rootmx[root_family]['participles']['app ●'] += [headword]
					counter += 1

				elif pos == 'ptp':
					rootmx[root_family]['participles']['ptp ●'] += [headword]
					counter += 1

				elif pos == 'adj' and re.findall("ptp", grammar):
					rootmx[root_family]['participles']['ptp ●'] += [headword]
					counter += 1				

				elif pos == 'masc':
					rootmx[root_family]['nouns']['masc ●'] += [headword]
					counter += 1

				elif pos == 'fem':
					rootmx[root_family]['nouns']['fem ●'] += [headword]
					counter += 1

				elif pos == 'nt':
					rootmx[root_family]['nouns']['nt ●'] += [headword]
					counter += 1

				elif pos == 'adj':
					rootmx[root_family]['adjectives']['adj ●'] += [headword]
					counter += 1

				elif pos == 'ind':
					rootmx[root_family]['adverbs']['ind ●'] += [headword]
					counter += 1
				
				else:
					print(f"{timeis()} {red}{headword}{white}")

			counter_total += 1
	
	print(f"{timeis()} {green}total roots added to matrix {white}{counter} / {counter_total}")
	
	# generate html

	print(f"{timeis()} {green}generating html and anki files", end=" ")

	with open(f"../exporter/assets/dpd-roots.css", "r") as css_file:
		css = css_file.read()
	
	anki_dict = {}

	for root_name, data1 in rootmx.items():
		html = ""

		# html = f"<style>{css}</style>"
		html += f"<table class='root_table2'>"
		total_count = 0

		for category, data2 in data1.items():
			cflag = True
			for pos, words  in data2.items():
				total_count += len(words)
				if words != []:

					if cflag == True:
						# html += f"<tr><th rowspan='1'>{category}</th><th>{pos}</th><td>"
						html += f"<tr><th colspan='2'>{category}</th></tr>"
						html += f"<td><b>{pos}<b></td><td>"
						cflag = False

					elif cflag == False:
						html += f"<tr><td><b>{pos}</b></td><td>"

					for word in words:
						if word != words[-1]:
							html += f"{word}, "
						else:
							html += f"{word}</td></tr>"

		html += f"<th colspan='2'>"
		if re.findall("●", html):
			html += f"●"
		else:
			html += f"√"
		html += f"</th></tr></table>"
		html += f"{total_count}"
		html = re.sub("●", "<span class='g3'>●</span>", html)

		# write html files

		with open(f"output/matrix/{root_name}.html", "w") as words:
			words.write(html)
		
		if not re.findall("●", html):
			anki_dict[root_name] = html
		
	# make csv for anki
	
	anki_df = pd.DataFrame.from_dict(anki_dict, orient="index")
	anki_df["Test"] = date
	anki_df.to_csv("../csvs for anki/root matrix.csv", header=None, sep="\t")

	print(f"{white}ok")