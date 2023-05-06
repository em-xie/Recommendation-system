import csv
import os.path

# from api.config import config

# anime_file = open(config['dataset_path']+'/anime.csv')

anime_file = open('E://PyCode/Recommendation-system/dataset/anime.csv', encoding='gb18030', errors='ignore')
reader = csv.DictReader(anime_file)
anime = {row['anime_id']: row for row in reader}


def get_anime(aid):
    aid = str(aid)
    if aid not in anime:
        return None
    return anime[aid]
