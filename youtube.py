api_key="AIzaSyC2maF-9v1KW2Z9KMd9CX3Rj1NhqXpdOYM"
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

youtube = build('youtube', 'v3', developerKey=api_key)
print(youtube)
req = youtube.search().list(q='avengers', part='snippet', type='video')
res = req.execute()
print(res)


CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)