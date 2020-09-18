import requests
from bs4 import BeautifulSoup

ROOMKEY_URL = "https://covid19.lacounty.gov/incident-updates/"


def parse_latest_incident_link():
    page = requests.get(ROOMKEY_URL)
    soup = BeautifulSoup(page.text, "html.parser")

    incident_updates_heading = soup.find("h3", text="Incident Updates")
    updates_this_month = incident_updates_heading.parent.next_sibling
    latest_update_link = updates_this_month.findChild("a")

    return latest_update_link["href"]


def save_latest_incident_update_from_project_roomkey_site():
    link = parse_latest_incident_link()
    filename = link.split("/")[-1]
    r = requests.get(link)

    with open(filename, "wb") as f:
        f.write(r.content)

    return filename
