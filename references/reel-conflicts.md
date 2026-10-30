# Conflicts between the `reel` route (skill-reel) and the rest of Designer Mestre, decided by the user on 29/10/2026

| # | Topic | Decision applied |
|---|---|---|
| C1 | Who handles "cut/edit spoken video" | the single flow of `video.md` (profile P1); profile P2 handles only captions, overlay, soundtrack, and endcard on finished video |
| C2 | Approval before the MP4 | Beat grid (floor plan + cards) shown and **approved by the user** before rendering `reel-v1.mp4` (decision of 29/10/2026) |
| C3 | Visual identity | The client's KV becomes the skin (colors and fonts via `skin.json`) whenever it exists; the native purple skin only without a KV |
| C4 | 9:16 safe zone | Core values (top 250, bottom 450 in Reels) hold in `reel`, overriding the engine's x 90–990 / y 220–1520 |
| C5 | Loudness | `reel` Reels: −14 LUFS ±0.3, peak ≤ −1 dBTP; other videos follow −16 LUFS |
| C6 | Render engine | HyperFrames and Remotion are options; the AI chooses the best for the piece, including a superior one from the internet or local, under the conditions of `video.md` §6 ("render engine is an option") (29/10/2026) |
| C7 | Narration and sound | **Motion without the client speaking on video: ElevenLabs (current default, `video.md` §3) with soundtrack.** **Video with the client speaking: real voice and SFX from the kit (≤ 0.8/s), no AI narration** |
| C8 | Folders | The core's current default location (`[AAAA]\[MM]\[data] [EV] Título\`); the reel's work (`cut/ render/ qa/ entrega/ assets/`) stays inside `Trabalho\` and the final goes straight to `Exportados\`. No parallel `reel-<slug>` folder and no copies of the video |
| C9 | Captions | Default: captions that follow the mouth; option of the KV's `.ass` captions (`caption_reels.py`) when requested |
| C10 | Repo license | Ignored by the user's decision: free material from the author, and this version is a new, improved work |
| C11 | Default route for spoken video | `video.md` profile P1 with the gates of §8; profile P2 only as a floor (captions, overlay, endcard on finished video) |
| C12 | Stops during editing | KV and templates decide without asking; gaps become assumptions; questions in one message before the grid |

No conflict (incorporated as is): R1–R3 (free face, sparing SFX, real material) coincide with the core; easings and entrance blur coincide with Jakub (`motion-cookbook.md` §1).
