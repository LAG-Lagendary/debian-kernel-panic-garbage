#!/bin/bash
# =========================================================================
# WEEKLY AIDE JOURNALIST SETUP SCRIPT
# Инициализирует AIDE и настраивает ежедневное и еженедельное задания CRON
# для ротации баз данных (4 последних копии) и тихого логирования.
# =========================================================================

# Проверка привилегий root
if [ "$EUID" -ne 0 ]; then
    echo "🚨 Скрипт 'Системный Журналист' ДОЛЖЕН быть запущен от имени root или с помощью sudo."
    exit 1
fi

# 1. КОНФИГУРАЦИЯ
LOG_DIR="/var/log/system_journalist"
ARCHIVE_FILE="$LOG_DIR/daily_changes_archive.log"
AIDE_DB_DIR="/var/lib/aide"
AIDE_DB="$AIDE_DB_DIR/aide.db"
AIDE_ARCHIVE_DIR="$AIDE_DB_DIR/archive" # Новый каталог для архивов базы данных
TEMP_REPORT="/tmp/aide_daily_report.tmp"
AIDE_RUN_SCRIPT="/usr/local/bin/run_aide_daily.sh"
AIDE_ROTATE_SCRIPT="/usr/local/bin/run_aide_weekly_rotate.sh"
CRON_JOB_DAILY="AIDE_DAILY_CHECK"
CRON_JOB_WEEKLY="AIDE_WEEKLY_ROTATE"

# 2. Создание каталогов и прав доступа
echo "====================================================="
echo "💥 АКТИВАЦИЯ СИСТЕМЫ 'СИСТЕМНЫЙ ЖУРНАЛИСТ' (AIDE) 💥"
echo "====================================================="

mkdir -p "$LOG_DIR" "$AIDE_ARCHIVE_DIR"
# Права 700 для защиты журнала изменений и архивов
chmod 700 "$LOG_DIR" "$AIDE_ARCHIVE_DIR"
echo "⚙️ Каталоги журнала и архива созданы: $LOG_DIR, $AIDE_ARCHIVE_DIR"

# 3. Инициализация AIDE database
if [ ! -f "$AIDE_DB" ]; then
    echo "🔐 Инициализация AIDE (создание эталонной базы данных)..."
    /usr/bin/aide --init
    if [ -f /var/lib/aide/aide.db.new ]; then
        mv /var/lib/aide/aide.db.new "$AIDE_DB"
        echo "✅ База данных AIDE создана и готова к работе."
    else
        echo "❌ Ошибка при инициализации AIDE. Проверьте конфигурацию AIDE."
        exit 1
    fi
else
    echo "✅ База данных AIDE уже существует. Пропускаем инициализацию."
fi


# 4. Создание скрипта еженедельной ротации (сохраняем в отдельный файл)
echo "⚙️ Шаг 2: Создание скрипта еженедельной ротации (сохранение 4-х последних баз)..."
# Вызываем второй скрипт для его создания
bash "$0" --create-rotate-script

# 5. Создание скрипта ежедневного мониторинга
echo "⚙️ Шаг 3: Создание ежедневного мониторингового скрипта..."
cat <<EOF > "$AIDE_RUN_SCRIPT"
#!/bin/bash

# Пути
LOG_DIR="$LOG_DIR"
ARCHIVE_FILE="$ARCHIVE_FILE"
TEMP_REPORT="$TEMP_REPORT"
AIDE_DB="$AIDE_DB"
DATE_STAMP="\$(date '+%Y-%m-%d %H:%M:%S')"

# Проверка, существует ли основная база
if [ ! -f \$AIDE_DB ]; then
    echo "🛑 [\$DATE_STAMP] КРИТИЧЕСКАЯ ОШИБКА: База данных AIDE не найдена! Пропустите проверку." >> \$ARCHIVE_FILE
    logger -t AIDE_ERROR "AIDE database file not found at \$AIDE_DB. Check installation."
    exit 1
fi

# Выполнение проверки AIDE
/usr/bin/aide --check > \$TEMP_REPORT 2>&1
AIDE_STATUS=\$?

# Добавление разделителя в архивный файл
echo -e "\n\n=======================================================" >> \$ARCHIVE_FILE
echo "=== АНАЛИЗ СИСТЕМНОЙ ЦЕЛОСТНОСТИ - \$DATE_STAMP ===" >> \$ARCHIVE_FILE
echo "=======================================================" >> \$ARCHIVE_FILE


