# Установка RU-версии скиллов (для агента на ноутбуке)

Рабочая RU-адаптация лежит НЕ в `main` GitHub-репозитория, а отдельным архивом.
Причина: ветка с коммитами адаптации не была запушена на remote.

## Способ 1 — из архива (рекомендуется)

1. Скачайте `social-media-skills-ru.tar.gz` и распакуйте:
   `tar xzf social-media-skills-ru.tar.gz`
2. Полученная папка `social-media-skills-ru/` — полная копия репозитория
   с адаптацией (22 скилла + brand/ + README). Замените ею текущий клон
   или используйте как новый рабочий каталог.
3. Проверка установки (должно быть True/существовать):
   - skills/social-media-ru/SKILL.md
   - skills/vk-publisher/scripts/vk_post.py
   - skills/telegram-publisher/scripts/tg_post.py
   - skills/crosspost-adapter/SKILL.md
   - skills/browser-publisher/SKILL.md
   - brand/accounts.md   (там три ваших сообщества ВК по приоритету:
     nord21vek → vod_str → southspecialnetwork)

## Способ 2 — git-патч поверх чистого main

В клоне репозитория (где сейчас main = оригинальный LinkedIn-пак):

    git checkout -b ru-adaptation
    git apply --3way ru-adaptation.patch        # патч всех 4 коммитов адаптации

(Патч формируется командой: `git format-patch main..HEAD` в рабочем репозитории.)

## Что дальше

1. Токен ВК для автопубликации: создать ключ сообщества (право `wall`)
   и `export VK_TOKEN=...` (или через переменные окружения opencode).
2. Первая команда агенту:
   «Прочитай skills/social-media-ru/SKILL.md и brand/accounts.md,
   адаптируй вот этот текст под пост для „Север-21 век"».
