from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import os

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = service_account.Credentials.from_service_account_file(
    key_file_location)

    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=scoped_credentials)

    return service

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/drive.file'
    key_file_location = 'service-account.json'

    try:
        # Authenticate and construct service.
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

        # Call the Drive v3 API
        folder_id = '1sBiKii7SMjq4G2ar3qkTbQHLOlhwGelH'
        dir_path = '/root/rps-contracts/build/contracts'

        for filename in os.listdir(dir_path):
            if filename.endswith(".json"):
                file_metadata = { 'name': filename, 'parents': [folder_id] }
                media = MediaFileUpload(os.path.join(dir_path, filename), mimetype='text/json')
                file = service.files().create(body=file_metadata, media_body=media,fields='id').execute()
                print(f"A new file was created: {file.get('id')}")
            else:
                print(f"Skipping file {filename}")
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
