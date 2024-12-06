import json
import requests
from datetime import datetime, timedelta
from utils import setup_logger, get_config

logger = setup_logger(__name__)


def test_keys():
    config = get_config()
    logger.info("Testing keys")
    account_id = config.get('app', 'account_id')
    headers = get_headers(config)
    whitelist = config.get('app', 'whitelist')
    videos = list_videos(account_id, headers)
    if videos is None:
        return "No Videos"
    else:
        logger.info("Found {} videos".format(len(videos)))
        return


def get_headers(config):
    # Headers for authentication
    headers = {
        'X-Auth-Email': config.get('app', 'email'),
        'X-Auth-Key': config.get('app', 'api_key'),
        'Content-Type': 'application/json',
    }
    return headers


def list_videos(account_id, headers):
    # Fetches a list of all videos
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/stream'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['result']
    else:
        logger.info('Error fetching video list:', response.json())
        return []


def delete_video(account_id, video_id, headers):
    # Deletes a specific video
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video_id}'
    response = requests.delete(url, headers=headers)
    return response.status_code == 200





def clean_videos():
    config = get_config()
    account_id = config.get('app', 'account_id')
    headers = get_headers(config)
    whitelist = config.get('app', 'whitelist')
    one_year_ago = datetime.now() - timedelta(days=365)
    videos = list_videos(account_id, headers)
    for video in videos:
        created_date = datetime.strptime(video['created'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if created_date < one_year_ago:
            if not video['uid'] in whitelist:
                logger.info(f"Deleted video: {video['uid']}")

                if delete_video(account_id, video['uid'], headers):
                    logger.info(f"Deleted video: {video['uid']}")
                    logger.info(video['meta']['name'])
                    logger.info(video['created'])
                else:
                    logger.info(f"Failed to delete video: {video['uid']}")
            else:
                logger.info(f"Skipping Whitelist Video: {video['uid']}")


def update_video(account_id, video_id, headers, payload):
    """Updates a specific video's metadata on Cloudflare Stream"""
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video_id}'

    # The payload should only include the metadata we want to update
    update_payload = {
        "meta": {
            "name": payload['meta']['name']
        }
    }

    # Cloudflare API expects PATCH method for updates
    response = requests.post(url, headers=headers, json=update_payload)

    if response.status_code != 200:
        logger.error(f"Error updating video: {response.json()}")

    return response.status_code == 200


def clean_names():
    config = get_config()
    account_id = config.get('app', 'account_id')
    headers = get_headers(config)
    whitelist = config.get('app', 'whitelist').split(',')  # Assuming comma-separated whitelist

    videos = list_videos(account_id, headers)
    for video in videos:
        if video['uid'] in whitelist:
            logger.info(f"Skipping Whitelist Video: {video['uid']}")
            continue

        original_name = video['meta']['name']
        if ".mp4" in original_name:
            new_name = original_name.replace(".mp4", "")

            # Only update if the name has actually changed
            if new_name != original_name:
                update_payload = video.copy()
                update_payload['meta']['name'] = new_name

                if update_video(account_id, video['uid'], headers, update_payload):
                    logger.info(f"Successfully updated video: {video['uid']}")
                    logger.info(f"New name: {new_name}")
                else:
                    logger.error(f"Failed to update video: {video['uid']}")


if __name__ == "__main__":
    clean_names()
