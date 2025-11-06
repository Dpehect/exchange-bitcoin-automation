#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bitcoin ve Borsa Fiyat Takip ve Analiz Uygulaması
Bitcoin ve hisse senetlerindeki yükseliş ve düşüşleri tespit eder.
"""

import requests
import yfinance as yf
import time
from datetime import datetime
from typing import Dict, List, Optional
import json
from dataclasses import dataclass, asdict


@dataclass
class PriceAlert:
    """Fiyat değişimi uyarısı"""
    symbol: str
    current_price: float
    previous_price: float
    change_percent: float
    change_type: str  # 'rise' veya 'fall'
    timestamp: str


class BitcoinMonitor:
    """Bitcoin fiyat takip sınıfı"""
    
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.previous_price: Optional[float] = None
        
    def get_bitcoin_price(self) -> Optional[float]:
        """Bitcoin'in güncel fiyatını al (USD)"""
        try:
            params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd'
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('bitcoin', {}).get('usd')
        except Exception as e:
            print(f"❌ Bitcoin fiyatı alınırken hata: {e}")
            return None
    
    def check_price_change(self, threshold: float = 1.0) -> Optional[PriceAlert]:
        """Fiyat değişimini kontrol et"""
        current_price = self.get_bitcoin_price()
        
        if current_price is None:
            return None
            
        if self.previous_price is None:
            self.previous_price = current_price
            return None
        
        change = current_price - self.previous_price
        change_percent = (change / self.previous_price) * 100
        
        if abs(change_percent) >= threshold:
            alert_type = 'rise' if change_percent > 0 else 'fall'
            alert = PriceAlert(
                symbol='BTC/USD',
                current_price=current_price,
                previous_price=self.previous_price,
                change_percent=change_percent,
                change_type=alert_type,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            self.previous_price = current_price
            return alert
        
        return None


class StockMonitor:
    """Hisse senedi fiyat takip sınıfı"""
    
    def __init__(self, symbols: List[str]):
        """
        Args:
            symbols: Takip edilecek hisse senetleri (örn: ['AAPL', 'GOOGL', 'TSLA'])
        """
        self.symbols = symbols
        self.previous_prices: Dict[str, float] = {}
        
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """Hisse senedinin güncel fiyatını al"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            print(f"❌ {symbol} fiyatı alınırken hata: {e}")
            return None
    
    def check_price_changes(self, threshold: float = 1.0) -> List[PriceAlert]:
        """Tüm hisse senetlerindeki fiyat değişimlerini kontrol et"""
        alerts = []
        
        for symbol in self.symbols:
            current_price = self.get_stock_price(symbol)
            
            if current_price is None:
                continue
            
            if symbol not in self.previous_prices:
                self.previous_prices[symbol] = current_price
                continue
            
            previous_price = self.previous_prices[symbol]
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
            
            if abs(change_percent) >= threshold:
                alert_type = 'rise' if change_percent > 0 else 'fall'
                alert = PriceAlert(
                    symbol=symbol,
                    current_price=current_price,
                    previous_price=previous_price,
                    change_percent=change_percent,
                    change_type=alert_type,
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                alerts.append(alert)
                self.previous_prices[symbol] = current_price
        
        return alerts


class PriceMonitorApp:
    """Ana fiyat takip uygulaması"""
    
    def __init__(self, stock_symbols: List[str] = None, threshold: float = 1.0):
        """
        Args:
            stock_symbols: Takip edilecek hisse senetleri
            threshold: Uyarı için minimum değişim yüzdesi
        """
        self.bitcoin_monitor = BitcoinMonitor()
        self.stock_monitor = StockMonitor(stock_symbols or ['AAPL', 'GOOGL', 'MSFT', 'TSLA'])
        self.threshold = threshold
        self.alerts_history: List[PriceAlert] = []
        
    def display_price_info(self, symbol: str, price: float, change: float = None):
        """Fiyat bilgisini ekranda göster"""
        print(f"\n{'='*60}")
        print(f"📊 {symbol}")
        print(f"💰 Fiyat: ${price:,.2f}")
        if change is not None:
            arrow = "📈" if change > 0 else "📉"
            print(f"{arrow} Değişim: {change:+.2f}%")
        print(f"🕐 Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
    
    def display_alert(self, alert: PriceAlert):
        """Uyarıyı ekranda göster"""
        emoji = "🚀" if alert.change_type == 'rise' else "⚠️"
        color_indicator = "🟢" if alert.change_type == 'rise' else "🔴"
        
        print(f"\n{color_indicator} {emoji} UYARI! {emoji} {color_indicator}")
        print(f"{'='*60}")
        print(f"📊 Sembol: {alert.symbol}")
        print(f"💰 Önceki Fiyat: ${alert.previous_price:,.2f}")
        print(f"💰 Güncel Fiyat: ${alert.current_price:,.2f}")
        print(f"📈 Değişim: {alert.change_percent:+.2f}%")
        print(f"📊 Tip: {'YÜKSELİŞ' if alert.change_type == 'rise' else 'DÜŞÜŞ'}")
        print(f"🕐 Zaman: {alert.timestamp}")
        print(f"{'='*60}\n")
        
        self.alerts_history.append(alert)
    
    def monitor_once(self):
        """Bir kez fiyat kontrolü yap"""
        # Bitcoin kontrolü
        btc_price = self.bitcoin_monitor.get_bitcoin_price()
        if btc_price:
            self.display_price_info('BTC/USD', btc_price)
            btc_alert = self.bitcoin_monitor.check_price_change(self.threshold)
            if btc_alert:
                self.display_alert(btc_alert)
        
        # Hisse senetleri kontrolü
        for symbol in self.stock_monitor.symbols:
            stock_price = self.stock_monitor.get_stock_price(symbol)
            if stock_price:
                self.display_price_info(symbol, stock_price)
        
        stock_alerts = self.stock_monitor.check_price_changes(self.threshold)
        for alert in stock_alerts:
            self.display_alert(alert)
    
    def monitor_continuous(self, interval: int = 60):
        """
        Sürekli fiyat takibi yap
        
        Args:
            interval: Kontrol aralığı (saniye)
        """
        print(f"\n🔄 Sürekli fiyat takibi başlatıldı...")
        print(f"⏱️  Kontrol aralığı: {interval} saniye")
        print(f"📊 Eşik değer: %{self.threshold}")
        print(f"💡 Çıkmak için Ctrl+C tuşlarına basın\n")
        
        try:
            while True:
                self.monitor_once()
                print(f"\n⏳ {interval} saniye bekleniyor...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n✅ Fiyat takibi durduruldu.")
            self.show_summary()
    
    def show_summary(self):
        """Özet bilgileri göster"""
        if not self.alerts_history:
            print("\n📊 Henüz uyarı oluşmadı.")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 ÖZET RAPOR")
        print(f"{'='*60}")
        print(f"📈 Toplam Uyarı: {len(self.alerts_history)}")
        
        rises = [a for a in self.alerts_history if a.change_type == 'rise']
        falls = [a for a in self.alerts_history if a.change_type == 'fall']
        
        print(f"🚀 Yükseliş: {len(rises)}")
        print(f"⚠️  Düşüş: {len(falls)}")
        
        if rises:
            max_rise = max(rises, key=lambda x: x.change_percent)
            print(f"\n📈 En Yüksek Yükseliş:")
            print(f"   {max_rise.symbol}: {max_rise.change_percent:+.2f}%")
        
        if falls:
            max_fall = min(falls, key=lambda x: x.change_percent)
            print(f"\n📉 En Yüksek Düşüş:")
            print(f"   {max_fall.symbol}: {max_fall.change_percent:+.2f}%")
        
        print(f"{'='*60}\n")
    
    def save_alerts_to_file(self, filename: str = 'alerts.json'):
        """Uyarıları JSON dosyasına kaydet"""
        alerts_data = [asdict(alert) for alert in self.alerts_history]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(alerts_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Uyarılar {filename} dosyasına kaydedildi.")


def main():
    """Ana fonksiyon"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   🚀 Bitcoin ve Borsa Fiyat Takip Uygulaması 🚀         ║
    ║   Yükseliş ve Düşüşleri Tespit Edin                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Config dosyasından ayarları yükle (varsa)
    try:
        import config
        stock_symbols = config.STOCK_SYMBOLS
        threshold = config.THRESHOLD_PERCENT
        default_interval = config.DEFAULT_INTERVAL
    except ImportError:
        # Varsayılan ayarlar
        stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
        threshold = 1.0
        default_interval = 60
    
    # Uygulamayı oluştur
    app = PriceMonitorApp(stock_symbols=stock_symbols, threshold=threshold)
    
    # Kullanıcı seçimi
    print("\nSeçenekler:")
    print("1. Tek seferlik kontrol")
    print("2. Sürekli takip (her 60 saniyede bir)")
    print("3. Özel aralık ile sürekli takip")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    
    if choice == '1':
        app.monitor_once()
        app.show_summary()
    elif choice == '2':
        app.monitor_continuous(interval=default_interval)
    elif choice == '3':
        try:
            interval = int(input("Kontrol aralığı (saniye): "))
            app.monitor_continuous(interval=interval)
        except ValueError:
            print(f"❌ Geçersiz giriş! Varsayılan {default_interval} saniye kullanılıyor.")
            app.monitor_continuous(interval=default_interval)
    else:
        print("❌ Geçersiz seçim! Tek seferlik kontrol yapılıyor.")
        app.monitor_once()
        app.show_summary()
    
    # Uyarıları kaydet
    if app.alerts_history:
        save = input("\nUyarıları dosyaya kaydetmek ister misiniz? (e/h): ").strip().lower()
        if save == 'e':
            app.save_alerts_to_file()


if __name__ == '__main__':
    main()

