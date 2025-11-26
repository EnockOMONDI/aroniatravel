# Aronia Travel Admin Guide
## Creating Tour Packages and Day Trips

**Version 1.0 | November 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Section 1: Creating Tour Packages](#section-1-creating-tour-packages)
4. [Section 2: Creating Day Trips](#section-2-creating-day-trips)
5. [Section 3: Managing Quote Inquiries](#section-3-managing-quote-inquiries)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference Guide](#quick-reference-guide)

---

## Introduction

Welcome to the Aronia Travel Admin Guide! This comprehensive manual will help you manage tour packages, day trips, and customer inquiries through the Django admin panel. The admin panel is your central hub for creating and managing all travel content on the Aronia Travel website.

### What You Can Do:
- ✅ Create and edit multi-day tour packages
- ✅ Set up day trips and excursions
- ✅ Manage customer quote inquiries
- ✅ Upload and organize tour images
- ✅ Set pricing and availability
- ✅ Track bookings and customer communications

### Admin Panel Features:
- **Django Jet Interface**: Modern, user-friendly admin interface
- **CKEditor 5**: Rich text editor for tour descriptions
- **UploadCare Integration**: Professional image management
- **Quote Management System**: Handle customer inquiries efficiently

---

## Getting Started

### Accessing the Admin Panel

**Production URL**: `https://your-production-domain.com/admin/`
**Development URL**: `http://127.0.0.1:8000/admin/`

### Login Credentials
Your administrator will provide you with login credentials. Contact your system administrator if you need access.

### Admin Panel Layout

When you log in, you'll see the main admin dashboard with several sections:

**Main Sections:**
- **ARONIA**: Tours, Day Trips, Destinations, Bookings, Quote Inquiries
- **USERS**: User accounts and profiles
- **BLOG**: Blog posts and categories
- **EVENTS**: Event management

**Navigation Tips:**
- Use the left sidebar for quick navigation
- The breadcrumb trail shows your current location
- Use the search function to find specific items quickly

---

## Section 1: Creating Tour Packages

### Step 1: Access Tour Management

1. Log in to the admin panel
2. Click on **"ARONIA"** in the left sidebar
3. Click on **"Tours"** to see all existing tours
4. Click the **"ADD TOUR"** button (top right)

### Step 2: Basic Tour Information

**Required Fields:**

**Destination** 🌍
- Select from existing destinations or create a new one
- Click the "+" icon to add a new destination if needed

**Tour Name** 📝
- Enter a descriptive, compelling tour name
- Example: "4 Days 3 Nights Cairo & Alexandria Tour"
- Keep it under 100 characters for best display

**Slug** 🔗
- Auto-generated from the tour name
- Used in the website URL (e.g., `/tour/cairo-alexandria-tour/`)
- Edit only if you need a specific URL format

**Description** 📄
- Use the CKEditor 5 rich text editor
- Include compelling tour overview
- Highlight unique selling points
- Format with headings, bullet points, and bold text

### Step 3: Tour Details

**Price** 💰
- Enter the base price per person in USD
- Use whole numbers (e.g., 450, not 450.00)
- This will be displayed as "From $450 per person"

**Duration** ⏰
- Number of days for the tour
- Enter as a whole number (e.g., 4 for a 4-day tour)

**Group Size** 👥
- Maximum number of people per tour group
- Recommended: 8-15 for small groups, 20-30 for larger tours

**Languages** 🗣️
- Languages in which the tour is conducted
- Separate multiple languages with commas
- Example: "English, Arabic, French"

**Is Featured** ⭐
- Check this box to feature the tour on the homepage
- Only feature your best and most popular tours

### Step 4: Adding Tour Images

**Main Image** 📸
- Primary tour image displayed in listings
- **Recommended size**: 800x600 pixels
- **Format**: JPG or PNG
- **File size**: Under 2MB for fast loading

**Gallery Images** 🖼️
- Up to 3 additional images
- Show different aspects of the tour
- **Recommended size**: 800x600 pixels
- **Tips**: Include destination highlights, activities, accommodations

**Image Upload Process:**
1. Click "Choose File" next to the image field
2. Select your image from your computer
3. The image will be automatically uploaded to UploadCare
4. You'll see a preview once uploaded successfully

### Step 5: Tour Highlights

Tour highlights appear as bullet points on the tour detail page.

**Adding Highlights:**
1. Scroll to the "Tour highlights" section
2. Click "Add another Tour highlight"
3. Enter one highlight per line
4. Examples:
   - "Visit the iconic Pyramids of Giza"
   - "Explore the ancient city of Alexandria"
   - "Professional English-speaking guide"
   - "All entrance fees included"

**Best Practices:**
- Keep highlights concise (under 50 characters)
- Focus on unique experiences
- Include practical benefits (meals, transport, guides)
- Use action words (Visit, Explore, Experience, Discover)

### Step 6: Tour Inclusions

Inclusions show what's included or excluded from the tour price.

**Adding Inclusions:**
1. Scroll to the "Tour inclusions" section
2. Click "Add another Tour inclusion"
3. Enter the item name
4. Check "Is included" if it's included in the price
5. Leave unchecked for exclusions

**Common Inclusions:**
- ✅ Accommodation (3 nights in 4-star hotels)
- ✅ All meals (breakfast, lunch, dinner)
- ✅ Transportation (air-conditioned vehicle)
- ✅ Professional guide
- ✅ Entrance fees to all attractions
- ❌ International flights
- ❌ Personal expenses
- ❌ Travel insurance

### Step 7: Day-by-Day Itinerary

Create a detailed daily itinerary for your tour.

**Adding Tour Days:**
1. Scroll to the "Tour days" section
2. Click "Add another Tour day"
3. Fill in the details for each day:

**Day Number** 📅
- Sequential number (1, 2, 3, 4...)

**Title** 📋
- Brief description of the day
- Example: "Arrival in Cairo - Pyramids Tour"

**Description** 📝
- Detailed daily activities
- Include timing, locations, and activities
- Use the rich text editor for formatting

**Example Day Description:**
```
**Morning (9:00 AM)**
- Pick up from your hotel in Cairo
- Drive to Giza Plateau (30 minutes)

**Giza Pyramids Tour (9:30 AM - 12:30 PM)**
- Explore the Great Pyramid of Khufu
- Visit the Pyramid of Khafre and Menkaure
- Photo opportunity at the Sphinx
- Optional camel ride (additional cost)

**Lunch (12:30 PM - 1:30 PM)**
- Traditional Egyptian lunch at local restaurant

**Afternoon (2:00 PM - 5:00 PM)**
- Visit the Egyptian Museum
- See Tutankhamun's treasures
- Explore ancient artifacts

**Evening**
- Return to hotel
- Free time for dinner and rest
```

### Step 8: Reviews and Ratings

**Rating** ⭐
- Overall tour rating (1-5 stars)
- Based on customer feedback
- Leave blank for new tours

**Reviews Count** 📊
- Number of customer reviews
- Auto-calculated from actual reviews
- Leave blank for new tours

### Step 9: Publishing Your Tour

**Before Publishing - Checklist:**
- ✅ All required fields completed
- ✅ Compelling description written
- ✅ High-quality images uploaded
- ✅ Tour highlights added (minimum 4)
- ✅ Inclusions/exclusions specified
- ✅ Complete day-by-day itinerary
- ✅ Pricing verified

**To Publish:**
1. Click **"SAVE"** at the bottom of the page
2. Your tour is now live on the website
3. Check the frontend to verify everything displays correctly

**To Save as Draft:**
1. Uncheck "Is featured" if you don't want it prominently displayed
2. Click **"SAVE"**
3. Complete remaining details before featuring

---

## Section 2: Creating Day Trips

Day trips are single-day excursions that don't require overnight accommodation.

### Step 1: Access Day Trip Management

1. From the admin dashboard, click **"ARONIA"**
2. Click on **"Day trips"**
3. Click **"ADD DAY TRIP"** button

### Step 2: Basic Day Trip Information

**Name** 📝
- Descriptive day trip name
- Example: "Pyramids & Sphinx Half-Day Tour"
- Keep under 80 characters

**Slug** 🔗
- Auto-generated from name
- Used in URL structure

**Description** 📄
- Detailed day trip overview
- Include duration, highlights, and what to expect
- Use rich text formatting

**Price** 💰
- Price per person in USD
- Include all costs except personal expenses

**Is Featured** ⭐
- Feature popular day trips on homepage

### Step 3: Day Trip Images

**Main Image** 📸
- Primary day trip image
- **Size**: 800x600 pixels recommended
- **Quality**: High-resolution, well-lit

**Gallery Images** 🖼️
- Up to 3 additional images
- Show key attractions and activities

### Step 4: Schedule and Timing

**Start Date** 📅
- When the day trip becomes available
- Use calendar picker

**End Date** 📅
- When the day trip stops being available
- Leave blank for ongoing availability

**Recurrence** 🔄
- How often the trip runs
- Options: Daily, Weekly, Monthly, One-time

**Group Size** 👥
- Maximum participants per trip
- Consider vehicle capacity and guide limitations

### Step 5: Pickup Details

**Pickup Location** 📍
- Where customers will be collected
- Be specific: "Hotel lobbies in Cairo city center"
- Include landmarks for easy identification

**Pickup Time** ⏰
- Standard pickup time
- Example: "08:00 AM"
- Mention if times vary by location

### Step 6: Inclusions

**Included Items** ✅
- Select from pre-defined inclusion items
- Add new items if needed
- Common inclusions:
  - Transportation
  - Professional guide
  - Entrance fees
  - Refreshments

**Adding New Included Items:**
1. Click the "+" next to "Included items"
2. Enter item name and description
3. Save and select for your day trip

### Step 7: Itinerary Items

Create a detailed timeline for the day trip.

**Adding Itinerary Items:**
1. Scroll to "Itinerary items" section
2. Click "Add another Itinerary item"
3. Fill in details:

**Time** ⏰
- Start time for this activity
- Use 24-hour format (09:00, 14:30)

**Activity** 📋
- Brief activity description
- Example: "Pyramids Tour"

**Description** 📝
- Detailed activity information
- Duration, what's included, special notes

**Order** 📊
- Sequence number for proper ordering
- Use increments of 10 (10, 20, 30) for easy reordering

### Step 8: Optional Activities

Add optional extras customers can purchase.

**Adding Optional Activities:**
1. Scroll to "Optional activities" section
2. Click "Add another Optional activity"
3. Enter details:

**Name** 📝
- Activity name
- Example: "Camel Ride at Pyramids"

**Description** 📄
- What's included in the optional activity
- Duration and any restrictions

**Price** 💰
- Additional cost per person
- Clearly state if it's per person or per group

**Duration** ⏰
- How long the optional activity takes
- Example: "30 minutes"

### Step 9: Publishing Day Trips

**Pre-Publication Checklist:**
- ✅ Compelling name and description
- ✅ Accurate pricing
- ✅ Clear pickup details
- ✅ Complete itinerary with times
- ✅ High-quality images
- ✅ Inclusions specified

**To Publish:**
1. Review all information
2. Click **"SAVE"**
3. Day trip is now bookable on the website

---

## Section 3: Managing Quote Inquiries

The quote inquiry system helps you manage customer requests for personalized tour quotes.

### Step 1: Accessing Quote Inquiries

1. From admin dashboard, click **"ARONIA"**
2. Click on **"Quote inquiries"**
3. View all customer quote requests

### Step 2: Understanding Quote Inquiry Information

**Inquiry Reference** 🔢
- Unique identifier (e.g., QI-000001)
- Use this reference in all communications

**Customer Details** 👤
- Full name, email, phone, nationality
- Contact information for follow-up

**Trip Requirements** ✈️
- Preferred date
- Number of people
- Special requirements/requests

**Status Options** 📊
- **Pending**: New inquiry, needs response
- **Responded**: Quote sent to customer
- **Closed**: Inquiry completed or cancelled

### Step 3: Responding to Quote Inquiries

**Step-by-Step Response Process:**

1. **Open the Inquiry**
   - Click on the inquiry reference number
   - Review all customer details and requirements

2. **Analyze Requirements**
   - Check tour availability for preferred date
   - Consider group size and special requests
   - Calculate pricing based on requirements

3. **Prepare Quote Details**
   - **Quoted Price**: Total price for the group
   - **Quote Valid Until**: Expiration date (typically 7-14 days)
   - **Admin Notes**: Internal notes for your reference

4. **Update Status**
   - Change status from "Pending" to "Responded"
   - Add any internal notes

5. **Save Changes**
   - Click "SAVE" to update the inquiry

### Step 4: Bulk Actions

**Managing Multiple Inquiries:**

1. **Select Multiple Inquiries**
   - Check boxes next to inquiries
   - Use "Select all" for bulk operations

2. **Available Actions**
   - **Mark as Responded**: For inquiries you've quoted
   - **Mark as Closed**: For completed or cancelled inquiries

3. **Apply Actions**
   - Select action from dropdown
   - Click "Go" to apply

### Step 5: Filtering and Searching

**Filter Options:**
- **Status**: Pending, Responded, Closed
- **Nationality**: Filter by customer nationality
- **Preferred Date**: Filter by travel dates
- **Inquiry Date**: When the inquiry was received
- **Tour Destination**: Filter by destination

**Search Function:**
- Search by customer name
- Search by email address
- Search by phone number
- Search by tour name
- Search by nationality

### Step 6: Quote Inquiry Best Practices

**Response Time** ⏰
- Respond within 2-24 hours as promised
- Set up email notifications for new inquiries

**Pricing Strategy** 💰
- Consider group size discounts
- Factor in seasonal pricing
- Include all costs clearly

**Communication** 📧
- Use the inquiry reference in all communications
- Be clear about what's included/excluded
- Provide detailed itinerary information

**Follow-up** 📞
- Follow up if no response within quote validity period
- Offer alternative dates or packages if needed

---

## Best Practices

### Writing Compelling Tour Descriptions

**Structure Your Description:**
1. **Opening Hook**: Capture attention immediately
2. **Overview**: Brief tour summary
3. **Highlights**: Key attractions and experiences
4. **Details**: Practical information
5. **Call to Action**: Encourage booking

**Writing Tips:**
- Use active voice and action verbs
- Paint vivid pictures with descriptive language
- Include sensory details (sights, sounds, tastes)
- Address customer concerns (safety, comfort, value)
- Keep paragraphs short for easy reading

**Example Opening:**
"Embark on an unforgettable journey through Egypt's most iconic destinations. This carefully crafted 4-day adventure combines the ancient wonders of Cairo with the Mediterranean charm of Alexandria, offering you a perfect blend of history, culture, and relaxation."

### Choosing Effective Images

**Image Selection Criteria:**
- **High Quality**: Sharp, well-lit, professional
- **Relevant**: Directly related to tour content
- **Diverse**: Show different aspects of the experience
- **Authentic**: Real locations and experiences
- **Engaging**: Visually appealing and inspiring

**Image Types to Include:**
- Iconic landmarks and attractions
- Cultural experiences and activities
- Accommodation examples
- Local cuisine and dining
- Transportation and guides
- Happy customers (with permission)

**Technical Requirements:**
- **Resolution**: Minimum 800x600 pixels
- **Format**: JPG or PNG
- **File Size**: Under 2MB each
- **Aspect Ratio**: 4:3 or 16:9 for best display

### Pricing Strategy

**Factors to Consider:**
- **Seasonality**: Peak vs. off-peak pricing
- **Group Size**: Discounts for larger groups
- **Competition**: Research competitor pricing
- **Value Proposition**: Justify premium pricing with unique value
- **Costs**: Ensure profitability after all expenses

**Pricing Display:**
- Use "From $X per person" for variable pricing
- Clearly state what's included in the base price
- List additional costs separately
- Offer package deals for multiple tours

### Content Organization

**Tour Categories:**
- **Duration**: Half-day, full-day, multi-day
- **Theme**: Cultural, adventure, luxury, budget
- **Region**: Cairo, Alexandria, Luxor, Aswan
- **Activity**: Sightseeing, adventure, relaxation

**Consistent Formatting:**
- Use the same structure for all tours
- Maintain consistent tone and style
- Follow naming conventions
- Use standard terminology

---

## Troubleshooting

### Common Issues and Solutions

**Problem: Images Not Uploading**
- **Check file size**: Must be under 2MB
- **Check format**: Use JPG or PNG only
- **Check internet connection**: Ensure stable connection
- **Try different browser**: Clear cache and cookies

**Problem: Tour Not Appearing on Website**
- **Check publication status**: Ensure tour is saved
- **Verify required fields**: All mandatory fields must be completed
- **Check featured status**: May need to be featured to appear prominently
- **Clear website cache**: Contact technical support if needed

**Problem: Rich Text Editor Not Working**
- **Browser compatibility**: Use Chrome, Firefox, or Safari
- **Disable ad blockers**: May interfere with editor
- **Check JavaScript**: Ensure JavaScript is enabled
- **Try incognito mode**: Test without browser extensions

**Problem: Slug Already Exists**
- **Modify slug manually**: Add numbers or descriptive words
- **Check existing tours**: Ensure unique naming
- **Use descriptive slugs**: Include destination or unique features

**Problem: Quote Inquiries Not Showing**
- **Check filters**: Remove any active filters
- **Verify permissions**: Ensure you have access rights
- **Check date range**: Expand date filter range
- **Contact administrator**: If issues persist

### Getting Help

**Technical Support:**
- Contact your system administrator
- Provide specific error messages
- Include screenshots of issues
- Mention browser and operating system

**Content Questions:**
- Consult with tour operations team
- Review competitor offerings
- Check tourism board resources
- Verify information with local guides

**Training Resources:**
- This admin guide
- Video tutorials (if available)
- Peer training sessions
- Practice on test tours

---

## Quick Reference Guide

### Essential Keyboard Shortcuts

**General Navigation:**
- `Ctrl + S` (Windows) / `Cmd + S` (Mac): Save
- `Ctrl + Z` (Windows) / `Cmd + Z` (Mac): Undo
- `Tab`: Move to next field
- `Shift + Tab`: Move to previous field

**Rich Text Editor:**
- `Ctrl + B`: Bold text
- `Ctrl + I`: Italic text
- `Ctrl + U`: Underline text
- `Ctrl + K`: Insert link

### Field Descriptions Quick Reference

**Tour Fields:**
- **Name**: Tour title (max 100 characters)
- **Slug**: URL identifier (auto-generated)
- **Description**: Rich text tour overview
- **Price**: Base price per person (USD)
- **Duration**: Number of days (integer)
- **Group Size**: Maximum participants
- **Languages**: Available languages (comma-separated)
- **Is Featured**: Display on homepage

**Day Trip Fields:**
- **Name**: Day trip title (max 80 characters)
- **Recurrence**: How often it runs
- **Pickup Location**: Collection point
- **Pickup Time**: Standard start time
- **Included Items**: What's included in price

**Quote Inquiry Fields:**
- **Status**: Pending/Responded/Closed
- **Quoted Price**: Total group price
- **Quote Valid Until**: Expiration date
- **Admin Notes**: Internal comments

### Status Indicators

**Tour Status:**
- ✅ **Published**: Live on website
- 📝 **Draft**: Saved but not complete
- ⭐ **Featured**: Highlighted on homepage

**Quote Status:**
- 🟡 **Pending**: Awaiting response
- 🟢 **Responded**: Quote sent
- ⚪ **Closed**: Completed/cancelled

**Booking Status:**
- 🟡 **Pending**: Awaiting confirmation
- 🟢 **Confirmed**: Booking confirmed
- 🔴 **Cancelled**: Booking cancelled

### Contact Information

**Technical Support:**
- Email: support@aroniatravel.com
- Phone: +254 758 355 325

**Content Questions:**
- Email: info@aroniatravel.com
- Operations Manager: [Contact Details]

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Next Review**: February 2026

© 2025 Aronia Travel. All rights reserved.
