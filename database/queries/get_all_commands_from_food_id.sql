SELECT post.*, user.username
FROM post
INNER JOIN user On post.user_id=user.id
WHERE food_id=:food_id;