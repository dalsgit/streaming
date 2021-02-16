--- Access token ---
1. Generate an access token with the following permissions:
Facebook App: LiveManager
User or Page: Sikh Sabha of NJ
Permissions:
    publish_video
    pages_show_list
    pages_read_engagement
    pages_manage_posts
    public_profile

https://developers.facebook.com/tools/explorer/?method=POST&path=610250765656576%2Flive_videos%3Fstatus%3DLIVE_NOW%26title%3DToday%2527s%2520Live%2520Video&version=v9.0

2. Take the token and go to Tools > Access Token Debugger
3. Click on extend life and use the token that you receive

--- Facebook Post ---
response = requests.post('https://graph.facebook.com/v9.0/610250765656576/live_videos?status=LIVE_NOW&title=Today's%20Live%20Video&access_token=EAADMZBhiQHmEBAEMoqllO7SVEuRhPOguMuYxJEfFBPnDSVidzu7a1KfxdwFlmfRZBWOWKNrOc2bwT0CdUlsoOrO4m11Ws7E7abXR0aZCLZCNa9vL7KTTfLZAvbZC63KfPfkSrvZANOCoZAzs0R4JAN2vKAkXsn2lIlNltPm5EKb6WH4NBHQQDOywTCKuy2Mq1xE6UmmzZAfJlA0oHR0ywumdN')

--- Setup ---
Check requirements file for list of packages
