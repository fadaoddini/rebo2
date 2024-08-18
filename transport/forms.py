from django import forms
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from transport.models import Transport, TransportReq, RouteMetrics, Location, PriceList
import math


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['car_name', 'transport_type', 'image', 'pelak', 'iran', 'capacity', 'description']


class TransportReqForm(forms.ModelForm):
    class Meta:
        model = TransportReq
        fields = ['origin', 'destination', 'distance', 'price', 'description', 'barnameh', 'my_transport']

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")
        price = cleaned_data.get("price")
        my_transport = cleaned_data.get("my_transport")
        capacity = my_transport.capacity if my_transport else None

        if origin and destination:
            try:
                # Ensure that origin and destination are Location instances
                if not isinstance(origin, Location) or not isinstance(destination, Location):
                    raise ValidationError("Invalid origin or destination provided.")

                # Retrieve the latest price list
                price_list = PriceList.objects.latest('create_time')

                # Check if the route exists or create a new one
                route_metrics, created = RouteMetrics.objects.get_or_create(
                    origin=origin,
                    destination=destination,
                    defaults={'distance_km': 0, 'min_cost': 0, 'max_cost': 0}
                )

                # Calculate distance if the route is newly created
                if created:
                    route_metrics.distance_km = calculate_distance(
                        origin.latitude, origin.longitude,
                        destination.latitude, destination.longitude
                    )
                    route_metrics.save()  # Save the new route with calculated values

                # Calculate costs based on the latest PriceList and capacity
                if capacity:
                    min_cost = round(
                        (price_list.min_cost_per_one_ton * capacity) +
                        (price_list.min_cost_per_one_km * route_metrics.distance_km)
                    )
                    max_cost = round(
                        (price_list.max_cost_per_one_ton * capacity) +
                        (price_list.max_cost_per_one_km * route_metrics.distance_km)
                    )
                else:
                    min_cost = round(price_list.min_cost_per_one_km * route_metrics.distance_km)
                    max_cost = round(price_list.max_cost_per_one_km * route_metrics.distance_km)

                # Update cleaned_data with calculated values
                cleaned_data['distance'] = route_metrics.distance_km
                cleaned_data['price'] = round(price * 1000000) / 1000000  # Adjust price rounding logic as needed

            except Location.DoesNotExist:
                raise ValidationError("Invalid origin or destination provided.")
            except PriceList.DoesNotExist:
                raise ValidationError("No price list found. Please configure the price list before proceeding.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set expire_time to 24 hours from now
        if not instance.expire_time:
            instance.expire_time = timezone.now() + timedelta(hours=24)

        if commit:
            instance.save()

        return instance


# تابع برای محاسبه مسافت بین دو نقطه
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c