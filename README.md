# NorthPeruLex paper
This repository includes all the code and data necessary to reproduce the results
and stats presented in the paper introducing the dataset "A lexical dataset of small
language families and isolates from Northern Peru" (2026).

## Replicating results

### Installing dependencies and data

Please install all the necessary Python packages in a new virtual environment
by running the following commands:

```shell
pip install -r requirements.txt
```
One final step for the dependencies is to modify the `lexstat.py` file from `lingpy`
in your `YOUR_VENV/lib/python3.12/site-packages/lingpy/compare/`. In order to not to crush
when producing the neighbornet, we need to remove the print staples from the
original script. Please find the next code lines and comment them and showed below:

```shell
# set the lexstat stamp
        #self._stamp = "# Created using the LexStat class of {0}\n".format(
        #        util.PROG)
        
# self._stamp += '# Cluster: ' + self.params['cluster']

# self._stamp += "# Parameters: " + parstring + '\n'
```

### Downloading NorthPeruLex data

```shell
make download
make preprocessing
```

### Reproduce stats

```shell
make stats
```

### Reproduce neighbornet

```shell
make neighbornet
```
