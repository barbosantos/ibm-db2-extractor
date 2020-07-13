import logging
import sys
import os

from google.cloud.exceptions import NotFound
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import secretmanager
from config import dataset_location

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def dataset_exists(client, dataset_ref):
    try:
        client.get_dataset(dataset_ref)
        return True
    except NotFound:
        return False


def upload_to_bigquery(df, table_nm, dataset_nm, SCHEMA):
    try:
        client = bigquery.Client()

        dataset = bigquery.Dataset('{}.{}'.format(client.project, dataset_nm))
        dataset.location = dataset_location
        if not dataset_exists(client, dataset):
            dataset = client.create_dataset(dataset)  # Make an API request.
            logger.info("Created dataset {}.{}".format(client.project, dataset.dataset_id))

        table_id = '{}.{}'.format(dataset.dataset_id, table_nm)
        
        job_config = bigquery.LoadJobConfig(schema=SCHEMA)
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        # Wait for the load job to complete.
        job.result()
        logger.info("Uploading %s completed", table_id)
        return "Uploading {} completed!".format(table_id)
    except Exception as e:
        logger.exception(e)
        logger.error("Uploading %s failed!", table_id)
        return "Uploading {} failed!".format(table_id)


def access_secret_version(project_id, secret_id, version_id='latest'):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = client.secret_version_path(project_id, secret_id, version_id)
    # Access the secret version.
    response = client.access_secret_version(name)
    return response.payload.data.decode('UTF-8')