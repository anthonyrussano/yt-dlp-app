import os
import datetime
from flask import Flask, render_template, request, send_file, after_this_request
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Set the download folder
download_folder = "downloads"


def cleanup_downloads():
    """
    Clean up the downloaded files in the specified folder.
    Only files older than 24 hours will be deleted.
    """
    current_time = datetime.datetime.now()
    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        if os.path.isfile(file_path):
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if (current_time - modified_time).total_seconds() >= 24 * 60 * 60:
                os.remove(file_path)


@app.route("/", methods=["GET", "POST"])
def download_video():
    if request.method == "POST":
        url = request.form["url"]

        # Set download options for yt-dlp
        ydl_opts = {
            "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # Get the downloaded file path
        file_path = os.path.join(download_folder, info["title"] + "." + info["ext"])

        @after_this_request
        def delete_file(response):
            # Delete the file after the response has been sent
            os.remove(file_path)
            return response

        return send_file(file_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    app.run(host="0.0.0.0", debug=True, port=8920)
