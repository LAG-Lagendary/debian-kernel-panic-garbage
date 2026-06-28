import argparse
import json
import sys
import time
from llama_cpp import Llama, LlamaGrammar

# --- Определение структуры JSON для музыкальных данных (ОБЯЗАТЕЛЬНО) ---
# Модель будет принудительно генерировать ответ, соответствующий этой схеме.
# JSON-схема для примера музыкальной композиции.
MUSIC_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Название музыкальной композиции."},
        "genre": {"type": "string", "description": "Жанр музыки (например, Electronic, Classical, Jazz)."},
        "tempo_bpm": {"type": "integer", "description": "Темп в ударах в минуту (например, 120)."},
        "key": {"type": "string", "description": "Основная тональность (например, C Major, F# Minor)."},
        "structure": {
            "type": "array",
            "description": "Список секций композиции.",
            "items": {
                "type": "object",
                "properties": {
                    "section_name": {"type": "string", "description": "Название секции (например, Intro, Verse 1, Chorus)."},
                    "instrumentation": {"type": "array", "items": {"type": "string"}, "description": "Список инструментов в секции."}
                },
                "required": ["section_name", "instrumentation"]
            }
        }
    },
    "required": ["title", "genre", "tempo_bpm", "key", "structure"]
}

def generate_music_json(model_path: str, model_name: str, output_file: str, prompt: str):
    """
    Загружает модель GGUF, генерирует ответ в формате JSON с индикатором прогресса
    и сохраняет результат в файл.
    """
    print(f"--- Запуск AI для создания музыки: {model_name} ---", file=sys.stderr)
    print(f"Путь к модели: {model_path}", file=sys.stderr)
    print(f"Целевой файл JSON: {output_file}", file=sys.stderr)

    try:
        # 1. Загрузка модели Llama
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Использовать все доступные слои GPU
            n_ctx=4096,       # Размер контекста
            verbose=False
        )

        # 2. Создание грамматики для принудительного JSON
        json_grammar = LlamaGrammar.from_json_schema(MUSIC_JSON_SCHEMA)

        # 3. Подготовка запроса
        system_prompt = (
            f"You are an AI Music Composer. Your task is to generate a detailed musical structure "
            f"in the requested JSON format based on the user's description. The output MUST be a valid JSON object "
            f"that strictly adheres to the provided JSON schema. Do not output any text or explanation, only the JSON."
        )

        full_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"{system_prompt}<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n"
            f"Generate a song structure based on the following description: {prompt}<|eot_id|>\n"
            f"<|start_header_id|>model<|end_header_id|>\n"
        )
        
        # Устанавливаем разумный лимит на максимальное количество токенов
        max_tokens = 2048
        
        # 4. Генерация с индикатором прогресса
        print("\n[Статус]: Начинается генерация...", file=sys.stderr)
        
        start_time = time.time()
        
        # Используем `generate` для пошагового вывода токенов и отображения прогресса
        output_tokens = []
        for i, token in enumerate(llm.generate(
            full_prompt, 
            max_tokens=max_tokens,
            grammar=json_grammar,  # Принудительная грамматика JSON
            temperature=0.8,
            stop=["<|eot_id|>"],
        )):
            output_tokens.append(token)
            
            # Прогресс в процентах
            progress = min(100, int((i / max_tokens) * 100))
            print(f"\r[Прогресс]: {progress}% ({i+1}/{max_tokens} токенов)", end="", file=sys.stderr)
            sys.stderr.flush()

        print("\n[Статус]: Генерация завершена. Вычисляется финальный JSON...", file=sys.stderr)

        # Объединяем токены в финальный JSON-строку
        generated_text = "".join(output_tokens)
        
        # 5. Очистка и сохранение
        # Поскольку грамматика принудительна, результат должен быть чистым JSON.
        # На всякий случай очищаем от возможного окружающего текста.
        try:
            # Ищем первый и последний символы JSON, чтобы избежать мусора
            json_start = generated_text.find('{')
            json_end = generated_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                final_json_string = generated_text[json_start:json_end]
                
                # Пробуем распарсить, чтобы убедиться в валидности
                parsed_json = json.loads(final_json_string)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(parsed_json, f, ensure_ascii=False, indent=4)
                    
                end_time = time.time()
                print(f"\n[Успех!]: Музыкальный JSON успешно сохранен в: {output_file}", file=sys.stderr)
                print(f"[Статистика]: Общее время генерации: {end_time - start_time:.2f} с", file=sys.stderr)
            else:
                raise json.JSONDecodeError("Не удалось найти чистый JSON в выводе модели.", generated_text, 0)
        
        except json.JSONDecodeError as e:
            print(f"\n[Ошибка!]: Сгенерирован невалидный JSON. Ошибка: {e}", file=sys.stderr)
            print("Неочищенный вывод модели (для отладки):", generated_text, file=sys.stderr)
            sys.exit(1)
        
    except Exception as e:
        print(f"\n[Критическая ошибка]: Произошла ошибка при работе с llama.cpp: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Запуск модели GGUF (Gemma 3 27B) для генерации JSON-структуры музыки.",
        epilog="Пример: acm gemma-3-27b-it-Q4_K_M.gguf /path/to/model/gemma-3-27b-it-Q4_K_M.gguf ./output.json 'Эпическая оркестровая тема для видеоигры.'"
    )
    
    # Модель имени (для отображения)
    parser.add_argument('model_name', type=str, help='Название файла модели (например, gemma-3-27b-it-Q4_K_M.gguf).')
    
    # Путь к файлу модели GGUF
    parser.add_argument('model_path', type=str, help='Полный путь к файлу GGUF-модели.')
    
    # Путь к файлу, куда будет записан JSON
    parser.add_argument('output_file', type=str, help='Путь к файлу, в который будет сохранен JSON.')
    
    # Запрос/инструкция для модели
    parser.add_argument('prompt', type=str, help='Ваш запрос/инструкция для AI (например, "Создай джазовую импровизацию...").')

    args = parser.parse_args()
    
    generate_music_json(args.model_path, args.model_name, args.output_file, args.prompt)
