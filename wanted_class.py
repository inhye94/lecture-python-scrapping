# 원티드 홈부터 시작
# playwright로 검색 > 포지션 > 3초 멈춤 > 스크롤 3번 내린 뒤 > 카드 긁어오기

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class WantedScraper:
  BASE_URL = "https://www.wanted.co.kr"

  def __init__(self):
    self.browser = None
    self.content = None
    self.page = None

  # 브라우저 설정
  def open(self):
    self.playwright = sync_playwright().start()
    self.browser = self.playwright.chromium.launch(headless=True)
    context = self.browser.new_context(
      user_agent=(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/120.0.0.0 Safari/537.36"
        )
      )

    self.page = context.new_page()
  
  def close(self):
    if (self.browser):
      self.browser.close()
    self.playwright.stop()

  # 광고 닫기
  def close_ad(self):
    try:
      ad_iframe = self.page.wait_for_selector('iframe[title="WANTED"]', timeout=5000)
      close_button = ad_iframe.locator('div.close').first
      close_button.wait_for(timeout=3000)
      close_button.click()
    except:
      pass

  # 검색
  def search(self, keyword):
    self.page.goto(f"{self.BASE_URL}/search?query={keyword}&tab=position")
    
    # self.page.goto(self.BASE_URL)
    # self.close_ad()

    # self.page.wait_for_selector('button[aria-label="검색"]')

    # self.page.locator('button[aria-label="검색"]').click()
    # self.page.get_by_placeholder("검색어를 입력해 주세요.").fill(keyword)
    # self.page.keyboard.press("Enter")


    # time.sleep(3)
    # self.page.click('a#search_tab_position')
    # time.sleep(3)

  # 스크롤 내리기
  def scroll_down(self, times=3):
    for _ in range(times):
      # page.mouse.wheel(0, 300)
      self.page.keyboard.press("End")
      time.sleep(2)
  
  # 카드 데이터 가져오기
  def parse_jobs(self):
    # 카드 요소들 가져오기
    self.content = self.page.content()
    soup = BeautifulSoup(self.content, "html.parser")
    cards = soup.find_all("a", {"data-position-list-type": "card"})

    jobs = []

    for card in cards:
      link = f"{self.BASE_URL}{card['href']}"
      company = card["data-company-name"]

      title_element = card.find('strong')
      title = title_element.text if title_element else None

      reward_element = card.find('span', class_="JobCard_reward__oCSIQ")
      reward = reward_element.text if reward_element else None

      jobs.append({
        "title": title,
        "company": company,
        "link": link,
        "reward": reward
      })

    return jobs
  

  # 원티드 채용 정보 스크래핑
  def scrape(self, keyword):
    print(f"🔍 Scraping wanted.co.kr for {keyword}...")
    self.search(keyword)
    self.scroll_down(times=3)
    return self.parse_jobs()

  # CSV로 저장
  @staticmethod
  def save_to_csv(datas, filename):
    file = open(f"scraped_datas/wanted_{filename}_jobs.csv", "w", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=datas[0].keys())
    writer.writeheader()
    writer.writerows(datas)

# 키워드로 스크래핑 레츠고
keywords = ["react", "nextjs", "flutter"]
scraper = WantedScraper()
scraper.open()

for keyword in keywords:
  datas = scraper.scrape(keyword)
  scraper.save_to_csv(datas, keyword)

scraper.close()