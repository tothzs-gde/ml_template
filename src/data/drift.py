from io import BytesIO

import pandas as pd
from uuid_extensions import uuid7str

from src.utils.minio import create_drift_bucket
from src.utils.minio import minio_client
from src.utils.settings import settings



def export_drift_data(X_drift, y_drift):
    '''

    Args:

    Returns:
        Name of the drift set file in the drift bucket.
    '''
    
    create_drift_bucket()

    df = pd.concat([X_drift, y_drift], axis=1)

    drift_set_name = uuid7str()  # UUID with timestamp
    filename = f"{drift_set_name}.csv"
    
    with BytesIO() as buffer:
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        minio_client.put_object(
            bucket_name=settings.minio_drift_bucket_name,
            object_name=filename,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="text/csv"
        )
    
    return drift_set_name


if __name__ =="__main__":

    import uuid

    for i in range(5):
        print(uuid.uuid1())