import pandas as pd
import networkx as nx
from sqlalchemy import create_engine
import configparser
import argparse
import logging

class MediaJournalistGraph:
    def __init__(self, config_file, output_excel, output_gexf):
        self.config_file = config_file
        self.output_excel = output_excel
        self.output_gexf = output_gexf
        self.load_config()
        self.connect_db()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        db_config = config['database']
        self.user = db_config.get('user')
        self.password = db_config.get('password')
        self.host = db_config.get('host')
        self.database = db_config.get('database')

    def connect_db(self):
        db_connection_str = f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
        self.db_connection = create_engine(db_connection_str)

    def fetch_data(self):
        query = """
        SELECT journalist.name AS journalist, media.name AS media
        FROM media
        JOIN journalist_media ON journalist_media.media_id = media.id
        JOIN journalist ON journalist_media.journalist_id = journalist.id
        GROUP BY journalist.name, media.name;
        """
        self.data = pd.read_sql(query, con=self.db_connection)

    def save_data(self):
        self.data.to_excel(self.output_excel)

    def create_graph(self):
        self.graph = nx.from_pandas_edgelist(self.data, source='journalist', target='media')

    def save_graph(self):
        nx.write_gexf(self.graph, self.output_gexf)

    def run(self):
        self.fetch_data()
        self.save_data()
        self.create_graph()
        self.save_graph()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate media-journalist graph")
    parser.add_argument('--config_file', type=str, default='config.ini', help='Path to the configuration file')
    parser.add_argument('--output_excel', type=str, default='medias_journalists_prev.xlsx', help='Path to the output Excel file')
    parser.add_argument('--output_gexf', type=str, default='medias_desinfo_prev.gexf', help='Path to the output GEXF file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    graph_generator = MediaJournalistGraph(args.config_file, args.output_excel, args.output_gexf)
    graph_generator.run()

