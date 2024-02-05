import os
import pandas as pd
from google.cloud import bigquery
import boto3
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

try:
    # Set Google ADC as env variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Gcloud_Creds_test_user.json"

    log.info("Google Cloud credentials set successfully.")

    # Initialize the BigQuery client
    client = bigquery.Client()

    log.info("BigQuery client initialized.")

except Exception as e:
    log.error(f"Error initializing Google BigQuery client: {e}")
    exit()

# Database id
DBTableID = "bigquery-public-data.crypto_zilliqa.transactions"

df = pd.DataFrame()

PageToken = None

chunkSize = 5000  # based on the system capabilities
SampleSize = 100  # for calculating incrimental statistics of chunks

try:
    while True:
        RowsIteretable = client.list_rows(DBTableID, max_results=chunkSize, page_token=PageToken)
        page = RowsIteretable.to_dataframe()

        # Transforming certain data's data-type
        page['block_timestamp'] = pd.to_datetime(page['block_timestamp'])
        page['amount'] = page['amount'].astype(float)
        page['gas_price'] = page['gas_price'].astype(float)

        # Extracting elements from timestamp
        page['year'] = page['block_timestamp'].dt.year
        page['month'] = page['block_timestamp'].dt.month
        page['day'] = page['block_timestamp'].dt.day
        page['weekday'] = page['block_timestamp'].dt.weekday

        df = pd.concat([df, page], ignore_index=True)

        # Log incremental statistics for the chunk (using a sample)
        if len(page) > SampleSize:
            sample = page.sample(n=SampleSize)
        else:
            sample = page

        log.info(f"Sample statistics for this chunk:\n{sample[['amount', 'gas_price']].describe()}")

        log.info(f"Fetched {len(page)} rows from table {DBTableID}")

        if not RowsIteretable.next_page_token:
            break

        PageToken = RowsIteretable.next_page_token

        if len(df) > 20000: break  # COMMENT this line to fetch full data from bigquery

except Exception as e:
    log.error(f"Error fetching or processing data from BigQuery: {e}")
    exit()

log.info(f"Downloaded a total of {len(df)} rows from table {DBTableID}")

# Log final aggregated statistics for numerical columns
log.info(f"Final DataFrame statistics for 'amount' and 'gas_price':\n\
                                {df[['amount', 'gas_price']].describe()}")

# Saving and migrating to S3 in loclastack

try:
    OutputFile = "transformed_transactions.parquet"
    df.to_parquet(OutputFile, index=False)

    log.info(f"Data saved to {OutputFile}")

except Exception as e:
    log.error(f"Error saving data to Parquet file: {e}")
    exit()

try:
    s3 = boto3.client('s3', endpoint_url='http://localstack:4566', aws_access_key_id='test',
                      aws_secret_access_key='test', region_name='us-east-1')

    S3BucketName = 'tydodata'  # Set a s3 bucket name

    # Create a bucket if it is not there already
    if S3BucketName not in [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]:
        s3.create_bucket(Bucket=S3BucketName)

    s3.upload_file(OutputFile, S3BucketName, "transformed_transactions.parquet")
    log.info(f"Data uploaded to S3 bucket {S3BucketName}")
except Exception as e:
    log.error(f"Error configuring LocalStack S3 client or uploading file: {e}")
    exit()
