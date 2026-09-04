🔍 API ANALYZER - Анализатор API-вызовов на веб-сайтах
========================

📝 ОПИСАНИЕ
========================

Программа для автоматического анализа веб-сайтов на наличие JavaScript-кода, 
использующего функции доступа к:

- 🎥 Камере
- 🎙️ Микрофону
- 📍 Геопозиции
- 🔔 Уведомлениям
- 📋 Буферу обмена
- 🔋 Датчикам (батарея, вибрация, ориентация)
- 🎤 Голосовому распознаванию

Инструмент загружает сайт через Selenium, анализирует JavaScript-код и 
классифицирует найденные API-вызовы по вероятности их реального использования.


🚀 УСТАНОВКА И ЗАПУСК
========================

1. Клонирование репозитория

   git clone https://github.com/ваш_username/api-analyzer.git
   cd api-analyzer

2. Установка зависимостей

   pip install -r requirements.txt

3. Запуск

   python api_analyzer.py

4. Ввод URL

   🌐 Введите URL для анализа: https://yandex.ru/maps/


📊 ПРИМЕР ВЫВОДА
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


📊 ИТОГИ
========================
🌐 https://yandex.ru/maps/
📜 Скриптов: 21
🔍 API: Notification, navigator.getBattery, webkitSpeechRecognition, SpeechRecognition

💾 Отчет сохранен: reports/report_yandex.ru_maps__20260904_173026.json
📊 Всего совпадений: 64
   🔴 High: 27
   🟡 Medium: 11
   🟢 Low: 26

✅ Готово!


📋 ФОРМАТ ОТЧЕТА (JSON)
========================

{
  "url": "https://yandex.ru/maps/",
  "timestamp": "2026-09-04 17:30:26",
  "analysis_duration": 62.22,
  "scripts_stats": {
    "inline": 11,
    "external": 10,
    "total": 21
  },
  "available_apis": [
    "Notification",
    "navigator.getBattery",
    "webkitSpeechRecognition",
    "SpeechRecognition"
  ],
  "interactions": [
    "Поиск",
    "Микрофон",
    "Меню",
    "Геолокация",
    "Прокрутка",
    "Карта"
  ],
  "summary": {
    "total_calls": 64,
    "high_confidence": 27,
    "medium_confidence": 11,
    "low_confidence": 26
  },
  "calls_by_confidence": {
    "high": {
      "count": 27,
      "summary": {
        "📍 Геопозиция": 15,
        "📷 Камера/Микрофон": 7,
        "📋 Буфер обмена": 3,
        "🔔 Уведомления": 1,
        "🔋 Датчики": 1
      },
      "calls": [
        {
          "category": "📍 Геопозиция",
          "matched": "geolocation",
          "type": "inline",
          "script_index": 3,
          "context": "navigator.geolocation.getCurrentPosition(function(position) { console.log(position.coords) });",
          "src": null
        }
      ]
    },
    "medium": {
      "count": 11,
      "summary": {},
      "calls": []
    },
    "low": {
      "count": 26,
      "summary": {},
      "calls": []
    }
  }
}


🎯 КЛАССИФИКАЦИЯ API-ВЫЗОВОВ
========================

Категории API:

| Категория        | Эмодзи | Примеры                                    |
|------------------|--------|--------------------------------------------|
| Геопозиция       | 📍     | geolocation, position, coords, latitude    |
| Камера/Микрофон  | 📷     | getUserMedia, mediaDevices, camera         |
| Уведомления      | 🔔     | Notification, requestPermission            |
| Буфер обмена     | 📋     | clipboard, writeText, readText             |
| Датчики          | 🔋     | getBattery, vibrate, DeviceOrientation     |
| Голос            | 🎤     | SpeechRecognition, webkitSpeechRecognition |

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
- Детальный анализ контекста — для каждого найденного паттерна анализируется контекст для определения вероятности


📁 СТРУКТУРА ПРОЕКТА
========================

api-analyzer/
├── api_analyzer.py          # Основной скрипт
├── requirements.txt          # Зависимости
├── README.md                # Документация
├── .gitignore               # Игнорируемые файлы
├── LICENSE                  # Лицензия MIT
└── setup.py                 # Для установки через pip


📈 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ
========================

| Сайт              | Скриптов | High | Medium | Low | Всего |
|-------------------|----------|------|--------|-----|-------|
| yandex.ru/maps    | 21       | 27   | 11     | 26  | 64    |
| zoom.us           | 33       | 12   | 13     | 19  | 44    |


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
================================================================================

Если проект полезен - поставьте звезду ⭐ на GitHub!
