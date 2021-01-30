import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["WebSite", "Title", "Company", "Link"])
    for job in jobs:
        if job:
            writer.writerow(list(job.values()))
    return
