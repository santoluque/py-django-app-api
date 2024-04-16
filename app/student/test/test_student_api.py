# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APIClient

# from core.models import Student
# from student.serializers import StudentDetailSerializer, StudentSerializer

# STUDENT_URL = reverse('student:student-list')

# def detail_url(student_id):
#     return reverse('student:student-detail', args=[student_id])

# def create_student(user, **params):
#     defaults = {
#             'name': 'DEFAULT',
#             'born_date': '1970-01-01',
#             'career': 'DEFAULT',
#             'register_date': '2024-04-10 11:00:00',
#     }

#     defaults.update(params)

#     student = Student.objects.create(user=user, **defaults)
#     return student

# def create_user(**params):
#     return get_user_model().objects.create(**params)

# class PublicStudentAPITests(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#     def test_auth_required(self):
#         res = self.client.get(STUDENT_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateStudentApiTests(TestCase):
    
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(email='user5@example.com', password='pass12345')
#         self.client.force_authenticate(self.user)

#     def test_retrieve_students(self):

#         create_student(user=self.user)
#         create_student(user=self.user)

#         res = self.client.get(STUDENT_URL)

#         students = Student.objects.all().order_by('-id')
#         serializer = StudentSerializer(students, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)


#     def test_student_list_limited_to_user(self):

#         other_user = create_user(email='otherusr@example.com', password='passt123')
#         create_student(user=other_user)
#         create_student(user=self.user)

#         res = self.client.get(STUDENT_URL)

#         recipes = Student.objects.filter(user=self.user)
#         serializer = StudentSerializer(recipes, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)


#     def test_get_student_detail(self):

#         student = create_student(user=self.user)

#         url = detail_url(student.id)
#         res = self.client.get(url)

#         serializer = StudentDetailSerializer(student)
#         self.assertEqual(res.data, serializer.data)