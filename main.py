"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from scrapper import remoteok_scrapper, stackoverflow_scrapper, weworkremotely_scrapper
from exporter import save_to_file

app = Flask("RomoteScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    term = request.args.get("term")
    if term:
        term = term.lower().strip()
        existingJobs = db.get(term)
        if existingJobs:
            jobs = existingJobs
        else:
            remoteok_list = remoteok_scrapper(term)
            stackoverflow_list = stackoverflow_scrapper(term)
            weworkremotely_list = weworkremotely_scrapper(term)
            jobs = remoteok_list + stackoverflow_list + weworkremotely_list

        if len(jobs) == 0:
            error = f"There are no jobs for {term}!"
        else:
            error = ""
            db[term] = jobs

    return render_template(
        "search.html",
        searchingBy=term,
        resultsNumber=len(jobs),
        jobs=jobs,
        error=error)


@app.route("/export")
def export():
    try:
        term = request.args.get('term')
        if not term:
            raise Exception()
        jobs = db.get(term)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file(
            "jobs.csv",
            mimetype="text/csv; charset='UTF-8'",
            attachment_filename=f"{term}.csv",
            as_attachment=True)
    except:
        return redirect("/")


app.run(host="0.0.0.0")
