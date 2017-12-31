select user.*, count(upvote.user_id) as rate
from food
left join upvote on food.id=upvote.food_id
inner join user on food.user_id=user.id
group by food.user_id
order by rate desc;
