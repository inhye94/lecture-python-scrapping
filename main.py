from wanted_class import WantedScraper
from flask import Flask, render_template, request

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html", page="Home", name="inhye")

@app.route("/hello")
def hello():
    return "<h1>Hey there!</h1>"

@app.route("/search")
def search():
    # 키워드 가져오기
    keyword = request.args.get('keyword')

    datas = None

    # 임의로 저장한 데이터를 가져오거나 웹 스크래핑 진행
    if keyword in db:
      datas = db[keyword]
      print("존재")
    else:
      print("존재하지 않음")
      scraper = WantedScraper()
      scraper.open()
      datas = scraper.scrape(keyword)
      scraper.close()

      db[keyword] = datas

    # 데이터 렌더링
    return render_template("search.html", page="Search", keyword = keyword, list = datas)

app.run(debug=True) # http://127.0.0.1:5000/에서 브라우저 실행됨. 터미널에서 cmd+c하면 서버 꺼짐

# # 키워드로 스크래핑 레츠고
# keywords = ["react", "nextjs", "flutter"]
# scraper = WantedScraper()
# scraper.open()

# for keyword in keywords:
#   datas = scraper.scrape(keyword)
#   scraper.save_to_csv(datas, keyword)

# scraper.close()