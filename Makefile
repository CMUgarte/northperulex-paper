download:
	git clone https://github.com/lexibank/northperulex.git

preprocessing:
	edictor wordlist --dataset=northperulex/cldf/cldf-metadata.json --name=northperulex --preprocessing=northperulex/analysis/realign.py --addon="language_subgroup:subgroup","alignment:alignment","cognacy:cogid","partial_cognacy:cogids","source:source"

stats:
	python get_stats.py

neighbornet:
	python get_neighbornet.py