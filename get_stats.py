from collections import defaultdict
from lingpy import Wordlist
from lingpy.compare.sanity import average_coverage, mutual_coverage
from tabulate import tabulate


wl = Wordlist.from_cldf(
	"northperulex/cldf/cldf-metadata.json",
	columns=(
		"language_id",
		"language_glottocode",
		"language_glottolog_name",
		"language_subgroup",
		"parameter_id",
		"segments",
		"form",
		"source"
	),
	namespace=(
		("language_id", "doculect"),
		("language_glottocode", "glottocode"),
		("language_glottolog_name", "glottolog_name"),
		("language_subgroup", "subgroup"),
		("parameter_id", "concept"),
		("segments", "tokens"),
		("form", "form"),
		("source", "source")
	)
)

print("Columns in wordlist:", wl.columns)
print(f"Number of entries: {len(wl)}")
print(f"Number of languages: {wl.width}")
print(f"Number of concepts: {wl.height}")

total_concepts = wl.height

lang_forms = defaultdict(int)
lang_concepts = defaultdict(set)
lang_sources = defaultdict(set)
lang_metadata = {}

for idx in wl:
	lang = wl[idx, "doculect"]
	concept = wl[idx, "concept"]
	source = wl[idx, "source"]
	lang_forms[lang] += 1
	lang_concepts[lang].add(concept)
	
	if source:
		if isinstance(source, list):
			for s in source:
				lang_sources[lang].add(s)
		else:
			lang_sources[lang].add(source)
	
	if lang not in lang_metadata:
		glottocode = wl[idx, "glottocode"]
		glottoname = wl[idx, "glottolog_name"]
		subgroup = wl[idx, "subgroup"]
		
		lang_metadata[lang] = {
			"glottocode": glottocode,
			"glottoname": glottoname,
			"subgroup": subgroup,
		}

table_data = []

for lang in sorted(lang_forms.keys()):
	forms_count = lang_forms[lang]
	concepts_count = len(lang_concepts[lang])
	
	syn = round(forms_count / concepts_count, 2)
	
	coverage = round(concepts_count / total_concepts, 3)
	
	metadata = lang_metadata[lang]
	
	sources = sorted(lang_sources[lang])
	source_str = ", ".join(sources)
	
	table_data.append([
		#lang,
		metadata["glottoname"],
		metadata["glottocode"],
		metadata["subgroup"],
		source_str,
		forms_count,
		concepts_count,
		syn,
		f"{coverage:.2f}"
	])
	
table_data.sort(key=lambda x: (-x[5], x[0]))

table = tabulate(
	table_data,
	headers=[
		"Variety",
		#"Name",
		"Glottocode",
		"Family",
		"Sources",
		"Forms",
		"Concepts",
		"Synonymy",
		"Coverage"
	],
	tablefmt="latex"
)

print(table)