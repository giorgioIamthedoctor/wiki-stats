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
    def num_min_link_on_state(self):
        mas,_min = wg.link_on_state("num_max","min")
        return int(mas.count(_min))
    def link_on_state(self,f,ff):
        num_links_on = [0] * self.get_number_of_pages()
        num_link = []
        num_redirects = [0] * self.get_number_of_pages()
        num_red = []
        for i in range(self.get_number_of_pages()):
            if not self.is_redirect(i):
                mas = self.get_links_from(i)
                for x in mas:
                    if num_links_on[x] != None:
                        num_links_on[x] += 1
            else:
                point = self.get_links_from(i)
                num_redirects[point[0]] += 1
                num_redirects[i] = None
                num_links_on[i] = None
        num_links_on_max = []
        num_links_on_min = []
        num_redirects_max = []
        num_redirects_min = []
        for x in num_redirects:
            if x != None:
                num_redirects_max.append(x)
                num_redirects_min.append(x)
            else:
                num_redirects_max.append(float("-inf"))
                num_redirects_min.append(float("+inf"))
        for x in num_links_on:
            if x != None:
                num_links_on_max.append(x)
                num_links_on_min.append(x)
            else:
                num_links_on_max.append(float("-inf"))
                num_links_on_min.append(float("+inf"))
        number = num_links_on.index(max(num_links_on_max))
        number_r = num_redirects.index(max(num_redirects_max))
        if f == "max":
            if ff == "max":
                return int(max(num_links_on_max))
            else:
                return int(min(num_links_on_min))
        elif f == "num_max":
            if ff == "max":
                return num_links_on,int(max(num_links_on_max))
            else:
                return num_links_on,int(min(num_links_on_min))
        elif f == "number":
            return self.get_title(number)
        elif f == "num_r":
            if ff == "max":
                return int(max(num_redirects_max))
            else:
                return int(min(num_redirects_min))
        elif f == "number_r":
            if ff == "max":
                return num_redirects,int(max(num_redirects_max))
            else:
                return num_redirects,int(min(num_redirects_min))
        elif f == "sred":
            num_link[:] = num_links_on[:]
            while num_link.count(None) > 0:
                num_link.remove(None)
            return round(statistics.mean(num_link),2),round(statistics.stdev(num_link),2)
        elif f == "number_r_":
            return self.get_title(number_r)
        elif f == "sred_r":
            num_red[:] = num_redirects[:]
            while num_red.count(None) > 0:
                num_red.remove(None)
            return round(statistics.mean(num_red),2),round(statistics.stdev(num_red),2)
    def num_max_link_on_state(self):
        mas,_max = wg.link_on_state("num_max","max")
        return int(mas.count(_max))
    def num_max_redirect_on_state(self):
        mas,_max = wg.link_on_state("number_r","max")
        return int(mas.count(_max))
    def num_min_redirect_on_state(self):
        mas,_min = wg.link_on_state("number_r","min")
        return int(mas.count(_min)+mas.count(None))

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
        print("Минимальное количество ссылок на статью: ",wg.link_on_state("max","min"))
        print("Количество статей с минимальным количеством внешних ссылок: ",wg.num_min_link_on_state())
        print("Максимальное количество ссылок на статью: ",wg.link_on_state("max","max"))
        print("Количество статей с максимальным количеством внешних ссылок: ",wg.num_max_link_on_state())
        print("Статья с наибольшим количеством внешних ссылок: ",wg.link_on_state("number","max"))
        a,b = wg.link_on_state("sred","")
        print("Среднее количество внешних ссылок на статью: ",a,"(ср. откл.",b,")")
        print("Минимальное количество перенаправлений на статью: ",wg.link_on_state("num_r","min"))
        print("Количество статей с минимальным количеством внешних перенаправлений: ",wg.num_min_redirect_on_state())
        print("Максимальное количество перенаправлений на статью: ",wg.link_on_state("num_r","max"))
        print("Количество статей с максимальным количеством внешних перенаправлений: ",wg.num_max_redirect_on_state())
        print("Статья с наибольшим количеством внешних перенаправлений: ",wg.link_on_state("number_r_",""))
        a,b = wg.link_on_state("sred_r","")
        print("Среднее количество внешних перенаправлений на статью: ",a,"(ср. откл. ",b,")")
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # TODO: статистика и гистограммы