from requests import get
from bs4 import BeautifulSoup

origin_url = "https://weworkremotely.com/remote-full-time-jobs"

all_jobs = []

def scrape_jobs(url):
    print(f"Scrapping {url}...")

    response = get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find('section', {'class': 'jobs'}).find_all('li')[:-1]

    for job in jobs:
        title = job.find('h3', class_='new-listing__header__title').text.strip()
        company = job.find('p', class_='new-listing__company-name').text.strip()
        location = job.find('p', class_='new-listing__company-headquarters').text.strip() if job.find('p', class_='new-listing__company-headquarters') else 'Worldwide'
        url = job.find('div', class_='tooltip--flag-logo').next_sibling['href']

        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'url': f"https://weworkremotely.com{url}"
        }

        all_jobs.append(job_data)

    return all_jobs

def find_pagenation(url):
    response = get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    return len(soup.find('div', class_="pagination").find_all('span', class_="page"))

total_pages = find_pagenation(origin_url)

for x in range(total_pages):
    job_list_url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_jobs(job_list_url)

print("all jobs scraped", len(all_jobs))