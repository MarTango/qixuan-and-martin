# Qixuan & Martin

Wedding photo gallery.

## Adding photos

1. Drop full-size originals (JPG, PNG, HEIC) into `originals/`. This folder is gitignored, so they are never uploaded.
2. Run `python3 build.py`. It writes 2000px versions to `photos/`, 600px thumbnails to `thumbs/`, and the index to `photos.json`.
3. Commit and push:
   ```
   git add photos thumbs photos.json
   git commit -m "Add photos"
   git push
   ```

## Notes

- Keep the repo under ~1 GB. At 2000px, expect roughly 0.5-1 MB per photo.
- Edit the title and subtitle in `index.html`.
