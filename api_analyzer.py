from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import os
import time
import psutil
from datetime import datetime


def setup_selenium_driver():
    options = Options()

    # Скрываем браузер
    options.add_argument("--headless=new")  # Полностью скрытый режим
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    prefs = {
        "profile.managed_default_content_settings.geolocation": 1,
        "profile.managed_default_content_settings.notifications": 1,
        "profile.managed_default_content_settings.media_stream": 1,
        "profile.managed_default_content_settings.media_stream_mic": 1,
        "profile.managed_default_content_settings.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_settings.popups": 0,
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    try:
        driver_manager = ChromeDriverManager()
        service = Service(driver_manager.install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.set_page_load_timeout(120)
        driver.set_script_timeout(60)
        return driver
    except Exception as e:
        print(f"❌ Ошибка при запуске драйвера: {e}")
        return None


def handle_2gis_warning(driver):
    try:
        button_texts = [
            "Пропустить обновление браузера и перейти в 2ГИС",
            "Пропустить обновление браузера",
            "Пропустить",
            "пропустить",
        ]

        for text in button_texts:
            try:
                xpath = f"//button[contains(text(), '{text}')]"
                elements = driver.find_elements(By.XPATH, xpath)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        time.sleep(2)
                        return True
            except:
                continue

        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                try:
                    link_text = link.text.lower()
                    if 'пропуст' in link_text or 'перейт' in link_text:
                        if link.is_displayed():
                            driver.execute_script("arguments[0].click();", link)
                            time.sleep(2)
                            return True
                except:
                    continue
        except:
            pass

        return False
    except Exception as e:
        return False


def interact_with_page(driver, url):
    actions_log = []
    performed_actions = set()

    # ============================================================
    # 1. SEARCH INPUT
    # ============================================================
    try:
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='Поиск']",
            "input[placeholder*='Search']",
            "input[placeholder*='Найти']",
            "input[aria-label*='поиск']",
            "input[aria-label*='search']",
            "[data-testid='search-input']",
            "[class*='search'] input",
            "form input[type='text']",
        ]

        for selector in search_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        el.click()
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].value = '';", el)
                        time.sleep(0.3)
                        el.send_keys("кафе")
                        time.sleep(0.8)
                        if "Search Input" not in performed_actions:
                            actions_log.append("Search Input")
                            performed_actions.add("Search Input")
                        time.sleep(1.5)
                        el.send_keys(u'\ue00c')
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].value = '';", el)
                        break
            except:
                pass
    except:
        pass

    # ============================================================
    # 2. SCREEN SHARE / GETDISPLAYMEDIA КНОПКИ
    # ============================================================
    screen_share_texts = [
        # Русские
        "Показать мой экран", "Показать экран", "Демонстрация экрана",
        "Начать демонстрацию", "Демонстрация", "Поделиться экраном",
        "Начать показ", "Показать", "Трансляция", "Захват экрана",
        "Поделиться", "Начать трансляцию", "Screen Share",
        # Английские
        "Share Screen", "Share your screen", "Start Sharing",
        "Start Screen Share", "Share", "Present", "Screen Share",
        "Start Broadcast", "Go Live", "Start Presentation",
        "Share screen", "Present now", "Present to meeting",
        # Общие
        "Screen", "Display", "Share my screen"
    ]

    for text in screen_share_texts:
        try:
            xpath = f"//*[contains(text(), '{text}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for el in elements:
                try:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", el)
                        if "Screen Share" not in performed_actions:
                            actions_log.append("Screen Share")
                            performed_actions.add("Screen Share")
                        time.sleep(5)  # Ждём загрузки модуля Screen Capture
                        # Закрываем возможный диалог выбора экрана
                        try:
                            driver.execute_script(
                                "window.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));")
                        except:
                            pass
                        break
                except:
                    continue
            if "Screen Share" in performed_actions:
                break
        except:
            pass

    # 2.1. Поиск кнопок по CSS-селекторам для screen share
    if "Screen Share" not in performed_actions:
        screen_css_selectors = [
            "[class*='share-screen']",
            "[class*='shareScreen']",
            "[class*='screen-share']",
            "[class*='screenShare']",
            "[class*='screenshare']",
            "[data-testid*='share']",
            "[data-testid*='screen']",
            "[aria-label*='share']",
            "[aria-label*='screen']",
            "[aria-label*='демонстрация']",
            "[aria-label*='экран']",
            "button[title*='share']",
            "button[title*='screen']",
            "button[title*='экран']",
            "[class*='share'] button",
            "[class*='screen'] button",
        ]

        for selector in screen_css_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    try:
                        if el.is_displayed() and el.is_enabled():
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", el)
                            if "Screen Share" not in performed_actions:
                                actions_log.append("Screen Share")
                                performed_actions.add("Screen Share")
                            time.sleep(5)
                            try:
                                driver.execute_script(
                                    "window.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));")
                            except:
                                pass
                            break
                    except:
                        continue
                if "Screen Share" in performed_actions:
                    break
            except:
                pass

    # ============================================================
    # 3. MICROPHONE / КНОПКИ МИКРОФОНА
    # ============================================================
    mic_texts = [
        "Включить микрофон", "Микрофон", "Включить звук", "Голос",
        "Microphone", "Enable microphone", "Unmute", "Mic on",
        "Включить", "Говорить"
    ]

    for text in mic_texts:
        try:
            xpath = f"//*[contains(text(), '{text}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for el in elements:
                try:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Microphone" not in performed_actions:
                            actions_log.append("Microphone")
                            performed_actions.add("Microphone")
                        time.sleep(2)
                        break
                except:
                    continue
            if "Microphone" in performed_actions:
                break
        except:
            pass

    if "Microphone" not in performed_actions:
        mic_css_selectors = [
            "[aria-label*='микрофон']",
            "[aria-label*='microphone']",
            "[class*='mic']",
            "[class*='voice']",
            "button[title*='микрофон']",
            "button[title*='microphone']",
            "[class*='microphone']",
        ]
        for selector in mic_css_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Microphone" not in performed_actions:
                            actions_log.append("Microphone")
                            performed_actions.add("Microphone")
                        time.sleep(2)
                        break
                if "Microphone" in performed_actions:
                    break
            except:
                pass

    # ============================================================
    # 4. КНОПКА КАМЕРЫ / ВИДЕО
    # ============================================================
    camera_texts = [
        "Включить камеру", "Камера", "Включить видео", "Видео",
        "Camera", "Enable camera", "Start video", "Video on"
    ]

    for text in camera_texts:
        try:
            xpath = f"//*[contains(text(), '{text}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for el in elements:
                try:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Camera" not in performed_actions:
                            actions_log.append("Camera")
                            performed_actions.add("Camera")
                        time.sleep(2)
                        break
                except:
                    continue
            if "Camera" in performed_actions:
                break
        except:
            pass

    if "Camera" not in performed_actions:
        camera_css_selectors = [
            "[aria-label*='камера']",
            "[aria-label*='camera']",
            "[class*='camera']",
            "[class*='video-toggle']",
            "button[title*='камера']",
            "button[title*='camera']",
        ]
        for selector in camera_css_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Camera" not in performed_actions:
                            actions_log.append("Camera")
                            performed_actions.add("Camera")
                        time.sleep(2)
                        break
                if "Camera" in performed_actions:
                    break
            except:
                pass

    # ============================================================
    # 5. МЕНЮ
    # ============================================================
    try:
        menu_selectors = ["[aria-label*='меню']", "[class*='menu'] button"]
        for selector in menu_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Menu" not in performed_actions:
                            actions_log.append("Menu")
                            performed_actions.add("Menu")
                        time.sleep(2)
                        break
            except:
                pass
    except:
        pass

    # ============================================================
    # 6. ГЕОЛОКАЦИЯ
    # ============================================================
    try:
        geo_selectors = [
            "[aria-label*='местоположение']",
            "[aria-label*='location']",
            "[class*='geolocation']",
            "[class*='location'] button",
        ]
        for selector in geo_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Geolocation" not in performed_actions:
                            actions_log.append("Geolocation")
                            performed_actions.add("Geolocation")
                        time.sleep(3)
                        break
            except:
                pass
    except:
        pass

    # ============================================================
    # 7. УВЕДОМЛЕНИЯ (запрос разрешений)
    # ============================================================
    try:
        notification_texts = [
            "Разрешить уведомления", "Включить уведомления", "Уведомления",
            "Allow notifications", "Enable notifications", "Notifications"
        ]
        for text in notification_texts:
            try:
                xpath = f"//*[contains(text(), '{text}')]"
                elements = driver.find_elements(By.XPATH, xpath)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Notifications" not in performed_actions:
                            actions_log.append("Notifications")
                            performed_actions.add("Notifications")
                        time.sleep(2)
                        break
                if "Notifications" in performed_actions:
                    break
            except:
                pass
    except:
        pass

    # ============================================================
    # 8. ИМИТАЦИЯ ДЕЙСТВИЙ ДЛЯ ДАТЧИКОВ
    # ============================================================
    try:
        # Имитация DeviceOrientation / DeviceMotion событий
        driver.execute_script("""
            // Имитация событий датчиков
            if (window.DeviceOrientationEvent) {
                const event = new DeviceOrientationEvent('deviceorientation', {
                    alpha: 0, beta: 0, gamma: 0, absolute: true
                });
                window.dispatchEvent(event);
            }
            if (window.DeviceMotionEvent) {
                const event = new DeviceMotionEvent('devicemotion', {
                    acceleration: { x: 0, y: 0, z: 0 },
                    accelerationIncludingGravity: { x: 0, y: 9.8, z: 0 },
                    rotationRate: { alpha: 0, beta: 0, gamma: 0 },
                    interval: 16
                });
                window.dispatchEvent(event);
            }
            // Имитация Battery API
            if (navigator.getBattery) {
                navigator.getBattery().then(battery => {
                    console.log('Battery:', battery.level);
                });
            }
            // Имитация Vibration API
            if (navigator.vibrate) {
                navigator.vibrate(100);
            }
        """)
        if "Sensors" not in performed_actions:
            actions_log.append("Sensors")
            performed_actions.add("Sensors")
        time.sleep(2)
    except:
        pass

    # ============================================================
    # 9. SCROLL
    # ============================================================
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
    if "Scroll" not in performed_actions:
        actions_log.append("Scroll")
        performed_actions.add("Scroll")

    # ============================================================
    # 10. КЛИК НА КАРТУ / ВИДЕО
    # ============================================================
    try:
        map_selectors = ["canvas", "ymaps", "[class*='map']", "video"]
        for selector in map_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed():
                        action_chains = ActionChains(driver)
                        action_chains.move_to_element(el).click().perform()
                        if "Map/Video Click" not in performed_actions:
                            actions_log.append("Map/Video Click")
                            performed_actions.add("Map/Video Click")
                        time.sleep(1)
                        break
            except:
                pass
    except:
        pass

    # ============================================================
    # 11. ФИНАЛЬНОЕ ОЖИДАНИЕ ДЛЯ ДИНАМИЧЕСКИХ СКРИПТОВ
    # ============================================================
    time.sleep(5)

    # Дополнительная прокрутка после всех действий
    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

    return actions_log


