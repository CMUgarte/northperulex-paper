"""
This script calculates distances between the languages on
the NorthPeruLex dataset based on the cognate sets using
the Lingpy package (List & Forkel 2021) and export them
as a distance matrix in Phylip format.
"""
from lingpy import Wordlist


wl = Wordlist("northperulex.tsv")

wl.calculate('dst', ref="cogid")
wl.output('dst', filename="npl_dst")