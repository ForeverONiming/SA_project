===========================================
醫療預約系統 Django 專案
===========================================

[執行方法]
-------------------------
1. 安裝 Python（建議 3.9 以上）
2. 安裝專案依賴套件
   pip install -r requirements.txt

3. 初始化資料庫
   python manage.py makemigrations
   python manage.py migrate

4. 創建管理員帳號（可選）
   python manage.py createsuperuser

5. 啟動本地伺服器
   python manage.py runserver

6. 開啟瀏覽器，輸入
   http://127.0.0.1:8000/

-------------------------
[注意事項]
-------------------------
- 初次部署時請務必執行 `makemigrations` 與 `migrate`。
- 預設 SQLite 資料庫檔為 `db.sqlite3`，可依需求修改。
- 靜態檔案（staticfiles）**不需手動上傳或維護**，請用：
    python manage.py collectstatic
  於正式部署（如 Render）時自動產生。

- 若有新增或修改 models.py（資料表結構），請再次執行
    python manage.py makemigrations
    python manage.py migrate

- 建議將 `.env`、`db.sqlite3`、`staticfiles/` 等資料夾/檔案加入 `.gitignore`，避免敏感資訊上傳。

- 開發完成後，請刪除預設密碼、不要在公開倉庫留存私人資料。

-------------------------
[管理員後台]
-------------------------
- 進入 http://127.0.0.1:8000/admin/ 使用 superuser 登入，可管理所有資料。

-------------------------
[醫師專屬功能]
-------------------------
- 註冊醫師帳號後，可使用專屬後台查看屬於自己的預約。

-------------------------
有任何問題請聯絡專案負責人。
