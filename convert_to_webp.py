import os
from pathlib import Path
from PIL import Image

# --- CONFIG ---
source_dir = Path("fabrication-painting-images")
target_dir = Path("design-webp")
quality = 80
max_width = 1920  # resize any image wider than this

# --- Helper to test WebP support ---
def check_webp_support():
    try:
        tmp = Path("test.webp")
        Image.new("RGB", (1, 1), color="white").save(tmp, "webp")
        tmp.unlink(missing_ok=True)
        return True
    except Exception as e:
        print("⚠️ WebP test failed:", e)
        return False

if not check_webp_support():
    raise RuntimeError("Your Pillow build lacks WebP support. Try reinstalling: pip install --upgrade pillow")

# --- Conversion ---
target_dir.mkdir(parents=True, exist_ok=True)
count, failed = 0, 0

for root, _, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            src_path = Path(root) / file
            rel_path = src_path.relative_to(source_dir)
            dst_path = target_dir / rel_path.with_suffix(".webp")
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with Image.open(src_path) as img:
                    img = img.convert("RGB")

                    # Optional resize for huge images
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_size = (max_width, int(img.height * ratio))
                        img = img.resize(new_size, Image.LANCZOS)

                    img.save(dst_path, "webp", quality=quality, method=6)
                count += 1
                print(f"✅ {src_path} → {dst_path}")
            except Exception as e:
                failed += 1
                print(f"❌ Failed on {src_path}: {e}")

print(f"\n✅ Done! {count} images converted, {failed} failed.")
print("Optimized WebP files saved in:", target_dir.resolve())
