# Social Media Skills — RU build (ВКонтакте)

Финальная сборка для работы с тремя VK-сообществами пользователя:
1. «Север-21 век» (nord21vek) — новости: мир, Россия, СВО
2. «Союз танкистов России» (vod_str) — ветеранская организация
3. «ЮгСпецСети» (southspecialnetwork) — агентство автоматизации

MAX / Telegram / TenChat переведены в спящий режим (карты площадок сохранены).

## Состав
- `skills/social-media-ru/` — роутер + platform-playbook + карты площадок
- `skills/vk-publisher/` — публикация через VK API (`scripts/vk_post.py`)
- `skills/crosspost-adapter/`, `browser-publisher/`, `telegram-publisher/`
- остальные 17 скиллов — генераторы контента (voice-builder, post-writer и т.д.)
- `brand/accounts.md` — реестр сообществ; `brand/changelog.md` — журнал
- `INSTALL-RU.md` — инструкция установки на ноутбук (архив / патч)
- `README.orig-linkedin.md` — оригинальный LinkedIn-README автора форка

## Быстрый старт
1. Распакуйте архив `social-media-skills-ru.tar.gz` (см. INSTALL-RU.md).
2. `export VK_TOKEN=<ключ сообщества с правом wall>`.
3. Команда агенту: «Прочитай skills/social-media-ru/SKILL.md и brand/accounts.md,
   подготовь пост про <тема> для „Север-21 век", после подтверждения опубликуй».
