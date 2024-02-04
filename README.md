# ETL data pipeline application for Tydo (POC)

## About

This assignment orchestrates an ETL process that extracts data from Google BigQuery public crypto_zillqa dataset, processes it, and then uploads the results to an AWS S3 using LocalStack for local emulation. The result is single file with parquet file format.


## Local operating Architecture

                         Start prrocess
		           |
               Spin Off Two Containers in Docker
              /                       \
  Application Container               LocalStack Container
     Interact with BigQuery                 |
     Transform Data                         |
     Aggregate into DataFrame               |
     Save as Parquet file    ------->       S3 bucket     

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

## Notes :
While this app was coded and tested on Windows, I hope it cooperates on Mac or Linux as well. In case you not, yo'ure free to make any necessary OS-specific changes.

And few thoughts towards how this applicaiton could be scaled in production grade env :

**scaling Opinion :**
- Scale by adding more application server instances behind the load balancer for increased capacity.
- Implement database scaling techniques for handling data growth.

**Edge cases :**
- Monitoring for resource limits and unexpected cost spikes.
-Implement robust error handling and retry mechanisms, especially when interacting with external services.
- Pay attention to security measures, including access controls and encryption, to protect sensitive data.


