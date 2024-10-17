import streamlit.components.v1 as components


def custom_audio_player(audio_url=None):
    with open('frontend/static/style.css', 'r') as f:
        css = f'<style>{f.read()}</style>'
    custom_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap" rel="stylesheet">
        {css}
    </head>
    <body>
        <div class="audio-container">
            <audio id="audioPlayer" src="{audio_url}"></audio>
            <button id="playPauseBtn" class="play-button">Play</button>
        </div>

        <script>
            var audio = document.getElementById('audioPlayer');
            var playPauseBtn = document.getElementById('playPauseBtn');

            playPauseBtn.addEventListener('click', function() {{
                if (audio.paused) {{
                    audio.play();
                    playPauseBtn.textContent = 'Pause';
                }} else {{
                    audio.pause();
                    playPauseBtn.textContent = 'Play';
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(custom_html, height=100)
