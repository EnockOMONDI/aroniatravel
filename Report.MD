# Note to self: keep every entry in this document extremely simple—use everyday words like “home page images,” “passwords,” “development website,” “not found,” etc., just like the sections below.

# Project Updates

### Jan 7, 2026 – Uploadcare passwords
- **Issue:** Files could not upload because the website still used the old Uploadcare passwords.
- **Fix:** Updated both Uploadcare passwords in the settings so every upload area uses the new ones.
- **Impact:** Upload forms now work again without login errors. *Estimated time: ~15 minutes.*

### Jan 7, 2026 – Home page images missing on development website
- **Issue:** The big home page images vanished on the development website because the browser could not find the stored image files.
- **Fix:** Only use the special image storage on the production website, so the development website serves its normal image files.
- **Impact:** Home page images now show up both on development and production websites. *Estimated time: ~20 minutes.*

### Jan 7, 2026 – General image cleanup
- **Issue:** Many images (logos, banners, location photos, favicon) still returned “not found” on the development website due to missing files and typos in the file names.
- **Fix:** Copied the `assets4/img` folder into the main `static` directory, removed the extra spaces from the image paths in the templates, tidied the static-file settings, and pointed the browser icon to the real logo.
- **Impact:** All images load correctly on the development website, `collectstatic` keeps working, and the browser no longer requests missing files. *Estimated time: ~35 minutes.*

# Tasks
- **High priority:** Plan and complete a full upgrade of the project to the new Django 5 toolset (Unfold admin, CKEditor 5, newer packages). This is needed so we keep receiving security fixes and can use the modern admin and media tools the business now expects.


