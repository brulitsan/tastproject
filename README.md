# Testproject

1. загрузить все зависимости
```shell
pip install poetry==1.7.1
```
```shell
poetry install --all-extras
```

```shell
docker compose up --build
```

чтобы дергать ручки, обязательно быть заренестрированным. 
дл яэтого нужно прокидывать токен в хедер запроса. (нужно для всех ручек, кроме регистрации и авторизации).


sql запрос из тз:
```shell
SELECT u.id, u.email,
       SUM(CASE WHEN l.link_type = 'website' THEN 1 ELSE 0 END) AS num_websites,
       SUM(CASE WHEN l.link_type = 'music' THEN 1 ELSE 0 END) AS num_music,
       SUM(CASE WHEN l.link_type = 'book' THEN 1 ELSE 0 END) AS num_books,
       SUM(CASE WHEN l.link_type = 'article'THEN 1 ELSE 0 END) AS num_article,
       SUM(CASE WHEN l.link_type = 'video'THEN 1 ELSE 0 END) AS num_video,
       COUNT(*) AS total_links
FROM links_link l
JOIN users_user u ON l.user_id = u.id
GROUP BY u.id, u.email, u.created_at
ORDER BY total_links DESC, u.created_at ASC
LIMIT 10;
```
