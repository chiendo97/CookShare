SELECT *, food.id as food_id
FROM food
WHERE food.user_id=:user_id;