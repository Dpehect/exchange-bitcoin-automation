#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Backend API
Bitcoin ve borsa fiyat takibi için REST API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from bitcoin_stock_monitor import BitcoinMonitor, StockMonitor, PriceMonitorApp
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)  # Vue.js frontend için CORS desteği

# Global monitor instance
bitcoin_monitor = BitcoinMonitor()
stock_monitor = None
price_app = None

# Fiyat geçmişi (grafikler için)
price_history = {
    'BTC/USD': [],
    'AAPL': [],
    'GOOGL': [],
    'MSFT': [],
    'TSLA': [],
    'AMZN': []
}

# Uyarılar listesi
alerts_list = []


def initialize_monitors():
    """Monitor'ları başlat"""
    global stock_monitor, price_app
    try:
        import config
        stock_symbols = config.STOCK_SYMBOLS
        threshold = config.THRESHOLD_PERCENT
    except ImportError:
        stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
        threshold = 1.0
    
    stock_monitor = StockMonitor(stock_symbols)
    price_app = PriceMonitorApp(stock_symbols=stock_symbols, threshold=threshold)


@app.route('/api/bitcoin/price', methods=['GET'])
def get_bitcoin_price():
    """Bitcoin fiyatını döndür"""
    try:
        price = bitcoin_monitor.get_bitcoin_price()
        if price is None:
            return jsonify({'error': 'Bitcoin fiyatı alınamadı'}), 500
        
        # Fiyat geçmişine ekle
        price_history['BTC/USD'].append({
            'price': price,
            'timestamp': datetime.now().isoformat()
        })
        # Son 100 kaydı tut
        if len(price_history['BTC/USD']) > 100:
            price_history['BTC/USD'] = price_history['BTC/USD'][-100:]
        
        # Değişim kontrolü
        change_percent = 0
        if bitcoin_monitor.previous_price:
            change_percent = ((price - bitcoin_monitor.previous_price) / bitcoin_monitor.previous_price) * 100
        
        # Önceki fiyatı güncelle
        bitcoin_monitor.previous_price = price
        
        return jsonify({
            'symbol': 'BTC/USD',
            'price': price,
            'change_percent': round(change_percent, 2),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stocks/price', methods=['GET'])
def get_stocks_price():
    """Tüm hisse senetlerinin fiyatlarını döndür"""
    try:
        if stock_monitor is None:
            initialize_monitors()
        
        stocks_data = []
        for symbol in stock_monitor.symbols:
            price = stock_monitor.get_stock_price(symbol)
            if price is not None:
                # Fiyat geçmişine ekle
                if symbol in price_history:
                    price_history[symbol].append({
                        'price': price,
                        'timestamp': datetime.now().isoformat()
                    })
                    # Son 100 kaydı tut
                    if len(price_history[symbol]) > 100:
                        price_history[symbol] = price_history[symbol][-100:]
                
                # Değişim kontrolü
                change_percent = 0
                if symbol in stock_monitor.previous_prices:
                    prev_price = stock_monitor.previous_prices[symbol]
                    change_percent = ((price - prev_price) / prev_price) * 100
                
                # Önceki fiyatı güncelle
                stock_monitor.previous_prices[symbol] = price
                
                stocks_data.append({
                    'symbol': symbol,
                    'price': price,
                    'change_percent': round(change_percent, 2),
                    'timestamp': datetime.now().isoformat()
                })
        
        return jsonify(stocks_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/all/prices', methods=['GET'])
def get_all_prices():
    """Bitcoin ve tüm hisse senetlerinin fiyatlarını döndür"""
    try:
        if stock_monitor is None:
            initialize_monitors()
        
        # Bitcoin fiyatı
        btc_price = bitcoin_monitor.get_bitcoin_price()
        all_data = []
        
        if btc_price:
            # Fiyat geçmişine ekle
            price_history['BTC/USD'].append({
                'price': btc_price,
                'timestamp': datetime.now().isoformat()
            })
            if len(price_history['BTC/USD']) > 100:
                price_history['BTC/USD'] = price_history['BTC/USD'][-100:]
            
            change_percent = 0
            if bitcoin_monitor.previous_price:
                change_percent = ((btc_price - bitcoin_monitor.previous_price) / bitcoin_monitor.previous_price) * 100
            
            # Önceki fiyatı güncelle
            bitcoin_monitor.previous_price = btc_price
            
            all_data.append({
                'symbol': 'BTC/USD',
                'price': btc_price,
                'change_percent': round(change_percent, 2),
                'timestamp': datetime.now().isoformat(),
                'type': 'crypto'
            })
        
        # Hisse senetleri fiyatları
        for symbol in stock_monitor.symbols:
            price = stock_monitor.get_stock_price(symbol)
            if price is not None:
                # Fiyat geçmişine ekle
                if symbol in price_history:
                    price_history[symbol].append({
                        'price': price,
                        'timestamp': datetime.now().isoformat()
                    })
                    if len(price_history[symbol]) > 100:
                        price_history[symbol] = price_history[symbol][-100:]
                
                change_percent = 0
                if symbol in stock_monitor.previous_prices:
                    prev_price = stock_monitor.previous_prices[symbol]
                    change_percent = ((price - prev_price) / prev_price) * 100
                
                # Önceki fiyatı güncelle
                stock_monitor.previous_prices[symbol] = price
                
                all_data.append({
                    'symbol': symbol,
                    'price': price,
                    'change_percent': round(change_percent, 2),
                    'timestamp': datetime.now().isoformat(),
                    'type': 'stock'
                })
        
        return jsonify(all_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Tüm uyarıları döndür"""
    return jsonify(alerts_list)


@app.route('/api/alerts/check', methods=['POST'])
def check_alerts():
    """Fiyat değişimlerini kontrol et ve uyarı oluştur"""
    try:
        if price_app is None:
            initialize_monitors()
        
        # Bitcoin kontrolü
        btc_alert = bitcoin_monitor.check_price_change(price_app.threshold)
        if btc_alert:
            alert_data = {
                'symbol': btc_alert.symbol,
                'current_price': btc_alert.current_price,
                'previous_price': btc_alert.previous_price,
                'change_percent': btc_alert.change_percent,
                'change_type': btc_alert.change_type,
                'timestamp': btc_alert.timestamp
            }
            alerts_list.append(alert_data)
            # Son 50 uyarıyı tut
            if len(alerts_list) > 50:
                alerts_list.pop(0)
        
        # Hisse senetleri kontrolü
        stock_alerts = stock_monitor.check_price_changes(price_app.threshold)
        for alert in stock_alerts:
            alert_data = {
                'symbol': alert.symbol,
                'current_price': alert.current_price,
                'previous_price': alert.previous_price,
                'change_percent': alert.change_percent,
                'change_type': alert.change_type,
                'timestamp': alert.timestamp
            }
            alerts_list.append(alert_data)
            if len(alerts_list) > 50:
                alerts_list.pop(0)
        
        return jsonify({'checked': True, 'new_alerts': len(stock_alerts) + (1 if btc_alert else 0)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<symbol>', methods=['GET'])
def get_price_history(symbol):
    """Belirli bir sembol için fiyat geçmişini döndür"""
    if symbol in price_history:
        return jsonify(price_history[symbol])
    return jsonify([])


@app.route('/api/config', methods=['GET'])
def get_config():
    """Yapılandırma bilgilerini döndür"""
    try:
        import config
        return jsonify({
            'stock_symbols': config.STOCK_SYMBOLS,
            'threshold': config.THRESHOLD_PERCENT,
            'default_interval': config.DEFAULT_INTERVAL
        })
    except ImportError:
        return jsonify({
            'stock_symbols': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
            'threshold': 1.0,
            'default_interval': 60
        })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    initialize_monitors()
    print("🚀 Flask API sunucusu başlatılıyor...")
    print("📡 API: http://localhost:5000")
    print("🌐 Frontend: index.html dosyasını tarayıcıda açın")
    app.run(debug=True, host='0.0.0.0', port=5000)

