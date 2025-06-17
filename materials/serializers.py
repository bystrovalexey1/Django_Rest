from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    total_lessons_in_course = serializers.SerializerMethodField()
    lessons_in_course = LessonSerializer(source='lesson_set', many=True)

    def get_total_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'total_lessons_in_course', 'lessons_in_course')
