from collections import defaultdict
from lingpy import Wordlist
from lingpy.compare.sanity import average_coverage, mutual_coverage
from tabulate import tabulate


wl = Wordlist.from_cldf(
	"northperulex/cldf/cldf-metadata.json",
	columns=(
		"parameter_id",
		"language_id",
		"name",
		"value",
		"segments",
		"form",
		"glottocode",
		"concepticon_id",
		"source",
		"subgroup"
	),
	namespace=(
		("language_id", "doculect"),
		("subgroup", "subgroup"),
		("name", "concept"),
		("segments", "tokens"),
		("forms", "forms"),
		("cognacy", "cogid"),
		("partial_cognacy", "cogids"),
		("source", "source"),
		("glottocode", "glottocode")
	)
)


lang_count = defaultdict(int)
concepts = set()

for idx in wl:
	lang = wl[idx, "doculect"]
	lang_count[lang] = lang_count[lang] + 1
	concepts.add(wl[idx, "parameter_id"])

total_concepts = len(concepts)
print(f"Total number of concepts: {total_concepts}")
print(f"Total number of languages: {len(lang_count)}")

table_data = []
covs_total = 0

for lang in sorted(lang_count.keys()):
	# Calculate coverage percentage
	coverage_pctg = round((lang_count[lang] / total_concepts) * 100, 1)
	covs_total += coverage_pctg
	
	for idx in wl:
		if wl[idx, "doculect"] == lang:
			lang_name = lang
			glottocode = wl[idx, "glottocode"]
			subgroup = wl[idx, "subgroup"]
			source = wl[idx, "source"]
			
			table_data.append([
				lang_name,
				glottocode,
				subgroup,
				source,
				f"{lang_count[lang]} ({coverage_pctg}%)"
			])
			break
		
table = tabulate(
	table_data,
	headers=[
		"Language",
		"Glottocode",
		"Language Family",
		"Sources",
		"Coverage"
	],
	tablefmt="pipe"
)

print(table)

avg_coverage = round(covs_total / len(lang_count), 2)
avg_mutualcov = average_coverage(wl)

print(f"Average coverage: {avg_coverage}%")
print(f"Average mutual coverage: {avg_mutualcov:2f}")

for i in range(total_concepts, 0, -1):
	if mutual_coverage(wl, i):
		print(f"Minimal mutual coverage: {i} concept pairs")