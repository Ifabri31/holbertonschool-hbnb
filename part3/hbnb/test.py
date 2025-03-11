import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # User Creation Tests
    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Fabri",
            "last_name": "Oviedo",
            "email": "fabri@example.com",
            "password": "Pep8"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_used_email(self):
        # Assuming the email was already registered
        self.client.post('/api/v1/users/', json={
            "first_name": "Fran",
            "last_name": "Reyes",
            "email": "example@example.com",
            "password": "8pep"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "El",
            "last_name": "Jona",
            "email": "example@example.com",  # Duplicate email
            "password": "jonita"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        # Create a user to retrieve
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jone.doe@example.com",
            "password": "jd"
        })        
        # Extract the user ID from the response
        user = res.get_json()  
        self.assertIn('id', user)
        user_id = user['id']
    
        # Retrieve the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

        returned_user = response.get_json()
        self.assertEqual(returned_user['id'], user_id)
        self.assertEqual(returned_user['email'], "jone.doe@example.com")
        self.assertEqual(returned_user['first_name'], "Jane")
        self.assertEqual(returned_user['last_name'], "Doe")
        self.assertEqual(returned_user['password'], "jd")

    def test_get_user_by_id_not_found(self):
        response = self.client.get('/api/v1/users/999')
        self.assertEqual(response.status_code, 404)

    # Place Creation Tests
    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
                "title": "Cozy Apartment",
                "description": "A nice place to stay",
                "price": 100.0,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 201)
        
    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
                "title": "casa",
                "description": "casa grande",
                "price": -777.0, #invalid price
                "latitude": 86.7749,
                "longitude": -176.4194,
                "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)    
    
    def test_create_place_invalid_tittle(self):
        response = self.client.post('/api/v1/places/', json={
                "title": "", #invalid tittle
                "description": "casa grande",
                "price": 100.0,
                "latitude": 86.7749,
                "longitude": -176.4194,
                "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude_and_latitude(self):
        response = self.client.post('/api/v1/places/', json={
                "title": "casa",
                "description": "casa grande",
                "price": 100.0,
                "latitude": 137.7749,  # Invalid latitude
                "longitude": -322.4194,  # Invalid longitude
                "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review(self):
        # First, create a user to associate with the review
        self.client.post('/api/v1/users/', json={
            "first_name": "Fabri",
            "last_name": "Reyes",
            "email": "example@example.com"
        })

        # Create a review
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Great place!",
            "rating": 5,
            "user_id": "1",
            "place_id": "1"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "",
            "rating": 6,  # Invalid rating (should be between 1-5)
            "user_id": "",  # Invalid user ID
            "place_id": ""  # Invalid place ID
        })
        self.assertEqual(response.status_code, 400)

    def test_get_review_by_id(self):
        # Create a review to retrieve
        res = self.client.post('/api/v1/reviews/', json={
            "comment": "Great place",
            "rating": 5,
            "user_id": "1",
            "place_id": "1"
        })
        
        # Extract the review ID from the response
        review = res.get_json()
        self.assertIn('id', review)
        review_id = review['id']

        # Retrieve the review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        returned_review = response.get_json()
        self.assertEqual(returned_review['id'], review_id)

    def test_update_review(self):
        # Create a review to update
        res = self.client.post('/api/v1/reviews/', json={
            "comment": "A decent place.",
            "rating": 3,
            "user_id": "1",
            "place_id": "1"
        })
        
        review = res.get_json()
        review_id = review['id']
        
        # Update the review
        update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "Updated review text.",
            "rating": 4
        })
        self.assertEqual(update_response.status_code, 200)

        # Verify the update
        updated_review = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(updated_review.get_json()['comment'], "Updated review text.")
        self.assertEqual(updated_review.get_json()['rating'], 4)

    def test_delete_review(self):
        # Create a review to delete
        res = self.client.post('/api/v1/reviews/', json={
            "comment": "Will not return.",
            "rating": 2,
            "user_id": "1",
            "place_id": "1"
        })
        
        review = res.get_json()
        review_id = review['id']

        # Delete the review
        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)

        # Verify that the review has been deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_all_reviews(self):
        # Create same reviews
        self.client.post('/api/v1/reviews/', json={
            "comment": "Review 0",
            "rating": 5,
            "user_id": "1",
            "place_id": "1"
        })
        self.client.post('/api/v1/reviews/', json={
            "comment": "Review 01",
            "rating": 4,
            "user_id": "1",
            "place_id": "1"
        })

        # Retrieve all reviews
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        reviews = response.get_json()
        self.assertGreaterEqual(len(reviews), 2)  # Ensure there are at least 2 reviews

if __name__ == '__main__':
    unittest.main()