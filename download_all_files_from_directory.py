from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
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

    credentials = service_account.Credentials.from_service_account_file(key_file_location)

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
        # List all files in the folder
        folder_id = '1sBiKii7SMjq4G2ar3qkTbQHLOlhwGelH'
        download_dir = 'contracts'
        results = service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                   pageSize=1000, fields="nextPageToken, files(id, name)").execute()
        files = results.get('files', [])

        # Download each file from the folder
        for file in files:
            request_file = service.files().get_media(fileId=file['id'])
            # Get the file metadata
            file_metadata = service.files().get(fileId=file['id']).execute()
            filename = file_metadata['name']

            # Download the file content
            fh = open(os.path.join("contracts", filename), 'wb')
            downloader = MediaIoBaseDownload(fh, request_file)

            done = False
            while done is False:
                status, done = downloader.next_chunk()

            print('File downloaded successfully.')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
