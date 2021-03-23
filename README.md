# galaxydubouleBioblendScripts

## Python scripts using bioblend to interact with galaxy more automatically

These python scripts are using [BioBlend](https://bioblend.readthedocs.io/) to interact with galaxy.

## Usage

As it uses BioBlend, you need to install it. The easiest way is to use conda:

```bash
$ conda create -n bioblend -c bioconda bioblend "python>=3.7"
```

Then activate your environment:

```bash
$ conda activate bioblend
```

Then you need to download the scripts, you can click on Code, Download ZIP on the upper part of the page and then unzip it. You will set the path of galaxydubouleBioblendScripts in a bash variable:
```bash
# You need to adapt to where you downloaded:
$ gitHubDirectory=/home/ldelisle/Documents/mygit/galaxydubouleBioblendScripts/
```

In order to use these script you need to get your api key from your galaxy instance.
Log in your galaxy, go to User, Settings, Manage API key. If there is no, you need to generate one. Then copy it and put it in a bash variable:

```bash
# You need to adapt to your API:
$ myAPI=blablabla
```

To be able to download a list of dataset you need to get their API ID. If you don't have a lot of them, you can get them clicking on the (i) icon on the galaxy webpage, checking the line "History Content API ID".

If you have more or if they are part of a collection, you may be interested to use one of the a script to get the list (`get_datasets_id.py` or `get_collections_id.py`).

For the moment, the tool is either designed for datasets or for collection, not both at the same time.

## Dataset point of view

### `get_datasets_id.py`

This script can be used to get all datasets ids from some histories or all histories.

If you want for all histories (not deleted), just do:

```bash
$ python ${gitHubDirectory}/scripts/get_datasets_id.py --api $myAPI > all_my_datasets.txt
```

If you have a lot of them, this can be long...

If you already know which history/ies you want, you need to go to the webpage, click on the (i) icon of one of your dataset of the history and copy the History API ID in a file. It should be one id per line.

Then run:

```bash
$ python ${gitHubDirectory}/scripts/get_datasets_id.py --api $myAPI --historiesTable my_histories.txt > my_datasets_in_my_histories.txt
```

The output file is a tabular delimited file whose first column is the dataset id, the second is the dataset name, the third is the size of the dataset, the fourth is history id and the fifth is the history_name.

You may want to modify this file to remove datasets that you don't want to download.


### `download_datasets.py`

This script can be used to download all datasets from a list of dataset ids.
The ids should be one per line. They can be obtained from the webpage by clicking on the (i) icon and using the History Content API ID or can be obtained with `get_datasets_id.py`.

It will download the datasets in one subdirectory per history and the name will be the one you would have if you would have downloaded it through the webpage.

An example usage is:

```bash
$ python ${gitHubDirectory}/scripts/download_datasets.py --api $myAPI --datasetTable my_datasets_in_my_histories.txt --outputFolder my_downloads/
```

Depending on the number of datasets, it can be quite long...


## Collection point of view

### `get_collections_id.py`

This script can be used to get all collection ids from some histories or all histories.

If you want for all histories (not deleted), just do:

```bash
$ python ${gitHubDirectory}/scripts/get_collections_id.py --api $myAPI > all_my_collections.txt
```

If you have a lot of them, this can be long...

If you already know which history/ies you want, you need to go to the webpage, click on the (i) icon of one of your dataset of the history and copy the History API ID in a file. It should be one id per line.

Then run:

```bash
$ python ${gitHubDirectory}/scripts/get_collections_id.py --api $myAPI --historiesTable my_histories.txt > my_collections_in_my_histories.txt
```

The output file is a tabular delimited file whose first column is the collection id, the second is the history id, the third is the number in your galaxy history, the fourth is the name of the collection, the fifth is the size of the collection, the sixth is the history_name.

You may want to modify this file to remove collections that you don't want to download.


### `download_collections.py`

This script can be used to download all datasets from a list of collection ids and history ids. There should be one line per collection, first column the collection id and second column the history id. They can be obtained with `get_collections_id.py`.

It will download the datasets in one subdirectory per history and one subsubdirectory per collection. The name will be the name of the identifier of within the collection with the correct extension.

An example usage is:

```bash
$ python ${gitHubDirectory}/scripts/download_collections.py --api $myAPI --collectionTable my_collections_in_my_histories.txt --outputFolder my_downloads/
```

Depending on the number of collection and the number of dataset per collection, it can be quite long...

## Documentation

Here is the full help:

### `get_datasets_id.py`

```text
usage: get_datasets_id.py [-h] [--url URL] --api API [--historiesTable HISTORIESTABLE] [--deleted] [--output OUTPUT]

Get all items from history ids.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             A FQDN or IP for a given instance of Galaxy.
  --api API             Your API key. Can be obtained from the webpage. User - Settings - Manage API key
  --historiesTable HISTORIESTABLE
                        [Optional] Input table with one line per history. It should correspond to the History API ID.
  --deleted             Get the deleted histories only.
  --output OUTPUT       Output table.
```

### `download_datasets.py`

``` text
usage: download_datasets.py [-h] [--url URL] --api API --datasetTable DATASETTABLE --outputFolder OUTPUTFOLDER

Download datasets from dataset ids.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             A FQDN or IP for a given instance of Galaxy.
  --api API             Your API key. Can be obtained from the webpage. User - Settings - Manage API key
  --datasetTable DATASETTABLE
                        Input table with one line per dataset. It should correspond to the History Content API ID. It can also be
                        generated by get_datasets.py
  --outputFolder OUTPUTFOLDER
                        Folder where files will be downloaded.
```

### `get_collection_id.py`

``` text
usage: get_collections_id.py [-h] [--url URL] --api API [--historiesTable HISTORIESTABLE] [--deleted] [--output OUTPUT]

Get all collections ids from history ids.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             A FQDN or IP for a given instance of Galaxy.
  --api API             Your API key. Can be obtained from the webpage. User - Settings - Manage API key
  --historiesTable HISTORIESTABLE
                        [Optional] Input table with one line per history. It should correspond to the History API ID.
  --deleted             Get the deleted histories only.
  --output OUTPUT       Output table.
```

### `download_collections.py`

``` text
usage: get_collections_id.py [-h] [--url URL] --api API [--historiesTable HISTORIESTABLE] [--deleted] [--output OUTPUT]

Get all collections ids from history ids.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             A FQDN or IP for a given instance of Galaxy.
  --api API             Your API key. Can be obtained from the webpage. User - Settings - Manage API key
  --historiesTable HISTORIESTABLE
                        [Optional] Input table with one line per history. It should correspond to the History API ID.
  --deleted             Get the deleted histories only.
  --output OUTPUT       Output table.
(bioblend) [ldelisle@SV-49-002 ~]$ python Documents/mygit/galaxydubouleBioblendScripts/scripts/download_collections.py 
usage: download_collections.py [-h] [--url URL] --api API --collectionTable COLLECTIONTABLE --outputFolder OUTPUTFOLDER

Download collections from collection ids.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             A FQDN or IP for a given instance of Galaxy.
  --api API             Your API key. Can be obtained from the webpage. User - Settings - Manage API key
  --collectionTable COLLECTIONTABLE
                        Input table with one line per collection. It needs to be generated by get_collections.py (first column
                        collection id, second column history id).
  --outputFolder OUTPUTFOLDER
                        Folder where files will be downloaded.

```

## Note

By default the `--url` is set to galaxyduboule.epfl.ch but if you are not part of Duboule lab, you can still use the scripts and change it...
