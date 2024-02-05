# ETL data pipeline application for Tydo (POC)

## About

This assignment orchestrates an ETL process that extracts data from Google BigQuery public crypto_zillqa dataset, processes it, and then uploads the results to an AWS S3 using LocalStack for local emulation. The result is single file with parquet file format.


## Local operating Architecture

![image](https://github.com/arun5k1095/ETLpipelineTydo/assets/46933151/342f8e49-cd9b-48a4-89b3-ba043cc5d32f)


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
2. **Set current Working directory**
   ```
   cd ETLpipelineTydo
   ```
2. **Google Cloud Credentials**
    - Replace `Gcloud_Creds_test_user.json` with your Google Cloud service account key file.
    
    To get this  :
	- Sign up for a Google Cloud account.
	- Create a project in your Google Cloud Console.
	- Enable the BigQuery API for your project.
	- Create a service account in the IAM & Admin section , and assign the "BigQuery User" role to it.
	- Download the service account credentials in JSON format, which we are using as Gcloud_Creds_Arun.json file.

3. **Build and Run**
   
   In your CLI give following command to build  and spin off the containers :
    ```
    docker-compose up --build
    ```

## Usage

After spinning off the containers via docker, the application will:
1. Extract data from Google BigQuery.
2. Transform the data according to the logic defined in `main.py`.
3. Upload the transformed data to the emulated S3 service in LocalStack.


The image below displays the output what you shall observe if you follow these steps , here code was modifed to fetch only part of whole data: :


![image](https://github.com/arun5k1095/ETLpipelineTydo/assets/46933151/caac5560-c1f3-493c-83ef-94d0870d7f1d)
![image](https://github.com/arun5k1095/ETLpipelineTydo/assets/46933151/5d937bbb-3680-4cd5-bdb4-59ef55849fa0)
![image](https://github.com/arun5k1095/ETLpipelineTydo/assets/46933151/146a9b1f-748f-4927-87c8-e8ef12bf0955)



## Accessing Data

To access the uploaded files in LocalStack's S3:
- Use AWS CLI configured for LocalStack
   ```aws --endpoint-url=http://localhost:4566 s3 ls```

## Notes :
While this app was coded and tested on Windows, I hope it cooperates on Mac or Linux as well. In case you not, yo'ure free to make any necessary OS-specific changes.

And few thoughts towards how this applicaiton could be scaled in production grade env :

**Scaling Opinion :**
- Scale by adding more application server instances behind the load balancer for increased capacity.
- Implement database scaling techniques for handling data growth.

**Edge cases :**
- Monitoring for resource limits and unexpected cost spikes.
- Implement robust error handling and retry mechanisms, especially when interacting with external services.
- Pay attention to security measures, including access controls and encryption, to protect sensitive data.


