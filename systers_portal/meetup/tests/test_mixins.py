from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.views.generic import TemplateView
from cities_light.models import City, Country

from meetup.mixins import MeetupLocationMixin
from meetup.models import MeetupLocation


class MeetupLocationMixinTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test location", sponsors="BarBaz")

    def test_get_context_data_no_meetup_location(self):
        """Test mixin with no meetup_location"""
        class DummyView(MeetupLocationMixin, TemplateView):
            pass

        view = DummyView()
        self.assertRaises(ImproperlyConfigured, view.get_context_data)

    def test_get_context_data_with_meeetup_location(self):
        """Test mixin with a meetup_location"""
        class DummyView(MeetupLocationMixin, TemplateView):
            def get_meetup_location(self):
                return MeetupLocation.objects.get()

        view = DummyView()
        context = view.get_context_data()
        self.assertEqual(context['meetup_location'], self.meetup_location)
