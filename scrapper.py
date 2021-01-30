import requests
from bs4 import BeautifulSoup


def remoteok_scrapper(term):
    base_url = "https://remoteok.io"
    search_url = f"{base_url}/remote-dev+{term}-jobs"
    response = requests.get(search_url)
    try:
        if response.status_code != 200:
            raise Exception()
        else:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("table", {"id": "jobsboard"})
            items = table.find_all("tr", {"class": "job"})
            remoteok_list = []
            for item in items:
                data = item.find("td", {"class": "company_and_position"})
                title = data.find("h2", {"itemprop": "title"})
                if title:
                    title = title.string.strip()
                company = data.find("h3", {"itemprop": "name"})
                if company:
                    company = company.string.strip()
                link = data.find("a", {"itemprop": "url"})
                if link:
                    link = base_url + link["href"]

                if title is not None and company is not None and link is not None:
                    job = {
                        "site": "remoteOK",
                        "title": title,
                        "company": company,
                        "link": link,
                        "img": "https://www.blocksocial.com/wp-content/uploads/2019/07/remoteok-logo.jpg"
                    }
                remoteok_list.append(job)
            return remoteok_list
    except Exception as e:
        print(e)
        return []


def stackoverflow_scrapper(term):
    base_url = "https://stackoverflow.com"
    search_url = f"{base_url}/jobs?r=true&q={term}"
    response = requests.get(search_url)
    try:
        if response.status_code != 200:
            raise Exception()
        else:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # Stack Overflow don't give 404 error, it recommend similar jobs
            # Therefore, let check found '# jobs' and if '0 jobs', return empty list.
            jobsNumber = soup.find("span", {"class": "description"})
            if jobsNumber:
                jobsNumber = jobsNumber.get_text().strip()
                if jobsNumber == '0 jobs':
                    return []

            table = soup.find("div", {"class": "listResults"})
            items = table.find_all("div", {"class": "-job"})
            stackoverflow_list = []
            for item in items:
                title = item.find("a", {"class": "s-link"})

                if title:
                    title = title.string.strip()
                company = item.find("h3")
                if company:
                    company = company.find(
                        "span",
                        recursive=False).string.strip().strip('\n').strip('\r')
                link = item.find("a", {"class": "s-link"})
                if link:
                    link = base_url + link["href"]

                if title is not None and company is not None and link is not None:
                    job = {
                        "site": "Stack Overflow",
                        "title": title,
                        "company": company,
                        "link": link,
                        "img": "https://miro.medium.com/max/1200/0*UEtwA2ask7vQYW06.png"
                    }
                    stackoverflow_list.append(job)
            return stackoverflow_list
    except Exception as e:
        print(e)
        return []


def weworkremotely_scrapper(term):
    base_url = "https://weworkremotely.com"
    search_url = f"{base_url}/remote-jobs/search?term={term}"
    response = requests.get(search_url)
    try:
        if response.status_code != 200:
            raise Exception()
        else:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("section", {"class": "jobs", "id": "category-2"})
            items = table.find_all("li", {"class": "feature"})
            weworkremotely_list = []
            for item in items:
                title = item.find("span", {"class": "title"})
                if title:
                    title = title.string.strip()
                company = item.find("span", {"class": "company"})
                if company:
                    company = company.string.strip()
                link = item.find("a")
                if link:
                    link = base_url + link["href"]

                if title is not None and company is not None and link is not None:
                    job = {
                        "site": "We Work Remotely",
                        "title": title,
                        "company": company,
                        "link": link,                     
                        "img": "https://files.growsumo.com/companyLogo/file_S2jVhU54hssUnC.png"
                    }
                    weworkremotely_list.append(job)
            return weworkremotely_list
    except Exception as e:
        print(e)
        return []
