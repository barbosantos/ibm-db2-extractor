# DB2 EXTRACTOR #

Extracts tables from IBM DB2 and export to Bigquery.
The job is executed as a web service deployed on Cloud Run and scheduled via Cloud Scheduler.

This is an example of a simple ETL; good for small jobs that don't need many computational resources.

## Changelog

0.0.1
- Export DB2 data to Google Bigquery
