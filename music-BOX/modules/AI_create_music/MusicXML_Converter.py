import json
import sys
import os
# ИСПРАВЛЕНИЕ: 'common' заменен на 'metadata' для совместимости
from music21 import stream, note, chord, meter, key, tempo, converter, metadata

# Устанавливаем минимальный уровень логирования, чтобы не засорять консоль.
# common.set ('warnings', 'log') # <-- Эта строка удалена, чтобы избежать AttributeError

def create_musicxml_from_json(json_filepath):
    """
    Основная функция конвертации Music-JSON в MusicXML.

    Читает файл JSON, создает объекты music21 (партии, такты, ноты)
    и сохраняет результат в файл MusicXML.
    """
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {json_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: Неверный формат JSON в файле {json_filepath}")
        return

    metadata_dict = data.get('metadata', {})
    events = data.get('events', [])

    # --- 1. Инициализация партитуры и партий ---

    # Главный поток, который будет содержать все партии
    score = stream.Score()

    # ИСПРАВЛЕНИЕ: Используем metadata.Metadata() вместо common.Metadata()
    score.metadata = metadata.Metadata()
    score.metadata.title = metadata_dict.get('title', 'Untitled Composition')
    score.metadata.composer = metadata_dict.get('composer', 'Unknown Composer')

    # Словарь для хранения объектов Part (дорожек), ключ - название партии (например, 'Melody')
    parts = {}

    # --- 2. Установка Метаданных (Оформление) ---

    time_signature_str = metadata_dict.get('time_signature') or '4/4'
    key_str = metadata_dict.get('key') or 'C Major'
    tempo_bpm = metadata_dict.get('tempo', 120)

    # --- 3. Обработка Событий ---

    try:
        # 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ KEY (Tonic/Mode)
        # Разделяем строку "D minor" на "D" и "minor"
        key_parts = key_str.split()
        if len(key_parts) == 2:
            # Передаем тонику и лад как отдельные аргументы
            current_key = key.Key(key_parts[0], key_parts[1])
        else:
            # Если тональность - одно слово (напр. "C")
            current_key = key.Key(key_str)
        # --- Конец Исправления ---

        current_tempo = tempo.MetronomeMark(number=tempo_bpm)
        current_time_signature = meter.TimeSignature(time_signature_str)

    except Exception as e:
        print(f"Предупреждение: Не удалось обработать метаданные (размер/тональность). Использование 4/4 и C Major. Ошибка: {e}")

        # 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ KEY (Fallback)
        # Явно указываем тонику "C" и лад "Major"
        current_key = key.Key('C', 'Major')
        # --- Конец Исправления ---

        current_tempo = tempo.MetronomeMark(number=120)
        current_time_signature = meter.TimeSignature('4/4')


    # Определяем, какие такты сейчас активны для каждой партии
    current_measures = {}

    for event in events:
        event_type = event.get('type')
        part_name = event.get('part')

        # Пропускаем пустые или некорректные события
        if not part_name or part_name == '.':
            continue

        # Создаем Part (дорожку), если ее еще нет
        if part_name not in parts:
            p = stream.Part()
            p.id = part_name
            p.partName = part_name
            parts[part_name] = p

            # Инициализируем первый Measure (такт) для новой партии
            m = stream.Measure()

            # Добавляем ключевые музыкальные символы в начало первого такта:
            m.append(current_time_signature)
            m.append(current_key)
            m.append(current_tempo)

            p.append(m)
            current_measures[part_name] = m
            score.insert(0, p) # Вставляем в партитуру

        # Получаем текущую партию и такт
        p = parts[part_name]
        m = current_measures[part_name]

        if event_type == 'bar_start':
            # Закрываем предыдущий такт и открываем новый

            # 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ TimeSignature: .totalLength заменен на .barDuration.quarterLength
            if m.duration.quarterLength < current_time_signature.barDuration.quarterLength:
                # 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ 'fillEmpty': Заменен на 'padWithRests'
                m.padWithRests()

            # Добавляем закрытый такт в партию
            p.append(m)

            # Создаем новый такт и делаем его текущим
            m = stream.Measure()
            current_measures[part_name] = m

        elif event_type == 'note':
            try:
                n = note.Note(event['pitch'])
                n.duration.quarterLength = event['duration']
                # Добавляем другие свойства, если они есть
                if 'velocity' in event:
                    n.volume.velocity = event['velocity']
                m.append(n)
            except Exception as e:
                print(f"Предупреждение: Пропуск невалидной ноты (Pitch: {event.get('pitch')}). Ошибка: {e}")

        elif event_type == 'rest':
            r = note.Rest()
            r.duration.quarterLength = event['duration']
            m.append(r)

        elif event_type == 'chord':
            try:
                # Обработка случая, когда pitch может быть строкой или массивом строк
                pitch_data = event['pitch']
                if isinstance(pitch_data, str):
                    # Если это строка (напр., "C4 E4 G4"), music21 может обработать ее
                    pitches = pitch_data.split()
                elif isinstance(pitch_data, list):
                    pitches = pitch_data
                else:
                    raise ValueError("Неверный тип данных для 'pitch' в аккорде.")

                c = chord.Chord(pitches)
                c.duration.quarterLength = event['duration']
                if 'velocity' in event:
                    c.volume.velocity = event['velocity']
                m.append(c)
            except Exception as e:
                print(f"Предупреждение: Пропуск невалидного аккорда (Pitch: {event.get('pitch')}). Ошибка: {e}")

    # --- 4. Финальная очистка и экспорт ---

    # После завершения цикла, добавляем последний активный такт в каждую партию
    for part_name, p in parts.items():
        m = current_measures[part_name]
        # Проверяем, что в такте есть контент, прежде чем заполнять и добавлять
        if m.duration.quarterLength > 0:
            # 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ 'fillEmpty': Заменен на 'padWithRests'
            m.padWithRests() # Гарантируем заполнение последнего такта
            p.append(m)

    # Определяем путь для сохранения MusicXML
    output_filepath = os.path.splitext(json_filepath)[0] + '.musicxml'

    # Конвертер будет работать, только если есть хоть одна партия
    if not score.parts:
         print(f"❌ Ошибка: В JSON-файле '{json_filepath}' не найдено ни одной ноты/партии для конвертации.")
         return

    print(f"\nКонвертация {json_filepath} -> {output_filepath}")

    # Сохраняем партитуру в формате MusicXML
    # Использование .write() напрямую - более надежный метод
    score.write('musicxml', fp=output_filepath)

    print("✅ Успешно сохранено.")


if __name__ == '__main__':
    # Скрипт ожидает один аргумент - путь к JSON файлу
    if len(sys.argv) < 2:
        print("Использование: python musicxml_converter.py <путь_к_json_файлу>")
        sys.exit(1)

    json_path = sys.argv[1]
    create_musicxml_from_json(json_path)
