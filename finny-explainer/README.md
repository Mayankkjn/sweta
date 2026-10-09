# Finny product explainer video

- `finny_explainer.mp4`: 16:9, 1920×1080, 30 fps, about 2:15, with an AI voiceover.
- `finny_explainer_9x16.mp4`: 9:16, 1080×1920. Same script, voice and timing in a vertical layout: logo and headline centred at the top (no stage labels or stepper) with the explainer text under them, and a large phone whose bottom edge runs slightly off the frame.

- **Script:** see `SCRIPT.md`. It is the founder's voiceover cleaned up into a happy-flow script. The raw transcript is in `original_voiceover_transcript.txt`.
- **Voice:** Kokoro TTS (`af_heart`). It runs offline and generates one clip per line.
- **Sync:** each script line is its own audio clip. The shots for that line share the line's duration.
  - If the footage is shorter than the line, the last frame is held so the screen keeps pace with the voice.
  - If the footage is longer, it is sped up (or trimmed) to fit.
- **Brand theme, taken from the app UI:**
  - Fonts: Poppins (sans) with Playfair Display Italic accents.
  - Colours: ink green `#0E3B2E`, primary `#1E6B48` → `#38976C` (button gradient), deep green `#01362E`, Basic-FIRE olive `#233021`, mint `#EBF5ED`, gold sparkle `#D6B26A`.
- **Logo:** the official Finny SVG (`assets/finny.svg`), rasterised in green for light scenes and white for dark ones. Pass the folder with `LOGO_DIR`.
- **Recording clean-up:** the phone status bar in the recording (it shows the screen-recorder pill) is masked out and replaced with a clean status bar. The black side strips and the Android navigation bar are cropped off.

## Rebuild

```bash
pip install kokoro-onnx sherpa-onnx soundfile scipy numpy pillow
# models: kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
python3 scripts/gen_vo.py <models_dir> <vo_dir>          # AI voiceover, one wav per line
LOGO_DIR=assets python3 scripts/render.py <recording.mp4> <vo_dir> <fonts_dir> finny_explainer.mp4
# VERTICAL=1 python3 scripts/render.py ...  -> 9:16 version
# PREVIEW=mid python3 scripts/render.py ...  -> contact sheets of every shot
```

To change the copy or the cuts, edit `scripts/spec.py`, then re-run both steps.
