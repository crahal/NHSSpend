<img src="https://github.com/crahal/NHSSpend/blob/master/papers/figures/nhs_spending_macro_header.png" width="900"/>

# NHSSpend

[![Generic badge](https://img.shields.io/badge/Python-3.6-<red>.svg)](https://shields.io/)  [![Generic badge](https://img.shields.io/badge/License-MIT-blue.svg)](https://shields.io/)  [![Generic badge](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://shields.io/)
---

## Introduction

This is a library to scrape and reconcile all payments made by a hiarcharcy of NHS institutions over time. It is the final of three projects on public procurement data (the first two of which were [centgovspend](https://github.com/crahal/centgovspend) and [TSRC-NCVO-CSDP](https://github.com/crahal/TSRC-NCVO-CSDP)). Code for an interactive dashboard is hosted in src/dashboard, with the help of [Ian M. Knowles](https://github.com/ianknowles) (and access to the prototype of the dashboard is available on request). Links to open-access (OSF) versions of the two headline academic papers (`The Role ofthe Third Sector in Public Health Service Provision: Evidence from 37,125 heterogeneous procurement datasets` and `Private networks of healthcare supply`) will be hosted on the Open Science Framework (OSF) in due course. If you would like to collaborate on these papers, please don't hestiate to get in touch.

## Pre-reqs

NHSSpend tries to minimize the number of pre-requisite installations outside of the standard library, and we recommend an Anaconda installation to provide a comprehensive set of basic tools. However, a couple are necessary due to the magnitude of the undertaking. These include a range of modules found in the the requirements.txt file (generated by pipreqs). The pdfparser is based on a version of the [pdftableparser](https://github.com/ianknowles/pdftableparser) library

## Data Origination

The data originates from one of two lists of recognised NHS institutions. These lists are used to create mappings to websites, and update on the status of the data  (data/data_support/ccg_list.xlsx and data/data_support/trust_list.xlsx) with a number of different parametres fed into the scraper (src\NHSscraper.py). The data curation exercise has stopped as of April 2020 in order to focus on the writing of academic papers, with datasets from those papers being hosted on OSF following their publication (an archive of the entire data/* subdirectory). This is also partly due to the Covid-19 pandemic and the restructuring of Clinical Commissioning groups more generally (where 18 mergers took the number of CCGs from 191 to 136). However, please do raise issues on here if you think any of those institutions are mislabelled, outdated. If you want to update this list (and the subsequent scrapers), please do raise an issue\get in touch (this is a constant ongoing work in progress until there is a centrally covened resource provided by the Government Data Service).

The procurement data itself is provided under an [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) (OGL). Guidance for publishing spend over £25,000 is published by [HM Treasury](https://www.gov.uk/government/publications/guidance-for-publishing-spend-over-25000).

## Reconciliation

The `es_configure.md` describes the reconciliation approach. These recocniliations are then manually verified and merged back into the procurement data.

## Structure

## Licensing

This code is made available under an MIT License.

## TODO:

* Complete analysis notebooks for figure creation and general content for inclusion into the initial two academic papers
* Clean up and review the scrapers and debug fully the scraping and parsing pipeline
* Finalise dashboar release
* Docstrings for src

Last updated: 2020-06-27
