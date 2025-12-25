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

lang_count = defaultdict(int)
for idx in wl:
	lang = wl[idx, "doculect"]
	lang_count[lang] += 1

table_data = []
lang_metadata = {}

for idx in wl:
	lang = wl[idx, "doculect"]
	if lang not in lang_metadata:
		glottocode = wl[idx, "glottocode"]
		glottoname = wl[idx, "glottolog_name"]
		subgroup = wl[idx, "subgroup"]
		source = wl[idx, "source"]
		
		lang_metadata[lang] = {
			"glottocode": glottocode,
			"glottoname": glottoname,
			"subgroup": subgroup,
			"source": source
		}
	
for lang in sorted(lang_count.keys()):
	coverage = round(lang_count[lang] / total_concepts, 3)
	metadata = lang_metadata[lang]
	
	source = metadata["source"]
	if isinstance(source, list):
		source = ", ".join(sorted(set(source)))
	
	table_data.append([
		lang,
		metadata["glottoname"],
		metadata["glottocode"],
		metadata["subgroup"],
		source,
		f"{coverage:.2f}"
	])
	
table = tabulate(
	table_data,
	headers=[
		"Variety",
		"Glottolog Name",
		"Glottocode",
		"Language Family",
		"Sources",
		"Coverage"
	],
	tablefmt="pipe"
)

print(table)