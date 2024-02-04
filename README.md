# POC ETL data pipeline for Tydo

## Overview

This assignment orchestrates an ETL process that extracts data from Google BigQuery public crypto_zillqa data set, processes it, and then uploads the results to an AWS S3 using LocalStack for local emulation. 


## Architecture

- **Application Container**: Executes the Python scriptto interact with BigQuery to extract data, transforms, and load it into a simulated S3 bucket in LocalStack as transformed_transactions.parquet file.

- **LocalStack Container**: Simulates AWS cloud services locally.

## Setup and Installation

### Prerequisites

- Docker must be installed in your windows
- A Google Cloud Platform account with a service account key for BigQuery access.
  However, for this assinment, for time being i have already provided a credential file as a test service account user.

### Configuration Steps

1. **Clone the Repository**
    ```
    git clone <repository-url>
    ```
   
2. **Google Cloud Credentials**
    - Replace `Gcloud_Creds_test_user.json` with your Google Cloud service account key file.

3. **LocalStack Setup**
    - Ensure the `docker-compose.yaml` file is configured to include LocalStack services.

4. **Build and Run**
    ```
    docker-compose up --build
    ```

## Usage

After starting the containers, the application will:
1. Extract data from Google BigQuery using the provided service account credentials.
2. Transform the data according to the logic defined in `main.py`.
3. Upload the transformed data to the emulated S3 service in LocalStack.

## Accessing Data

To access the uploaded files in LocalStack's S3:
- Use AWS CLI configured for LocalStack, or
- Access LocalStack's web interface (if available) to navigate the S3 bucket contents.

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under [specify your license], providing freedom to use, modify, and distribute the software.
