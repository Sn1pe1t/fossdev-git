# Микросервисы заказов

Проект состоит из трёх сервисов: product-service (товары), discount-service (скидки) и order-service (заказы). Взаимодействие через Docker Compose. Запуск автоматизирован через Makefile.

## Команды Make

- make build – собрать образы
- make up – запустить контейнеры
- make down – остановить
- make logs – посмотреть логи
- make ps – статус контейнеров
- make clean – полная очистка

## Пример запроса

curl -X POST http://localhost:8002/orders -H "Content-Type: application/json" -d '{"product_id":"notebook","quantity":2,"promo_code":"STUDENT10"}'
