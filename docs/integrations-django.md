# Django Integration

DIGIPIN-Py provides a custom Django field for storing and querying DIGIPIN codes with automatic validation.

## Installation

```bash
pip install digipinpy[django]
```

**Requirements:** django>=3.2

## Quick Start

```python
from django.db import models
from digipin.django_ext import DigipinField

class Location(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField()  # Auto-validates and normalizes!

# Usage
location = Location.objects.create(
    name="Dak Bhawan",
    digipin="39j49ll8t4"  # Automatically converted to '39J49LL8T4'
)

print(location.digipin)  # Output: 39J49LL8T4
```

## DigipinField

### Basic Usage

```python
from django.db import models
from digipin.django_ext import DigipinField

class DeliveryAddress(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    digipin = DigipinField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.digipin}"
```

### Field Options

```python
class Store(models.Model):
    name = models.CharField(max_length=100)

    # Optional DIGIPIN
    digipin = DigipinField(blank=True, null=True)

    # Custom max length (default is 10)
    digipin_code = DigipinField(max_length=15)

    # With help text
    location_code = DigipinField(
        help_text="Enter the 10-character DIGIPIN code"
    )
```

## Features

### Automatic Validation

The field automatically validates DIGIPIN codes:

```python
# Valid codes - will be saved
location = Location(name="Valid", digipin="39J49LL8T4")
location.full_clean()  # ✓ Passes validation
location.save()

# Invalid codes - will raise ValidationError
try:
    location = Location(name="Invalid", digipin="INVALID")
    location.full_clean()  # ✗ Raises ValidationError
except ValidationError as e:
    print(e)  # "Invalid DIGIPIN code"
```

### Automatic Normalization

Codes are automatically converted to uppercase:

```python
# Lowercase input
location = Location.objects.create(
    name="Test",
    digipin="39j49ll8t4"  # lowercase
)

# Retrieved as uppercase
print(location.digipin)  # Output: 39J49LL8T4

# Mixed case also normalized
location.digipin = "39j49LL8t4"
location.save()
print(location.digipin)  # Output: 39J49LL8T4
```

## Custom Lookups

### `__within` Lookup

Filter locations within a geographic region:

```python
# Find all locations in district 39J49
locations = Location.objects.filter(digipin__within='39J49')

# Find all locations in broader region 39J
locations = Location.objects.filter(digipin__within='39J')

# Find all locations in very specific area
locations = Location.objects.filter(digipin__within='39J49LL8')
```

### Standard Lookups

All standard Django lookups work:

```python
# Exact match
Location.objects.filter(digipin='39J49LL8T4')

# Starts with (hierarchical queries)
Location.objects.filter(digipin__startswith='39J49')

# In list
codes = ['39J49LL8T4', '39J49LL8T9', '39J49LL8TC']
Location.objects.filter(digipin__in=codes)

# Exclude
Location.objects.exclude(digipin='39J49LL8T4')
```

## Migrations

### Creating Migrations

```python
# models.py
from django.db import models
from digipin.django_ext import DigipinField

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField()
```

```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### Migration File Example

```python
# Generated migration file
from django.db import migrations
import digipin.django_ext

class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('digipin', digipin.django_ext.DigipinField()),
            ],
        ),
    ]
```

### Adding Field to Existing Model

```python
# models.py - Add DIGIPIN to existing model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    digipin = DigipinField(blank=True, null=True)  # Make optional initially
```

```bash
python manage.py makemigrations
python manage.py migrate
```

## Real-World Examples

### Delivery Management System

```python
from django.db import models
from digipin.django_ext import DigipinField

class DeliveryHub(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField()
    capacity = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['digipin']),
        ]

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    delivery_digipin = DigipinField()
    assigned_hub = models.ForeignKey(
        DeliveryHub,
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def assign_to_nearest_hub(self):
        """Assign order to hub in same region"""
        # Get district code (first 5 characters)
        district = self.delivery_digipin[:5]

        # Find hub in same district
        hub = DeliveryHub.objects.filter(
            digipin__startswith=district
        ).first()

        if hub:
            self.assigned_hub = hub
            self.save()
```

### Location-Based Services

```python
from django.db import models
from digipin.django_ext import DigipinField

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=50)
    digipin = DigipinField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    @classmethod
    def find_nearby(cls, customer_digipin, precision=7):
        """Find restaurants in same area"""
        area_code = customer_digipin[:precision]
        return cls.objects.filter(digipin__startswith=area_code)

# Usage
customer_location = "39J49LL8T4"
nearby_restaurants = Restaurant.find_nearby(customer_location)
```

### Emergency Services Database

```python
from django.db import models
from digipin.django_ext import DigipinField

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    digipin = DigipinField()
    emergency_beds = models.IntegerField()
    has_trauma_center = models.BooleanField(default=False)

class Ambulance(models.Model):
    vehicle_number = models.CharField(max_length=20)
    current_digipin = DigipinField()
    is_available = models.BooleanField(default=True)
    assigned_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

class EmergencyIncident(models.Model):
    incident_id = models.CharField(max_length=20, unique=True)
    location_digipin = DigipinField()
    incident_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    reported_at = models.DateTimeField(auto_now_add=True)

    def find_nearest_hospital(self):
        """Find hospital in same district"""
        district = self.location_digipin[:5]
        return Hospital.objects.filter(
            digipin__within=district,
            emergency_beds__gt=0
        ).first()
```

## Django Admin Integration

### Basic Admin

```python
from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'digipin', 'created_at']
    search_fields = ['name', 'digipin']
    list_filter = ['created_at']
```

### Advanced Admin with DIGIPIN Filters

```python
from django.contrib import admin
from .models import DeliveryAddress

