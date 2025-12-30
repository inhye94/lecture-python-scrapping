# 원티드 홈부터 시작
# playwright로 검색 > 포지션 > 3초 멈춤 > 스크롤 3번 내린 뒤 > 카드 긁어오기

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

URL = "https://www.wanted.co.kr"

jobs = []

with sync_playwright() as p:
  # 브라우저 설정
  browser = p.chromium.launch(headless=True)
  context = browser.new_context(
    user_agent=(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36"
    )
  )

  page = context.new_page()
  page.goto(URL)

  # 광고 닫기
  # ad_iframe = page.frame_locator('div.ab-iam-root')

  # if ad_iframe:
  #   ad_iframe.locator('button.close').click()

  # 검색창 대기
  page.wait_for_selector('button[aria-label="검색"]')

  # 검색어 입력
  page.locator('button[aria-label="검색"]').click()
  page.get_by_placeholder("검색어를 입력해 주세요.").fill("프론트엔드")
  page.keyboard.press("Enter")


  # 포지션 페이지 대기
  time.sleep(3)
  page.click('a#search_tab_position')
  time.sleep(3)

  # 스크롤 3번 내리기
  for _ in range(3):
    # page.mouse.wheel(0, 300)
    page.keyboard.press("End")
    time.sleep(2)


  # 카드 요소들 가져오기
  content = page.content()
  soup = BeautifulSoup(content, "html.parser")
  cards = soup.find_all("a", {"data-position-list-type": "card"})

  for card in cards:
    link = f"{URL}{card['href']}"
    company = card["data-company-name"]
    title = card.find('strong').text
    reward = card.find('span', class_="JobCard_reward__oCSIQ").text
    
    jobs.append({
      "title": title,
      "company": company,
      "link": link,
      "reward": reward
    })

  print(jobs)
  
  browser.close()