# Анализ статуса AIDE
case \$AIDE_STATUS in
    0)
        # 0: Изменений нет (NOMINAL)
        echo "🟢 [\$DATE_STAMP] Статус: НАРУШЕНИЯ НЕ ОБНАРУЖЕНЫ. Система NOMINAL." >> \$ARCHIVE_FILE
        rm -f \$TEMP_REPORT
        ;;
    1)
        # 1: Обнаружены только 'нормальные' изменения (например, файлы логов)
        echo "🟡 [\$DATE_STAMP] Статус: ОБНАРУЖЕНЫ ИЗМЕНЕНИЯ (Логи/временные файлы)." >> \$ARCHIVE_FILE
        # Архивируем краткий отчет
        cat \$TEMP_REPORT >> \$ARCHIVE_FILE
        rm -f \$TEMP_REPORT
        ;;
    2)
        # 2: Обнаружены НЕРАЗРЕШЕННЫЕ изменения (критическое нарушение целостности)
        CRITICAL_MESSAGE="🚨 CRITICAL ALARM: Обнаружено НЕРАЗРЕШЕННОЕ ИЗМЕНЕНИЕ. Сбой целостности AIDE. [\$DATE_STAMP]"
        
        # 1. Отправка оповещения администраторам APP
        logger -t AIDE_INTEGRITY_VIOLATION "\$CRITICAL_MESSAGE. Отчет сохранен в \$LOG_DIR/aide_report_violation_\$(date '+%Y%m%d_%H%M%S').log"
        echo "❌ [\$DATE_STAMP] \$CRITICAL_MESSAGE" >> \$ARCHIVE_FILE
        
        # 2. Перемещение полного отчета (Улики)
        REPORT_FILENAME="aide_report_violation_\$(date '+%Y%m%d_%H%M%S').log"
        mv \$TEMP_REPORT "\$LOG_DIR/\$REPORT_FILENAME"
        echo "Полный отчет о нарушении сохранен: \$LOG_DIR/\$REPORT_FILENAME" >> \$ARCHIVE_FILE
        
        # 3. Сохранение улик: База данных AIDE НЕ ОБНОВЛЯЕТСЯ (остается на уровне прошлой недели)
        echo "!!! ВНИМАНИЕ: База данных AIDE НЕ ОБНОВЛЕНА. УЛИКИ СОХРАНЕНЫ. !!!" >> \$ARCHIVE_FILE
        
        ;;
    *)
        # 3-255: Ошибка при выполнении AIDE
        echo "🛑 [\$DATE_STAMP] СИСТЕМНАЯ ОШИБКА: AIDE вернул код \$AIDE_STATUS. Проверьте скрипт." >> \$ARCHIVE_FILE
        logger -t AIDE_ERROR "AIDE Monitoring failed with status code \$AIDE_STATUS."
        rm -f \$TEMP_REPORT
        ;;
esac

# ВАЖНО: ЕЖЕДНЕВНОЕ ОБНОВЛЕНИЕ БАЗЫ ДАННЫХ AIDE ЗДЕСЬ ОТКЛЮЧЕНО.
# Обновление выполняется ТОЛЬКО ЕЖЕНЕДЕЛЬНЫМ скриптом ротации.
EOF

chmod +x "$AIDE_RUN_SCRIPT"
echo "✅ Ежедневный скрипт мониторинга создан: $AIDE_RUN_SCRIPT"


# 6. Настройка заданий CRON
echo "⚙️ Шаг 4: Настройка CRON..."

# DAILY CHECK: Запуск ежедневной проверки (тихое логирование изменений)
CRON_ENTRY_DAILY="0 3 * * * $AIDE_RUN_SCRIPT" # Каждое утро в 3:00

# WEEKLY ROTATION: Запуск еженедельной ротации (обновление базы)
CRON_ENTRY_WEEKLY="0 4 * * 1 $AIDE_ROTATE_SCRIPT" # Каждый понедельник в 4:00 (после ежедневной проверки)

# Удаляем любые старые задачи и добавляем новые
(
    crontab -l 2>/dev/null | grep -v "$CRON_JOB_DAILY" | grep -v "$CRON_JOB_WEEKLY"
    echo "$CRON_ENTRY_DAILY # $CRON_JOB_DAILY"
    echo "$CRON_ENTRY_WEEKLY # $CRON_JOB_WEEKLY"
) | crontab -

echo "✅ Задание CRON для ежедневной проверки (03:00) и еженедельной ротации (Пн, 04:00) добавлено."

