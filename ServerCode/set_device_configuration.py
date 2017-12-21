

import base64
import datetime
import json

import googleapiclient
import jwt
import requests
from google.oauth2 import service_account
from googleapiclient import discovery

service_account_json = 'UniversalClockAndWeather-d07ba0b7dfb9.json' # Location of the server service account credential file
device_id = 'rasp123'  # Enter your Device ID here
project_id = 'universalclockandweather'  # Enter your project ID here
registry_id = 'raspberrym123'  # Enter your Registry ID here
configuration_payload = 'Test Configuration'  # This is the configuration to be sent to the device, any binary data should work

# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
###

device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
    project_id, cloud_region, registry_id, device_id)


def get_client():
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)


body = {"versionToUpdate": "0", "binaryData": base64.urlsafe_b64encode(configuration_payload)}

print get_client().projects().locations().registries().devices().modifyCloudToDeviceConfig(name=device_name,
                                                                                           body=body).execute()
