

# Project Updates

### Jan 7, 2026 – Uploadcare passwords
- **Issue:** Files could not upload because the website still used the old Uploadcare passwords.
- **Fix:** Updated both Uploadcare passwords in the settings so every upload area uses the new ones.
- **Impact:** Upload forms now work again without login errors. *Time taken: ~1hr 35 minutes.*

### Jan 7, 2026 – Uploadcare images missing
- **Issue:** Newly uploaded tour images (like the Ngorongoro/Serengeti tour) still showed “Not Found” because the project was using Uploadcare’s custom CDN host without the trailing slash, so every `cdn_url` pointed to a broken location.
- **Fix:** Updated the Uploadcare configuration so the CDN base matches the dashboard host (`https://ioc6rcdjx5.ucarecd.net/`) and cleaned up templates to always use `tour.Image`. Re-uploaded the tour media so the new URLs match the working host.
- **Impact:** Uploadcare images now load in both development and production after each upload. *Time taken : ~5 hrs 30 minutes.*

### Jan 7, 2026 – Home page images missing on development website
- **Issue:** The big home page images vanished on the development website because the browser could not find the stored image files.
- **Fix:** Only use the special image storage on the production website, so the development website serves its normal image files.
- **Impact:** Home page images now show up both on development and production websites. *Time taken: ~50 minutes.*

### Jan 7, 2026 – General image cleanup
- **Issue:** Many images (logos, banners, location photos, favicon) still returned “not found” on the development website due to missing files and typos in the file names.
- **Fix:** Copied the `assets4/img` folder into the main `static` directory, removed the extra spaces from the image paths in the templates, tidied the static-file settings, and pointed the browser icon to the real logo.
- **Impact:** All images load correctly on the development website, `collectstatic` keeps working, and the browser no longer requests missing files. *Time taken: ~45 minutes.*

### Jan 7, 2026 – Email delivery failures
- **Issue:** Website messages stopped sending because the Mailtrap API password was outdated.
- **Fix:** Updated `.env`, `.sample_env`, and Render’s environment variables with the new Mailtrap token (`a773b5`) and restarted the app so Django uses the fresh credentials.
- **Impact:** All inquiry forms send emails again through Mailtrap without errors. *Time taken: ~30 minutes.*

### Jan 7, 2026 – Quote inquiry experience
- **Issue:** The internal “New Quote Inquiry” email looked basic and didn’t spell out next steps, and guests weren’t reminded to check their inbox.
- **Fix:** Rebuilt the admin email with Aronia’s premium styling, highlighted the guest’s brief, and added a clear three-step action list. Also updated the on-site success alert so guests know to watch for our confirmation email.
- **Impact:** The concierge team receives a world-class brief with actions, and guests feel confident their request was received. *Time taken: ~45 minutes.*




# Tasks
- **High priority:** Plan and complete a full upgrade of the project to the new Django 5 toolset (Unfold admin, CKEditor 5, newer packages). This is needed so we keep receiving security fixes and can use the modern admin and media tools the business now expects.
- **High priority:** Add a dedicated “Hotels” section inside the admin so team members can create, edit, and manage hotel listings without touching the database manually.






# Note to self: keep every entry in this document extremely simple—use everyday words like “home page images,” “passwords,” “development website,” “not found,” etc., just like the sections below.s
