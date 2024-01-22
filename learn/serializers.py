from rest_framework import serializers

from learn.models import Learn, Section, Lesson, Category


class LearnAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learn
        fields = ('id', 'title', 'image', 'type', 'is_active', 'is_free', 'auther', 'price', 'category')

    def create(self, validated_data):
        key = validated_data.pop('key')
        instance = super().create(validated_data)
        return instance


class LearnDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    num_section = serializers.SerializerMethodField()

    class Meta:
        model = Learn
        fields = ('id', 'title', 'image', 'type', 'is_active', 'is_free', 'auther', 'price', 'user', 'num_section')

    def get_user(self, obj):
        name2 = obj.user.info.name + " " + obj.user.info.family
        return name2

    def get_num_section(self, obj):
        num = obj.sections.count()
        return num


class SectionByLearnIdSerializer(serializers.ModelSerializer):
    # learn = serializers.CharField(source='learn.title')
    learn = LearnDetailSerializer()
    num_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('id', 'title', 'learn', 'is_active', 'is_free', 'num_lesson')

    def get_num_lesson(self, obj):
        num = obj.lessons.count()
        return num


class LessonBySectionIdSerializer(serializers.ModelSerializer):
    section = SectionByLearnIdSerializer()
    class Meta:
        model = Lesson
        fields = ('id', 'section', 'title', 'image', 'video', 'three1', 'three2', 'voice',
                  'description', 'is_active', 'is_free')


class CategorySerializer(serializers.ModelSerializer):
    num_learn = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'num_learn')

    def get_num_learn(self, obj):
        num = obj.learns.count()
        return num

    def get_title(self, obj):
        title = obj.title
        title = title
        return title
