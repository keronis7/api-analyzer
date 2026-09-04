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


# ============================================================
# НАСТРОЙКА SELENIUM
# ============================================================

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


# ============================================================
# ОБРАБОТКА ПРЕДУПРЕЖДЕНИЙ
# ============================================================

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


# ============================================================
# ВЗАИМОДЕЙСТВИЕ СО СТРАНИЦЕЙ
# ============================================================

def interact_with_page(driver, url):
    actions_log = []
    performed_actions = set()

    # 1. Поиск поля поиска
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
                        if "Поиск" not in performed_actions:
                            actions_log.append("Поиск")
                            performed_actions.add("Поиск")
                        time.sleep(1.5)
                        el.send_keys(u'\ue00c')
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].value = '';", el)
                        break
            except:
                pass
    except:
        pass

    # 2. Кнопка микрофона
    try:
        mic_selectors = [
            "[aria-label*='голос']",
            "[aria-label*='Voice']",
            "[class*='mic']",
            "[class*='voice']",
            "button[title*='голос']",
        ]

        for selector in mic_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Микрофон" not in performed_actions:
                            actions_log.append("Микрофон")
                            performed_actions.add("Микрофон")
                        time.sleep(2)
                        break
            except:
                pass
    except:
        pass

    # 3. Меню
    try:
        menu_selectors = ["[aria-label*='меню']", "[class*='menu'] button"]
        for selector in menu_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        if "Меню" not in performed_actions:
                            actions_log.append("Меню")
                            performed_actions.add("Меню")
                        time.sleep(2)
                        break
            except:
                pass
    except:
        pass

    # 4. Кнопка геолокации
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
                        if "Геолокация" not in performed_actions:
                            actions_log.append("Геолокация")
                            performed_actions.add("Геолокация")
                        time.sleep(3)
                        break
            except:
                pass
    except:
        pass

    # 5. Прокрутка
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
    if "Прокрутка" not in performed_actions:
        actions_log.append("Прокрутка")
        performed_actions.add("Прокрутка")

    # 6. Клик на карту
    try:
        map_selectors = ["canvas", "ymaps", "[class*='map']"]
        for selector in map_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed():
                        action_chains = ActionChains(driver)
                        action_chains.move_to_element(el).click().perform()
                        if "Карта" not in performed_actions:
                            actions_log.append("Карта")
                            performed_actions.add("Карта")
                        time.sleep(1)
                        break
            except:
                pass
    except:
        pass

    return actions_log


# ============================================================
# ОЦЕНКА ВЕРОЯТНОСТИ ВЫЗОВА
# ============================================================

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


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

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
    if re.search(r'(getCurrentPosition|watchPosition|geolocation|position|coords|latitude|longitude)', matched,
                 re.IGNORECASE):
        return '📍 Геопозиция'
    elif re.search(r'(getUserMedia|mediaDevices|MediaStream|camera|microphone|audio|video|createMediaStreamSource)',
                   matched, re.IGNORECASE):
        return '📷 Камера/Микрофон'
    elif re.search(r'(Notification|requestPermission|permission)', matched, re.IGNORECASE):
        return '🔔 Уведомления'
    elif re.search(r'(clipboard|writeText|readText)', matched, re.IGNORECASE):
        return '📋 Буфер обмена'
    elif re.search(r'(getBattery|vibrate|DeviceOrientation|DeviceMotion)', matched, re.IGNORECASE):
        return '🔋 Датчики'
    elif re.search(r'(SpeechRecognition|webkitSpeechRecognition|recognition)', matched, re.IGNORECASE):
        return '🎤 Голос'
    return '❓ Другое'


# ============================================================
# ОСНОВНАЯ ФУНКЦИЯ АНАЛИЗА
# ============================================================

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
                'SpeechRecognition'
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

        patterns = [
            r'getCurrentPosition', r'watchPosition', r'geolocation',
            r'position', r'coords', r'latitude', r'longitude',
            r'getUserMedia', r'mediaDevices', r'MediaStream',
            r'camera', r'microphone', r'audio', r'video',
            r'Notification', r'requestPermission',
            r'clipboard', r'writeText', r'readText',
            r'getBattery', r'vibrate', r'DeviceOrientation', r'DeviceMotion',
            r'SpeechRecognition', r'webkitSpeechRecognition', r'recognition'
        ]

        all_calls = []
        seen = set()

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

        for script in all_scripts:
            code = script['code']
            code_len = len(code)

            if code_len < 100:
                continue

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
                            'confidence': confidence
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


# ============================================================
# ФУНКЦИИ ОЧИСТКИ ПРОЦЕССОВ
# ============================================================

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


# ============================================================
# СОХРАНЕНИЕ ОТЧЕТА В JSON
# ============================================================

def save_report_json(results):
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    url_clean = results['url'].replace('https://', '').replace('http://', '').replace('/', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(reports_dir, f"report_{url_clean}_{timestamp}.json")

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
                'context': call.get('context', '')[:300]
            }
            if call.get('src'):
                compact_call['src'] = call['src']

            report_data['calls_by_confidence'][confidence]['calls'].append(compact_call)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    return filename


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

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