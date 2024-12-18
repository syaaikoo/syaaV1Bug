import importlib
import random
from textblob import TextBlob
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import datetime
import cv2
import numpy as np
from PIL import Image
import piexif
import folium
from geopy.geocoders import Nominatim

class InstagramScraper:
    def __init__(self, module_name):
        self.module = importlib.import_module(module_name)
        self.geolocator = Nominatim(user_agent="phantom_exploit")

    def get_account_data(self, username):
        if self.module.__name__ == 'instaloader':
            return self._get_data_instaloader(username)
        elif self.module.__name__ == 'instagram_scraper':
            return self._get_data_instagram_scraper(username)
        elif self.module.__name__ == 'instagram_python_scraper':
            return self._get_data_instagram_python_scraper(username)
        else:
            raise ValueError(f"Unsupported module: {self.module.__name__}")

    def _get_data_instaloader(self, username):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        return {
            'username': profile.username,
            'full_name': profile.full_name,
            'biography': profile.biography,
            'followers': profile.followers,
            'following': profile.followees,
            'posts': profile.mediacount,
        }

    def _get_data_instagram_scraper(self, username):
        scraper = self.module.InstagramScraper()
        return scraper.scrape_profile(username)

    def _get_data_instagram_python_scraper(self, username):
        scraper = self.module.InstagramPythonScraper()
        return scraper.get_profile(username)

    def analyze_sentiment(self, username, post_count=10):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        sentiments = []

        for post in profile.get_posts():
            if len(sentiments) >= post_count:
                break
            for comment in post.get_comments():
                blob = TextBlob(comment.text)
                sentiments.append(blob.sentiment.polarity)

        return sum(sentiments) / len(sentiments) if sentiments else 0

    def detect_bot_followers(self, username, sample_size=100):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        followers = list(profile.get_followers())
        sample = random.sample(followers, min(sample_size, len(followers)))

        bot_count = 0
        for follower in sample:
            if self._is_likely_bot(follower):
                bot_count += 1

        return bot_count / len(sample)

    def _is_likely_bot(self, profile):
        # Simplified bot detection logic
        return (profile.mediacount == 0 or
                profile.followers == 0 or
                profile.followees / profile.followers > 50 if profile.followers > 0 else False)

    def visualize_social_network(self, username, depth=2):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        G = nx.Graph()

        def add_connections(user, current_depth):
            if current_depth > depth:
                return
            for follower in user.get_followers():
                G.add_edge(user.username, follower.username)
                if current_depth < depth:
                    add_connections(follower, current_depth + 1)

        add_connections(profile, 0)

        plt.figure(figsize=(12, 8))
        nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=8, font_weight='bold')
        plt.title(f"Social Network for {username}")
        plt.savefig(f"{username}_social_network.png")
        plt.close()

    def analyze_hashtag_trends(self, username, post_count=50):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        hashtags = []

        for post in profile.get_posts():
            if len(hashtags) >= post_count:
                break
            hashtags.extend(post.caption_hashtags)

        counter = Counter(hashtags)
        top_hashtags = counter.most_common(10)

        plt.figure(figsize=(10, 6))
        plt.bar([tag for tag, count in top_hashtags], [count for tag, count in top_hashtags])
        plt.title(f"Top Hashtags for {username}")
        plt.xlabel("Hashtags")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{username}_hashtag_trends.png")
        plt.close()

        return top_hashtags

    def predict_optimal_posting_time(self, username, days=30):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        posting_times = []

        for post in profile.get_posts():
            if (datetime.datetime.now() - post.date).days > days:
                break
            posting_times.append(post.date.hour)

        optimal_hour = max(set(posting_times), key=posting_times.count)
        return optimal_hour

    def detect_fake_content(self, username, post_count=10):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        fake_content = []

        for post in profile.get_posts():
            if len(fake_content) >= post_count:
                break
            if post.typename == 'GraphImage':
                L.download_post(post, target=f"{username}_temp")
                image_path = f"{username}_temp/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.jpg"
                if self._is_likely_fake(image_path):
                    fake_content.append(post.shortcode)

        return fake_content

    def _is_likely_fake(self, image_path):
        image = cv2.imread(image_path)
        ela_image = self._ela(image_path, 90)
        threshold = 50
        return np.mean(ela_image) > threshold

    def _ela(self, image_path, quality):
        temp_filename = 'temp_ela.jpg'
        ela_filename = 'temp_ela.png'
        
        image = Image.open(image_path)
        image.save(temp_filename, 'JPEG', quality=quality)
        temp_image = Image.open(temp_filename)
        
        ela_image = ImageChops.difference(image, temp_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        return ela_image

    def analyze_account_growth(self, username, days=30):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        followers = []
        engagement_rates = []
        dates = []

        for post in profile.get_posts():
            if (datetime.datetime.now() - post.date).days > days:
                break
            followers.append(post.owner_profile.followers)
            engagement_rate = (post.likes + post.comments) / post.owner_profile.followers * 100
            engagement_rates.append(engagement_rate)
            dates.append(post.date)

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(dates, followers)
        plt.title(f"Follower Growth for {username}")
        plt.xlabel("Date")
        plt.ylabel("Followers")

        plt.subplot(2, 1, 2)
        plt.plot(dates, engagement_rates)
        plt.title(f"Engagement Rate for {username}")
        plt.xlabel("Date")
        plt.ylabel("Engagement Rate (%)")

        plt.tight_layout()
        plt.savefig(f"{username}_account_growth.png")
        plt.close()

    def extract_exif_data(self, username, post_count=10):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        exif_data = []

        for post in profile.get_posts():
            if len(exif_data) >= post_count:
                break
            if post.typename == 'GraphImage':
                L.download_post(post, target=f"{username}_temp")
                image_path = f"{username}_temp/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.jpg"
                try:
                    exif = piexif.load(image_path)
                    exif_data.append({
                        'shortcode': post.shortcode,
                        'exif': exif
                    })
                except:
                    pass

        return exif_data

    def analyze_locations(self, username, post_count=50):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        locations = []

        for post in profile.get_posts():
            if len(locations) >= post_count:
                break
            if post.location:
                locations.append(post.location)

        map_center = [sum(loc.lat for loc in locations) / len(locations),
                      sum(loc.lng for loc in locations) / len(locations)]
        
        m = folium.Map(location=map_center, zoom_start=10)

        for loc in locations:
            folium.Marker([loc.lat, loc.lng], popup=loc.name).add_to(m)

        m.save(f"{username}_locations.html")

        return locations

    def detect_influencer_collaborations(self, username, post_count=50):
        L = self.module.Instaloader()
        profile = self.module.Profile.from_username(L.context, username)
        collaborations = []

        for post in profile.get_posts():
            if len(collaborations) >= post_count:
                break
            mentioned_users = post.caption_mentions
            if mentioned_users:
                for mentioned_user in mentioned_users:
                    mentioned_profile = self.module.Profile.from_username(L.context, mentioned_user)
                    if mentioned_profile.followers > 10000:  # Arbitrary threshold for influencers
                        collaborations.append({
                            'post': post.shortcode,
                            'collaborator': mentioned_user,
                            'collaborator_followers': mentioned_profile.followers
                        })

        return collaborations

