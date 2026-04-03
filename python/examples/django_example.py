"""
Django Integration Example

This example demonstrates how to use the DigipinField in a Django model.
Note: This script is for demonstration purposes and requires a Django environment to run.

Setup:
    pip install digipinpy[django]

Documentation:
    The DigipinField is a custom Django CharField that:
    - Automatically validates DIGIPIN format
    - Normalizes codes to uppercase
    - Provides custom database lookups
"""

# ============================================================================
# In your Django app's models.py
# ============================================================================

try:
    from django.db import models
    from digipin.django_ext import DigipinField

    class DeliveryLocation(models.Model):
        """
        Example model for delivery locations with DIGIPIN codes.
        """
        name = models.CharField(max_length=100)
        address = models.TextField(blank=True)

        # The DigipinField handles validation and normalization automatically
        digipin = DigipinField(db_index=True)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            ordering = ['name']
            verbose_name = "Delivery Location"
            verbose_name_plural = "Delivery Locations"

        def __str__(self):
            return f"{self.name} ({self.digipin})"


    class Warehouse(models.Model):
        """
        Example warehouse model with DIGIPIN location code.
        """
        name = models.CharField(max_length=200)
        digipin = DigipinField(db_index=True, help_text="10-character DIGIPIN code")
        capacity = models.IntegerField(default=0)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return f"{self.name} - {self.digipin}"


    # ========================================================================
    # Usage Examples (in views.py, shell, etc.)
    # ========================================================================

    def example_basic_operations():
        """Basic CRUD operations with DigipinField."""

        # CREATE: The field automatically validates and normalizes
        location = DeliveryLocation.objects.create(
            name="Customer Home",
            digipin="39J49LL8T4"  # Will be stored as uppercase
        )
        print(f"Created: {location}")

        # CREATE with lowercase (auto-normalized)
        location2 = DeliveryLocation.objects.create(
            name="Office",
            digipin="39j49ll8t4"  # Automatically converted to uppercase
        )
        print(f"Created (normalized): {location2.digipin}")  # Outputs: 39J49LL8T4

        # VALIDATION ERROR: Invalid DIGIPIN will raise ValidationError
        try:
            invalid = DeliveryLocation(name="Bad Location", digipin="INVALID123")
            invalid.full_clean()  # This will raise ValidationError
        except Exception as e:
            print(f"Validation error caught: {e}")

        # READ
        location = DeliveryLocation.objects.get(digipin="39J49LL8T4")
        print(f"Found: {location.name}")


    def example_hierarchical_queries():
        """
        Demonstrates the custom 'within' lookup for hierarchical queries.
        This allows you to find all locations within a specific region.
        """

        # Find all locations in Delhi region (codes starting with '39')
        delhi_locations = DeliveryLocation.objects.filter(digipin__within='39')
        print(f"Locations in Delhi region: {delhi_locations.count()}")

        # Find locations in a more specific area (sub-region)
        subregion = DeliveryLocation.objects.filter(digipin__within='39J4')
        print(f"Locations in sub-region 39J4: {subregion.count()}")

        # Find locations in a very specific grid
        grid = DeliveryLocation.objects.filter(digipin__within='39J49LL')
        print(f"Locations in grid 39J49LL: {grid.count()}")

        # Combine with other filters
        active_in_region = Warehouse.objects.filter(
            digipin__within='39J4',
            is_active=True
        )
        print(f"Active warehouses in region: {active_in_region.count()}")


    def example_standard_queries():
        """Standard Django queries work as expected."""

        # Exact match
        exact = DeliveryLocation.objects.filter(digipin='39J49LL8T4')

        # Starts with (for region-based queries)
        region = DeliveryLocation.objects.filter(digipin__startswith='39J')

        # Case-insensitive (though DIGIPIN is always uppercase)
        iexact = DeliveryLocation.objects.filter(digipin__iexact='39j49ll8t4')

        # In a list
        codes = ['39J49LL8T4', '39J49LL8T5', '39J49LL8T6']
        batch = DeliveryLocation.objects.filter(digipin__in=codes)

        # Exclude
        not_in_region = DeliveryLocation.objects.exclude(digipin__startswith='39')


    def example_aggregation():
        """Aggregation and annotation examples."""
        from django.db.models import Count, Q

        # Count locations per region (first 2 chars)
        from django.db.models.functions import Substr

        # Group by region prefix
        by_region = (
            DeliveryLocation.objects
            .annotate(region=Substr('digipin', 1, 2))
            .values('region')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        for item in by_region:
            print(f"Region {item['region']}: {item['count']} locations")


    def example_nearest_locations():
        """
        Finding locations in the same area as a reference point.
        This uses the hierarchical properties of DIGIPIN.
        """
        from digipin import get_neighbors

        # Get a reference location
        reference = DeliveryLocation.objects.first()
        if reference:
            # Get neighboring DIGIPIN codes (application level)
            neighbors = get_neighbors(reference.digipin)

            # Find locations in neighboring cells
            nearby = DeliveryLocation.objects.filter(
                digipin__in=neighbors
            ).exclude(
                id=reference.id  # Exclude the reference itself
            )

            print(f"Locations near {reference.name}: {nearby.count()}")


    # ========================================================================
    # Admin Integration (in admin.py)
    # ========================================================================

    from django.contrib import admin

    @admin.register(DeliveryLocation)
    class DeliveryLocationAdmin(admin.ModelAdmin):
        list_display = ['name', 'digipin', 'created_at']
        list_filter = ['created_at']
        search_fields = ['name', 'digipin', 'address']

        # Group by region in admin
        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.select_related()


    @admin.register(Warehouse)
    class WarehouseAdmin(admin.ModelAdmin):
        list_display = ['name', 'digipin', 'capacity', 'is_active']
        list_filter = ['is_active']
        search_fields = ['name', 'digipin']


    # ========================================================================
    # REST API Integration (with Django REST Framework)
    # ========================================================================

    try:
        from rest_framework import serializers, viewsets

        class DeliveryLocationSerializer(serializers.ModelSerializer):
            class Meta:
                model = DeliveryLocation
                fields = ['id', 'name', 'address', 'digipin', 'created_at']

            # The DigipinField is automatically validated by the serializer
            # No custom validation needed!


        class DeliveryLocationViewSet(viewsets.ModelViewSet):
            queryset = DeliveryLocation.objects.all()
            serializer_class = DeliveryLocationSerializer
            filterset_fields = ['digipin']

            # Custom filter for region-based queries
            def get_queryset(self):
                queryset = super().get_queryset()
                region = self.request.query_params.get('region', None)

                if region:
                    # Use the custom 'within' lookup
                    queryset = queryset.filter(digipin__within=region)

                return queryset

    except ImportError:
        print("Django REST Framework not installed. Skipping DRF examples.")


    print("Django integration examples loaded successfully!")
    print("\nTo use these examples:")
    print("1. Add 'digipin' to INSTALLED_APPS (if needed)")
    print("2. Run: python manage.py makemigrations")
    print("3. Run: python manage.py migrate")
    print("4. Use the models in your views, serializers, etc.")

except ImportError as e:
    print(f"Error: {e}")
    print("Please install Django: pip install digipinpy[django]")
