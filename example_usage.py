#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Örnek kullanım dosyası
Bu dosya, uygulamanın farklı şekillerde nasıl kullanılabileceğini gösterir.
"""

from bitcoin_stock_monitor import BitcoinMonitor, StockMonitor, PriceMonitorApp
import time


def example_1_bitcoin_only():
    """Örnek 1: Sadece Bitcoin takibi"""
    print("\n=== Örnek 1: Sadece Bitcoin Takibi ===\n")
    
    monitor = BitcoinMonitor()
    price = monitor.get_bitcoin_price()
    
    if price:
        print(f"Bitcoin Fiyatı: ${price:,.2f}")
    else:
        print("Bitcoin fiyatı alınamadı.")


def example_2_stocks_only():
    """Örnek 2: Sadece hisse senetleri takibi"""
    print("\n=== Örnek 2: Sadece Hisse Senetleri Takibi ===\n")
    
    symbols = ['AAPL', 'TSLA']
    monitor = StockMonitor(symbols)
    
    for symbol in symbols:
        price = monitor.get_stock_price(symbol)
        if price:
            print(f"{symbol}: ${price:,.2f}")
        else:
            print(f"{symbol}: Fiyat alınamadı")


def example_3_custom_threshold():
    """Örnek 3: Özel eşik değeri ile takip"""
    print("\n=== Örnek 3: Özel Eşik Değeri (%0.5) ===\n")
    
    app = PriceMonitorApp(
        stock_symbols=['AAPL', 'GOOGL'],
        threshold=0.5  # %0.5 değişim eşiği
    )
    
    print("İlk kontrol yapılıyor...")
    app.monitor_once()
    
    print("\n5 saniye bekleniyor...")
    time.sleep(5)
    
    print("\nİkinci kontrol yapılıyor...")
    app.monitor_once()


def example_4_continuous_monitoring():
    """Örnek 4: Kısa süreli sürekli takip"""
    print("\n=== Örnek 4: Sürekli Takip (30 saniye, 3 kez) ===\n")
    
    app = PriceMonitorApp(
        stock_symbols=['AAPL', 'TSLA'],
        threshold=0.5
    )
    
    # 3 kez kontrol et (her 30 saniyede bir)
    for i in range(3):
        print(f"\n--- Kontrol {i+1}/3 ---")
        app.monitor_once()
        if i < 2:  # Son kontrolden sonra bekleme
            print("30 saniye bekleniyor...")
            time.sleep(30)
    
    app.show_summary()


def example_5_save_alerts():
    """Örnek 5: Uyarıları kaydetme"""
    print("\n=== Örnek 5: Uyarıları Dosyaya Kaydetme ===\n")
    
    app = PriceMonitorApp(
        stock_symbols=['AAPL'],
        threshold=0.1  # Düşük eşik (test için)
    )
    
    # Birkaç kontrol yap
    for i in range(3):
        app.monitor_once()
        time.sleep(2)
    
    # Uyarıları kaydet
    app.save_alerts_to_file('example_alerts.json')
    app.show_summary()


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║              Örnek Kullanım Senaryoları                  ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\nHangi örneği çalıştırmak istersiniz?")
    print("1. Sadece Bitcoin takibi")
    print("2. Sadece hisse senetleri takibi")
    print("3. Özel eşik değeri ile takip")
    print("4. Sürekli takip (kısa süreli)")
    print("5. Uyarıları kaydetme")
    
    choice = input("\nSeçiminiz (1-5): ").strip()
    
    try:
        if choice == '1':
            example_1_bitcoin_only()
        elif choice == '2':
            example_2_stocks_only()
        elif choice == '3':
            example_3_custom_threshold()
        elif choice == '4':
            example_4_continuous_monitoring()
        elif choice == '5':
            example_5_save_alerts()
        else:
            print("❌ Geçersiz seçim!")
    except KeyboardInterrupt:
        print("\n\n✅ İşlem kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")

