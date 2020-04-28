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

    def test_can_not_create(self):
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

    def test_not_found(self):
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

    def test_can_not_create(self):
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

    def test_can_not_delete(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_not_found_delete(self):
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
                    
    def test_not_found_update(self):
        res = self.client().patch('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    def test_bad_req_to_update(self):
        res = self.client().patch('/actors/4', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)            
    
if __name__=="__main__":
    unittest.main()        