echo "====================================================="
echo "✅ 'СИСТЕМНЫЙ ЖУРНАЛИСТ' АКТИВИРОВАН. Журнал: $ARCHIVE_FILE"
echo "=========================================================================================="
echo "🔔 Не забудьте запустить этот скрипт с флагом --create-rotate-script, если он не был создан автоматически!"
echo "=========================================================================================="

# 7. Логика создания второго скрипта (для самодостаточности)
if [ "$1" == "--create-rotate-script" ]; then
    cat <<'EOF_ROTATE' > "$AIDE_ROTATE_SCRIPT"
#!/bin/bash
# =========================================================================
# WEEKLY AIDE DATABASE ROTATOR AND UPDATER
# Запускается каждую неделю для обновления эталонной базы и архивирования
# предыдущей версии (хранение 4 последних копий).
# =========================================================================

# Конфигурация
AIDE_DB_DIR="/var/lib/aide"
AIDE_DB="$AIDE_DB_DIR/aide.db"
AIDE_ARCHIVE_DIR="$AIDE_DB_DIR/archive"
MAX_ARCHIVES=4
DATE_STAMP_WEEKLY="$(date '+%Y-%m-%d_Week%V')"
LOG_DIR="/var/log/system_journalist"
ARCHIVE_FILE="$LOG_DIR/daily_changes_archive.log"

echo -e "\n\n=======================================================" >> "$ARCHIVE_FILE"
echo "=== ЕЖЕНЕДЕЛЬНАЯ РОТАЦИЯ БАЗЫ ДАННЫХ AIDE - $DATE_STAMP_WEEKLY ===" >> "$ARCHIVE_FILE"
echo "=======================================================" >> "$ARCHIVE_FILE"


# 1. Проверка наличия базы данных
if [ ! -f "$AIDE_DB" ]; then
    echo "🛑 [\$DATE_STAMP_WEEKLY] КРИТИЧЕСКАЯ ОШИБКА: Основная база AIDE не найдена. Ротация отменена." >> "$ARCHIVE_FILE"
    logger -t AIDE_ROTATE_ERROR "AIDE database file not found. Weekly rotation aborted."
    exit 1
fi

# 2. Сохранение текущей базы AIDE как архивной копии
ARCHIVE_PATH="$AIDE_ARCHIVE_DIR/aide.db.$DATE_STAMP_WEEKLY"
echo "⚙️ Шаг 1: Архивирование текущей эталонной базы в $ARCHIVE_PATH" >> "$ARCHIVE_FILE"

cp "$AIDE_DB" "$ARCHIVE_PATH"

# 3. Обновление эталонной базы AIDE
echo "⚙️ Шаг 2: Создание новой базы данных (обновление эталона)..." >> "$ARCHIVE_FILE"
/usr/bin/aide --update > /dev/null 2>&1

if [ -f "$AIDE_DB_DIR/aide.db.new" ]; then
    # Замена старой базы на новую
    mv "$AIDE_DB_DIR/aide.db.new" "$AIDE_DB"
    echo "✅ База данных AIDE успешно обновлена и заменена." >> "$ARCHIVE_FILE"
else
    # Если обновление не удалось, но архивация уже прошла, это не критично
    echo "❌ Ошибка при создании новой базы данных AIDE (aide.db.new не найден). Эталон НЕ ОБНОВЛЕН." >> "$ARCHIVE_FILE"
    logger -t AIDE_ROTATE_WARN "AIDE database failed to update (aide.db.new missing)."
fi

# 4. Ротация архивов (оставляем только MAX_ARCHIVES последних)
echo "⚙️ Шаг 3: Ротация архивов (сохраняем $MAX_ARCHIVES последних копий)..." >> "$ARCHIVE_FILE"

# Получаем список архивов, сортируем по дате и удаляем лишние
find "$AIDE_ARCHIVE_DIR" -type f -name 'aide.db.*' | sort -r | sed "1,${MAX_ARCHIVES}d" | xargs -r rm -f

# Подсчет оставшихся для проверки
REMAINING_ARCHIVES=$(find "$AIDE_ARCHIVE_DIR" -type f -name 'aide.db.*' | wc -l)
echo "✅ Ротация завершена. В архиве сохранено $REMAINING_ARCHIVES копий (не более $MAX_ARCHIVES)." >> "$ARCHIVE_FILE"

EOF_ROTATE
    chmod +x "$AIDE_ROTATE_SCRIPT"
    echo "✅ Скрипт еженедельной ротации создан: $AIDE_ROTATE_SCRIPT"
    exit 0
fi
