# NHSSpend

[![Generic badge](https://img.shields.io/badge/Python-3.6-<red>.svg)](https://shields.io/)  [![Generic badge](https://img.shields.io/badge/License-MIT-blue.svg)](https://shields.io/)  [![Generic badge](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://shields.io/)
---

## Introduction

This is a library to scrape and reconcile all payments made by a hiarcharcy of NHS institutions over time. It is the final of three projects on public procurement data (the first two of which were [centgovspend](https://github.com/crahal/centgovspend) and [TSRC-NCVO-CSDP](https://github.com/crahal/TSRC-NCVO-CSDP)).

## Pre-reqs

NHSSpend tries to minimize the number of pre-requisite installations outside of the standard library, and we recommend an Anaconda installation to provide a comprehensive set of basic tools. However, a couple are necessary due to the magnitude of the undertaking. These include; ```BeautifulSoup```,..., and can be found in the requirements.txt file.  

## Data Origination
The data originates from the list of recognised NHS institutions as found on [this](https://www.nhs.uk/ServiceDirectories/Pages/NHSTrustListing.aspx) page. This list is used to create a substantial dictionary (NHSInstitutions.txt, found at data\support) with a number of different parametres fed into the scraper (src\NHSscraper.py). For example, the dictionary contains a link to the procurement data of each institution (i.e. CCG, Trust, etc.). However, please do raise issues on this repo or via e-mail if you think any of the institutions are mislabelled, outdated, require updating or if you think any other institutions should be added. A useful introduction to and definition of each of these types of institution can be found [here](https://www.nhs.uk/using-the-nhs/about-the-nhs/nhs-authorities-and-trusts/). The procurement data itself is provided under an [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) (OGL). Guidance for publishing spend over £25,000 is published by [HM Treasury](https://www.gov.uk/government/publications/guidance-for-publishing-spend-over-25000)


## TODO:

* Write all scrapers
* Integrate the ES and PDF parsing modules
* Write a parser
* Reconcile with cached bulk downloads
* Make reconcilations read from an offline dictionary of manual matches.
* Visualisation

Last updated: 2019-09-9
