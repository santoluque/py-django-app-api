from django.test import TestCase
from django.contrib.auth import get_user_model

''' 4 '''
from core import models
''' 4 '''

class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        email = 'santo@email.com'
        password = 'pass1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['santo@email.com','santoaaa@email.com'],
            ['sant1o@email.com','sant1o@email.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            
        self.assertEqual(user.email, expected)
            
    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')
            
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
        'santo@email.com',
        'abc123',
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    ''' 4 '''
    # creation studend OK 200
    def test_create_student(self):
        user = get_user_model().objects.create_user(
            'user4@mail.com',
            'passuser4'
        )

        student = models.Student.objects.create(
            user=user,
            name = 'JOSE PRADO',
            born_date = '2010-01-25',
            career= 'MECHANIC',
            register_date = '2024-04-01 10:00:00',
        )

        self.assertEqual(str(student),student.name)