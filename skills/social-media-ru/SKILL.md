---
name: social-media-ru
description: >
  Router and platform knowledge base for running Russian social media accounts
  (ВКонтакте, MAX, Telegram, TenChat) from opencode. Use this skill whenever the user
  mentions ВКонтакте, VK, ВК, МАКС, max.ru, Телеграм, Telegram, Тенчат, TenChat,
  "выложить/опубликовать пост", "кросспост", "адаптировать под площадку", or asks which
  publishing skill to use. Provides platform cards (limits, formatting, algorithms) in
  references/platforms/ and routing rules in references/platform-playbook.md. Delegates
  writing to post-writer/crosspost-adapter and publishing to vk-publisher,
  telegram-publisher, browser-publisher.
---

# Social Media RU — роутер и база знаний по площадкам

## Назначение
Единая точка входа для работы с российскими соцсетями проекта:
**ВКонтакте, MAX, Telegram, TenChat**. Этот скилл НЕ пишет и НЕ публикует сам —
он даёт знания о площадках и маршрутизирует задачу в правильный скилл.

## Шаг 1. Определить сообщество и площадку
1. Прочитать `/workspace/brand/accounts.md` — там заполненный реестр трёх ВК-сообществ в порядке приоритета: `nord21vek` (новости/СВО), `vod_str` (танкисты), `southspecialnetwork` (ЮгСпецСети).
2. Определить целевое сообщество по теме запроса; если непонятно — спросить одним вопросом. Тон брать из playbook, раздел 4 (тон привязан к сообществу).
3. Площадка по умолчанию — **только ВКонтакте**. MAX / Telegram / TenChat — спящий режим: трогать их можно только по явной просьбе пользователя.

## Шаг 2. Маршрутизация задачи

| Задача пользователя | Куда идти |
|---|---|
| Написать пост под площадку | `post-writer` (с чтением карты площадки перед финальной сборкой) |
| Один текст → несколько площадок | `crosspost-adapter` |
| Опубликовать во ВКонтакте | `vk-publisher` (API) или `browser-publisher` (UI) |
| Опубликовать в Telegram | `telegram-publisher` (Bot API) или `browser-publisher` |
| Опубликовать в MAX / TenChat | `browser-publisher` (API нет) |
| Рубрики и контент-план | `content-matrix` + карта площадки |
| Проверить лимиты/форматирование | прочитать нужную карту здесь, в `references/platforms/` |

## Шаг 3. Правила чтения карт
- Перед любой адаптацией текста прочитать полную карту площадки из `references/platforms/<slug>.md`. Не использовать «память модели» о площадке — правила меняются.
- Если у карты `confidence: предположение` — явно предупредить пользователя, что лимиты не верифицированы, и после первой публикации обновить карту (инструкции в разделе «Актуализация карт» playbook'а).
- Пустые поля карты = неизвестные факты. Спросить пользователя или проверить через browser-скилл; никогда не додумывать.

## Безопасность публикаций
- Публикация только после явного подтверждения пользователем финального текста.
- Никогда не печатать токены в вывод; токены читать из переменных окружения (`VK_TOKEN`, `TELEGRAM_BOT_TOKEN`).
- Один инфоповод на нескольких площадках — всегда разными текстами (см. playbook, раздел 5).

## Файлы
- `references/platform-playbook.md` — реестр площадок, порядок адаптации, тона направлений, правила актуализации.
- `references/platforms/vk.md` — карта ВКонтакте.
- `references/platforms/max.md` — карта MAX (требует браузерной верификации).
- `references/platforms/telegram.md` — карта Telegram.
- `references/platforms/tenchat.md` — карта TenChat (требует браузерной верификации).
- `references/platforms/_TEMPLATE.md` — шаблон для новых площадок (OK/RU.Studio/Dzen при необходимости).
