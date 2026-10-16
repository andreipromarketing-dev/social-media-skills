---
name: telegram-publisher
description: >
  Publish confirmed posts to Telegram channels via the official Bot API
  (sendMessage / sendPhoto with caption). Use this skill whenever the user says
  "опубликуй в телеграм", "выложи в канал", "запостить в TG", mentions a channel
  or @botusername, or when crosspost-adapter hands off a confirmed Telegram
  version. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the environment;
  falls back to browser-publisher when posting must come from the personal
  account instead of a bot.
---

# Telegram Publisher — публикация через Bot API

## Предусловия
1. `TELEGRAM_BOT_TOKEN` (от @BotFather) и `TELEGRAM_CHAT_ID` (id канала, для паблик-каналов — `@username` или отрицательный числовой id). Бот должен быть админом канала. Если переменных нет — объяснить получение и предложить `browser-publisher` как запасной путь. Токены не печатать.
2. Финальный текст подтверждён пользователем ЯВНО.

## Шаг 1. Проверка по карте площадки
Прочитать `skills/social-media-ru/references/platforms/telegram.md`:
- подпись к фото ≤ 1024 символов (если длиннее — резать или отправлять отдельным текстовым сообщением);
- хештеги 1–3;
- MarkdownV2 требует экранирования спецсимволов — надёжнее HTML-разметка (`parse_mode=HTML`).

## Шаг 2. Публикация

```bash
python3 scripts/tg_post.py --text-file draft.txt [--photo /path/img.jpg] [--html]
```

Скрипт читает env-переменные, вызывает `sendPhoto` (caption) или `sendMessage`, печатает `message_id` и ссылку `t.me/<channel>/<id>` (для каналов с публичным username).

## Шаг 3. После публикации
1. Показать ссылку на сообщение.
2. Запись в `/workspace/brand/changelog.md`.
3. Расхождения с картой → обновить карту (playbook, «Актуализация карт»).

## Отказоустойчивость
- `403 bot is not a member` → попросить добавить бота админом канала.
- `429 Too Many Requests` → подождать `retry_after`, не спамить.
- Нужна публикация от личного аккаунта или планирование в UI → `browser-publisher`.
