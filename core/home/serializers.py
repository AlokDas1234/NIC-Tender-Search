from rest_framework import serializers
from .models import Client, TenderResults,Search
from rest_framework import serializers
from .models import Search
import re


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class SearchTenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = "__all__"

class TenderResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderResults
        fields = "__all__"



class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ["site_url", "search_key", "exclude_key", "state_name"]

    # 🔹 search_key validation (comma separated)
    def validate_search_key(self, value):
        if not value:
            raise serializers.ValidationError("Search key is required")

        # Remove extra spaces
        value = value.strip()

        # If multiple words exist but no comma
        if " " in value and "," not in value:
            raise serializers.ValidationError(
                "Multiple search keys must be separated by comma (,)"
            )

        # Validate comma-separated format
        if "," in value:
            parts = [p.strip() for p in value.split(",")]
            if any(not p for p in parts):
                raise serializers.ValidationError(
                    "Invalid comma-separated search keys"
                )

        return value

    # 🔹 exclude_key validation (pipe separated)
    def validate_exclude_key(self, value):
        if not value:
            return value  # exclude_key is optional

        value = value.strip()

        # If multiple words exist but no |
        if " " in value and "|" not in value:
            raise serializers.ValidationError(
                "Multiple exclude keys must be separated by pipe (|)"
            )

        # Validate pipe-separated format
        if "|" in value:
            parts = [p.strip() for p in value.split("|")]
            if any(not p for p in parts):
                raise serializers.ValidationError(
                    "Invalid pipe-separated exclude keys"
                )
        return value

    def validate_site_url(self, value):
        if not value.startswith("http"):
            raise serializers.ValidationError("Invalid site URL")
        return value
