from facebook_scraper import get_posts
import csv

page = "ccc72716"
max_pages = 100

with open("jixuan_posts.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "date", "text", "post_url", "image", "video", "likes", "comments", "shares", "post_id"
    ])
    for post in get_posts(page, pages=max_pages, extra_info=True, cookies="/Users/jamie/Desktop/農友日記/mapping/cookies.txt"):
        print(post)
        try:
            writer.writerow([
                post.get("time", ""),
                post.get("text", ""),
                post.get("post_url", ""),
                post.get("image", ""),
                post.get("video", ""),
                post.get("likes", ""),
                post.get("comments", ""),
                post.get("shares", ""),
                post.get("post_id", ""),
            ])
        except Exception as e:
            print("⚠️ Error writing post:", e)