from flask import Flask, render_template
import requests
import config
import facebook

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("/index.html")


# # Replace ACCESS_TOKEN with a valid Facebook Page Access Token
# graph = facebook.GraphAPI(access_token=config.codePagetoken, version="3.0")

# # Get the most recent post data from the page
# page_posts = graph.get_object(
#     id=f'{config.codePageId}/posts',
#     fields=
#     'message,permalink_url,reactions.limit(0).summary(true),comments.limit(0).summary(true)',
#     limit=20)

# # Iterate over the 20 posts
# for first_post in page_posts['data']:
#     # Get the post message and permalink
#     post_message = first_post.get('message')
#     post_permalink = first_post.get('permalink_url')

#     # Get the engagement data
#     post_reactions_count = first_post.get('reactions',
#                                           {}).get('summary',
#                                                   {}).get('total_count', 0)
#     post_comments_count = first_post.get('comments',
#                                          {}).get('summary',
#                                                  {}).get('total_count', 0)

#     # Print the post data and engagement data
#     print("Post Message: ", post_message)
#     print("Post Permalink: ", post_permalink)
#     print("Post Reactions Count: ", post_reactions_count)
#     print("Post Comments Count: ", post_comments_count)

#     # Get the comments data
#     comments = first_post.get('comments', {}).get('data', [])
#     if comments:
#         for comment in comments:
#             comment_message = comment.get('message')
#             comment_created_time = comment.get('created_time')

#             # Print the comment data
#             print("Comment Message: ", comment_message)
#             print("Comment Created Time: ", comment_created_time)
#     else:
#         print("No comments found for this post.")


def get_facebook_page_posts_with_engagement(access_token, page_id, num_posts):
    graph = facebook.GraphAPI(access_token)

    try:
        posts = graph.get_object(id=str(page_id) + "/posts",
                                 limit=str(num_posts))['data']
    except facebook.GraphAPIError as e:
        print(f"Error getting Facebook Page posts: {e}")
        return []

    filtered_posts = []
    for post in posts:
        post_id = post["id"]
        engagement = []
        try:
            engagement = graph.get_object(id=post_id + "/likes",
                                          limit=1)['data']
        except facebook.GraphAPIError as e:
            print(f"Error getting engagement data for post {post_id}: {e}")

        post["engagement"] = engagement

        # Get comments data
        try:
            comments = graph.get_object(id=post_id + "/comments")['data']
        except facebook.GraphAPIError as e:
            print(f"Error getting comments data for post {post_id}: {e}")
            comments = []
        post["comments"] = comments

        filtered_posts.append(post)

    return filtered_posts


access_token = config.codePagetoken
page_id = config.codePageId
num_posts = 20

posts = get_facebook_page_posts_with_engagement(access_token, page_id,
                                                num_posts)
print(posts)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)