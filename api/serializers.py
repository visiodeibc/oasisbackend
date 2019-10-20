from rest_framework import serializers

from .models import Places, Descriptions, enAddress, hkAddress, Review

class enAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = enAddress
        fields = ('name', 'address')

class hkAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = hkAddress
        fields = ('name', 'address')

class descriptionsSerializer(serializers.ModelSerializer):

    enAddress = enAddressSerializer(many=False)
    hkAddress = hkAddressSerializer(many=False)

    class Meta:
        model = Descriptions
        fields = ('enAddress', 'hkAddress')

class NestedDynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        def parse_nested_fields(fields):
            field_object = {"fields": []}
            for f in fields:
                obj = field_object
                nested_fields = f.split("__")
                for v in nested_fields:
                    if v not in obj["fields"]:
                        obj["fields"].append(v)
                    if nested_fields.index(v) < len(nested_fields) - 1:
                        obj[v] = obj.get(v, {"fields": []})
                        obj = obj[v]
            return field_object

        def select_nested_fields(serializer, fields):
            for k in fields:
                if k == "fields":
                    fields_to_include(serializer, fields[k])
                else:
                    select_nested_fields(serializer.fields[k], fields[k])

        def fields_to_include(serializer, fields):
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            if isinstance(serializer, serializers.ListSerializer):
                existing = set(serializer.child.fields.keys())
                for field_name in existing - allowed:
                    serializer.child.fields.pop(field_name)
            else:
                existing = set(serializer.fields.keys())
                for field_name in existing - allowed:
                    serializer.fields.pop(field_name)

    # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
    # Instantiate the superclass normally
        super(NestedDynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # import pdb; pdb.set_trace()
            fields = parse_nested_fields(fields)
            # Drop any fields that are not specified in the `fields` argument.
            select_nested_fields(self, fields)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'text')

class PlacesSerializer(NestedDynamicFieldsModelSerializer):

    descriptions = descriptionsSerializer(many=False)
    review = ReviewSerializer(many=True)

    class Meta:
        model = Places
        fields = ('facilityId', 'facilityType', 'lat', 'lng', 'descriptions', 'phone', 'accessibility', 'rating','review')

    def create(self, validated_data):
        descriptions_data = validated_data.pop('descriptions')
        enAddress_data = descriptions_data.pop('enAddress')
        hkAddress_data = descriptions_data.pop('hkAddress')
        places = Places.objects.create(**validated_data)
        descriptions = Descriptions.objects.create(places=places, **descriptions_data)
        enAddress.objects.create(descriptions=descriptions, **enAddress_data)
        hkAddress.objects.create(descriptions=descriptions, **hkAddress_data)
        return places
    