class DistrictFilter(admin.SimpleListFilter):
    title = 'District'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        # Get unique district codes (first 5 chars)
        districts = DeliveryAddress.objects.values_list(
            'digipin', flat=True
        ).distinct()
        district_codes = set(code[:5] for code in districts if code)
        return [(code, code) for code in sorted(district_codes)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(digipin__startswith=self.value())
        return queryset

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'digipin', 'created_at']
    search_fields = ['customer_name', 'digipin']
    list_filter = [DistrictFilter, 'created_at']
    readonly_fields = ['created_at']
```

## QuerySet Methods

### Custom Manager

```python
from django.db import models
from digipin.django_ext import DigipinField

class LocationManager(models.Manager):
    def in_region(self, region_code):
        """Filter by region code"""
        return self.filter(digipin__within=region_code)

    def nearby(self, digipin_code, precision=7):
        """Find locations in same area"""
        area = digipin_code[:precision]
        return self.filter(digipin__startswith=area)

class Store(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField()

    objects = LocationManager()

# Usage
delhi_stores = Store.objects.in_region('39J')
nearby_stores = Store.objects.nearby('39J49LL8T4')
```

## Forms

### ModelForm

```python
from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'digipin']
        widgets = {
            'digipin': forms.TextInput(attrs={
                'placeholder': '39J49LL8T4',
                'maxlength': 10,
                'style': 'text-transform: uppercase;'
            })
        }

# In view
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'add_location.html', {'form': form})
```

### Custom Validation in Forms

```python
from django import forms
from digipin import is_valid
from .models import DeliveryAddress

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['customer_name', 'address', 'digipin']

    def clean_digipin(self):
        code = self.cleaned_data['digipin']

        # Additional custom validation
        if not code.startswith('39'):
            raise forms.ValidationError(
                "We only deliver in region 39 (Delhi)"
            )

        return code
```

## REST API with Django REST Framework

```python
from rest_framework import serializers, viewsets
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'digipin', 'created_at']

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by region if provided
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(digipin__within=region)

        return queryset

# urls.py
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'locations', LocationViewSet)

# GET /api/locations/?region=39J49
# Returns all locations in district 39J49
```

## Performance Tips

### Database Indexes

```python
from django.db import models
from digipin.django_ext import DigipinField

class Location(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField(db_index=True)  # Add index

    class Meta:
        indexes = [
            # Composite index for common queries
            models.Index(fields=['digipin', 'created_at']),

            # Prefix index for hierarchical queries
            models.Index(fields=['digipin'], name='digipin_prefix_idx'),
        ]
```

### Query Optimization

```python
# ✓ Good - Use select_related for foreign keys
orders = Order.objects.select_related('assigned_hub').filter(
    delivery_digipin__within='39J49'
)

# ✓ Good - Use prefetch_related for reverse relations
hubs = DeliveryHub.objects.prefetch_related('order_set').all()

# ✓ Good - Use values() for aggregation
from django.db.models import Count
district_counts = Location.objects.values('digipin__startswith'[:5]).annotate(
    count=Count('id')
)
```

## Testing

```python
from django.test import TestCase
from .models import Location

class LocationModelTest(TestCase):
    def test_digipin_normalization(self):
        """Test that DIGIPIN is normalized to uppercase"""
        location = Location.objects.create(
            name="Test",
            digipin="39j49ll8t4"  # lowercase
        )
        self.assertEqual(location.digipin, "39J49LL8T4")

    def test_invalid_digipin(self):
        """Test that invalid DIGIPIN raises error"""
        from django.core.exceptions import ValidationError

        location = Location(name="Invalid", digipin="INVALID")
        with self.assertRaises(ValidationError):
            location.full_clean()

    def test_within_lookup(self):
        """Test custom __within lookup"""
        Location.objects.create(name="Loc1", digipin="39J49LL8T4")
        Location.objects.create(name="Loc2", digipin="39J49LL8T9")
        Location.objects.create(name="Loc3", digipin="2MK8MP3K63")

        # Should return 2 locations in 39J49
        results = Location.objects.filter(digipin__within='39J49')
        self.assertEqual(results.count(), 2)
```

## Common Patterns

### Geofencing

```python
class ServiceArea(models.Model):
    name = models.CharField(max_length=100)
    region_code = models.CharField(max_length=10)  # e.g., "39J49"

    def is_serviceable(self, customer_digipin):
        """Check if customer is in service area"""
        return customer_digipin.startswith(self.region_code)

# Usage
service_area = ServiceArea.objects.get(name="North Delhi")
is_serviceable = service_area.is_serviceable("39J49LL8T4")
```

### Distance Approximation

```python
def get_common_region_level(digipin1, digipin2):
    """Find common ancestor level"""
    for i in range(min(len(digipin1), len(digipin2)), 0, -1):
        if digipin1[:i] == digipin2[:i]:
            return i
    return 0

# Usage
level = get_common_region_level("39J49LL8T4", "39J49LL8T9")
print(f"Common region at level {level}")  # 9 (very close)
```

## Troubleshooting

### ValidationError: Invalid DIGIPIN code

**Problem:** Saving fails with validation error.

**Solution:** Check code format:
- Only contains: `23456789CFJKLMPT`
- Length 1-10 characters
- No lowercase (auto-converted)

### `__within` lookup not working

**Problem:** Custom lookup not recognized.

**Solution:** Ensure Django app is properly installed in `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'digipin.django_ext',  # Add this
    'yourapp',
]
```

## See Also

- [Getting Started](getting-started.md) - Basic DIGIPIN concepts
- [API Reference](../DOCUMENTATION.md) - Complete function documentation
- [Use Cases](use-cases.md) - Real-world examples
