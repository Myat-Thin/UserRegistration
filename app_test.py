import unittest
import os
import jwt
from app import app, users  # Assuming the Flask app is in a file called 'app.py'
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')

class UsersEndpointTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def generate_token(self, user):
        """Helper function to generate JWT token for a user."""
        return jwt.encode(
            {'id': user['id'], 'username': user['username'], 'role': user['role']},
            JWT_SECRET,
            algorithm='HS256'
        )

    def test_get_users_as_admin(self):
        """Test that an admin user can access the /users endpoint."""
        admin_user = users[0]  # Admin user from the simulated database
        token = self.generate_token(admin_user)
        
        # Make a request to /users with the admin token
        response = self.app.get('/users', headers={'Authorization': f'Bearer {token}'})
        
        # Assert the response is successful and contains the user list
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, users)

    def test_get_users_as_non_admin(self):
        """Test that a non-admin user cannot access the /users endpoint."""
        normal_user = users[1]  # Non-admin user
        token = self.generate_token(normal_user)
        
        # Make a request to /users with the non-admin token
        response = self.app.get('/users', headers={'Authorization': f'Bearer {token}'})
        
        # Assert the response is unauthorized
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['message'], 'Admin access required')

    def test_get_users_without_token(self):
        """Test that a request to /users without a token is unauthorized."""
        response = self.app.get('/users')
        
        # Assert the response is unauthorized
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Token is missing')



if __name__ == '__main__':
    unittest.main()
