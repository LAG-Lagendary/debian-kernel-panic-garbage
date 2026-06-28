import argparse
import json
import sys
import time
from llama_cpp import Llama, LlamaGrammar
import os

# --- Параметры надежности генерации ---
MIN_EVENTS_THRESHOLD = 16  # Минимальное количество музыкальных событий в списке 'events' для успешной генерации.
MAX_RETRIES = 3            # Максимальное количество попыток генерации в случае неполного ответа.

# --- Определение структуры JSON для музыкальных данных (ОБЯЗАТЕЛЬНО) ---
# Модель будет принудительно генерировать ответ, соответствующий этой схеме.
MUSIC_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "object",
            "description": "Общие метаданные композиции, используемые MusicXML Converter.",
            "properties": {
                "title": {"type": "string", "description": "Название композиции."},
                "composer": {"type": "string", "description": "Имя композитора или AI."},
                "tempo": {"type": "integer", "description": "Темп в ударах в минуту (BPM)."},
                "key": {"type": "string", "description": "Основная тональность (напр., C Major)."},
                "time_signature": {"type": "string", "description": "Размер (напр., 4/4)."}
            },
            "required": ["title", "tempo", "key", "time_signature"]
        },
        "events": {
            "type": "array",
            "description": "Список всех музыкальных событий (ноты, паузы, начало такта) для всех инструментов. Этот список должен быть максимально полным.",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["note", "rest", "chord", "bar_start"], "description": "Тип события: note, rest, chord, или bar_start."},
                    "part": {"type": "string", "description": "Название партии/инструмента (точное название)."},
                    "pitch": {"type": "string", "description": "Название ноты (напр., C4) или массив строк для аккорда (напр., ['C4', 'E4', 'G4'])."},
                    "duration": {"type": "number", "description": "Длительность в четвертных нотах (напр., 1.0 - четверть, 0.5 - восьмая)."},
                    "velocity": {"type": "integer", "description": "Громкость ноты (0-127)."}
                },
                "required": ["type", "part", "duration"] 
            }
        }
    },
    "required": ["metadata", "events"]
}

