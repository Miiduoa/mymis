from flask import Flask, render_template, request
from datetime import datetime,timezone,timedelta

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>顧晉瑋Python網頁</h1>"
    homepage += "<a href='/today'>顯示日期時間</a><br>"
    homepage += "<a href='/about'>顧晉瑋簡介網頁</a><br>"
    homepage += "<a href='/account'>網頁表單傳值</a><br>"
    return homepage

@app.route("/today")
def today():
    # 設定時區為 UTC+8（臺灣）
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html", datetime=str(now))

@app.route("/about")
def about():
    return "<h1>顧晉瑋簡介網頁</h1><p>這裡放個人簡介內容，例如個人網頁、聯絡資訊等。</p>"

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd
        return result
    else:
        return render_template("account.html")

if __name__ == "__main__":
    app.run(debug=True)