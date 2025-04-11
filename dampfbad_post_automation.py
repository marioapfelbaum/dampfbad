{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # dampfbad_post_automation.py\
# Automatisierter Workflow f\'fcr Instagram-Reel mit yt-dlp, ffmpeg, GitHub Upload und Instagram Posting\
\
import os\
import requests\
import subprocess\
from datetime import datetime\
\
ACCESS_TOKEN = "EAATNhZBBo8A0BO0U0w8sbbnAVrbV6pfjr2myBTZA2RpNVzcsevND2dp0xqlZBPaF83sVGwCJ3mS8AFrTpm8mbJA8L3KPtuZCUe03U2xgl74SLCaIg6w92BTZAxhoxIO9PCOxyIEE9IkaDObhgDqpoL9o1tMVP2MR8XvdTYhrvVZC3Vq74CcjcjdAZCxRGYLPa8H70NN9AH5Fqlhjp90jwZDZD"\
IG_USER_ID = "17841401998289420"\
\
# === 1. Clip-Info (dies k\'f6nnte auch aus einer JSON-Datei gelesen werden) ===\
youtube_url = "https://www.youtube.com/watch?v=mMfxI3r_LyA"\
clip_start = "00:17"\
clip_end = "00:37"\
cover_path = "cover.jpg"  # lokales Bild, optional in Video integrierbar\
output_path = "modjo_clip_ready.mp4"\
\
caption = (\
    "\uc0\u55356 \u57269  Track des Tages: Modjo \'96 Lady (Hear Me Tonight)\\n"\
    "\uc0\u55356 \u57255  Fun Fact: Der Track basiert auf einem Disco-Sample von Chic aus den fr\'fchen 80ern.\\n"\
    "\uc0\u55357 \u56599  https://open.spotify.com/track/6fHiG6wQpW3IofnBf9XDcT\\n"\
    "#HouseMusic #SampleFacts #Y2KRevival"\
)\
\
# === 2. Clip schneiden ===\
def download_and_cut():\
    print("\uc0\u55357 \u56549  Lade Video herunter und schneide...")\
    subprocess.run([\
        "yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",\
        "--download-sections", f"*\{clip_start\}-\{clip_end\}",\
        "-o", "temp_clip.%(ext)s",\
        youtube_url\
    ], check=True)\
\
    subprocess.run([\
        "ffmpeg", "-y", "-i", "temp_clip.mp4",\
        "-vf", "scale=720:720,setsar=1:1",\
        output_path\
    ], check=True)\
\
# === 3. Upload zu GitHub vorbereiten ===\
def upload_to_github():\
    print("\uc0\u11014 \u65039   Push zu GitHub...")\
    os.system(f"git add \{output_path\} && git commit -m 'Auto-Post: \{output_path\}' && git push")\
    # GitHub Actions k\'f6nnen nach dem Commit getriggert werden\
\
# === 4. Posten auf Instagram ===\
def post_to_instagram():\
    github_raw_url = f"https://raw.githubusercontent.com/marioapfelbaum/dampfbad/main/\{output_path\}"\
\
    create_container = requests.post(\
        f"https://graph.facebook.com/v19.0/\{IG_USER_ID\}/media",\
        params=\{\
            "media_type": "VIDEO",\
            "video_url": github_raw_url,\
            "caption": caption,\
            "access_token": ACCESS_TOKEN\
        \}\
    )\
    container_id = create_container.json().get("id")\
    print("Container-ID:", container_id)\
\
    if container_id:\
        publish = requests.post(\
            f"https://graph.facebook.com/v19.0/\{IG_USER_ID\}/media_publish",\
            params=\{\
                "creation_id": container_id,\
                "access_token": ACCESS_TOKEN\
            \}\
        )\
        print("Ergebnis:", publish.json())\
    else:\
        print("Fehler beim Erstellen des Containers:", create_container.json())\
\
\
if __name__ == "__main__":\
    download_and_cut()\
    upload_to_github()\
    post_to_instagram()\
}