def get_call_confidence(matched, context):
    score = 0

    if re.search(r'\.\w+\s*\(', context):
        score += 5

    if re.search(r'navigator\s*\.', context) or re.search(r'window\s*\.', context):
        score += 3

    if re.search(r'function\s*\(', context) or re.search(r'=>\s*\{', context):
        score += 2

    if re.search(r'try\s*\{', context) and re.search(r'catch', context):
        score += 1

    if re.search(r'Promise|await', context):
        score += 1

    api_keywords = [
        'getCurrentPosition', 'watchPosition', 'geolocation',
        'getUserMedia', 'mediaDevices', 'MediaStream',
        'Notification', 'requestPermission',
        'clipboard', 'writeText', 'readText',
        'getBattery', 'vibrate', 'DeviceOrientation',
        'SpeechRecognition'
    ]
    for keyword in api_keywords:
        if keyword in matched:
            score += 2
            break

    if score >= 7:
        return 'high'
    elif score >= 4:
        return 'medium'
    else:
        return 'low'


def is_tracker_script(src):
    skip_patterns = [
        'top100', 'tns-counter', 'metrika', 'clickstream',
        'privacy', 'counter', 'analytics',
        'surveys.yandex.ru'
    ]
    return any(p in src.lower() for p in skip_patterns)


