---
name: vk-publisher
description: >
  Publish verified posts to ВКонтакте communities via the official VK API
  (wall.post with photo attachments). Use this skill whenever the user says
  "опубликуй в ВК", "выложи во ВКонтакте", "запостить в паблик", mentions a
  vk.com group id, or when crosspost-adapter hands off a confirmed VK version.
  Requires VK_TOKEN in the environment; falls back to browser-publisher when
  no token or an unsupported format (polls, stories, complex carousels) is needed.
---

# VK Publisher — публикация во ВКонтакте через API

## Предусловия
1. Переменная окружения `VK_TOKEN` (ключ сообщества с правом `wall`). Если её нет — сказать пользователю, как получить: сообщество → Управление → Страницы… нет → «Работать с API» → ключ доступа; либо предложить путь через `browser-publisher`. Никогда не печатать значение токена.
2. `group_id` целевого сообщества — из `/workspace/brand/accounts.md` или спросить. Принимается и `club12345`, и числом.
3. Финальный текст подтверждён пользователем ЯВНО. Без подтверждения — остановиться.

## Шаг 1. Проверка по карте площадки
Прочитать `skills/social-media-ru/references/platforms/vk.md`:
- длина ≤ лимита стены; если >~1800 знаков — предупредить про «под кат»;
- хештеги 3–5, в конце;
- внешних ссылок много нет (по карте — риск снижения охвата).

## Шаг 2. Публикация
Текст передать файлом (не аргументом командной строки), чтобы экранирование не сломало кириллицу/переносы:

```bash
python3 scripts/vk_post.py --group-id <ID> --text-file draft.txt [--photo /path/img.jpg] [--publish-after UNIXTIME]
```

Скрипт: загрузка фото (getWallUploadServer→saveWallPhoto) при наличии, затем `wall.post` с `from_group=1`, `attachments`, опционально `publish_date`. Выводит `post_id` и ссылку `vk.com/wall-<gid>_<pid>`.

## Шаг 3. После публикации
1. Показать пользователю ссылку на пост.
2. Записать запись в `/workspace/brand/changelog.md`: дата, площадка, post_id, направление.
3. Если обнаружено расхождение поведения с картой — обновить карту (см. playbook, «Актуализация карт»).

## Отказоустойчивость
- Ошибка API `permission denied` → проверить права токена (нужен `wall` сообщества).
- `flood control` / анти-спам → не повторять сразу; предложить отложенную публикацию или браузерный путь.
- Нужен формат без API (опрос, карусель, история) → маршрутизировать в `browser-publisher`.
