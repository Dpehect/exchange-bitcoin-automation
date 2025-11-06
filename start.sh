#!/bin/bash

# Bitcoin ve Borsa Fiyat Takip Uygulaması Başlatma Scripti

echo "🚀 Bitcoin ve Borsa Fiyat Takip Uygulaması Başlatılıyor..."
echo ""

# Python'un yüklü olup olmadığını kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python3 yükleyin."
    exit 1
fi

# Gerekli kütüphanelerin yüklü olup olmadığını kontrol et
echo "📦 Gerekli kütüphaneler kontrol ediliyor..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask bulunamadı. Kütüphaneler yükleniyor..."
    pip3 install -r requirements.txt
fi

# Backend sunucusunu başlat
echo ""
echo "🌐 Backend sunucusu başlatılıyor..."
echo "📡 API: http://localhost:5000"
echo ""
echo "💡 Tarayıcınızda index.html dosyasını açın!"
echo "💡 Durdurmak için Ctrl+C tuşlarına basın"
echo ""

python3 app.py

