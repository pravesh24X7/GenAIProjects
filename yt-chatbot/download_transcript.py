from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

video_id = input("Input VideoId: ").strip()

ytt_api = YouTubeTranscriptApi()

try:
    transcript_list = ytt_api.fetch(video_id, languages=["en"])
    transcript = " ".join(chunk.text for chunk in transcript_list)

except TranscriptsDisabled:
    print("NO CAPTIONS FOUND!!!")

else:
    with open(f"{video_id}-transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"[+] Data saved to {video_id}-transcript.txt")