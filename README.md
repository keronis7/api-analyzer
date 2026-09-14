========================
🔍 API ANALYZER - Анализатор API-вызовов на веб-сайтах
========================

📝 ОПИСАНИЕ
========================

Программа для автоматического анализа веб-сайтов на наличие JavaScript-кода,
использующего функции доступа к:

- 📍 Геопозиции
- 📷 Камере
- 🎙️ Микрофону
- 🖥️ Экрану
- 📹 Видео
- 🔔 Уведомлениям
- 📋 Буферу обмена
- 💳 Платежам
- 🔋 Датчикам
- 🎤 Голосовому распознаванию

Инструмент загружает сайт через Selenium, анализирует JavaScript-код и
классифицирует найденные API-вызовы по вероятности их реального использования.


🚀 УСТАНОВКА И ЗАПУСК
========================

1. Клонирование репозитория

   git clone https://github.com/keronis7/api-analyzer.git
   cd api-analyzer

2. Установка зависимостей

   pip install -r requirements.txt

3. Запуск

   python api_analyzer.py

4. Ввод URL

   🌐 Введите URL для анализа: https://yandex.ru/maps/


📊 ПРИМЕР ВЫВОДА
========================

========================
🔍 API ANALYZER
========================

💡 Анализирует сайт на наличие API
   ✅ Классифицирует по вероятности вызова
   ✅ Показывает контекст каждого вызова
   ✅ Сохраняет все вызовы с разделением по вероятности в JSON
   ✅ Автоматически управляет драйвером через webdriver-manager

🌐 Введите URL для анализа: https://yandex.ru/maps/

⏳ Загрузка...
🔍 Проверка предупреждений...
⏳ Ожидание скриптов...

========================
📊 ИТОГИ
========================
🌐 https://yandex.ru/maps/
📜 Скриптов: 21
🔍 API: Notification, navigator.getBattery, webkitSpeechRecognition, SpeechRecognition, PaymentRequest

💾 Отчет сохранен: reports/yandex.ru_maps__20260914_120000/report.json
📊 Всего совпадений: 66
   🔴 High: 29
   🟡 Medium: 12
   🟢 Low: 25

✅ Готово!


📁 СТРУКТУРА ОТЧЕТА
========================

reports/
└── yandex.ru_maps__20260914_120000/
    ├── report.json              # Результаты анализа
    └── scripts/                 # Сохраненные скрипты
        ├── script_0001.js
        ├── script_0002.js
        └── ...


📋 ФОРМАТ ОТЧЕТА (JSON)
========================

{
  "url": "https://yandex.ru/maps/",
  "timestamp": "2026-09-14 12:00:00",
  "analysis_duration": 92.44,
  "scripts_stats": {
    "inline": 11,
    "external": 10,
    "total": 21
  },
  "available_apis": [
    "Notification",
    "navigator.getBattery",
    "webkitSpeechRecognition",
    "SpeechRecognition",
    "PaymentRequest"
  ],
  "interactions": [
    "Search Input",
    "Screen Share",
    "Menu",
    "Geolocation",
    "Sensors",
    "Scroll",
    "Map/Video Click"
  ],
  "saved_scripts": [
    "script_0001.js",
    "script_0002.js"
  ],
  "summary": {
    "total_calls": 66,
    "high_confidence": 29,
    "medium_confidence": 12,
    "low_confidence": 25
  },
  "calls_by_confidence": {
    "high": {
      "count": 29,
      "summary": {
        "📍 Геопозиция": 16,
        "📹 Видео": 5,
        "📋 Буфер обмена": 4,
        "📷 Камера": 2,
        "🔔 Уведомления": 1,
        "🔋 Датчики": 1
      },
      "calls": [
        {
          "category": "📍 Геопозиция",
          "matched": "geolocation",
          "type": "external",
          "script_index": 4,
          "confidence": "high",
          "context": "...userLocation:e.geolocation,formType:e.form.formType...",
          "script_file": "script_0008.js",
          "src": "https://maps.yastatic.net/s3/front-maps-static/..."
        }
      ]
    },
    "medium": {
      "count": 12,
      "summary": {},
      "calls": []
    },
    "low": {
      "count": 25,
      "summary": {},
      "calls": []
    }
  }
}


