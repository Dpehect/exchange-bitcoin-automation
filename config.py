#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yapılandırma dosyası
Bu dosyayı düzenleyerek uygulama ayarlarını değiştirebilirsiniz.
"""

# Takip edilecek hisse senetleri
# Popüler semboller: AAPL (Apple), GOOGL (Google), MSFT (Microsoft), 
# TSLA (Tesla), AMZN (Amazon), META (Meta), NVDA (Nvidia)
STOCK_SYMBOLS = [
    'AAPL',   # Apple
    'GOOGL',  # Google
    'MSFT',   # Microsoft
    'TSLA',   # Tesla
    'AMZN',   # Amazon
]

# Uyarı için minimum değişim yüzdesi
# Örnek: 1.0 = %1 değişim
THRESHOLD_PERCENT = 1.0

# Sürekli takip modunda varsayılan kontrol aralığı (saniye)
DEFAULT_INTERVAL = 60

# Bitcoin API ayarları
BITCOIN_API_URL = "https://api.coingecko.com/api/v3/simple/price"
BITCOIN_SYMBOL = "bitcoin"
BITCOIN_CURRENCY = "usd"

# Uyarı dosyası adı
ALERTS_FILENAME = "alerts.json"

# Konsol çıktı ayarları
SHOW_DETAILED_INFO = True
SHOW_TIMESTAMP = True

