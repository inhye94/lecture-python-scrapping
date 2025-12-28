from playwright.sync_api import sync_playwright

URL = "https://www.jobkorea.co.kr/Search/?stext=프론트엔드"

# https://www.jobkorea.co.kr/Search?stext=프론트엔드&Page_No=4
results = []

def get_pages(url):
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )

    page = context.new_page()
    page.goto(url)

    # 페이지 수 가져오기
    page.wait_for_selector('nav[aria-label="pagination"]')
    pagenation = page.locator('nav[aria-label="pagination"]')
    total_pages = pagenation.locator('li:not(:first-child):not(:last-child)').count()

    browser.close()
    return total_pages

def scrape_jobkorea(url):
  print(f"🔍 Scraping {url}...")

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )

    page = context.new_page()
    page.goto(url)

    # 1️⃣ 첫 카드 로딩 대기
    page.wait_for_selector('div[data-sentry-component="CardJob"]')

    # 2️⃣ 스크롤해서 카드 더 로딩
    for _ in range(5):
      page.mouse.wheel(0, 3000)
      page.wait_for_timeout(1500)

    # 3️⃣ 카드 요소들 가져오기
    cards = page.locator('div[data-sentry-component="CardJob"]')
    print("🃏 카드 개수:", cards.count())

    # 4️⃣ 카드 정보 추출
    for i in range(cards.count()):
      card = cards.nth(i)

      excluded_colors = ["yellow", "theme-primary", "pink", "theme-secondary4", "theme-secondary2", "theme-secondary3"]

      # excluded_colors 리스트의 항목들을 각각 :not([data-accent-color="..."]) 으로 만들어
      # 하나의 선택자 문자열로 결합한 뒤 locator에 적용합니다.
      not_selectors = ''.join([f':not([data-accent-color="{c}"])' for c in excluded_colors])
      selector = f'span[data-sentry-element="Typography"]{not_selectors}'
      texts = card.locator(selector).all_inner_texts()

      title = texts[0]
      company = texts[1]
      location = texts[3]

      if not title:
        print(f"{i + 1} 번째 카드에서 제목을 찾을 수 없습니다.")
        print("texts:", texts)
      elif not company:
        print(f"{i + 1} 번째 카드에서 회사를 찾을 수 없습니다.")
        print("texts:", texts)
      elif not location:
        print(f"{i + 1} 번째 카드에서 위치를 찾을 수 없습니다.")
        print("texts:", texts)
      else:
        continue

      link = card.locator("a", has_text=title).get_attribute('href')

      # results.append({
      #   "title": title.strip(),
      #   "company": company.strip(),
      #   "location": location.strip(),
      #   "url": link.strip()
      # })

    browser.close()

# 결과 확인
total_pages = get_pages(URL)

for page in range(total_pages):
  scrape_jobkorea(f"{URL}&Page_No={page + 1}")

print("총 결과 개수:", len(results))

for r in results[:5]:
  print(r)
