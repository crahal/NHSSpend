<img src="https://github.com/crahal/NHSSpend/blob/master/papers/figures/matching_summary_header.png" width="900"/>

##  :bar_chart: :chart_with_upwards_trend: NHSSpend: Tools and data for NHS procurement :chart_with_downwards_trend: :bar_chart:	

![coverage](https://img.shields.io/badge/Purpose-Research-yellow)
[![Generic badge](https://img.shields.io/badge/Python-3.6-<red>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/License-MIT-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/BuildPassing-No-orange.svg)](https://shields.io/)
![coverage](https://img.shields.io/badge/Rating-5\5-orange)
---

## Introduction

This is a library to scrape and reconcile all payments made by a hiarcharcy of NHS institutions over time. It is the final of three projects on public procurement data (the first two of which were [centgovspend](https://github.com/crahal/centgovspend) and [TSRC-NCVO-CSDP](https://github.com/crahal/TSRC-NCVO-CSDP)). Code for an interactive dashboard is found at src/dashboard, and an **extremely unfinished prototype** of the dashboard itself is at:
<p align="center">
  <a href="#">http://nhsspend.org/</a>
</p>

with the help of [Ian M. Knowles](https://github.com/ianknowles). Links to open-access (OSF) versions of the two headline academic papers (`The Role of Non-Profits in Public Health Service Provision: Evidence from 25,338 heterogeneous procurement datasets` and `Private networks of healthcare supply`) will be hosted on the Open Science Framework (OSF) in due course, and linked here. If you would like to collaborate on these papers or related, please don't hestiate to get in touch.

## Pre-reqs

NHSSpend tries to minimize the number of pre-requisite installations outside of the standard library, and we recommend an Anaconda installation to provide a comprehensive set of basic tools. However, a couple are necessary due to the magnitude of the undertaking. These include a range of modules found in the requirements.txt file (generated by pipreqs). The pdfparser is based on a version of the [pdftableparser](https://github.com/ianknowles/pdftableparser) library, and the Charity Commission data is extracted using the charity-commission-extract library from [NCVO](https://github.com/ncvo/charity-commission-extract). The Elasticsearch functionality is a custom implementation.

## Data Origination

The data originates from one of two lists of recognised NHS institutions (Trusts and CCGs) and the main NHS England data provision [page](https://www.england.nhs.uk/contact-us/pub-scheme/spend/#payments). These lists are used to create mappings to websites, and update on the status of the data  (data/data_support/ccg_list.xlsx and data/data_support/trust_list.xlsx) with a number of different parametres fed into the scraper (src/NHSscraper.py). The data curation exercise has stopped as of April 2020 in order to focus on the analysis of the data, with the compresse datasets found in data/merged/* subdirectory of this repository). This is also partly due to the Covid-19 pandemic and the restructuring of Clinical Commissioning groups more generally (where 18 mergers took the number of CCGs from 191 to 136). However, please do raise issues on here if you think any of those institutions are mislabelled, or outdated. If you want to update this list (and the subsequent scrapers), please do raise an issue\get in touch (this is a constant ongoing work in progress until there is a centrally covened resource provided by the Government Data Service).

The procurement data itself is provided under an [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) (OGL). Guidance for publishing spend over £25,000 is published by [HM Treasury](https://www.gov.uk/government/publications/guidance-for-publishing-spend-over-25000).

## Reconciliation

The `es_configure.md` describes the reconciliation approach. These reconciliations are then manually verified and merged back into the procurement data.

## Structure

Repo structure is based on the ```tree``` [utility](https://en.wikipedia.org/wiki/Tree_%28Unix%29).

├ readme.mdes_configure.md  
├ es_configure.md  
├ requirements.txt  
├ src  
│   └ analysis  
│   │   ├ charity_analysis_notebook.ipynb  
│   │   ├ general_analysis_functions.py  
│   │   ├ helper_functions.py  
│   │   ├ charity_analysis_functions.py  
│   └ dashboard  
│   ├ scrape_and_parse_ccgs.py  
│   ├ scrape_and_parse_trusts.py  
│   ├ scraping_tools.py  
│   ├ generate_output.py  
│   ├ ingest_everything.py  
│   ├ merge_and_evaluate_tools.py  
│   ├ NHSSpend.py  
│   ├ parsing_tools.py  
│   ├ pdf_table_parser.py  
│   ├ preconciliation.py  
├ data  
│   └ data_support/*  
│   └ data_cc/*  
│   └  data_ch/*  
│   └ data_dashboard/*  
│   └ data_masteringest/*  
│   └ data_merge/*  
│   └ data_nhsccgs/*  
│   └ data_nhsdigital/*  
│   └ data_nhsengland/*  
│   └ data_nhstrusts/*  
│   └ data_reconciled/*  
│   └ data_shapefiles/*  
│   └ data_summary/*  
├ papers  
│   └ corporate_networks  
│   └ figures  
│   └ tables  
│   └ third_sector  
├ logging  
│   │   ├ nhsspend.log  
│   └ eval_logs  
├ tokens  

## Licensing

This code is made available under an MIT License.

## TODO:

* Docstrings, docstrings, docstrings
* Publish related academic papers

Last updated: 2020-08-30
