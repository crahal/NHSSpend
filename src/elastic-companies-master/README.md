# elastic-companies
The first example script companies.py shows how to properly create a python class representation of a data source to
import it into an Elasticsearch cluster. The second script query.py demonstrates how to query the cluster for matches
against the data.

These examples require:
* Elasticsearch
* Python 3.6+
* Python packages
  * elasticsearch 
  * elasticsearch-dsl

## Elasticsearch cluster setup
Download the MSI from https://www.elastic.co/downloads/elasticsearch

Install and follow the install steps at the download URL.

Ensure your HDD has more than 5% free space, Elasticsearch locks down nodes when free space is below 5% to avoid using
100% of drive space.

Run the Elasticsearch service as instructed in the install steps and confirm it is reachable via localhost.

## Running the examples
Both examples should be run as scripts without parameters.

Run companies.py to ingest the companies house data, 20 hours run time (approx.).

Run query.py for matches, expects a file named example 'example_for_matching.tsv' at the project top level containing a
list of strings to query, one string per line. The output will be saved to 'matches.csv'.

## Constructing your own data mappings
The classes within companies.py are all involved in creating a structured representation of company data. Each row of
the input csv is mapped to a Company object by the ingest function and then added to the Companies index in the ES
cluster. Mapping the data into a structured format allows us to write complex queries of the data using Elasticsearch.

To create your own index and mapping for other data sources familiarise yourself with the ES datatypes.

https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-data-types.html

Each field of your input data should use the data type that best describes its contents.
When designing the data structure consider if a field is unique or if it may appear multiple times and whether multiple
fields form a group of related data. Subclasses are used to create data groups and reusable reprenstations of
sub-structures in the data. An Address subclass stores all elements of an address together in a single field, we can
then reuse this subclass to represent more addresses in the data or additional instances of a type of address.

The Object class is used for fields that use a subclass for their representation but only appear once, while the Nested
class is used for fields that may repeat many times, such as previous company name.


## TODO
* Integrating new data into an existing cluster.
* Complex queries
* Queries across data from 2 indices.