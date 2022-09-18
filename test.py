import json
from turtle import pd
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class FlaskTests(TestCase):
    def test_get_start_form(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                '<form action="/" method="POST" id="row-form" class="ui form container">', html)

    def test_submit_row_form(self):
        with app.test_client() as client:
            res = client.post("/", data={"row": "5"})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(
                '<form action="/" method="POST" id="row-form" class="ui form container">', html)
            self.assertIn("</table>", html)
            self.assertEqual(session["row"], 5)
            self.assertEqual(session["highest_score"], 0)
            self.assertIs(type(session["board"]), list)

    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["row"] = 5
                change_session["board"] = [['C', 'W', 'A', 'A', 'M'],
                                           ['L', 'D', 'W', 'C', 'P'],
                                           ['T', 'P', 'V', 'B', 'M'],
                                           ['O', 'P', 'W', 'T', 'W'],
                                           ['T', 'U', 'N', 'Y', 'M']]

            res = client.get("/check?word=some_word")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.is_json, True)
            self.assertIn("result", html)

    def test_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["highest_score"] = 20

            res = client.post("/score", data={"score": 50})

            self.assertEqual(session["highest_score"], 50)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_score_redirect(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["highest_score"] = 20

            res = client.post(
                "/score", data={"score": 50}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                '<form action="/" method="POST" id="row-form" class="ui form container">', html)
