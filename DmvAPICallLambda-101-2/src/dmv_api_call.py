import json
import logging
import csv
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# Read the underwriting validation prompt from the local file system
with open('/var/task/underwriting_validation.prompt') as f:
    UNDERWRITING_VALIDATION_PROMPT = f.read()

def load_csv_from_s3(bucket_name, file_key):
    local_path = '/tmp/generated_ids.csv'
    s3.download_file(bucket_name, file_key, local_path)
    with open(local_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Load the DMV dataset from S3
dmv_records = load_csv_from_s3('generated-dmv-dataset', 'generated_ids.csv')

def fetch_dmv_record_from_dataset(license_id):
    for record in dmv_records:
        if record['ID Number'] == license_id:
            return {
                "license_status": record['License Type'],
                "violations": record['Violation Code Description'].split(",") if record['Violation Code Description'] else ["none"],
                "vehicle": record['Vehicle'],
                "vehicle_use": record['Vehicle Use'],
                "prior_insurance_coverage": record['Prior Insurance Coverage'],
                "marital_status": record['Marital Status'],
            }
    return {
        "license_status": "unknown",
        "violations": ["none"],
        "vehicle": "unknown",
        "vehicle_use": "unknown",
        "prior_insurance_coverage": "unknown",
        "marital_status": "unknown"
    }

def append_dmv_record_to_prompt(dmv_record, prompt):
    driver_info = [f"{key}:{','.join(value) if isinstance(value, list) else value}" for key, value in dmv_record.items()]
    driver_info_str = ",".join(driver_info)
    return prompt.replace("\n<driver>\n</driver>", f"\n<driver>\n{driver_info_str}\n</driver>")

def lambda_handler(event, context):
    try:
        logger.info(json.dumps(event))

        first_name = event['Body']['content'][0]['text'].split(',')[0].split(':')[1].strip()
        last_name = event['Body']['content'][0]['text'].split(',')[1].split(':')[1].strip()
        license_id = event['Body']['content'][0]['text'].split(',')[2].split(':')[1].strip()

        logger.info(f"First Name: {first_name}, Last Name: {last_name}, License ID: {license_id}")

        dmv_record = fetch_dmv_record_from_dataset(license_id)
        underwriting_prompt = append_dmv_record_to_prompt(dmv_record, UNDERWRITING_VALIDATION_PROMPT)

        return {
            'statusCode': 200,
            'body': underwriting_prompt
        }

    except Exception as e:
        logger.error(f"Error occurred while processing the event: {e}")
        return {
            'statusCode': 500,
            'body': 'An error occurred while processing your request.'
        }