def extract_context(code, match_start, match_end, max_len=300):
    start = code.rfind('\n', 0, match_start)
    if start == -1:
        start = 0
    else:
        start += 1

    end = code.find('\n', match_end)
    if end == -1:
        end = len(code)

    line = code[start:end].strip()

    if len(line) > max_len:
        pattern_text = code[match_start:match_end]
        pos = line.find(pattern_text)
        if pos != -1:
            half = max_len // 2
            start_pos = max(0, pos - half)
            end_pos = min(len(line), pos + len(pattern_text) + half)
            line = line[start_pos:end_pos]
            if start_pos > 0:
                line = "..." + line
            if end_pos < len(line):
                line = line + "..."

    return line


def get_api_type(matched):
    # Геопозиция
    if re.search(r'(getCurrentPosition|watchPosition|geolocation|position|coords|latitude|longitude)', matched, re.IGNORECASE):
        return '📍 Геопозиция'
    # Камера
    elif re.search(r'(getUserMedia|mediaDevices|getCamera|camera|enumerateDevices|MediaStream|Camera)', matched, re.IGNORECASE):
        return '📷 Камера'
    # Микрофон
    elif re.search(r'(microphone|audioinput|audio input|getAudio|createMediaStreamSource|audio)', matched, re.IGNORECASE):
        return '🎙️ Микрофон'
    # Экран
    elif re.search(r'(getDisplayMedia|displayMedia|screenCapture|desktopCapture|shareScreen)', matched, re.IGNORECASE):
        return '🖥️ Экран'
    # Видео
    elif re.search(r'(video|VIDEO|Video|player|playback)', matched, re.IGNORECASE):
        return '📹 Видео'
    # Уведомления
    elif re.search(r'(Notification|pushManager|showNotification|notifications)', matched, re.IGNORECASE):
        return '🔔 Уведомления'
    # Буфер обмена
    elif re.search(r'(clipboard|writeText|readText|clipboardData)', matched, re.IGNORECASE):
        return '📋 Буфер обмена'
    # Платежи
    elif re.search(r'(PaymentRequest|PaymentResponse|PaymentMethod|canMakePayment|showPayment|ApplePaySession|applePay|paymentMethod|disbursement)', matched, re.IGNORECASE):
        return '💳 Платежи'
    # Датчики
    elif re.search(r'(getBattery|vibrate|DeviceOrientation|DeviceMotion|accelerometer|gyroscope|devicemotion|deviceorientation)', matched, re.IGNORECASE):
        return '🔋 Датчики'
    # Голос
    elif re.search(r'(SpeechRecognition|webkitSpeechRecognition|recognition|SpeechSynthesis|speechSynthesis)', matched, re.IGNORECASE):
        return '🎤 Голос'
    return '❓ Другое'


