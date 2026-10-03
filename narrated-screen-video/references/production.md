# Production notes

These settings reproduce the approved high-resolution app films. Treat them as starting points, not a requirement to use a particular tool or app. Discover the available tooling and verify capture behavior in the current environment.

## Native capture and layout

The successful browser capture used Playwright/Chromium with a 1280 × 960 CSS-pixel viewport, `deviceScaleFactor: 2`, and `recordVideo.size` set to 2560 × 1920. The final frames were inspected to confirm sharp native UI. The same recorder settings can behave differently with another browser or installation: record a short test and inspect it with `ffprobe` and extracted frames.

For 16:9, a possible starting point is 1920 × 1080 logical pixels at scale factor 2, with 3840 × 2160 capture. For a smaller, more readable app layout, use a smaller logical viewport at an appropriate scale factor and verify the result. Portrait requires a genuinely usable responsive layout. Do not crop important controls or choose dimensions merely because an encoder accepts them.

Browser video may be buffered until the recording context closes. Close the context and wait for the file to finish before editing. Use the actual recorded page/context, not a different tab. Verify the screen state after each significant interaction. Framework-specific input events matter: filling a search box may not trigger a key-up handler; use actual typing where required and confirm the results changed.

A subtle visible cursor helps explain clicks. Keep it small, move it deliberately, and ensure any cursor overlay cannot intercept pointer events. Avoid recording development tools, permission dialogs, or unrelated desktop content.

## Speech and timing

Use the configured speech provider supporting Cedar. In the tested workflow this was OpenAI speech generation with `gpt-4o-mini-tts`, voice `cedar`, and WAV output. Check current supported APIs and voices before use. Keep credentials in their existing secure configuration; never print them or include them in production files.

Useful delivery direction:

> Speak like a relaxed person showing a useful app to a friend. Warm, gentle lower register. Keep phrases connected and flowing. Pause between complete thoughts, not inside short clauses. No announcer delivery or exaggerated emphasis.

Generate narration in coherent chunks, each tied to a timeline segment. Store the text, start times, and filenames in working production notes. Measure real chunk durations before finalizing the timeline. Audition the opening and any tricky wording early. Correct unnatural pauses in text or delivery rather than globally slowing the narration.

Some streamed WAV responses have placeholder length headers, causing audio libraries to report an enormous duration. Remux such files through FFmpeg to normal PCM WAV, with a sensible maximum duration for that chunk, before reading durations or padding. Use `ffprobe` on the normalized file.

Every command that pads or loops media must have an explicit finite duration. For example, `apad` without an output `-t` can produce an effectively endless file. Set subprocess timeouts as well. Finalize a silent narration timeline of exactly the target duration, placing chunks at their approved start times, so the music-only ending has the correct length.

## Tested subtle mix

For a complete narration WAV and a music track already extended to at least the film duration, the following filter graph is a useful starting point. Substitute the numeric last-five-seconds start for `FADE_START` (for a 130-second video, 125). Input 0 is narration; input 1 is music.

```text
[0:a]volume=1.25,equalizer=f=4500:t=q:w=0.7:g=-2,asplit=2[voice][detector];
[1:a]volume=0.38,afade=t=in:d=1,afade=t=out:st=FADE_START:d=5[music];
[music][detector]sidechaincompress=threshold=0.012:ratio=3:attack=40:release=700[ducked];
[voice][ducked]amix=inputs=2:normalize=0,alimiter=limit=0.93:level=false,aresample=48000[mix]
```

The gain values depend on the input files. Audition and adjust them; `volume=1.25` is a gain on a relatively quiet source, not a request for loud voiceover. The modest high-frequency reduction softens the voice. Compression lowers music gently during speech and releases slowly between phrases. The approved films measured approximately −23 dB RMS, with peaks around −3 to −5 dBFS. Use listening judgment as well as measurements; these values are references, not loudness guarantees.

The bundled track is about 172 seconds long. For longer films, extend a suitable passage with a musically sensible crossfade, preferably behind narration. Avoid an obvious restart. One tested 180-second extension combined the first 90 seconds with the portion starting at 80 seconds, using a two-second triangular crossfade; cap the result at 180 seconds. For other durations choose suitable phrase boundaries instead of mechanically repeating these offsets.

## Editing and export

Preserve the screen's native dimensions throughout the edit. Trim waits and join shots at logical boundaries. Avoid needless speed changes; readable selection and result shots deserve a hold. If adapting existing footage, map source intervals to the new board before rendering. Do not reuse low-resolution footage for a requested native high-resolution replica.

Use H.264 with `-crf 16`, `-pix_fmt yuv420p`, and `-r 30`; use AAC with `-b:a 192k -ar 48000 -ac 2` and `-movflags +faststart`. Set explicit `-t DURATION`, and ensure both audio and picture cover the full duration. Encoder preset can trade render time for file size without changing the quality target. Finish with the picture fade and audio fade specified in SKILL.md.

Useful verification commands, with actual paths substituted safely:

```sh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of json final.mp4
ffmpeg -v error -i final.mp4 -f null -
ffmpeg -i final.mp4 -vn -af astats -f null -
```

Extract and view frames at the opening, important choices, generated or saved results, edit transitions, and the ending. Listen across the film, not just to isolated narration. Confirm the final seconds contain the intended visual hold or gentle scroll and music tail.
