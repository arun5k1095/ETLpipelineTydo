import os
import pandas as pd
from google.cloud import bigquery
import boto3

# Set your Google Cloud credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Gcloud_Creds_test_user.json"

# Initialize the BigQuery client
client = bigquery.Client()

# ID of the table to browse data rows
table_id = "bigquery-public-data.crypto_zilliqa.transactions"

# Fetch rows and directly convert to a pandas DataFrame
df = pd.DataFrame()

page_token = None  # Start with no page token
print("Connecting to database..")
while True:
    rows_iter = client.list_rows(table_id, max_results=5000, page_token=page_token)  # Fetch rows
    page = rows_iter.to_dataframe()  # Convert to pandas DataFrame

    # 1. Data Type Conversion
    page['block_timestamp'] = pd.to_datetime(page['block_timestamp'])
    page['amount'] = page['amount'].astype(float)
    page['gas_price'] = page['gas_price'].astype(float)

    # 2. Datetime Features Extraction
    page['year'] = page['block_timestamp'].dt.year
    page['month'] = page['block_timestamp'].dt.month
    page['day'] = page['block_timestamp'].dt.day
    page['weekday'] = page['block_timestamp'].dt.weekday

    df = pd.concat([df, page], ignore_index=True)

    print(f"Fetched {len(page)} rows from table {table_id}")

    if not rows_iter.next_page_token:
        break

    page_token = rows_iter.next_page_token
    break

print(f"Downloaded a total of {len(df)} rows from table {table_id}")



# Save the DataFrame to a Parquet file in a known location inside the container
output_file = "transformed_transactions.parquet"
df.to_parquet(output_file, index=False)

print(f"Data saved to {output_file}")

# Configure client to use LocalStack
s3 = boto3.client('s3', endpoint_url='http://localstack:4566', aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')

bucket_name = 'tydodata'

# Create the S3 bucket if it doesn't exist
if bucket_name not in [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]:
    s3.create_bucket(Bucket=bucket_name)


# Upload the Parquet file to the S3 bucket
s3.upload_file(output_file, bucket_name, "transformed_transactions.parquet")

print(f"Data uploaded to S3 bucket {bucket_name}")

