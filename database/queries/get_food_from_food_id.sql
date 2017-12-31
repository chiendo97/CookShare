SELECT food.*, user.*, COUNT(upvote.user_id) as rate
FROM food
INNER JOIN user ON food.user_id=user.id
LEFT JOIN upvote ON food.id=upvote.food_id
WHERE food.id=:food_id
GROUP BY food.id