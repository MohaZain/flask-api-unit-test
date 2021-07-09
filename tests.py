import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Course, Student, Enrollment, Professor


class UniversityTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres@localhost:5432/flask-api-unit-test-test"
        setup_db(self.app, self.database_path)
        c = Course(name="Software Engineering",
                   semester=1)
        s = Student(name="Mohammed",
                    email="mohammed@student.com",
                    gpa=3.5)
        p = Professor(name="Abdullah",
                      email="abdullah@professor.com")
        c.insert()
        s.insert()
        p.insert()
        
        self.row_num = '4'
        self.del_row_num = '9'
        self.new_course = {
            'name': 'Discrete Mathematics',
            'semester': 2,
        }

        self.new_student = {
            'name': 'Test Student',
            'email': 'student@student.com',
            'gpa': 3.93
        }

        self.new_professor = {
            'name': 'Test Professor',
            'email': 'professor@professor.com',
        }
        self.new_enrollment = {
            'course_id': 1,
            'student_id': 1,
            'professor_id': 1,
            'grade': 2.8
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ''' 
    Courses test
    
    '''

    def test_given_courses(self):
        """Test _____________ """
        res = self.client().get('/courses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/courses?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_course(self):
        res = self.client().post('/courses', json=self.new_course)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_given_course(self):
        res = self.client().get('/courses/'+self.row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_not_exist(self):
        res = self.client().get('/courses/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_course(self):
        res = self.client().put('/courses/'+self.row_num, json=self.new_course)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_course_not_exist(self):
        res = self.client().put('/courses/10000', json=self.new_course)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_course(self):
        res = self.client().delete('/courses/'+self.del_row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_course_not_exist(self):
        res = self.client().delete('/courses/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # ------------------
    ''' 
    Student test
    
    '''

    def test_given_students(self):
        res = self.client().get('/students')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/students?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_given_student(self):
        res = self.client().get('/students/'+self.row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_not_exist(self):
        res = self.client().get('/students/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_student(self):
        res = self.client().post('/students', json=self.new_student)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_student(self):
        res = self.client().put('/students/'+self.row_num, json=self.new_student)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_student_not_exist(self):
        res = self.client().put('/students/10000', json=self.new_student)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_remove_student(self):
        res = self.client().delete('/students/'+self.del_row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_remove_student_not_exist(self):
        res = self.client().delete('/students/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
# ****************************************************************
    ''' 
    Professor test

    '''

    def test_given_professors(self):
        res = self.client().get('/professors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/professors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_professor(self):
        res = self.client().post('/professors', json=self.new_professor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_given_professor(self):
        res = self.client().get('/professors/'+self.row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_not_exist(self):
        res = self.client().get('/professors/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_professor(self):
        res = self.client().put('/professors/'+self.row_num, json=self.new_professor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_professor_not_exist(self):
        res = self.client().put('/professors/10000', json=self.new_professor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_remove_professor(self):
        res = self.client().delete('/professors/'+self.del_row_num)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_remove_professors_not_exist(self):
        res = self.client().delete('/professors/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
# *******************************************************************************************
    ''' 
    Professor test
    
    '''
    def test_given_enrollments(self):
        res = self.client().get('/enrollments')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/enrollments?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_enrollment(self):
        res = self.client().post('/enrollments',json=self.new_enrollment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_given_enrollment(self):
        res = self.client().get('/enrollments/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_not_exist(self):
        res = self.client().get('/enrollments/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_enrollment(self):
        res = self.client().put('/enrollments/1',json=self.new_enrollment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_enrollment_not_exist(self):
        res = self.client().put('/enrollments/10000',json=self.new_enrollment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # def test_remove_enrollment(self):
    #     res = self.client().delete('/enrollments/1')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_404_remove_enrollments_not_exist(self):
        res = self.client().delete('/enrollments/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
