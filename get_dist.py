"""
This script calculates distances between a set of language families of the NorthPeruLex
dataset based on the cognate sets using the Lingpy package (List & Forkel 2021)
and export them as a distance matrix in Phylip format. It also performs sound
correspondence pattern identification with LingRex (List 2018).
"""
from lingpy import Wordlist, Alignments, LexStat
from lingpy.read.qlc import normalize_alignment, reduce_alignment
from lingpy.sequence.sound_classes import tokens2class
from lingrex.copar import CoPaR
from lingrex.trimming import prep_alignments, Sites
from lingpy.compare.sanity import mutual_coverage_subset


wl = Wordlist("northperulex.tsv")

# Filter
for idx in wl:
	wl[idx, "tokens"] = [x.split("/")[1] if "/" in x else x for x in wl[idx, "tokens"]]

coverage = wl.coverage()
number_of_languages, pairs = mutual_coverage_subset(wl, 100, concepts='concept')
for number_of_items, languages in pairs:
	print(number_of_items, ','.join(languages))

selected_ls = set().union(*(langs for _, langs in pairs))

selected_ls.discard("Proto-Bora-Muinane")

D = {0: [c for c in wl.columns]}
for idx in wl:
	if (
		wl[idx, "doculect"] in selected_ls
	):
		D[idx] = [wl[idx, c] for c in D[0]]
		
wl_filtered = Wordlist(D)
wl_filtered.output(fileformat='tsv', filename='npl-filtered')

lex = LexStat(wl_filtered)
lex.get_scorer(runs=10000)
lex.cluster(method='sca', cluster_method='infomap')

# Calculate distances
lex.calculate('dst', ref="cogid")
lex.output('dst', filename='distances')

# Infer sound correspondences only from these languages
alms = Alignments(lex, ref='cogid', transcription='form')
alms = prep_alignments(alms)
alms.align()

dct = {}
for _, msa in alms.msa["cogid"].items():
	normalized = normalize_alignment(reduce_alignment(msa["alignment"]))
	msa_new = []
	for site in normalized:
		msa_new.append([s.split("/")[1] if "/" in s else s for s in site])
		
	sites = Sites(alms=msa_new)
	trimmed_sites = sites.trimmed(
		strategy='gap-oriented',
		threshold=0.5,
		skeletons=("CV", "VC")
	)
	
	trimmed_alignment = trimmed_sites.to_alignment()
	
	# Check if sequence becomes all gaps. If so, don't trim
	if any(all(cell == "-" for cell in row) for row in trimmed_alignment):
		print(f"Skipping trimming for cognate set")
		trimmed_alignment = msa_new
		
	for i, row in enumerate(trimmed_alignment):
		dct[msa["ID"][i]] = row
		msa["alignment"][i] = row
		
alms.add_entries("tokens", dct, lambda x: [y for y in x if y != "-"], override=True)
alms.add_entries("alignment", dct, lambda x: list(x), override=True)
alms.add_entries("structure", "tokens", lambda x: tokens2class(x, "cv"), override=True)

cop = CoPaR(alms, transcription='form', ref='cogid', min_refs=2)
cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
cop.add_patterns()
cop.write_patterns("npl-patterns.tsv")