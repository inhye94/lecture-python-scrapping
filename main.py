from wanted_class import WantedScraper
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

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

  # 키워드가 없으면 홈으로 리다이렉트
  if keyword == None:
    return redirect("/")

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

@app.route('/export')
def export():
  # 키워드 가져오기
  keyword = request.args.get('keyword')

  # 키워드가 없으면 홈으로 리다이렉트
  if keyword == None:
    return redirect("/")
  
  # 키워드가 db에 없으면 검색으로 리다이렉트
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  
  WantedScraper.save_to_csv(db[keyword], keyword)
  return send_file(f"scraped_datas/wanted_{keyword}_jobs.csv", as_attachment=True, download_name=f'{keyword}.csv')


if __name__ == "__main__":
  app.run(debug=True, port=5001)

# # 키워드로 스크래핑 레츠고
# keywords = ["react", "nextjs", "flutter"]
# scraper = WantedScraper()
# scraper.open()

# for keyword in keywords:
#   datas = scraper.scrape(keyword)
#   scraper.save_to_csv(datas, keyword)

# scraper.close()