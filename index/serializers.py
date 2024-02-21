from rest_framework import serializers

from index.models import SettingApp


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingApp
        fields = ('id', 'title', 'description', 'favicon', 'logo', 'login_text', 'tel', 'mobile', 'address', 'email',
                  'about_text', 'footer_text', 'is_active')