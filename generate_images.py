#!/usr/bin/env python3
"""
Voynich Manuscript — Gemini Image Generation
=============================================

Generates 10 atmospheric images + social preview banner for the repository
using Google's Gemini API (Imagen 4.0).

Usage:
    pip install google-genai
    export GEMINI_API_KEY="your-key-here"
    python generate_images.py

Images are saved to images/ directory.
"""

import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable")
    print("  export GEMINI_API_KEY='your-key-here'")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# IMAGE PROMPTS — atmospheric, scholarly, medieval-meets-modern
# No text overlays on any image.
# ═══════════════════════════════════════════════════════════════

IMAGES = [
    {
        "filename": "01_manuscript_hero.png",
        "prompt": (
            "Aged parchment pages of a mysterious medieval manuscript lying open on "
            "a dark wooden table. The pages show hand-drawn botanical illustrations "
            "of strange plants with roots and leaves, surrounded by lines of an "
            "unknown flowing script. Dramatic side lighting from a single source, "
            "warm golden tones, dust particles visible in the light beam. Museum-quality "
            "photography, shallow depth of field. The manuscript looks ancient, precious, "
            "and enigmatic. No text overlays. 16:9 aspect ratio, ultra high resolution."
        ),
    },
    {
        "filename": "02_beinecke_library.png",
        "prompt": (
            "Interior of a prestigious university rare book library. A glass display "
            "case in the center contains a small, ancient manuscript open to a page "
            "with botanical illustrations. The room has marble floors, tall shelves "
            "of rare books behind glass, and soft diffused lighting. Reverent, hushed "
            "atmosphere. Modern conservation architecture with clean lines. No people "
            "visible. No text overlays. Professional architectural photography, 16:9."
        ),
    },
    {
        "filename": "03_zodiac_decode.png",
        "prompt": (
            "A medieval zodiac wheel drawn on aged parchment. Twelve segments arranged "
            "in a circle, each containing a stylized astrological symbol — ram, bull, "
            "twins, crab, lion, virgin, scales, scorpion, archer, goat, water-bearer, "
            "fish. Gold and deep blue ink on cream vellum. Celestial stars and moon "
            "motifs around the border. The style is authentic 15th-century European "
            "manuscript illumination. No text overlays. Square format, high resolution."
        ),
    },
    {
        "filename": "04_herbal_botanical.png",
        "prompt": (
            "A medieval botanical illustration of a medicinal plant on aged parchment. "
            "The plant has detailed roots exposed below a soil line, a thick green stem, "
            "compound leaves with serrated edges, and small flowers at the top. Drawn "
            "in the style of a 15th-century European herbal manuscript — hand-painted "
            "with natural pigments in greens, browns, and subtle reds. Parchment texture "
            "visible. No text overlays. Portrait format, high resolution."
        ),
    },
    {
        "filename": "05_decoder_terminal.png",
        "prompt": (
            "A modern computer terminal screen in a dark room showing lines of "
            "cryptographic analysis output — columns of aligned text, statistical "
            "scores, and pattern matching results. Green and amber text on a dark "
            "background. Behind the screen, barely visible, are photocopies of ancient "
            "manuscript pages pinned to a wall. The scene suggests late-night cipher "
            "breaking — intense, focused, breakthrough imminent. Cinematic lighting "
            "from the screen only. No readable text. 16:9."
        ),
    },
    {
        "filename": "06_medieval_scriptorium.png",
        "prompt": (
            "A 15th-century European scriptorium interior. A scholar in period clothing "
            "sits at a wooden writing desk, hunched over a manuscript, writing with a "
            "quill pen by candlelight. Shelves of bound manuscripts line the stone walls. "
            "An inkwell, a penknife, and loose parchment sheets are on the desk. Warm "
            "candlelight creates deep shadows. The atmosphere is contemplative, solitary, "
            "monastic. Oil painting style, Vermeer-like lighting. No text overlays. 16:9."
        ),
    },
    {
        "filename": "07_wilfrid_voynich.png",
        "prompt": (
            "An early 1900s antiquarian book dealer in a dusty European villa library, "
            "examining an ancient manuscript. The man wears Edwardian-era clothing — "
            "tweed suit, wire-rimmed spectacles. He holds a small, aged codex carefully "
            "in gloved hands, studying it with intense fascination. Bookshelves stuffed "
            "with old volumes surround him. Afternoon light streams through tall windows. "
            "Sepia-toned, atmospheric, historical. No text overlays. 16:9."
        ),
    },
    {
        "filename": "08_star_chart.png",
        "prompt": (
            "A medieval astronomical star chart drawn on dark blue-black parchment. "
            "Constellation lines connect stars rendered as gold dots. Latin-style "
            "annotations in small script label the constellations. A large central "
            "rosette pattern radiates outward with concentric rings. The style is "
            "authentic 15th-century European astronomical illustration — hand-drawn "
            "with gold leaf and mineral pigments. No modern text overlays. Square format."
        ),
    },
    {
        "filename": "09_600_years.png",
        "prompt": (
            "A visual metaphor for the passage of 600 years. On the left side, a "
            "medieval writing desk with a quill pen, candle, inkwell, and parchment "
            "manuscript — 15th century. On the right side, a modern research desk "
            "with a laptop showing data analysis, a coffee cup, and printed manuscript "
            "scans — 21st century. The two scenes blend together in the middle, time "
            "collapsing. Warm tones on the left, cool blue tones on the right. "
            "Cinematic, atmospheric. No text overlays. 16:9 widescreen."
        ),
    },
    {
        "filename": "social_preview_banner.png",
        "prompt": (
            "A dramatic wide banner image showing aged medieval manuscript pages with "
            "mysterious botanical illustrations and unknown script on the left side, "
            "transitioning into a dark scholarly atmosphere on the right. Golden "
            "candlelight illuminates the manuscript from below. Dust particles float "
            "in the light. The right side fades to deep dark blue-black, perfect for "
            "overlaying a title. The feeling is ancient mystery meeting modern discovery. "
            "Cinematic, museum-quality. No text overlays. Ultra-wide 2:1 aspect ratio."
        ),
    },
]


def generate_image(prompt_data):
    """Generate a single image using Imagen 4.0."""
    filename = prompt_data["filename"]
    prompt = prompt_data["prompt"]
    output_path = IMAGES_DIR / filename

    if output_path.exists():
        print(f"  [SKIP] {filename} already exists")
        return True

    print(f"  [GEN]  {filename}...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1),
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"  [OK]   {filename} ({len(image_data):,} bytes)")
            return True

        print(f"  [WARN] {filename} — no image in response")
        return False

    except Exception as e:
        print(f"  [ERR]  {filename} — {e}")
        return False


def main():
    print("=" * 60)
    print("  VOYNICH MANUSCRIPT — GEMINI IMAGE GENERATION")
    print("=" * 60)
    print(f"  Output: {IMAGES_DIR}")
    print(f"  Images: {len(IMAGES)}")
    print()

    success = 0
    for img in IMAGES:
        if generate_image(img):
            success += 1

    print()
    print(f"  Done: {success}/{len(IMAGES)} images generated")
    print(f"  Output directory: {IMAGES_DIR}")

    if success < len(IMAGES):
        print(f"  WARNING: {len(IMAGES) - success} images failed — re-run to retry")


if __name__ == "__main__":
    main()
