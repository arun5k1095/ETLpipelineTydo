#ETL data pipeline application for Tydo (POC)

## About

This assignment orchestrates an ETL process that extracts data from Google BigQuery public crypto_zillqa data set, processes it, and then uploads the results to an AWS S3 using LocalStack for local emulation. 



## Docker operating Architecture

- **Application Container**: Executes the Python scriptto interact with BigQuery to extract data, transforms, and load it into a simulated S3 bucket in LocalStack as transformed_transactions.parquet file.

- **LocalStack Container**: Simulates AWS cloud services locally.

## System Setup and Installation

### Prerequisites

- Docker must be installed in your windows
- A Google Cloud Platform account with a service account key for BigQuery access.
  However, for this assinment, for time being i have already provided a credential file as a test service account user.
- AWS cli installed in the system (Optional though).

### Configuration Steps and run process

1. **Clone the Repository**
    ```
    git clone https://github.com/arun5k1095/ETLpipelineTydo.git
    ```
   
2. **Google Cloud Credentials**
    - Replace `Gcloud_Creds_test_user.json` with your Google Cloud service account key file.

3. **Build and Run**
	In your CLI  , set the CWD as this cloned project , and give following command 
    ```
    docker-compose up --build
    ```

## Usage

After spinning off the containers via docker, the application will:
1. Extract data from Google BigQuery.
2. Transform the data according to the logic defined in `main.py`.
3. Upload the transformed data to the emulated S3 service in LocalStack.

## Accessing Data

To access the uploaded files in LocalStack's S3:
- Use AWS CLI configured for LocalStack
   e.g  command :  aws --endpoint-url=http://localhost:4566 s3 ls

