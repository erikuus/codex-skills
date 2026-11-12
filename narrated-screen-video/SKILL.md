---
name: narrated-screen-video
description: Plan and produce screen recordings of apps or selected features with natural voiceover, background music, deliberate pacing, and a polished ending. Use for narrated app demos, walkthroughs, product tours, and revisions or alternate cuts of existing screen videos. Establish scope and aspect ratio, offer a scenario or timed storyboard, then record, edit, mix, and deliver a verified video.
---

# Narrated Screen Video

Turn an app workflow into a watchable demonstration. Keep the proven production defaults below, while adapting the story, duration, language, framing, and app interactions to the user's brief. Do not assume this is a sales video: a personal demonstration, tutorial, or thank-you can have a different voice and purpose.

## Establish the brief

Read the conversation first. Reuse decisions already made, including an approved board, and ask only about missing details. Keep the initial questions to one concise batch of at most three, using the available question tool when appropriate:

1. **Scope:** Is this a tour of the whole app or a demonstration of selected features? Which app and workflows should appear?
2. **Framing:** Which aspect ratio and viewing destination? Offer 4:3 as the established default, 16:9 for widescreen, and 9:16 for a vertical clip. Explain the visible layout tradeoff briefly if useful.
3. **Story:** How long, who is it for, and what narration language or tone should it use? Suggest a duration if the user has not chosen one.

For Estonian narration, offer a female or male ElevenLabs voice from the production notes. Use a voice or voice ID the user has already chosen. The voice and soundtrack are independent choices. Either voice can be used with the bundled soundtrack, a track the user supplies, or narration only.

Ask about missing voice and soundtrack preferences in the initial batch if there is room, or when offering the scenario or storyboard. If the user delegates, pick a suitable voice and use the bundled soundtrack for the choices they delegate.

Resolve any remaining essential details, such as app access, demonstration data, and the output folder, while doing independent preparation. Use `<project>/_media` for output when suitable and no location has been specified. Use the defaults for captions and quality when they satisfy the brief.

Inspect the app and available recording, speech, and editing tools before promising a specific capture method. Prefer supported browser or native automation. Reuse installed tools where possible. If a required capability is unavailable, explain the concrete gap and offer a workable alternative; do not silently substitute a robotic voice or lower-resolution export.

## Offer and prepare the story

Offer a short scenario or a full timed storyboard; recommend the timed board for production. Once the user chooses, write it here in the conversation so it can be reviewed. If they already ask for a board or authorize a complete video, proceed with the appropriate level of planning.

For a board, use a compact table:

| Time | On-screen action | Spoken narration | Pacing / transition |
| --- | --- | --- | --- |

The board should:

- Explain the app's purpose before the first detailed interaction.
- Follow a coherent flow of thought between features, rather than narrating every click.
- Make important choices and results legible. Budget more time for selecting or creating than for navigation.
- Use short, conversational sentences with natural rhythm and accurate product terms.
- Include the result of each demonstrated workflow, not just its setup.
- Reserve approximately 4–7 seconds after the last spoken line for an unhurried visual ending, with music if selected.

Provide the full voiceover text, proposed narration provider and voice, and soundtrack choice with the board. Avoid written-sounding clauses, artificial pauses, announcer language, and unnecessary narration of actions that are obvious on screen. Read the script aloud mentally; rewrite clumsy phrasing before generating speech. A warm closing observation or light joke can fit a personal demo, but should follow the user's tone.

By default, obtain the user's review of the concrete board before recording. This is a creative review, not a separate permission ceremony. An existing instruction to make the video, proceed, or use an approved script already authorizes production; do not ask for confirmation again. Incorporate feedback into the board and narration before capturing dependent scenes.

## Production defaults

| Setting | Default |
| --- | --- |
| Aspect ratio | 4:3, unless the user chooses otherwise |
| Capture | Native 2560 × 1920 pixels at 30 fps for 4:3. Prefer lossless frames or recording. |
| Browser layout | Start with 1280 × 960 CSS pixels at device scale factor 2 for 4:3. Verify the recorded dimensions. |
| Narration provider and voice | OpenAI with Cedar by default. For Estonian (`et`, including `et-EE`), use ElevenLabs and select a voice using the production notes. |
| Voice style | Relaxed and conversational, with a gentle lower register and connected phrases |
| Delivery | Start near 150–160 words per minute; allow visual holds and natural pauses between thoughts |
| Soundtrack | Choose with the user for each video |
| Audio | Clear, comfortable narration. Keep any music barely audible, even between phrases. |
| Captions | No burned-in captions, titles, or text overlays unless requested |
| Export | MP4, H.264, CRF 16, yuv420p, 30 fps, AAC stereo 192 kbps / 48 kHz, faststart |
| Ending | Keep the app visible. When using music, keep a music-only tail and fade the music over the last 5 seconds. Fade the picture over the last 1.5 seconds. |

Use the provider the user requests, or use the language default above. Use an explicitly requested voice for the selected provider. Resolve the choice once for the video. For ElevenLabs, check the key and voice setup in the production notes during preparation. Surface missing setup or incompatible choices so the user can choose how to proceed.

Choose the viewport, capture resolution, and delivery resolution to suit the brief. Preserve readable app layout and capture at native resolution. If the brief calls for a smaller export, scale the footage down at delivery.

Read the production notes for capture and export checks, privacy masks, pronunciation, and the quiet soundtrack mix. [Production notes](references/production.md)

## Record and edit

1. Prepare demonstration data and the opening state. Check the responsive layout and adjust the browser framing. When sign-in needs the user, pause capture, let them sign in in the same browser, and resume after sign-in.
2. Encode a short capture using the delivery settings before recording the full workflow. Compare it with a browser screenshot of the same view. Check small text, gradients, and moving frames for visible degradation. Fix quality issues and repeat the test.
3. Before generating the full narration, audition a short sample in the chosen voice and language. Include app names, acronyms, and words with tricky pronunciation or stress. If you cannot hear the sample, send it to the user for a pronunciation check while continuing capture preparation.
4. Show the cursor reach the control, the click, and the resulting view. Show scrolling as continuous movement and hold on results long enough to read them. Keep forms unsaved when demonstrating their fields. If the brief calls for showing a saved result, exercise the save through the app with suitable demonstration data.
5. Assemble the shots and narration on the timed board. Keep the relevant view on screen while explaining it. Mask visible sensitive data as described in the production notes. Reuse approved footage when it suits the new cut.
6. If the user chose music, match the reference mix in the production notes. Keep its gain steady through speech and pauses. Extend the track with a discreet crossfade when needed. Listen at normal playback volume and check that the voice stays clear and the music barely registers in gaps.
7. Export to the requested duration and destination. Keep raw captures and intermediates in a separate working directory so the delivery folder stays understandable.

Exercise demonstrated app behavior through the app. Do not fake saved state, generation, or responses by rewriting app code or database contents. Consider persistent demo changes and paid generation in the context of the user's authorized workflows; reuse valid results where appropriate. Publish, send, or upload the video only on the user's explicit request. Preserve existing media and project files; clean up only within the user's requested scope.

## Verify and deliver

Play the finished MP4 from start to finish with sound. Check picture quality in motion, pacing, cursor and action visibility, mask coverage, pronunciation, audio balance, and the final hold and fades. Verify duration, delivery dimensions, aspect ratio, frame rate, codecs, and full decode. Report any part of the review you could not perform.

Deliver a clickable local video link or inline preview, its duration and resolution, and any material limitation. Keep the response concise. Offer title and description when useful, but do not let optional extras delay the requested video.
