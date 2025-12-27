"""
This script produces a phylogenetic network using the Neighbor-net
algorithm (Bryant & Moulton 2004, Huson & Bryan 2006)
"""
from lingpy import Wordlist


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
		"cognacy",
	),
	namespace=(
		("language_id", "doculect"),
		("language_glottocode", "glottocode"),
		("language_glottolog_name", "glottolog_name"),
		("language_subgroup", "subgroup"),
		("parameter_id", "concept"),
		("segments", "tokens"),
		("form", "form"),
		("cognacy", 'cogid')
	)
)

wl.calculate('dst', ref="cogid")
wl.output('dst', filename="npl_dst")


wl2 = Wordlist("northperulex.tsv")
wl2.calculate('dst', ref="cogid")
wl2.output('dst', filename="npl2_dst")