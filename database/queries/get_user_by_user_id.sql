SELECT user.*, count(upvote.user_id) as rate
FROM food
LEFT JOIN upvote ON food.id=upvote.food_id
INNER JOIN user ON food.user_id=user.id
WHERE user.id=:user_id
GROUP BY food.user_id;