def analyze_website(url):
    results = {
        'url': url,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analysis_duration': 0,
        'scripts_stats': {'inline': 0, 'external': 0, 'total': 0},
        'available_apis': [],
        'warnings_handled': [],
        'interactions': [],
        'api_calls': [],
        'saved_scripts': [],
        'analysis_dir': '',  # <-- ДОБАВЛЯЕМ
        'status': 'success',
        'summary': {
            'total_calls': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0
        }
    }

    start_time = time.time()
    driver = None

    # СОЗДАЕМ ПАПКУ ДЛЯ АНАЛИЗА СРАЗУ
    url_clean = url.replace('https://', '').replace('http://', '').replace('/', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    analysis_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", f"{url_clean}_{timestamp}")
    os.makedirs(analysis_dir, exist_ok=True)

    # СОХРАНЯЕМ ПУТЬ В RESULTS
    results['analysis_dir'] = analysis_dir

    try:
        driver = setup_selenium_driver()
        if not driver:
            results['status'] = 'error'
            results['error'] = 'Не удалось запустить драйвер'
            return results

        print("⏳ Загрузка...")
        driver.get(url)
        time.sleep(3)

        print("🔍 Проверка предупреждений...")
        for attempt in range(3):
            if handle_2gis_warning(driver):
                results['warnings_handled'].append('2gis_warning')
                time.sleep(2)
                break
            time.sleep(1)

        interactions = interact_with_page(driver, url)
        results['interactions'] = interactions

        print("⏳ Ожидание скриптов...")
        time.sleep(5)

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

        data = driver.execute_script("""
            const scripts = document.getElementsByTagName('script');
            const inlineScripts = [];
            const externalScripts = [];

            for (let script of scripts) {
                if (script.src) {
                    externalScripts.push({src: script.src});
                } else {
                    const code = script.textContent || script.innerHTML || '';
                    if (code.trim()) {
                        inlineScripts.push({code: code});
                    }
                }
            }

            const apis = [
                'navigator.mediaDevices',
                'navigator.geolocation',
                'Notification',
                'navigator.clipboard',
                'navigator.getBattery',
                'webkitSpeechRecognition',
                'SpeechRecognition',
                'PaymentRequest',
                'ApplePaySession'
            ];

            const foundApis = [];
            for (let api of apis) {
                try {
                    const parts = api.split('.');
                    let current = window;
                    for (let part of parts) {
                        if (current && current[part] !== undefined) {
                            current = current[part];
                        } else {
                            throw new Error('Not found');
                        }
                    }
                    if (current && typeof current === 'function') {
                        foundApis.push(api);
                    }
                } catch(e) {}
            }

            return {
                inlineScripts: inlineScripts,
                externalScripts: externalScripts,
                availableApis: foundApis
            };
        """)

        inline_scripts = data.get('inlineScripts', [])
        external_scripts = data.get('externalScripts', [])
        available_apis = data.get('availableApis', [])

        results['available_apis'] = available_apis
        results['scripts_stats']['inline'] = len(inline_scripts)
        results['scripts_stats']['external'] = len(external_scripts)
        results['scripts_stats']['total'] = len(inline_scripts) + len(external_scripts)

        # РАСШИРЕННЫЕ паттерны для поиска API
        patterns = [
            # Геопозиция
            r'getCurrentPosition', r'watchPosition', r'geolocation',
            r'position', r'coords', r'latitude', r'longitude',
            # Камера, Микрофон, Экран
            r'getUserMedia', r'mediaDevices', r'MediaStream',
            r'camera', r'microphone', r'audio', r'video',
            r'getDisplayMedia', r'displayMedia', r'screenCapture',
            r'enumerateDevices', r'audioinput', r'createMediaStreamSource',
            # Уведомления
            r'Notification', r'pushManager', r'showNotification',
            # Буфер обмена
            r'clipboard', r'writeText', r'readText', r'clipboardData',
            # Платежи
            r'PaymentRequest', r'PaymentResponse', r'PaymentMethod',
            r'canMakePayment', r'showPayment', r'ApplePaySession',
            r'applePay', r'paymentMethod', r'disbursement',
            # Датчики
            r'getBattery', r'vibrate', r'DeviceOrientation', r'DeviceMotion',
            r'accelerometer', r'gyroscope', r'devicemotion', r'deviceorientation',
            # Голос
            r'SpeechRecognition', r'webkitSpeechRecognition', r'recognition',
            r'SpeechSynthesis', r'speechSynthesis',
        ]

        all_calls = []
        seen = set()
        saved_scripts = {}

        all_scripts = []
        for i, script in enumerate(inline_scripts):
            all_scripts.append({'code': script.get('code', ''), 'type': 'inline', 'index': i + 1})

        for i, script in enumerate(external_scripts):
            src = script.get('src', '')
            if not is_tracker_script(src):
                try:
                    driver.get(src)
                    time.sleep(0.3)
                    code = driver.page_source
                    if code and len(code) > 1000 and len(code) < 2000000:
                        all_scripts.append({'code': code, 'type': 'external', 'index': i + 1, 'src': src})
                except:
                    pass

        # Сохраняем скрипты с API-вызовами
        for script in all_scripts:
            code = script['code']
            code_len = len(code)

            if code_len < 100:
                continue

            # Проверяем, есть ли в скрипте какие-либо API-вызовы
            has_api = False
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    has_api = True
                    break

            # Если есть API-вызовы, сохраняем скрипт
            if has_api:
                script_key = f"{script['type']}_{script['index']}"
                if script_key not in saved_scripts:
                    # ПЕРЕДАЕМ analysis_dir
                    filename = save_script_file(
                        code,
                        script['type'],
                        script['index'],
                        url_clean,
                        timestamp,
                        script.get('src'),
                        analysis_dir  # <-- ВАЖНО!
                    )
                    saved_scripts[script_key] = filename
                    results['saved_scripts'].append(filename)

        # Анализируем скрипты на конкретные вызовы
        for script in all_scripts:
            code = script['code']
            code_len = len(code)

            if code_len < 100:
                continue

            script_key = f"{script['type']}_{script['index']}"
            script_file = saved_scripts.get(script_key, None)

            for pattern in patterns:
                for match in re.finditer(pattern, code, re.IGNORECASE):
                    context = extract_context(code, match.start(), match.end())
                    key = f"{match.group()}:{context[:50]}"

                    if key not in seen:
                        seen.add(key)
                        category = get_api_type(match.group())
                        confidence = get_call_confidence(match.group(), context)

                        call_data = {
                            'category': category,
                            'matched': match.group(),
                            'context': context,
                            'type': script['type'],
                            'script_index': script['index'],
                            'confidence': confidence,
                            'script_file': script_file
                        }
                        if script.get('src'):
                            call_data['src'] = script['src']

                        all_calls.append(call_data)

        results['api_calls'] = all_calls

        high_count = sum(1 for c in all_calls if c['confidence'] == 'high')
        medium_count = sum(1 for c in all_calls if c['confidence'] == 'medium')
        low_count = sum(1 for c in all_calls if c['confidence'] == 'low')

        results['summary'] = {
            'total_calls': len(all_calls),
            'high_confidence': high_count,
            'medium_confidence': medium_count,
            'low_confidence': low_count
        }

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        results['status'] = 'error'
        results['error'] = str(e)
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            try:
                kill_chrome_processes_by_pid(os.getpid())
            except:
                pass

    results['analysis_duration'] = round(time.time() - start_time, 2)
    return results


def kill_chrome_processes_by_pid(driver_pid=None):
    try:
        current_process = psutil.Process()
        parent_pid = current_process.pid
        killed = []
        for proc in psutil.process_iter(['pid', 'name', 'ppid']):
            try:
                name = proc.info['name'].lower() if proc.info['name'] else ''
                ppid = proc.info['ppid']
                if ('chrome' in name or 'chromedriver' in name):
                    if ppid == parent_pid or ppid == driver_pid:
                        proc.kill()
                        killed.append(f"{name} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if killed:
            print(f"🧹 Закрыто Chrome-процессов: {len(killed)}")
    except Exception as e:
        print(f"⚠️ Ошибка очистки: {e}")


def save_report_json(results):
    # Используем путь из results, если он есть
    analysis_dir = results.get('analysis_dir')

    if not analysis_dir:
        # Если по какой-то причине пути нет, создаем новый
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        url_clean = results['url'].replace('https://', '').replace('http://', '').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        analysis_dir = os.path.join(reports_dir, f"{url_clean}_{timestamp}")
        os.makedirs(analysis_dir, exist_ok=True)

    # Убеждаемся, что папка существует
    os.makedirs(analysis_dir, exist_ok=True)

    # Создаем папку для скриптов внутри папки анализа
    scripts_dir = os.path.join(analysis_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Получаем список сохраненных скриптов
    saved_scripts = results.get('saved_scripts', [])

    # Перемещаем скрипты в папку scripts, если они еще не там
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    for script_filename in saved_scripts:
        # Проверяем, не лежит ли уже в правильной папке
        correct_path = os.path.join(scripts_dir, script_filename)
        if os.path.exists(correct_path):
            continue

        # Проверяем разные возможные пути
        old_paths = [
            os.path.join(reports_dir, script_filename),  # reports/script_0001.js
            os.path.join(analysis_dir, script_filename),  # reports/папка/script_0001.js
        ]

        for old_path in old_paths:
            if os.path.exists(old_path) and old_path != correct_path:
                import shutil
                shutil.move(old_path, correct_path)
                break

    # Формируем JSON отчет
    calls_by_confidence = {
        'high': [],
        'medium': [],
        'low': []
    }

    for call in results.get('api_calls', []):
        confidence = call.get('confidence', 'low')
        if confidence in calls_by_confidence:
            calls_by_confidence[confidence].append(call)
        else:
            calls_by_confidence['low'].append(call)

    report_data = {
        'url': results['url'],
        'timestamp': results['timestamp'],
        'analysis_duration': results['analysis_duration'],
        'scripts_stats': results['scripts_stats'],
        'available_apis': results['available_apis'],
        'interactions': results.get('interactions', []),
        'saved_scripts': saved_scripts,
        'summary': results.get('summary', {
            'total_calls': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0
        }),
        'calls_by_confidence': {
            'high': {
                'count': len(calls_by_confidence['high']),
                'summary': {},
                'calls': []
            },
            'medium': {
                'count': len(calls_by_confidence['medium']),
                'summary': {},
                'calls': []
            },
            'low': {
                'count': len(calls_by_confidence['low']),
                'summary': {},
                'calls': []
            }
        }
    }

    for confidence in ['high', 'medium', 'low']:
        calls = calls_by_confidence[confidence]

        category_summary = {}
        for call in calls:
            cat = call.get('category', '❓ Другое')
            category_summary[cat] = category_summary.get(cat, 0) + 1
        report_data['calls_by_confidence'][confidence]['summary'] = category_summary

        for call in calls:
            compact_call = {
                'category': call.get('category', '❓ Другое'),
                'matched': call.get('matched', ''),
                'type': call.get('type', 'unknown'),
                'script_index': call.get('script_index', 0),
                'confidence': call.get('confidence', 'low'),
                'context': call.get('context', '')[:300],
                'script_file': call.get('script_file', None)
            }
            if call.get('src'):
                compact_call['src'] = call['src']

            report_data['calls_by_confidence'][confidence]['calls'].append(compact_call)

    # Сохраняем JSON отчет в папку анализа
    report_filename = os.path.join(analysis_dir, "report.json")
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    return report_filename


def save_script_file(code, script_type, script_index, url_clean, timestamp, src=None, analysis_dir=None):
    """Сохраняет код скрипта в папку reports/{analysis_dir}/scripts/"""
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

    # Если analysis_dir не указан, создаем временную папку
    if not analysis_dir:
        analysis_dir = os.path.join(reports_dir, f"{url_clean}_{timestamp}")

    scripts_dir = os.path.join(analysis_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Глобальный счетчик для порядковых номеров
    script_counter = len(os.listdir(scripts_dir)) + 1

    # Формируем имя файла с порядковым номером
    filename = f"script_{script_counter:04d}.js"
    filepath = os.path.join(scripts_dir, filename)

    # Формируем информацию о скрипте
    header = f"""// ============================================================
// Script #{script_counter:04d}
// Source: {script_type} script #{script_index}
// Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    if src:
        header += f"// URL: {src}\n"
    header += "// ============================================================\n\n"

    # Сохраняем код
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(code)

    return filename


def main():
    print("=" * 70)
    print("🔍 API ANALYZER")
    print("=" * 70)
    print("\n💡 Анализирует сайт на наличие API")
    print("   ✅ Классифицирует по вероятности вызова")
    print("   ✅ Показывает контекст каждого вызова")
    print("   ✅ Сохраняет все вызовы с разделением по вероятности в JSON")
    print("   ✅ Автоматически управляет драйвером через webdriver-manager\n")

    url = input("🌐 Введите URL для анализа: ").strip()
    if not url:
        print("❌ URL не может быть пустым!")
        return

    start = time.time()
    results = analyze_website(url)

    print("\n" + "=" * 70)
    print("📊 ИТОГИ")
    print("=" * 70)
    print(f"🌐 {results['url']}")
    print(f"📜 Скриптов: {results['scripts_stats']['total']}")

    if results.get('available_apis'):
        print(f"🔍 API: {', '.join(results['available_apis'])}")

    filename = save_report_json(results)

    total = results['summary']['total_calls']
    high = results['summary']['high_confidence']
    medium = results['summary']['medium_confidence']
    low = results['summary']['low_confidence']

    print(f"\n💾 Отчет сохранен: {filename}")
    print(f"📊 Всего совпадений: {total}")
    print(f"   🔴 High: {high}")
    print(f"   🟡 Medium: {medium}")
    print(f"   🟢 Low: {low}")

    print("\n✅ Готово!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
    finally:
        try:
            kill_chrome_processes_by_pid(os.getpid())
        except:
            pass