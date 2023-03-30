import pandas as pd
import numpy as np
import datetime
import json
import glob
import os


class FakeHealthDataset:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def parse_content_files(self, folder_name):
        folder_path = os.path.join(self.dataset_path, folder_name, "*.json")
        json_files = glob.glob(folder_path)

        json_data = []
        for file_name in json_files:
            with open(file_name) as json_file:
                data = json.load(json_file)
                publish_date = data.get('publish_date')
                if publish_date is not None:
                    publish_date = datetime.datetime.fromtimestamp(publish_date).isoformat()
                    data['publish_date'] = publish_date
                json_data.append(data)

        df = pd.DataFrame(json_data)
        return df

    def parse_engagement_files(self, folder_name, file_name):
        file_path = os.path.join(self.dataset_path, folder_name, file_name)

        json_data = []
        with open(file_path) as json_file:
            data = json.load(json_file)
            for news_id, actions in data.items():
                for action_type, user_ids in actions.items():
                    for user_id in user_ids:
                        json_data.append({
                            'news_id': news_id,
                            'user_id': user_id,
                            'action': action_type
                        })
        df = pd.DataFrame(json_data)
        return df

    def parse_reviews_files(self, folder_name, file_name):
        file_path = os.path.join(self.dataset_path, folder_name, file_name)

        with open(file_path) as json_file:
            data = json.load(json_file)
            filtered_data = [{'news_id': item['news_id'], 'rating': item['rating']} for item in data]
        df = pd.DataFrame(filtered_data)
        return df

    def parse_user_followers_files(self, folder_name):
        json_data = []
        file_path = os.path.join(self.dataset_path, folder_name)
        for filename in os.listdir(file_path):
            if filename.endswith('.json'):
                main_user_id = os.path.splitext(filename)[0]
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                follower_ids = data['ids']
                for follower_id in follower_ids:
                    json_data.append({
                        'main_user_id': int(main_user_id),
                        'follower_id': follower_id
                    })

        df = pd.DataFrame(json_data)
        return df

    def parse_user_following_files(self, folder_name):
        json_data = []
        file_path = os.path.join(self.dataset_path, folder_name)
        for filename in os.listdir(file_path):
            if filename.endswith('.json'):
                main_user_id = os.path.splitext(filename)[0]
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                following_ids = data['ids']
                for follower_id in following_ids:
                    json_data.append({
                        'main_user_id': int(main_user_id),
                        'following_ids': following_ids
                    })

        df = pd.DataFrame(json_data)
        return df

    def parse_dataset(self):
        content_HR = self.parse_content_files("content/HealthRelease")
        content_HS = self.parse_content_files("content/HealthStory")
        engagement_HR = self.parse_engagement_files("engagements", "HealthRelease.json")
        engagement_HS = self.parse_engagement_files("engagements", "HealthStory.json")
        reviews_HR = self.parse_reviews_files("reviews", "HealthRelease.json")
        reviews_HS = self.parse_reviews_files("reviews", "HealthStory.json")
        user_followers = self.parse_user_followers_files("user_network/user_followers")
        user_following = self.parse_user_following_files("user_network/user_following")

        return content_HR, content_HS, engagement_HR, engagement_HS, reviews_HR, reviews_HS, user_followers, user_following


dataset = FakeHealthDataset()
content_HR, content_HS, engagement_HR, engagement_HS, reviews_HS, reviews_HR, user_followers, user_following = dataset.parse_dataset()