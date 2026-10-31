import boto3 
from support_agent.config import get_settings


def get_client(endpoint_url="http://localhost:3900"):
    client = boto3.client(
        "s3",
        region_name="garage",
        endpoint_url=endpoint_url,
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

