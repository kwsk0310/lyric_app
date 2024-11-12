from flask import Flask, render_template, jsonify, request

from app_class import UtaMap, UtaNet, UtaTen, KKBox


# 創建一個 Flask 應用程式實例
app = Flask(__name__)
webDict = {
    'UtaMap': UtaMap(),
    'UtaNet': UtaNet(),
    'UtaTen': UtaTen(),
    'KKBox': KKBox(),
}

# 定義一個路由，當使用者訪問主頁 ("/") 時，回傳 "Hello, World!"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lyrics')
def lyrics():
    # 從 URL 參數中提取歌詞資料
    songName = request.args.get('songName') or ''
    lyric = request.args.get('lyric') or ''
    
    # 渲染歌詞頁面，將資料傳遞給模板
    return render_template('lyric.html', songName=songName, lyric=lyric)

# 處理 POST 請求
@app.route('/get-songList', methods=['POST'])
def get_songList():
    data = request.get_json()
    webName = data.get('web')
    songName = data.get('songName')
    # 根據 'web' 找到對應的 web 對象
    web = webDict.get(webName)  # 這裡假設 webDict 是一個字典，包含了所有 web 對象
    if not web:
        return jsonify({'error': 'Invalid web key'}), 400  # 若找不到對應的 web，返回錯誤
    songList = web.search_songs(songName)

    # 顯示接收到的資料
    return jsonify({'songList': songList, 'web': webName})

@app.route('/get-lyric', methods=['POST'])
def get_lyrics():
    data = request.get_json()
    web = data.get('web')
    url = data.get('url')
    songName = data.get('songName')
    web = webDict[web]
    lyric = web.search_lyrics(url)

    # 顯示接收到的資料
    return jsonify({'songName': songName, 'lyric': lyric})

# 啟動伺服器
if __name__ == '__main__':
    app.run(debug=True, port=5000)