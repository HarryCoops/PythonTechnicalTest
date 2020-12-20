import datetime

from rest_framework import serializers

from bonds.models import Bond

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        exclude = ["id", "created"]

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )