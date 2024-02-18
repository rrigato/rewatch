first_episode="Episode 3"
first_episode_link="https://pluto.tv/en/on-demand/series/602c16c0f2c1bd001af24c31/season/1/episode/60394e6c6c2a2d001410c37b"
first_episode_title="The Assassin of Flash"
item_sort_key="cyborg009"
post_date="2024-02-17"
#for Test subreddit
# rewatch_flair_id="6b39b4a6-be2f-11e8-ac14-0e2593696d0a"
rewatch_flair_id="693636e6-ba17-11e3-a364-12313d31e5b1"
second_episode="Episode 4"
second_episode_link="https://pluto.tv/en/on-demand/series/602c16c0f2c1bd001af24c31/season/1/episode/60394e6d6c2a2d001410c3b2"
second_episode_title="At the End of the Battle"
show_title_name="Cyborg 009"
#for Test subreddit post
#subreddit_name="Test"
subreddit_name="Toonami"
table_title="Episode | Source\n-------|------\n"


# '"$<variable_name>"' enables string concatenation
aws dynamodb put-item \
    --table-name rewatch_shared_table \
    --item '{
        "PK": {"S": "rewatch#'"$post_date"'"}, 
        "SK": {"S": "cyborg009"}, 
        "flair_id": {"S": "'"$rewatch_flair_id"'"},
        "post_title": {"S": "Cyborg 009 '"$first_episode"' and '"$second_episode"' Rewatch"},
        "post_message": {
                "S": "'"$table_title"'**'"$first_episode_title"'** | ['"$first_episode"']('"$first_episode_link"')\n**'"$second_episode_title"'** | ['"$second_episode"']('"$second_episode_link"')"
            },
        "subreddit": {
            "S": "'"$subreddit_name"'"
        }

    }' \
    --region us-east-1