import boto3 
from botocore.config import Config
from support_agent.config import get_settings

settings = get_settings()

def get_s3_client(host="localhost", port=3900):
    client = boto3.client(
        "s3",
        region_name="garage",
        endpoint_url=f"http://{host}:{port}",
        aws_access_key_id=settings.db.s3_access_key_id,
        aws_secret_access_key=settings.db.s3_secret_access_key,
        config = Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            # Avoids checksum incompatibilities with newer boto3 versions
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        )
    )    
    return client

