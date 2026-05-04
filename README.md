# Custom Auth RBAC API

## Сущности

User — пользователь.  
Session — активная сессия пользователя.  
Role — роль.  
UserRole — связь пользователя и роли.  
Resource — защищаемый ресурс.  
Action — действие.  
Permission — разрешение роли выполнять действие над ресурсом.

## Проверка доступа

После login пользователь получает токен.

Токен передается в заголовке:

Authorization: Bearer TOKEN

Если токена нет или он неверный, API возвращает 401.

Если пользователь найден, но у него нет нужного permission, API возвращает 403.

## Пример правила

role=user  
resource=orders  
action=read

Значит пользователь может открыть:

GET /api/mock/orders/

Но не может создать report, если у него нет:

resource=reports  
action=create