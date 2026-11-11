# Production notes

These settings reproduce the approved high-resolution app films. Treat them as starting points, not a requirement to use a particular tool or app. Discover the available tooling and verify capture behavior in the current environment.

## Native capture and layout

The successful browser capture used Playwright/Chromium with a 1280 × 960 CSS-pixel viewport, `deviceScaleFactor: 2`, and `recordVideo.size` set to 2560 × 1920. The final frames were inspected to confirm sharp native UI. The same recorder settings can behave differently with another browser or installation: record a short test and inspect it with `ffprobe` and extracted frames.

For 16:9, a possible starting point is 1920 × 1080 logical pixels at scale factor 2, with 3840 × 2160 capture. For a smaller, more readable app layout, use a smaller logical viewport at an appropriate scale factor and verify the result. Portrait requires a genuinely usable responsive layout. Do not crop important controls or choose dimensions merely because an encoder accepts them.

Browser video may be buffered until the recording context closes. Close the context and wait for the file to finish before editing. Use the actual recorded page/context, not a different tab. Verify the screen state after each significant interaction. Framework-specific input events matter: filling a search box may not trigger a key-up handler; use actual typing where required and confirm the results changed.

A subtle visible cursor helps explain clicks. Keep it small, move it deliberately, and ensure any cursor overlay cannot intercept pointer events. Avoid recording development tools, permission dialogs, or unrelated desktop content.

## Speech and timing

### OpenAI

Use the existing OpenAI speech generation workflow with `gpt-4o-mini-tts`, voice `cedar` unless explicitly overridden, and WAV output. Check current supported APIs and voices before use. Keep credentials in their existing secure configuration and out of logs and production files.

> Speak like a relaxed person showing a useful app to a friend. Warm, gentle lower register. Keep phrases connected and flowing. Pause between complete thoughts, not inside short clauses. No announcer delivery or exaggerated emphasis.

### ElevenLabs

Use a voice explicitly requested by name or ID. For a female or male Estonian voice request, use the matching option below. Record reusable voices here by name and ID.

| Language | Option | Voice | Voice ID |
| --- | --- | --- | --- |
| Estonian (`et`) | Female | Sarah | `EXAVITQu4vr4xnSDxMaL` |
| Estonian (`et`) | Male | George | `JBFqnCBsd6RMkjVDRZzb` |

ElevenLabs lists both IDs as voices that expire on December 31, 2026. If an option is unavailable, offer to audition its suggested successor in Estonian. For Sarah, audition Talia (`OZ0L6eISlOejga3XjDFt`). For George, audition Eldrin (`6WwXjDDEMyNmFG95zycZ`). Show the proposed voice with the storyboard. [ElevenLabs voice transition guide](https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-default-voices)

For Estonian, audition a native voice when one is available to the account. Use a short sample with real product terms, names, and numbers. Listen for natural Estonian stress and rhythm, a gentle lower register, and a relaxed conversational delivery. Write complete thoughts with natural punctuation. Spell out tricky numbers or abbreviations as spoken when needed.

Provide `ELEVENLABS_API_KEY` through the environment of the process running the helper. Pass the selected ID with `--voice-id` and use it across the video. Replace `VOICE_ID` in the examples with the selected ID.

Run the [chunk helper](../scripts/synthesize_elevenlabs.py) with Python 3, using paths relative to the current working directory or absolute paths. The output directory must already exist.

```sh
python3 /path/to/narrated-screen-video/scripts/synthesize_elevenlabs.py \
  --language et --voice-id VOICE_ID --text-file chunk-01.txt --output chunk-01.wav
```

If the user exports the API key in `~/.zshrc` and the command environment lacks it, run the helper through interactive zsh so it loads the export.

```sh
/bin/zsh -ic 'exec python3 "$@"' zsh \
  /path/to/narrated-screen-video/scripts/synthesize_elevenlabs.py \
  --language et --voice-id VOICE_ID --text-file chunk-01.txt --output chunk-01.wav
```

