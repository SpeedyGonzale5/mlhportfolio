import os
from flask import Flask, render_template, request, json, Response, abort, jsonify
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime
import json
from logging import error
load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306
                         )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


profile_file = open("app/static/data/profile.json")
profile = json.load(profile_file)

experience_file = open("app/static/data/exp.json")
experience = json.load(experience_file)

education_file = open("app/static/data/edu.json")
education = json.load(education_file)

pexperience_file = open("app/static/data/pexp.json")
pexperience = json.load(pexperience_file)

peducation_file = open("app/static/data/pedu.json")
peducation = json.load(peducation_file)

rhobbies_file = open("app/static/data/hobbies.json")
rhobbies = json.load(rhobbies_file)


phobbies_file = open("app/static/data/phobbies.json")
phobbies = json.load(phobbies_file)


@ app.route("/")
def index():
    return render_template("index.html", title="Cyber Sapiens", url=os.getenv("URL"))


@app.route("/home2")
def home2():
    return render_template("home2.html", title="New Homepage")

# First timeline


@ app.route("/timeline")
def timeline():
    return render_template("timeline.html", timeline_profiles=profile)


@ app.route("/timeline/Roa/pro")
def rexperience():
    return render_template("rexp.html", rexperience=experience, redu=education)


@ app.route("/timeline/Pedro/pro")
def experiencep():
    return render_template("pexp.html", pexperience=pexperience, pedu=peducation)


@ app.route("/timeline/Roa/hobbies")
def hobbiesr():
    return render_template("rhobbies.html", rhobbies=rhobbies)


@ app.route("/timeline/Pedro/hobbies")
def hobbiesp():
    return render_template("phobbies.html", phobbies=phobbies)

# Maps Section


@ app.route("/maps")
def map():
    return render_template("maps.html", apikey=os.getenv("mapkey"))

# Second Timeline


@app.route("/timeline2")
def timeline2():
    return render_template("timeline2.html", title="Timeline 2")


# Endpoint to retrieve timelineposts


@app.route("/api/timeline_post", methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if content == "" or content is None:
        return "Invalid content", 400
    elif name == "" or name is None:
        return "Invalid name", 400
    elif email == "" or email is None or "@" not in email:
        return "Invalid email", 400
    else:
        timeline_post = TimelinePost.create(
            name=name, email=email, content=content)
        return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
