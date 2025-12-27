download:
	git clone https://github.com/lexibank/northperulex.git

preprocessing:
	edictor wordlist --dataset=northperulex/cldf/cldf-metadata.json --name=northperulex --preprocessing=northperulex/analysis/realign.py --addon="language_subgroup:subgroup","alignment:alignment","cognacy:cogid","partial_cognacy:cogids","source:source"

stats:
	python get_stats.py

neighbornets:
	python get_dist.py
	outline -a npl_dst.dst -n npl.nex -o npl_neighbornet.png
	outline -a nplcore_dst.dst -n nplcore.nex -o nplcore_neighbornet.png