The helper sends the UTF-8 spoken text to the [ElevenLabs Create speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) using `eleven_v4`, the selected voice ID, and the primary language code (`et` for `et-EE`). It wraps the returned mono 24 kHz PCM in a WAV with a finalized length header. Put only the spoken lines in the text file. Shape the delivery through voice choice, phrasing, and punctuation.

### Shared timing and captions

Generate narration in coherent chunks, each tied to a timeline segment. Store the text, start times, and filenames in working production notes. Measure real chunk durations before finalizing the timeline. Audition the opening and any tricky wording early. Correct unnatural pauses in text or delivery rather than globally slowing the narration.

Some streamed WAV responses have placeholder length headers, causing audio libraries to report an enormous duration. Remux such files through FFmpeg to normal PCM WAV, with a sensible maximum duration for that chunk, before reading durations or padding. Use `ffprobe` on the normalized file.

Check the measured end of each chunk against the next shot or narration cue. If captions are requested, take the cue text from the approved script and time cues against the audible speech on the final timeline. Account for any leading or trailing silence and recheck the cues after moving or regenerating a chunk.

Every command that pads or loops media must have an explicit finite duration. For example, `apad` without an output `-t` can produce an effectively endless file. Set subprocess timeouts as well. Finalize a silent narration timeline of exactly the target duration, placing chunks at their approved start times, so the ending has the correct length.

## Soundtrack

The sole bundled track is the user-supplied [Clean UI Product Demo Background](../assets/clean-ui-product-demo-background.mp3). It runs about 32 seconds. For longer videos, crossfade between suitable phrase boundaries and check the join at the final playback level.

Use the same quiet mix for a user-supplied track unless the brief calls for a different level. For a video without music, use the narration track on its own and keep the planned visual hold after the last line.

## Quiet music mix

Use the approved 7.5-second Estonian preview as the reference. Its narration measured −20 LUFS and its soundtrack measured −46 LUFS, a difference of 26 LU. Set narration for comfortable listening first, then set the music 26 LU below it. Measure representative speech and the chosen music passage separately with FFmpeg's `ebur128` filter in the same stereo layout. To find the gain in dB, subtract the measured loudness from the target for each track.

Keep the same music gain under speech, in pauses, and through the ending hold before the fade. At normal playback volume it should barely fill the silence and be easiest to notice when muted. If the music draws attention in a gap or at a crossfade, lower it further.

Fade the music in and out at the ends. In the filter below, input 0 is the narration timeline and input 1 is music already trimmed or extended to the film duration. Replace `VOICE_GAIN` and `MUSIC_GAIN` with the gain adjustments in dB. Set `FADE_START` to the duration minus five seconds for a full video. For a short sample, shorten the fades to fit.

```text
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=VOICE_GAINdB[voice];
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=MUSIC_GAINdB,afade=t=in:d=1,afade=t=out:st=FADE_START:d=5[music];
[voice][music]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false:latency=1[mix]
```

## Editing and export

Preserve the screen's native dimensions throughout the edit. Trim waits and join shots at logical boundaries. Avoid needless speed changes; readable selection and result shots deserve a hold. If adapting existing footage, map source intervals to the new board before rendering. Do not reuse low-resolution footage for a requested native high-resolution replica.

Use H.264 with `-crf 16`, `-pix_fmt yuv420p`, and `-r 30`; use AAC with `-b:a 192k -ar 48000 -ac 2` and `-movflags +faststart`. Set explicit `-t DURATION`, and ensure both audio and picture cover the full duration. Encoder preset can trade render time for file size without changing the quality target. Finish with the picture fade and audio fade specified in SKILL.md.

Useful verification commands, with actual paths substituted safely:

```sh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of json final.mp4
ffmpeg -v error -i final.mp4 -f null -
ffmpeg -i final.mp4 -vn -af astats -f null -
```

Extract and view frames at the opening, important choices, generated or saved results, edit transitions, and the ending. Listen across the film, not just to isolated narration. Confirm the final seconds contain the intended visual hold or gentle scroll and the music tail if selected.
