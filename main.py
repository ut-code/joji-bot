import requests
import feedparser
import os

# --- Configuration ---
import os
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
CHANNEL_ID = 'UCGxzWLH1_1ABKKfSiy2WIAw'
RSS_URL = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'
LAST_ID_FILE = 'last_video_id.txt' # File to store the previous video ID

def main():
    # Fetch RSS feed
    response = requests.get(RSS_URL)
    feed = feedparser.parse(response.content)
    if not feed.entries:
        print("No entries found in RSS feed")
        return

    latest_video = feed.entries[0]
    latest_id = latest_video.id.split(':')[-1] # Extract video ID
    video_url = latest_video.link
    video_title = latest_video.title
    print(f"Latest video: {video_title} (ID: {latest_id})")

    # Compare with previously sent ID
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, 'r') as f:
            last_id = f.read().strip()
        if last_id == latest_id:
            print(f"No new video (last ID: {last_id})")
            return # Exit if no update

    # Send notification to Discord
    message = {
        "content": f"**{video_title}**\nNew video uploaded!\n{video_url}"
    }
    res = requests.post(WEBHOOK_URL, json=message)
    print(f"Discord response: {res.status_code}")
    
    if res.status_code == 204:
        # Save the latest ID on success
        with open(LAST_ID_FILE, 'w') as f:
            f.write(latest_id)
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {res.text}")

if __name__ == "__main__":
    main()
