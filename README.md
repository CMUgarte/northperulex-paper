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

### Downloading NorthPeruLex data

```shell
make download
make preprocessing
```

### Reproduce stats

```shell
make stats
```

### Reproduce neighborgnets

```shell
make neighbornets
```