🎯 КЛАССИФИКАЦИЯ API-ВЫЗОВОВ
========================

Категории API:

| Категория        | Эмодзи | Примеры                                            |
|------------------|--------|----------------------------------------------------|
| Геопозиция       | 📍     | geolocation, position, coords, latitude, longitude |
| Камера           | 📷     | getUserMedia, mediaDevices, camera                 |
| Микрофон         | 🎙️     | microphone, audio, audioinput                      |
| Экран            | 🖥️     | getDisplayMedia, screenCapture, desktopCapture     |
| Видео            | 📹     | video, player, playback                            |
| Уведомления      | 🔔     | Notification, pushManager, showNotification        |
| Буфер обмена     | 📋     | clipboard, writeText, readText, clipboardData      |
| Платежи          | 💳     | PaymentRequest, ApplePaySession, canMakePayment    |
| Датчики          | 🔋     | getBattery, vibrate, DeviceOrientation             |
| Голос            | 🎤     | SpeechRecognition, webkitSpeechRecognition         |

Оценка вероятности:

| Уровень | Описание                              | Критерии                                    |
|---------|---------------------------------------|---------------------------------------------|
| 🔴 High | Высокая вероятность реального вызова  | Метод с скобками, navigator./window.,       |
|         |                                       | функция-колбэк, try/catch, Promise/await    |
| 🟡 Medium| Средняя вероятность                   | Частичное соответствие критериям            |
| 🟢 Low  | Низкая вероятность                    | Простое упоминание без контекста вызова     |


🔧 ОСОБЕННОСТИ РЕАЛИЗАЦИИ
========================

- Headless режим — браузер работает в фоновом режиме, пользователь не видит процесс
- Автоматическое управление драйвером — webdriver-manager сам загружает подходящую версию ChromeDriver
- Очистка процессов — после завершения работы все процессы Chrome автоматически закрываются
- Детальный анализ контекста — для каждого найденного паттерна анализируется контекст
- Активация API через взаимодействие — нажатие кнопок Screen Share, Microphone, Camera, Notifications
- Имитация датчиков — генерация событий DeviceOrientation, DeviceMotion, Battery, Vibration
- Сохранение скриптов — все скрипты с API-вызовами сохраняются в папку scripts/


📁 СТРУКТУРА ПРОЕКТА
========================

api-analyzer/
├── api_analyzer.py          # Основной скрипт
├── requirements.txt          # Зависимости
├── README.md                # Документация
├── .gitignore               # Игнорируемые файлы
├── LICENSE                  # Лицензия MIT
├── setup.py                 # Для установки через pip
└── reports/                 # Папка с отчетами
    └── {сайт}_{дата}_{время}/
        ├── report.json      # Результаты анализа
        └── scripts/         # Сохраненные скрипты


📈 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ
========================

| Сайт                    | Скриптов | High | Medium | Low | Всего |
|-------------------------|----------|------|--------|-----|-------|
| yandex.ru/maps          | 21       | 29   | 12     | 25  | 66    |
| zoom.us                 | 33       | 12   | 13     | 19  | 44    |
| applepaydemo.apple.com  | 19       | 24   | 16     | 72  | 112   |
| timbrica.com            | 80       | 54   | 41     | 81  | 176   |


📚 ИСПОЛЬЗУЕМЫЕ ТЕХНОЛОГИИ
========================

- Python 3.8+ — основной язык программирования
- Selenium — управление браузером и загрузка страниц
- webdriver-manager — автоматическое управление драйверами
- psutil — управление процессами


📝 ЛИЦЕНЗИЯ
========================

MIT License — см. файл LICENSE


🤝 КАК ВНЕСТИ ВКЛАД
========================

1. Форкните репозиторий
2. Создайте ветку для фичи (git checkout -b feature/AmazingFeature)
3. Закоммитьте изменения (git commit -m 'Add some AmazingFeature')
4. Запушьте ветку (git push origin feature/AmazingFeature)
5. Откройте Pull Request


📧 КОНТАКТЫ
========================

- GitHub: @keronis7
- Email: keronis7@yandex.ru


⭐ ПОДДЕРЖКА
========================

Если проект полезен - поставьте звезду ⭐ на GitHub!
