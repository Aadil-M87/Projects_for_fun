import re
from googleapiclient.discovery import build
from datetime import timedelta
from googleapiclient.errors import HttpError

api_key = "AIzaSyABkJtC1toPoeapbXsTQOsRDOpcPbGEkaA"
try:
    youtube = build("youtube", "v3", developerKey=api_key)
    nextPageToken = None
    total_sec = 0
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')


    while True:
        pl_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId='PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU',
            maxResults=50,
            pageToken=nextPageToken

        )

        pl_response = pl_request.execute()
        vid_ids = []
        for item in pl_response["items"]:
            vid_ids.append(item['contentDetails']['videoId'])
        vid_request = youtube.videos().list(
            part='contentDetails',
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()



        for item in vid_response['items']:
            vid_duration = item['contentDetails']['duration']

            hours = hours_pattern.search(vid_duration)
            minutes = minutes_pattern.search(vid_duration)
            seconds = seconds_pattern.search(vid_duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=float(hours),
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_sec += video_seconds

        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken:
            break
except HttpError as e:
    print(f"An HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

total_sec = int(total_sec)

minutes, seconds = divmod(total_sec,60)
hours, minutes = divmod(minutes, 60)

print(f"{hours}:{minutes}:{seconds}")
