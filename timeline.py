import base64

import streamlit.components.v1 as components

from rhythm import get_beat_marker_positions


def show_animated_timeline(
    high_beats,
    low_beats,
    beats_per_measure,
    measure_seconds,
    audio_bytes,
):
    """Draw an animated timeline with a playhead synced to the audio player."""
    high_markers = get_beat_marker_positions(high_beats, beats_per_measure)
    low_markers = get_beat_marker_positions(low_beats, beats_per_measure)
    audio_base64 = base64.b64encode(audio_bytes).decode()

    def marker_html(positions, row_name):
        html = ""

        for position in positions:
            beat_time = position / 100 * measure_seconds
            downbeat_class = " downbeat-marker" if position == 0 else ""
            html += f"""
            <span
                class="beat-marker {row_name}{downbeat_class}"
                style="left: {position}%;"
                data-beat-time="{beat_time}"
            ></span>
            """

        return html

    beat_lines_html = ""

    for beat in range(beats_per_measure + 1):
        beat_percent = beat / beats_per_measure * 100
        downbeat_class = " downbeat-line" if beat == 0 else ""
        beat_lines_html += f"""
        <span
            class="beat-line{downbeat_class}"
            style="left: {beat_percent}%;"
        ></span>
        """

    html = f"""
    <style>
        .timeline-wrapper {{
            font-family: sans-serif;
            margin-top: 1rem;
            margin-bottom: 1rem;
            color: #f5f5f5;
        }}

        .timeline-title {{
            font-weight: 700;
            margin-bottom: 0.75rem;
        }}

        .timeline {{
            position: relative;
            height: 180px;
            border: 1px solid #dddddd;
            border-radius: 8px;
            background: #ffffff;
            overflow: hidden;
        }}

        .beat-line {{
            position: absolute;
            top: 24px;
            bottom: 24px;
            width: 1px;
            background: #dddddd;
        }}

        .downbeat-line {{
            width: 3px;
            background: #111111;
        }}

        .rhythm-row {{
            position: absolute;
            left: 90px;
            right: 24px;
            height: 50px;
            border-top: 1px solid #999999;
        }}

        .high-row {{
            top: 58px;
        }}

        .low-row {{
            top: 118px;
        }}

        .row-label {{
            position: absolute;
            left: 16px;
            width: 64px;
            font-size: 13px;
            color: #333333;
        }}

        .high-label {{
            top: 48px;
        }}

        .low-label {{
            top: 108px;
        }}

        .beat-marker {{
            position: absolute;
            top: -10px;
            width: 20px;
            height: 20px;
            transform: translateX(-50%);
            border: 2px solid #111111;
            border-radius: 50%;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
        }}

        .high {{
            background: #2E86AB;
        }}

        .low {{
            background: #C44536;
        }}

        .downbeat-marker {{
            width: 28px;
            height: 28px;
            top: -14px;
            border-width: 3px;
        }}

        .active-marker {{
            transform: translateX(-50%) scale(1.35);
            box-shadow: 0 0 0 5px rgba(17, 17, 17, 0.15);
        }}

        .playhead {{
            position: absolute;
            top: 20px;
            bottom: 20px;
            left: 90px;
            width: 3px;
            background: #111111;
        }}

        .loop-note {{
            margin-top: 0.5rem;
            color: #cfcfcf;
            font-size: 13px;
        }}

        .audio-controls {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.9rem;
        }}

        .play-button {{
            border: 0;
            border-radius: 999px;
            background: #ffffff;
            color: #111111;
            cursor: pointer;
            font-size: 15px;
            font-weight: 700;
            min-width: 88px;
            padding: 0.6rem 1rem;
        }}

        .time-label {{
            color: #cfcfcf;
            font-size: 14px;
        }}
    </style>

    <div class="timeline-wrapper">
        <div class="timeline-title">Animated rhythm timeline</div>
        <div class="timeline" id="rhythm-timeline">
            <div class="row-label high-label">High</div>
            <div class="row-label low-label">Low</div>
            <div class="rhythm-row high-row">
                {beat_lines_html}
                {marker_html(high_markers, "high")}
            </div>
            <div class="rhythm-row low-row">
                {beat_lines_html}
                {marker_html(low_markers, "low")}
            </div>
            <div class="playhead"></div>
        </div>
        <div class="loop-note">
            Press play to hear the rhythm and watch the playhead follow the beat.
        </div>
        <div class="audio-controls">
            <button class="play-button" id="play-button">Play</button>
            <span class="time-label" id="time-label">0:00</span>
        </div>
    </div>

    <script>
        const timeline = document.getElementById("rhythm-timeline");
        const playhead = document.querySelector(".playhead");
        const markers = document.querySelectorAll(".beat-marker");
        const playButton = document.getElementById("play-button");
        const timeLabel = document.getElementById("time-label");
        const measureSeconds = {measure_seconds};
        const audioBase64 = "{audio_base64}";
        const audioContext = new AudioContext();
        let audioBuffer = null;
        let source = null;
        let isPlaying = false;
        let startedAt = 0;
        let pausedAt = 0;
        let animationFrameId = null;

        function base64ToArrayBuffer(base64) {{
            const binaryString = window.atob(base64);
            const bytes = new Uint8Array(binaryString.length);

            for (let i = 0; i < binaryString.length; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}

            return bytes.buffer;
        }}

        async function loadAudioBuffer() {{
            if (audioBuffer === null) {{
                const audioData = base64ToArrayBuffer(audioBase64);
                audioBuffer = await audioContext.decodeAudioData(audioData);
            }}

            return audioBuffer;
        }}

        function getPlaybackTime() {{
            if (audioBuffer === null) {{
                return 0;
            }}

            if (isPlaying) {{
                return (audioContext.currentTime - startedAt) % audioBuffer.duration;
            }}

            return pausedAt;
        }}

        function formatTime(seconds) {{
            const wholeSeconds = Math.floor(seconds);
            const minutes = Math.floor(wholeSeconds / 60);
            const remainingSeconds = wholeSeconds % 60;

            return minutes + ":" + String(remainingSeconds).padStart(2, "0");
        }}

        function updateTimeline() {{
            const playbackTime = getPlaybackTime();
            const measureTime = playbackTime % measureSeconds;
            const measurePercent = measureTime / measureSeconds;
            const timelineWidth = timeline.clientWidth;
            const leftEdge = 90;
            const rightEdge = 24;
            const playableWidth = timelineWidth - leftEdge - rightEdge;

            playhead.style.left = leftEdge + measurePercent * playableWidth + "px";
            timeLabel.textContent = formatTime(playbackTime);

            markers.forEach(function(marker) {{
                const beatTime = Number(marker.dataset.beatTime);
                const distance = Math.abs(measureTime - beatTime);
                const wrappedDistance = Math.min(distance, measureSeconds - distance);

                if (wrappedDistance < 0.06) {{
                    marker.classList.add("active-marker");
                }} else {{
                    marker.classList.remove("active-marker");
                }}
            }});

            if (isPlaying) {{
                animationFrameId = requestAnimationFrame(updateTimeline);
            }}
        }}

        async function playLoop() {{
            await audioContext.resume();
            const buffer = await loadAudioBuffer();

            source = audioContext.createBufferSource();
            source.buffer = buffer;
            source.loop = true;
            source.connect(audioContext.destination);
            source.start(0, pausedAt);

            startedAt = audioContext.currentTime - pausedAt;
            isPlaying = true;
            playButton.textContent = "Pause";
            updateTimeline();
        }}

        function pauseLoop() {{
            if (source !== null) {{
                source.stop();
                source.disconnect();
                source = null;
            }}

            pausedAt = getPlaybackTime();
            isPlaying = false;
            playButton.textContent = "Play";
            cancelAnimationFrame(animationFrameId);
            updateTimeline();
        }}

        playButton.addEventListener("click", async function() {{
            if (isPlaying) {{
                pauseLoop();
            }} else {{
                await playLoop();
            }}
        }});

        updateTimeline();
    </script>
    """

    components.html(html, height=320)
