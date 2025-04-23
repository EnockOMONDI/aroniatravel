from django.contrib import admin
from .models import Tour, TourHighlight, TourInclusion, TourDay, Review, Destination, Booking, DayTripBooking
from .models import DayTrip, ItineraryItem, IncludedItem, OptionalActivity

class TourHighlightInline(admin.TabularInline):
    model = TourHighlight
    extra = 1

class TourInclusionInline(admin.TabularInline):
    model = TourInclusion
    extra = 1

class TourDayInline(admin.TabularInline):
    model = TourDay
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price', 'duration', 'reviews_count', 'is_featured')
    list_filter = ('destination', 'duration', 'is_featured')
    search_fields = ('name', 'description', 'destination__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourHighlightInline, TourInclusionInline, TourDayInline, ReviewInline]
    
    fieldsets = (
        (None, {
            'fields': ('destination', 'name', 'slug', 'description')
        }),
        ('Tour Details', {
            'fields': ('price', 'duration', 'group_size', 'languages', 'is_featured')  # Added group_size here
        }),
        ('Images', {
            'fields': (
                'Image',
                'gallery_image1',
                'gallery_image2',
                'gallery_image3',
            ),
            'classes': ('wide',)
        }),
        ('Ratings', {
            'fields': ('rating', 'reviews_count'),
            'classes': ('collapse',)
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['destination'].widget.can_add_related = True
        form.base_fields['destination'].widget.can_change_related = True
        return form

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'location', 'description')
        }),
        ('Image', {
            'fields': ('main_image',),
            'classes': ('wide',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user_name', 'rating', 'created_at')
    list_filter = ('tour', 'rating', 'created_at')
    search_fields = ('user_name', 'comment', 'tour__name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('tour', 'user_name', 'comment')
        }),
        ('Ratings', {
            'fields': (
                'rating',
                'location_rating',
                'price_rating',
                'amenities_rating',
                'services_rating',
                'rooms_rating'
            )
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(TourHighlight)
class TourHighlightAdmin(admin.ModelAdmin):
    list_display = ('tour', 'highlight')
    list_filter = ('tour',)
    search_fields = ('highlight', 'tour__name')

@admin.register(TourInclusion)
class TourInclusionAdmin(admin.ModelAdmin):
    list_display = ('tour', 'item', 'is_included')
    list_filter = ('tour', 'is_included')
    search_fields = ('item', 'tour__name')

@admin.register(TourDay)
class TourDayAdmin(admin.ModelAdmin):
    list_display = ('tour', 'day_number', 'title')
    list_filter = ('tour',)
    search_fields = ('title', 'description', 'tour__name')
    ordering = ('tour', 'day_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'tour', 'full_name', 'travel_date', 
                   'number_of_people', 'booking_status', 'payment_status', 'total_price']
    list_filter = ['booking_status', 'payment_status', 'travel_date', 'created_at', 'user']
    search_fields = ['booking_reference', 'full_name', 'email', 'tour__name', 'user__username']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'user', 'tour', 'travel_date', 'number_of_people')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'special_requirements')
        }),
        ('Status & Payment', {
            'fields': ('booking_status', 'payment_status', 'total_price', 'deposit_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.total_price:
            obj.total_price = obj.calculate_total_price()
        super().save_model(request, obj, form, change)




class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    ordering = ['order', 'time']

class OptionalActivityInline(admin.TabularInline):
    model = OptionalActivity
    extra = 1

@admin.register(DayTrip)
class DayTripAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'recurrence', 'price', 'is_featured')  # Removed 'status'
    list_filter = ('recurrence', 'is_featured', 'pickup_location')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'price', 'is_featured')
        }),
        ('Images', {
            'fields': ('Image', 'gallery_image1', 'gallery_image2', 'gallery_image3')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'recurrence', 'group_size')
        }),
        ('Pickup Details', {
            'fields': ('pickup_location', 'pickup_time')
        }),
        ('Inclusions', {
            'fields': ('included_items',)
        }),
    )

@admin.register(IncludedItem)
class IncludedItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(DayTripBooking)
class DayTripBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'daytrip', 'full_name', 'travel_date', 
                   'number_of_people', 'total_price', 'booking_status', 'payment_status')
    list_filter = ('booking_status', 'payment_status', 'travel_date', 'created_at')
    search_fields = ('booking_reference', 'full_name', 'email', 'phone', 
                    'daytrip__name')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'daytrip', 'travel_date', 'number_of_people')
        }),
        ('Customer Details', {
            'fields': ('user', 'full_name', 'email', 'phone', 'special_requirements')
        }),
        ('Status & Payment', {
            'fields': ('booking_status', 'payment_status', 'total_price', 'deposit_paid')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new booking
            obj.total_price = obj.calculate_total_price()
        super().save_model(request, obj, form, change)

