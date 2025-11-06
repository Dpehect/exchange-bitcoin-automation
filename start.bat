@echo off
REM Bitcoin ve Borsa Fiyat Takip Uygulaması Başlatma Scripti (Windows)

echo 🚀 Bitcoin ve Borsa Fiyat Takip Uygulaması Başlatılıyor...
echo.

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python yükleyin.
    pause
    exit /b 1
)

REM Gerekli kütüphanelerin yüklü olup olmadığını kontrol et
echo 📦 Gerekli kütüphaneler kontrol ediliyor...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask bulunamadı. Kütüphaneler yükleniyor...
    pip install -r requirements.txt
)

REM Backend sunucusunu başlat
echo.
echo 🌐 Backend sunucusu başlatılıyor...
echo 📡 API: http://localhost:5000
echo.
echo 💡 Tarayıcınızda index.html dosyasını açın!
echo 💡 Durdurmak için Ctrl+C tuşlarına basın
echo.

python app.py

pause

