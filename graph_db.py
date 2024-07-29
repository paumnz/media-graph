import pandas as pd
import configparser
from sqlalchemy import create_engine
import mysql.connector
import difflib
import argparse
import logging

class MediaJournalistDatabase:
    def __init__(self, config_file, input_file):
        self.config_file = config_file
        self.input_file = input_file
        self.load_config()
        self.connect_db()
        self.load_data()
    
    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        db_config = config['database']
        self.host = db_config.get('host')
        self.user = db_config.get('user')
        self.password = db_config.get('password')
        self.database = db_config.get('database')

    def connect_db(self):
        self.sql_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.sql_cursor = self.sql_db.cursor(buffered=True)
    
    def load_data(self):
        self.accs = pd.read_excel(self.input_file, index_col=0)
    
    def fetch_existing_data(self):
        self.sql_cursor.execute("SELECT DISTINCT(media.name) FROM media")
        self.all_medias_list = [media[0].lower() for media in self.sql_cursor.fetchall()]

        self.sql_cursor.execute("SELECT DISTINCT(journalist.name) FROM journalist")
        self.all_journalists_list = [journalist[0].lower().strip() for journalist in self.sql_cursor.fetchall()]

    def find_media(self, name):
        self.sql_cursor.execute("SELECT media.id FROM media WHERE media.name=%s", (name,))
        res = self.sql_cursor.fetchone()
        return res[0] if res else False

    def find_journalist(self, name):
        self.sql_cursor.execute("SELECT journalist.id FROM journalist WHERE journalist.name=%s", (name,))
        res = self.sql_cursor.fetchone()
        return res[0] if res else False

    def insert_journalist(self, name):
        self.sql_cursor.execute("INSERT INTO journalist(name) VALUES (%s)", (name,))
        self.sql_db.commit()
        return self.sql_cursor.lastrowid

    def insert_media(self, name):
        self.sql_cursor.execute("INSERT INTO media(name) VALUES (%s)", (name,))
        self.sql_db.commit()
        return self.sql_cursor.lastrowid

    def insert_media_journalist(self, media_id, journalist_id):
        try:
            self.sql_cursor.execute(
                "INSERT INTO journalist_media(journalist_id, media_id) VALUES (%s, %s)",
                (journalist_id, media_id)
            )
            self.sql_db.commit()
            return True
        except Exception as e:
            logging.error(f"Error creating relation: {str(e)}")
            return False

    def process_data(self):
        for row in self.accs.iterrows():
            try:
                author = (row[0].lower()).strip()
                author_identified = difflib.get_close_matches(author, self.all_journalists_list)
                match_ratio = difflib.SequenceMatcher(None, author_identified[0], author).ratio() if author_identified else 0

                if author_identified and match_ratio > 0.85:
                    author_id = self.find_journalist(author_identified[0])
                else:
                    author_id = self.insert_journalist(author)

                media_list = row[1][1].lower().replace("/", ",").replace(" ", "").replace("\n", "").split(",")
                for media in media_list:
                    media_identified = difflib.get_close_matches(media, self.all_medias_list)
                    if media_identified:
                        media_id = self.find_media(media_identified[0])
                        self.insert_media_journalist(media_id, author_id)
                    elif media.strip():
                        media_id = self.insert_media(media)
                        self.insert_media_journalist(media_id, author_id)
            except Exception as e:
                logging.error(f"Error processing row: {str(e)}")

    def run(self):
        self.fetch_existing_data()
        self.process_data()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process media and journalist data")
    parser.add_argument('--config_file', type=str, default='config.ini', help='Path to the configuration file')
    parser.add_argument('--input_file', type=str, default='detoxorig.ods', help='Path to the input ODS file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    db_processor = MediaJournalistDatabase(args.config_file, args.input_file)
    db_processor.run()

