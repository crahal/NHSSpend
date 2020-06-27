<img src="https://github.com/crahal/NHSSpend/blob/master/papers/figures/matching_summary_header.png" width="900"/>

# Configuring Elasticsearch for NHSSpend

This is a readme to detail how to set up the elastic search functionality associated with the NHSSpend repo (where the figure header shows the match performance from the entire library). It represents an extremely high level implementation for approximate string matching of procurement suppliers with institutional registers (NHS Digital, Companies House and the Charity Commission).

This functionality requires:
* Elasticsearch
* Python 3.6+
* Python packages
  * elasticsearch
  * elasticsearch-dsl

## Elasticsearch cluster setup

Download the installers from https://www.elastic.co/downloads/elasticsearch.

Follow the install steps at the download URL.

Ensure your local drive has more than 5% free space, as Elasticsearch locks down nodes when free space is below 5% to avoid using 100% of drive space.

Run the Elasticsearch service as instructed in the install steps and confirm it is reachable via localhost.

Run `python ingest_everything.py` to ingest everything. This script downloads the necessary datasets to each of data/data_cc, data/data_ch and data/nhsdigital. It ingests them into the ES cluster. If you have any errors here, please make sure that the Elasticsearch service is running and that you do indeed have >5% free disk space. The amount of time that this ingestion will take is highly
variable. The code within NHSSpend which calls this ingested cluster is found in reconciliation.py, and is called by `main()` in NHSSpend.py after the download and parse is complete.

## Constructing your own data mappings
The classes within ingest_everything.py are all involved in creating a structured representation of institutional data.
Mapping the data into a structured format allows us to write complex queries of the data using Elasticsearch.

To create your own index and mapping for other data sources, please familiarise yourself with the ES datatypes:

https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-data-types.html

Each field of your input data should use the data type that best describes its contents. When designing the data structure consider if a field is unique or if it may appear multiple times and whether multiple fields form a group of related data. Subclasses are used to create data groups and reusable representations of sub-structures in the data.


## TODO
* Integrating new data into an existing cluster.
* Complex queries
* Queries across data from 2 indices.
