from wanted_class import WantedScraper
from flask import Flask

app = Flask("JobScrapper")

@app.route("/")
def home():
  return "Hello! Welcome to Job Scrapper!"

app.run(debug=True) # http://127.0.0.1:5000/에서 브라우저 실행됨. 터미널에서 cmd+c하면 서버 꺼짐

# # 키워드로 스크래핑 레츠고
# keywords = ["react", "nextjs", "flutter"]
# scraper = WantedScraper()
# scraper.open()

# for keyword in keywords:
#   datas = scraper.scrape(keyword)
#   scraper.save_to_csv(datas, keyword)

# scraper.close()