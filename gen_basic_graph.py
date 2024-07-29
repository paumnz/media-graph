import argparse
import logging
import networkx as nx
import json

class MediaGraphBuilder:
    def __init__(self, medias_file, journalist_file, output_file):
        self.medias_file = medias_file
        self.journalist_file = journalist_file
        self.output_file = output_file
        self.all_medias = self.load_medias()
        self.data = self.load_journalist_data()
        self.G = nx.Graph()

    def load_medias(self):
        with open(self.medias_file, "r") as file:
            file_content = file.read()
        return file_content.split("\n")

    def load_journalist_data(self):
        with open(self.journalist_file, "r") as file:
            return json.load(file)

    def build_graph(self):
        for media1 in self.all_medias:
            for media2 in self.all_medias:
                for journalist in self.data.keys():
                    journalist_media = self.data[journalist]
                    if media1 in journalist_media and media2 in journalist_media:
                        logging.info(f"New relation {media1} - {media2}")
                        e = (media1, media2)
                        if self.G.has_edge(*e):
                            self.G[media1][media2]['weight'] += 1
                        else:
                            self.G.add_edge(*e, weight=1)

    def save_graph(self):
        nx.write_gexf(self.G, self.output_file)

    def run(self):
        self.build_graph()
        self.save_graph()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build media graph from journalist data")
    parser.add_argument('--medias_file', type=str, default='all_medias.csv', help='Path to the CSV file containing media names')
    parser.add_argument('--journalist_file', type=str, default='journalist_graph.json', help='Path to the JSON file containing journalist data')
    parser.add_argument('--output_file', type=str, default='medias_inter.gexf', help='Path to the output GEXF file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = MediaGraphBuilder(args.medias_file, args.journalist_file, args.output_file)
    builder.run()

