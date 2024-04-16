from rest_framework import serializers

from core.models import (
    Student,
)


# user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     name = models.CharField(max_length=100,blank=False)
#     born_date = models.TextField(blank=True)
#     career = models.CharField(max_length=100,blank=False)
#     register_date = models.DateTimeField(null=False)
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id', 'name', 'born_date', 'career', 'register_date',
        ]
        read_only_fields = ['id']


    def create(self, validated_data):
        
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StudentDetailSerializer(StudentSerializer):

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ['name']

