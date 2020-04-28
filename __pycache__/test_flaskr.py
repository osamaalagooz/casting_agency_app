import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config['SECRET_KEY'] = 'secretkeyfortesting'
        self.client = self.app.test_client
        self.database_name = "test_casting"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'robot9000', 'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_movie = {
            'title': 'Attack On Titan',
            'release_date': '8-7-2026'
        }
        self.new_actor = {
            'name': 'Tota',
            'age': 28,
            'gender': 'male'            
        }
        self.director_role_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlPWlpYZGlEeGRUODFjZ3dWRXIyRiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEwNzA4NzQyNzQzNDM1MjE4NDEzIiwiYXVkIjpbInNob3dzIiwiaHR0cHM6Ly9jYXN0aW5nYWdlbmN5LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODgwODEwMDgsImV4cCI6MTU4ODE3NzU1MSwiYXpwIjoiWmpnVWtNQjlKeFFiaXMyaFZoMWQyZDlqZmN5ZVRaUXUiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.JcZp3mELB6FyMhkVZsWafear3Wj-k2t4OFoFPz0Rmie3yasxAqLd1byfi_BueClQeo_n9kTUlaGrAc3FSrFcpzO8dELE9UnGN0HL31oX7iKFAGWPbDgNft_AV0TaNYEDkjtNyrHOvzGCT2QFEKfvbbjB6k6H3kF13jS2lL4Kpc0bd4AAj4ch8pCAz9TeaCySM6wgOOzrhz9fvuLxup6UeOmcAyFOgPU05MVL_ZHYbbqa-a0t2DpekdLfh6vGmAu97ecBMgLBKdcbkWjJqsDrKLY50jZl8cRbG5E05UPk4CCB4H8jS3C5pLHvcQer_C2fP9EqWzNMBn5OTIVXlzsmLQ'
        self.assistant_role_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlPWlpYZGlEeGRUODFjZ3dWRXIyRiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImdpdGh1Ynw1OTM0MzYwMiIsImF1ZCI6WyJzaG93cyIsImh0dHBzOi8vY2FzdGluZ2FnZW5jeS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg4MDgyMTg1LCJleHAiOjE1ODgxNzg3MjgsImF6cCI6IlpqZ1VrTUI5SnhRYmlzMmhWaDFkMmQ5amZjeWVUWlF1Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.TyYuLICh14msMs_62dbnfWBIwoYD7chOHeSZkzLrCEdmPzGJaQirP8YdLOehVbrfMwzYTd83H4o3AAk0IEbVTXs0AD-yXFSNIx3qCYYs7YoRuk6BJPViJTgoEwLUmgKgpbc5xMnzWsl1p4snYmnXi0J2FLI8-gGp5lDn7Ok8eokwX7-80FzpY_4LwtUCZHhL__AV9J1Strkq-0tBGh-1uxk97_TptHrP7ycMEarzjcroah7AlMnweJi2KayFb8bJU5FuTTVo_pZPcuGlAg5XpJ_41zqQWUlPIB7bVPlP3tSmkVN56gkmyr0w3PpYpaDLO-6gdOY2NPijO4Vrh-NbJw'
        self.producer_role_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlPWlpYZGlEeGRUODFjZ3dWRXIyRiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE0NjQ0MTU3NDU0NDk2OTU5OTU5IiwiYXVkIjpbInNob3dzIiwiaHR0cHM6Ly9jYXN0aW5nYWdlbmN5LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODgwODA5MTksImV4cCI6MTU4ODE3NzQ2MiwiYXpwIjoiWmpnVWtNQjlKeFFiaXMyaFZoMWQyZDlqZmN5ZVRaUXUiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.XnoAVhkfbXdRQG1lcHXLcGWIXD7OEqS0C-Z2da9CIX3MeLp9n2lmR5npvQziTsEFORR4fSeJ66VkEyqb2M3gf8cielabQuegNCqTBd9qBLvnRDcDiFNHjEdrbRkcaTj5g_TSkcn4xdn2op1baCBTPsCDcWSYxxWjeIu1bgO4BibNzfbRx_j9KEpkvV88YMX1N4GJSW_BbqwQ4dw8ExRBXOWeFUC2KTAGKeUSleYZ7xuJVCpL9NyC_GZ3m4NdXz-GfSZ4sOTMALuMk-n3OT4LSNPJFhqihzJNGQYrBP1y2sq8xhe-VfPD-VNO_Xm3rSev1ai7DVKIl51_FWbizs-4Yg'
    def tearDown(self):
        pass        

    def test_get_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies_data'])

    def test_not_found(self):
        res = self.client().get('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.title == "Attack On Titan").first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies_data'])
        self.assertEqual(movie.title, 'Attack On Titan')

    def test_can_not_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Engineering'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)        


    def test_delete_movie(self):
        res = self.client().delete('/movies/7')
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies_data'])
        self.assertEqual(movie, None)

    def test_can_not_delete(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_not_found_delete(self):
        res = self.client().delete('/movies/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)


    def test_update_movie(self):
        res = self.client().patch('/movies/4', json= {'title': 'Normandy'})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['movies_data'])
        self.assertEqual(movie.title, 'Normandy')                
                    
    def test_not_found_update(self):
        res = self.client().patch('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_bad_req_to_update(self):
        res = self.client().patch('/movies/4', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['actors_data'])

    def test_not_found_actor(self):
        res = self.client().get('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        res = self.client().post("/actors", data=dict(name='Moneca5',age=29,gender='female'))
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.name == "Moneca").first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors_data'])
        self.assertEqual(actor.name, 'Moneca5')

    def test_can_not_create_actor(self):
        res = self.client().post('/actors?name=osama')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)        


    def test_delete_actor(self):
        res = self.client().delete('/actors/6')
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['actor_deleted'])
        self.assertEqual(actor, None)

    def test_can_not_delete_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_not_found_delete_actor(self):
        res = self.client().delete('/actors/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)


    def test_update_actor(self):
        res = self.client().patch('/actors/2', json= {'name': 'Ahmed Ezz'})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['actors_data'])
        self.assertEqual(actor.name, 'Ahmed Ezz')                
                    
    def test_not_found_update_actor(self):
        res = self.client().patch('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_bad_req_to_update_actor(self):
        res = self.client().patch('/actors/4', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_auth_assistant_role_success(self):
        with self.client() as c:
            with c.session_transaction() as session:
                session['Authorization'] = self.assistant_role_token
            res = c.get('/actors')
        self.assertEqual(res.status_code, 200)                     
    
    def test_auth_assistant_role_error(self):
            res = self.client().get('/actors')
            self.assertEqual(res.status_code, 401) 

    def test_auth_director_role_success(self):
        with self.client() as c:
            with c.session_transaction() as session:
                session['Authorization'] = self.director_role_token
            res = c.delete('/actors/1')
        self.assertEqual(res.status_code, 200)

    def test_auth_director_role_error(self):
            res = self.client().delete('/actors/1')
            self.assertEqual(res.status_code, 401)

    def test_auth_producer_role_success(self):
        with self.client() as c:
            with c.session_transaction() as session:
                session['Authorization'] = self.producer_role_token
            res = c.delete('/movies/1')
        self.assertEqual(res.status_code, 200)

    def test_auth_producer_role_error(self):
            res = self.client().get('/movies/1')
            self.assertEqual(res.status_code, 401)

if __name__=="__main__":
    unittest.main()        