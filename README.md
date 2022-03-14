# 3006_final
## Final Project Overview
### Group Members
<p> Elizabeth Fugikawa <br>
Brian McCullough </p>

### Analysis Objective
Compare crime rates to precipitation, by county in Colorado. 

### Datasets that will be utilized
[Crime Rates](https://data.colorado.gov/Public-Safety/Crimes-in-Colorado-1997-to-2015/6vnq-az4b) <br>
[Colorado precipitation](https://data.colorado.gov/Environment/Rain-Hail-and-Snow-in-Colorado-2015/mqid-8hv2) <br>
[Colorado County Seats](https://data-cdphe.opendata.arcgis.com/datasets/colorado-county-boundaries/) <br>

### Python functionalities
Pandas, Geopy, matplotlib, requests, argparse, logging, numpy 

### How to run this script
Required args - Year := 1999 through 2015
Optional args - --verbose := VERBOSE -> changes logging level for recording to the log file
              - --split := 7d, 30d, 90d -> changes the date range fences to apply to the considered ranges after a precipitation event

### Results of Analysis
Hypothesis: Rain causes a dip in immediate time frame crime. 

### Deliverables
1. This README file
2. Data files
3. requirements.txt file
4. Python scripts
5. Screenshot of console virtual environment
