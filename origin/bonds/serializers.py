from rest_framework import serializers

from bonds.models import Bond

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = "__all__"