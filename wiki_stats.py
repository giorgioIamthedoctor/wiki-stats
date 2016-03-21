#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            num,numlinks = f.readline().split()
            (n, _nlinks) = (int(num),int(numlinks)) # TODO: прочитать из файла
            
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            x = f.readline()
            n = 1
            m = 0
            while x:
                self._titles.append(x.replace("\n",""))
                size,flag,n_links = f.readline().split()
                size,flag,n_links = int(size),int(flag),int(n_links)
                self._offset[n] = n_links + self._offset[n-1]
                self._sizes[n-1] = size
                self._redirect[n-1] = flag
                n += 1
                for i in range(n_links):
                    link = f.readline()
                    self._links[m] = int(link)
                    m += 1
                x = f.readline()

            # TODO: прочитать граф из файла

        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        num = self._offset[int(_id) + 1] - self._offset[int(_id)]
        return num

    def get_links_from(self, _id):
        links = self._links[self._offset[int(_id)]:self._offset[int(_id)+1]]
        return(links)

    def get_id(self, title):
        num = self._titles.index(str(title))
        return num

    def get_number_of_pages(self):
        num = len(self._titles)
        return(num)

    def is_redirect(self, _id):
        return self._redirect[int(_id)]== 1

    def get_title(self, _id):
        return self._titles[int(_id)]

    def get_page_size(self, _id):
        return self._sizes[int(_id)]
    def get_number_redirect(self):
        num = 0
        allnums = self.get_number_of_pages()
        for i in range(self.get_number_of_pages()):
            if self.is_redirect(i):
                num += 1
        return num,round(num/allnums*100,2)
    def get_number_min_links(self):
        for i in range(self.get_number_of_pages()):
            if i == 0:
                _min = self.get_number_of_links_from(i)
            else:
                _min = min(_min,self.get_number_of_links_from(i))
        return _min
    def get_number_pages_with_min_links(self):
        minimum = int(self.get_number_min_links())
        num = 0
        for i in range(self.get_number_of_pages()):
            if self.get_number_of_links_from(i) == minimum:
                num += 1
        return num
    def get_number_max_links(self):
        for i in range(self.get_number_of_pages()):
            if i == 0:
                _max = self.get_number_of_links_from(i)
            else:
                _max = max(_max,self.get_number_of_links_from(i))
        return _max
    def get_number_pages_with_max_links(self):
        maximum = int(self.get_number_max_links())
        num = 0
        for i in range(self.get_number_of_pages()):
            if self.get_number_of_links_from(i) == maximum:
                num += 1
                number = i
        title = self.get_title(number)
        return num , title
    def get_mean(self):
        num_links = []
        for i in range(self.get_number_of_pages()):
            if not self.is_redirect(i):
                num_links.append(self.get_number_of_links_from(i))
        return round(statistics.mean(num_links),2),round(statistics.stdev(num_links),2)


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
        a,b = wg.get_number_redirect()
        print("Количество статей с перенаправлением: " + str(a) + " (" + str(b) + "%)")
        print("Минимальное количество ссылок из статьи: " + str(wg.get_number_min_links()))
        print("Количество статей с минимальным количеством ссылок: " + str(wg.get_number_pages_with_min_links()))
        print("Максимальное количество ссылок из статьи: " + str(wg.get_number_max_links()))
        a,b = wg.get_number_pages_with_max_links()
        print("Количество статей с максимальным количеством ссылок: " + str(a))
        print("Статья с наибольшим количеством ссылок: "+str(b))
        a,b = wg.get_mean()
        print("Среднее количество ссылок в статье: "+str(a)+ " (ср. откл."+str(b)+ ")")

    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # TODO: статистика и гистограммы