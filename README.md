# DB2 EXTRACTOR #

Extracts a table from IBM DB2 and export to Bigquery.
The job is executed as a web service deployed on Cloud Run and can be scheduled via Cloud Scheduler.

This is an example of a simple ETL; good for small jobs that don't need many computational resources and don't take a long time to finish.

Test

## Changelog

0.0.1
- Export DB2 data to Google Bigquery
