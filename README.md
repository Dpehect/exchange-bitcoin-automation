# 🚀 Bitcoin ve Borsa Fiyat Takip Uygulaması

Bitcoin ve hisse senetlerindeki fiyat değişimlerini takip eden ve yükseliş/düşüşleri tespit eden Python uygulaması. **Vue.js** ile modern web arayüzü içerir!

## ✨ Özellikler

- 📊 **Bitcoin Fiyat Takibi**: CoinGecko API kullanarak Bitcoin fiyatını takip eder
- 📈 **Hisse Senedi Takibi**: Yahoo Finance API ile popüler hisse senetlerini takip eder
- 🚨 **Otomatik Uyarılar**: Belirlenen eşik değerini aşan değişimlerde uyarı verir
- 📝 **Raporlama**: Tüm uyarıları JSON formatında kaydedebilir
- ⏱️ **Sürekli Takip**: Belirli aralıklarla otomatik fiyat kontrolü yapar
- 🌐 **Web Arayüzü**: Vue.js ile modern, responsive web arayüzü
- 📊 **Grafikler**: Chart.js ile interaktif fiyat grafikleri
- 🔄 **Gerçek Zamanlı Güncelleme**: Otomatik fiyat güncellemeleri

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- İnternet bağlantısı

## 🛠️ Kurulum

1. Projeyi klonlayın veya indirin:
```bash
cd exchange-bitcoin
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

veya

```bash
pip3 install -r requirements.txt
```

## ⚡ Hızlı Başlangıç

### macOS/Linux:
```bash
./start.sh
```

### Windows:
```bash
start.bat
```

veya manuel olarak:
```bash
python app.py
```

Sonra tarayıcınızda `index.html` dosyasını açın!

## 🚀 Kullanım

### 🌐 Web Arayüzü ile Kullanım (Önerilen)

1. **Backend sunucusunu başlatın:**
```bash
python app.py
```

2. **Tarayıcınızda `index.html` dosyasını açın:**
   - Dosyaya çift tıklayarak açabilirsiniz
   - Veya tarayıcıda `file:///path/to/index.html` adresini açın

3. **Web arayüzü özellikleri:**
   - 📊 Gerçek zamanlı fiyat gösterimi
   - 📈 İnteraktif grafikler
   - 🚨 Otomatik uyarı sistemi
   - 🔄 Otomatik güncelleme (açıp kapatılabilir)
   - 📱 Responsive tasarım (mobil uyumlu)

### 💻 Komut Satırı Kullanımı

```bash
python bitcoin_stock_monitor.py
```

### Program Seçenekleri

1. **Tek Seferlik Kontrol**: Mevcut fiyatları bir kez kontrol eder
2. **Sürekli Takip**: Her 60 saniyede bir otomatik kontrol yapar
3. **Özel Aralık**: Kendi belirlediğiniz aralıkta sürekli takip yapar

### Kod İçinde Kullanım

```python
from bitcoin_stock_monitor import PriceMonitorApp

# Uygulamayı oluştur
app = PriceMonitorApp(
    stock_symbols=['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
    threshold=1.0  # %1 değişim eşiği
)

# Tek seferlik kontrol
app.monitor_once()

# Sürekli takip (60 saniye aralıkla)
app.monitor_continuous(interval=60)
```

## ⚙️ Yapılandırma

### Takip Edilecek Hisse Senetleri

`bitcoin_stock_monitor.py` dosyasındaki `main()` fonksiyonunda `stock_symbols` listesini düzenleyebilirsiniz:

```python
stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
```

### Eşik Değeri

Uyarı için minimum değişim yüzdesini ayarlayabilirsiniz:

```python
threshold = 1.0  # %1 değişim
```

## 📊 Çıktı Örneği

```
╔══════════════════════════════════════════════════════════╗
║   🚀 Bitcoin ve Borsa Fiyat Takip Uygulaması 🚀         ║
║   Yükseliş ve Düşüşleri Tespit Edin                     ║
╚══════════════════════════════════════════════════════════╝

============================================================
📊 BTC/USD
💰 Fiyat: $43,250.50
🕐 Zaman: 2024-01-15 14:30:00
============================================================

🚀 🚀 UYARI! 🚀 🚀
============================================================
📊 Sembol: BTC/USD
💰 Önceki Fiyat: $42,800.00
💰 Güncel Fiyat: $43,250.50
📈 Değişim: +1.05%
📊 Tip: YÜKSELİŞ
🕐 Zaman: 2024-01-15 14:30:00
============================================================
```

## 📝 Uyarı Kaydetme

Uyarılar JSON formatında kaydedilebilir:

```python
app.save_alerts_to_file('alerts.json')
```

## 🔧 API'ler

- **Bitcoin**: CoinGecko API (ücretsiz, API anahtarı gerekmez)
- **Hisse Senetleri**: Yahoo Finance API (yfinance kütüphanesi)

## ⚠️ Notlar

- CoinGecko API'si ücretsizdir ancak rate limit'i vardır
- Yahoo Finance API'si bazen gecikmeli veri sağlayabilir
- Gerçek zamanlı veriler için ücretli API'ler kullanılabilir

## 📄 Lisans

Bu proje eğitim amaçlıdır.

## 🤝 Katkıda Bulunma

Önerileriniz ve katkılarınız için issue açabilirsiniz.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

