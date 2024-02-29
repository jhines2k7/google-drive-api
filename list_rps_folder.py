from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import datetime

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
    scope = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    key_file_location = 'service-account.json'

    try:
        folder_name = 'rock-paper-scissors-v2'
        # Authenticate and construct service.
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)
        
        results = service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'").execute()
        folders = results.get('files', [])

        # Print the folder's ID if found
        if len(folders) > 0:
            folder_id = folders[0]['id']
            print(folders[0]['id'])
        else:
            print("Folder not found.")

        query = f"'{folder_id}' in parents"

        # Call the Drive v3 API
        results = service.files().list(
            q=query, spaces='drive', fields="nextPageToken, files(id, name, createdTime)", pageToken=None).execute()
        files = results.get('files', [])

        if not files:
            print('No files found.')
            return
        for file in files:
            file_name = file['name']
            created_time = datetime.datetime.strptime(file['createdTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            print(f"File Name: {file_name}, Created Time: {created_time}")
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
