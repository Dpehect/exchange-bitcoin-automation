# 🚀 Kullanım Kılavuzu

## Hızlı Başlangıç

### 1. Backend Sunucusunu Başlatın

Terminal'de şu komutu çalıştırın:

```bash
python3 app.py
```

veya

```bash
./start.sh
```

Sunucu başladığında şu mesajı göreceksiniz:
```
🚀 Flask API sunucusu başlatılıyor...
📡 API: http://localhost:5000
🌐 Frontend: index.html dosyasını tarayıcıda açın
```

### 2. Web Arayüzünü Açın

**Yöntem 1: Dosyaya çift tıklayın**
- `index.html` dosyasına çift tıklayın
- Varsayılan tarayıcınızda açılacaktır

**Yöntem 2: Tarayıcıdan açın**
- Tarayıcınızı açın (Chrome, Firefox, Safari, Edge)
- `Cmd+O` (Mac) veya `Ctrl+O` (Windows/Linux) tuşlarına basın
- `index.html` dosyasını seçin

**Yöntem 3: Sürükle-bırak**
- `index.html` dosyasını tarayıcı penceresine sürükleyip bırakın

### 3. Kullanım

Web arayüzü açıldığında:

1. **Fiyatları Görüntüleme**
   - Tüm fiyatlar otomatik olarak yüklenecektir
   - Her fiyat kartında güncel fiyat ve değişim yüzdesi gösterilir

2. **Otomatik Güncelleme**
   - Sağ üstteki "Otomatik Güncelleme" anahtarını açın
   - Her 5 saniyede bir fiyatlar otomatik güncellenecektir

3. **Uyarıları Kontrol Etme**
   - "Uyarıları Kontrol Et" butonuna tıklayın
   - Belirlenen eşik değerini aşan değişimler için uyarılar gösterilir

4. **Grafikleri Görüntüleme**
   - Alt kısımdaki grafik bölümünde fiyat geçmişini görebilirsiniz
   - Dropdown menüden farklı semboller seçebilirsiniz

## Özellikler

### 📊 Fiyat Kartları
- Bitcoin ve hisse senetleri için ayrı kartlar
- Renk kodlu değişim göstergeleri (yeşil: yükseliş, kırmızı: düşüş)
- Gerçek zamanlı fiyat bilgisi

### 📈 Grafikler
- İnteraktif fiyat grafikleri
- Farklı semboller için grafik görüntüleme
- Chart.js ile güçlü görselleştirme

### 🚨 Uyarı Sistemi
- Otomatik yükseliş/düşüş tespiti
- Özelleştirilebilir eşik değerleri
- Detaylı uyarı bilgileri

### 🔄 Gerçek Zamanlı Güncelleme
- Otomatik fiyat güncellemeleri
- Ayarlanabilir güncelleme aralığı
- Bağlantı durumu göstergesi

## Sorun Giderme

### Sunucu Başlamıyor
- Python 3.7+ yüklü olduğundan emin olun
- Gerekli kütüphaneleri yükleyin: `pip3 install -r requirements.txt`
- Port 5000'in kullanılabilir olduğundan emin olun

### Fiyatlar Yüklenmiyor
- Backend sunucusunun çalıştığından emin olun
- Tarayıcı konsolunda hata mesajlarını kontrol edin (F12)
- İnternet bağlantınızı kontrol edin

### CORS Hatası
- `flask-cors` kütüphanesinin yüklü olduğundan emin olun
- Sunucuyu yeniden başlatın

## API Endpoints

Backend sunucusu şu endpoint'leri sağlar:

- `GET /api/health` - Sağlık kontrolü
- `GET /api/bitcoin/price` - Bitcoin fiyatı
- `GET /api/stocks/price` - Tüm hisse senetleri fiyatları
- `GET /api/all/prices` - Tüm fiyatlar (Bitcoin + Hisse senetleri)
- `GET /api/alerts` - Tüm uyarılar
- `POST /api/alerts/check` - Uyarıları kontrol et
- `GET /api/history/<symbol>` - Fiyat geçmişi
- `GET /api/config` - Yapılandırma bilgileri

## İpuçları

1. **Eşik Değerini Ayarlama**: `config.py` dosyasında `THRESHOLD_PERCENT` değerini değiştirebilirsiniz
2. **Hisse Senetleri Ekleme**: `config.py` dosyasında `STOCK_SYMBOLS` listesine yeni semboller ekleyebilirsiniz
3. **Güncelleme Aralığı**: Web arayüzünde otomatik güncelleme açıkken, kod içinde aralığı değiştirebilirsiniz

## Destek

Sorun yaşarsanız:
1. Terminal çıktısını kontrol edin
2. Tarayıcı konsolunu açın (F12)
3. Hata mesajlarını okuyun
4. Sunucuyu yeniden başlatmayı deneyin

