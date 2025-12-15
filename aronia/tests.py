from django.test import TestCase

from .models import Tour


class TourImageAvailabilityTest(TestCase):
    """Ensure every stored tour exposes an Uploadcare-backed image."""

    def test_available_tours_have_primary_images(self):
        tours = Tour.objects.all()
        if not tours.exists():
            self.skipTest("No tours are present to validate image availability.")

        tours_missing_images = []
        for tour in tours:
            has_primary = bool(tour.Image)
            has_cdn_url = bool(getattr(tour.Image, "cdn_url", None)) if has_primary else False

            if not (has_primary and has_cdn_url):
                tours_missing_images.append(tour.name)

        self.assertFalse(
            tours_missing_images,
            "Tours missing Uploadcare images: {}".format(
                ", ".join(tours_missing_images)
            ),
        )
