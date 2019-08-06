
## Introduction
Here we have two scripts that was designed to fetch specific data from Zabbix via API.

- **zabbix_info_local_final.py**
  
  This script will collect information about active and all configured triggers, discovery rules and trigger protorypes, and also about 
  web checks for all active hosts in zabbix and store that data to few general csv files named like type of data.
  
  So, as a result we will have 5 files with all that fetched data inside for each host.

- **zabbix_info_local_separate_final.py**

  This script will collect information about active and all configured triggers, discovery rules and trigger protorypes, and also about 
  web checks for all active hosts in zabbix and store that data to a separate csv files named like hostname.
  
  So, as a result we will have one file for each host with all that fetched information inside.


## Notes

Custom scripts were written using Python 3.7
