'''
Author: Meet Shah(a.k.a slim_shah)
'''

import os
import json
import pickle
import networkx as nx
import matplotlib.pyplot as plt

class ParseDump:
    def __init__(self):
        cwd = os.getcwd()
        self.Graph = {}
        self.meta = {}
        self.BasePath = os.path.join(cwd, 'DATA')
        if not os.path.isdir(os.path.join(cwd, 'DATA')):
            os.makedirs(os.path.join(cwd, 'DATA'))

    def Read_File(self, Path_to_file):
        listOfLines = open(Path_to_file, 'r', encoding='UTF-8').read().split('Recno::')
        for line in listOfLines[1:]:
            L = line.split('\n')
            docid = int(L[0].strip())
            self.Graph[docid] = {'Outlinks': [], 'OutlinkNo': ''}
            self.meta[docid] = {'URL': '',  'Title': '',  "recno": docid, 'pagerank': 0.01}
            for i in L[1:]:
                j = i.strip(' ')
                if 'URL::' in j:
                    temp = j.replace('URL::', '')
                    temp = temp.strip()
                    self.meta[docid]['URL'] = temp

                if 'Title:' in j:
                    temp = j.replace('Title:', '')
                    temp = temp.strip()
                    self.meta[docid]['Title'] = temp

                if 'Title:' in j:
                    temp = j.replace('Title:', '')
                    temp = temp.strip()
                    self.meta[docid]['Title'] = temp

                if 'Outlinks:' in j:
                    temp = j.replace('Outlinks:', '')
                    temp = temp.strip()
                    self.Graph[docid]['OutlinkNo'] = temp

                if 'outlink: toUrl:' in j:
                    start = j.index('outlink: toUrl:') + len('outlink: toUrl:')
                    end = j.index('anchor:')
                    temp = j[start:end]
                    temp = temp.strip(' ')
                    self.Graph[docid]['Outlinks'].append(temp)
            #End inner loop
            start = line.index('ParseText::') + len('ParseText::')
            line = line[start:]
            end = len(line)
            try:
                end = line.index('ParseData::')
            except:
                pass
            text_data = line[:end]
            with open(os.path.join(self.BasePath, str(docid) + '.txt'), 'w+', encoding='UTF-8') as F:
                F.write(text_data)
        #End For Main loop


    def Compute_Page_Rank(self):
        Graph = nx.from_dict_of_lists(self.Graph)
        self.page_rank = nx.pagerank(Graph, alpha=0.9)
        nx.draw(Graph, with_labels=True, font_weight='bold')
        plt.savefig("Graph.png")

    def Save_Data(self):
        L = []
        K = list(self.Graph.keys())
        K.sort()
        for i in K:
            self.meta[i]['pagerank'] = round(self.page_rank[i],6)
            L.append(self.meta[i])

        with open('meta_dump.json', 'w') as fp:
            json.dump(L, fp, indent=4, sort_keys=True)

        with open('Graph.pkl', 'wb') as output:
            pickle.dump(self.Graph, output, pickle.HIGHEST_PROTOCOL)