def generate_music_json(model_name, model_path, user_prompt, json_filepath):
    """
    Запускает Llama с LlamaGrammar для генерации JSON-структуры музыки.
    Включает логику повторных попыток для обеспечения полноты вывода.
    """
    if not os.path.exists(model_path):
        print(f"\n[Ошибка!]: Файл модели не найден по пути: {model_path}", file=sys.stderr)
        sys.exit(1)

    print(f"--- Запуск AI для создания музыки: {model_name} ---")
    print(f"Путь к модели: {model_path}")
    print(f"Целевой файл JSON: {json_filepath}")
    
    try:
        # Инициализация Llama
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,  # Увеличенное окно контекста для больших JSON
            n_gpu_layers=0, # Используем все доступные слои GPU
            n_threads=8,     # <--- ДОБАВИТЬ: Установите количество потоков CPU
            n_batch=512,     # <--- ДОБАВИТЬ: Увеличьте размер пакета
            verbose=False
        )
        
        # Создание грамматики из JSON-схемы
        schema_string = json.dumps(MUSIC_JSON_SCHEMA)
        grammar = LlamaGrammar.from_json_schema(schema_string)
        
        # Общий начальный промпт
        initial_prompt = (
            f"Ты высококвалифицированный AI-помощник, специализирующийся на генерации музыкальных структур в формате JSON. "
            f"Твоя задача — создать детальную музыкальную композицию, строго соответствующую предоставленной JSON-схеме. "
            f"Вот запрос: '{user_prompt}'\n\nСгенерируй полный и детальный JSON:"
        )

        final_data = None
        start_time = time.time()
        
        # --- Логика повторных попыток для надежности ---
        for attempt in range(MAX_RETRIES):
            print(f"\n[Статус]: Начинается генерация, Попытка {attempt + 1}/{MAX_RETRIES}...")

            current_prompt = initial_prompt
            if attempt > 0:
                current_prompt = (
                    f"Предыдущая попытка генерации была слишком короткой или неполной. "
                    f"Пожалуйста, СГЕНЕРИРУЙ ПОЛНУЮ МУЗЫКАЛЬНУЮ КОМПОЗИЦИЮ заново, включая МИНИМУМ {MIN_EVENTS_THRESHOLD} событий в списке 'events'. "
                    f"Оригинальный запрос: '{user_prompt}'\n\nСгенерируй полный и детальный JSON:"
                )

            # Генерация ответа
            output = llm.create_completion(
                current_prompt,
                max_tokens=2048, # Максимум токенов для ответа
                temperature=0.7,
                grammar=grammar,
                stop=["\n#", "user", "```", "```json"], # Дополнительные стоп-фразы для предотвращения выхода из JSON
                stream=True 
            )

            generated_text = ""
            for token in output:
                token_text = token['choices'][0]['text']
                generated_text += token_text
                # Выводим прогресс только для первой попытки
                if attempt == 0:
                    sys.stdout.write(token_text)
                    sys.stdout.flush()

            # Очистка и парсинг JSON
            generated_text = generated_text.strip()
            
            try:
                # Поиск и исправление распространенной ошибки: лишние пробелы в начале/конце и т.д.
                if generated_text.startswith("```json"):
                    generated_text = generated_text.replace("```json", "").strip()
                if generated_text.endswith("```"):
                    generated_text = generated_text.replace("```", "").strip()
                
                data = json.loads(generated_text)
                events = data.get('events', [])
                
                print(f"\n[Проверка]: Сгенерировано {len(events)} событий.")

                # Проверка на минимальный контент
                if len(events) >= MIN_EVENTS_THRESHOLD:
                    final_data = data
                    print("✅ Проверка пройдена: Содержимого достаточно.")
                    break # Выход из цикла повторных попыток
                else:
                    print(f"❌ Проверка не пройдена: Недостаточно событий (минимум {MIN_EVENTS_THRESHOLD}). Повторная попытка...")

            except json.JSONDecodeError as e:
                print(f"\n[Ошибка!]: Сгенерирован невалидный JSON. Ошибка: {e}", file=sys.stderr)
                print("Неочищенный вывод модели (для отладки):", generated_text, file=sys.stderr)
                
            except Exception as e:
                 print(f"\n[Ошибка]: Произошла внутренняя ошибка при проверке: {e}", file=sys.stderr)

        # --- Сохранение или выход ---

        if final_data:
            # Сохраняем успешно сгенерированный JSON
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=4, ensure_ascii=False)
            
            total_time = time.time() - start_time
            print(f"\n[Успех!]: Музыкальный JSON успешно сохранен в: {json_filepath}")
            print(f"[Статистика]: Общее время генерации: {total_time:.2f} с")
            
        else:
            print(f"\n[Провал!]: Не удалось сгенерировать валидный JSON с минимум {MIN_EVENTS_THRESHOLD} событиями после {MAX_RETRIES} попыток.", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[Критическая ошибка]: Произошла ошибка при работе с llama.cpp: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Запуск модели GGUF (Phi-3-mini) для генерации JSON-структуры музыки.",
        epilog="Пример: python acm_runner.py Phi-3-mini-4k-instruct-q4.gguf /path/to/model/Phi-3-mini-4k-instruct-q4.gguf ./output.json 'Эпическая оркестровая тема для видеоигры.' \n\nВАЖНО: Обновленный скрипт пытается сгенерировать минимум 16 событий в списке 'events'."
    )
    
    # Модель имени (для отображения)
    parser.add_argument('model_name', type=str, help='Название файла модели (например, Phi-3-mini-4k-instruct-q4.gguf).')
    
    # Путь к файлу модели GGUF
    parser.add_argument('model_path', type=str, help='Полный путь к файлу GGUF-модели.')
    
    # Путь к файлу, куда будет сохранен JSON
    parser.add_argument('json_filepath', type=str, help='Путь для сохранения сгенерированного JSON-файла.')
    
    # Промпт пользователя
    parser.add_argument('user_prompt', type=str, help='Текстовый запрос для генерации музыкальной структуры/нот.')

    args = parser.parse_args()
    
    generate_music_json(
        args.model_name,
        args.model_path,
        args.user_prompt,
        args.json_filepath
    )
