import subprocess

import googlesearch


def mpris_get_metadata_field(field):
    result = subprocess.run(
        ["playerctl", "metadata", field], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    value = result.stdout.decode("utf-8").strip()
    return value if value and result.returncode == 0 else None


def google_spotify_url(query):
    search_results = googlesearch.search("spotify " + query, num_results=10)
    for result in search_results:
        if result.find("open.spotify.com/track") != -1:
            return result
    return None


def download(spotify_url, output):
    subprocess.run(["spotdl", "--output", output, "download", spotify_url])


def default_music_dir():
    result = subprocess.run(["xdg-user-dir", "MUSIC"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip() or "$HOME/Music"


def main():
    title = mpris_get_metadata_field("title")
    if not title:
        print("Unable to get title")
        exit(1)

    artist = mpris_get_metadata_field("artist")
    if not artist:
        print("Couldn't get artist")
        exit(1)

    query = title + " " + artist
    spotify_url = google_spotify_url(query)
    if not spotify_url:
        print("Couldn't get spotify url")
        exit(1)

    download(spotify_url, default_music_dir())


if __name__ == "__main__":
    main()
