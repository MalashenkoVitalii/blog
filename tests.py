from datetime import datetime, timedelta
import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        """ run setUp test"""
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """end test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="Mark")
        u.set_password('dog')
        self.assertFalse(u.check_password("cat"))
        self.assertTrue(u.check_password("dog"))

    def test_avatar(self):
        u = User(username="Mark", email="mark@ukr.net")
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/e6cac309e9b898798cca2d70de75df9a?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username="john", email="john@ukr.net")
        u2 = User(username="susan", email="susan@ukr.net")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))

    def test_followed_posts(self):
        u1 = User(username="john", email="john@ukr.net")
        u2 = User(username="susan", email="susan@ukr.net")
        u3 = User(username="mary", email="mary@ukr.net")
        u4 = User(username="david", email="david@ukr.net")
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body="post John", author=u1, timestamp=now+timedelta(seconds=1))
        p2 = Post(body="post Susan", author=u2, timestamp=now+timedelta(seconds=1))
        p3 = Post(body="post Mary", author=u3, timestamp=now+timedelta(seconds=1))
        p4 = Post(body="post David", author=u4, timestamp=now+timedelta(seconds=1))
        db.session.add_all([p1, p2, p3, p4])

        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)

        db.session.commit()
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        print(f1, f2, f3, f4)
        self.assertEqual(f1, [p1, p2, p4])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)