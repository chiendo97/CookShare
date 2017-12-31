SELECT *, food.id as food_id
FROM food
INNER JOIN user ON food.user_id=user.id
WHERE food.name LIKE :name;