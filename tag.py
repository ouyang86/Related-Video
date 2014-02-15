import urllib2
import os, json, re
from bs4 import BeautifulSoup

wikisource = 'http://en.wikipedia.org'
allStopWords={'about':1, 'above':1, 'after':1, 'again':1, 'against':1, 'all':1, 'am':1, 'an':1, 'and':1, 'any':1, 'are':1, 'arent':1, 'as':1, 'at':1, 'be':1, 'because':1, 'been':1, 'before':1, 'being':1, 'below':1, 'between':1, 'both':1, 'but':1, 'by':1, 'cant':1, 'cannot':1, 'could':1, 'couldnt':1, 'did':1, 'didnt':1, 'do':1, 'does':1, 'doesnt':1, 'doing':1, 'dont':1, 'down':1, 'during':1, 'each':1, 'few':1, 'for':1, 'from':1, 'further':1, 'had':1, 'hadnt':1, 'has':1, 'hasnt':1, 'have':1, 'havent':1, 'having':1, 'he':1, 'hed':1, 'hell':1, 'hes':1, 'her':1, 'here':1, 'heres':1, 'hers':1, 'herself':1, 'him':1, 'himself':1, 'his':1, 'how':1, 'hows':1, 'i':1, 'id':1, 'ill':1, 'im':1, 'ive':1, 'if':1, 'in':1, 'into':1, 'is':1, 'isnt':1, 'it':1, 'its':1, 'its':1, 'itself':1, 'lets':1, 'me':1, 'more':1, 'most':1, 'mustnt':1, 'my':1, 'myself':1, 'no':1, 'nor':1, 'not':1, 'of':1, 'off':1, 'on':1, 'once':1, 'only':1, 'or':1, 'other':1, 'ought':1, 'our':1, 'ours ':1, 'ourselves':1, 'out':1, 'over':1, 'own':1, 'same':1, 'shant':1, 'she':1, 'shed':1, 'shell':1, 'shes':1, 'should':1, 'shouldnt':1, 'so':1, 'some':1, 'such':1, 'than':1, 'that':1, 'thats':1, 'the':1, 'their':1, 'theirs':1, 'them':1, 'themselves':1, 'then':1, 'there':1, 'theres':1, 'these':1, 'they':1, 'theyd':1, 'theyll':1, 'theyre':1, 'theyve':1, 'this':1, 'those':1, 'through':1, 'to':1, 'too':1, 'under':1, 'until':1, 'up':1, 'very':1, 'was':1, 'wasnt':1, 'we':1, 'wed':1, 'well':1, 'were':1, 'weve':1, 'were':1, 'werent':1, 'what':1, 'whats':1, 'when':1, 'whens':1, 'where':1, 'wheres':1, 'which':1, 'while':1, 'who':1, 'whos':1, 'whom':1, 'why':1, 'whys':1, 'with':1, 'wont':1, 'would':1, 'wouldnt':1, 'you':1, 'youd':1, 'youll':1, 'youre':1, 'youve':1, 'your':1, 'yours':1, 'yourself':1, 'yourselves':1}
deParan = re.compile(r'\(.+\)')                     #remove paranthesis from the name
deThe = re.compile(r'^[ ]*[Tt]he[ ]+')              #remove 'the' in front of a name
deA = re.compile(r'^[ ]*[Aa][n]?[ ]+')              #remove 'a' in front of a name
deShow = re.compile(r'[ ]+[Ss]how[ ]*$')            #remove 'show' from end of a name

workdir = raw_input('Type the directory for your input and output dataset:\n')
os.chdir(workdir)

#Scrapping American actors name from wikipedia

def fetchactor(gender, cat, limit = None):
    if gender.lower() == 'male':
        rest = 'male_'+cat.lower()+'_actors'
    else: rest = str(cat).lower()+'_actresses'
    pagestart = urllib2.urlopen(wikisource+'/w/index.php?title=Category:American_'+rest+'&from=A')
                                                             
    pagestart = pagestart.read()
    soup = BeautifulSoup(pagestart)
    actor = []
    i = 0
    if limit == None: lim = float('inf')
    else: lim = limit

    while i < lim:
        div = soup.find('div', id = 'mw-pages')
        for namelist in div.find_all('ul'):
            for name in namelist.find_all('a'):
                if name != []: actor.append(name.contents[0])
        nextpage = div.find('a',text = 'next 200')
        if nextpage != None:
            filmnext = urllib2.urlopen(wikisource+nextpage['href'])
            filmnext = filmnext.read()
            soup = BeautifulSoup(filmnext)
        else: break
        i += 200
    return actor
    


#Scrapping American films name after 1900

def fetchfilm(start, until):
    time = range(start, until)
    film = []

    for year in time:
        page = urllib2.urlopen(wikisource+'/wiki/List_of_American_films_of_'+str(year))
        page = page.read()
        soup = BeautifulSoup(page)
        for table in soup.find_all('table', class_ = 'wikitable')+soup.find_all('table', class_ = 'wikitable-sortable'):
            for tr in table.find_all('tr'):
                a = tr.find('a')
                if a != None: film.append(a.contents[0])
    return film

#Scrapping American television Series name

def fetchtvbydecade(decade, limit = None):
    tvshow = []
    page = urllib2.urlopen(wikisource+'/wiki/Category:'+str(decade)+'s_American_television_series')
    page = page.read()
    soup = BeautifulSoup(page)
    if limit == None: lim = float('inf')
    else: lim = limit
    i = 0

    while i < lim:
        div = soup.find('div', id = 'mw-pages')
        for tvlist in div.find_all('ul'):
            for tv in tvlist.find_all('a'):
                tvshow.append(tv.contents[0])
        nextpage = div.find('a', text = 'next 200')
        if nextpage != None:
            nextpage = urllib2.urlopen(wikisource+nextpage['href'])
            nextpage = nextpage.read()
            soup = BeautifulSoup(nextpage)
        else: break
        i+=200
    return tvshow

def fetchtv(start, end, limit = None):
    i = 10 * start // 10
    last = 10 * end // 10
    out = []
    while i <= last:
        out+=fetchtvbydecade(i, limit)
        i += 10    
    tvshow = urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_American_television_series')    #another source of American television series data source
    tvshow = tvshow.read()
    soup = BeautifulSoup(tvshow)
    cantv = []
    for item in soup.find_all('i'):
        temp = item.find('a')
        if temp != None:
            cantv.append(temp.contents[0])
    out+=cantv
    return out


#simplify candidate film/TV Show name
def simName(name):
    refine = deParan.sub(u'', name)
    if len(re.findall('[\w\d\']+', refine)) > 2: refine = deThe.sub(u'', refine)
    refine = refine.strip()
    return refine

#film/TV show name initial detection
def checkName(name, reference):
    if name not in reference: return False
    for item in re.findall('[\w\d\'/]+', name):                                     #Make sure that the candidate name is a anagram in the reference
        if item not in re.findall('[\w\d\'/]+', reference): return False
    return True
    

# class describing youtube video information                
class video:
    def __init__(self, title = None, content = None, cat = None):
        self.title = title
        self.content = content
        self.cat = set(cat)
        self.tag = {'actor':set(), 'movie':set(), 'tv':set()}
        self.close = []

    def tagActor(self, actor):                       #assign actor name tags
        for i in actor:
            i = deParan.sub(u'', i)                  #remove paranthesis
            i = i.strip()
            if len(i.split()) <= 1: continue         #remove single word name
            t = i in self.title                      #search video title
            c = i in self.content                    #search video description
            if t or c :                              #detecting actor name from text content
                self.tag['actor'].add(i)

    def tagFilm(self, film):                                                          #assign film tags
        for name in film:
            if hasattr(name, 'contents'):
                name = name.contents[0]
            refine = simName(name)
            if len(refine) <= 1 or refine.lower() in allStopWords:                    #remove single word film name that is a stop word
                continue
            if len(refine.split()) == 1 and re.search('[\d]+',refine ) != None:       #remove single word film name that is a number
                continue
            t = checkName(refine, self.title)                                         #search video title
            c = checkName(refine, self.content)                                       #search video description
            if t or c :
                if len(self.tag['movie']) == 0:
                    self.tag['movie'].add(name)
                    continue
                clean = set()
                include = False
                for item in self.tag['movie']:                                        #detecting the longest/maximal matching film name from text content
                    if simName(item) in name:
                        clean.add(item)
                    else:
                        if refine in item:
                            include = True
                for rem in clean:
                    self.tag['movie'].remove(rem)                                  #remove inappropriate Movie tags
                if include == False: self.tag['movie'].add(name)                   #assign Movie tags to video

    def tagTV(self, tv):                                                           #assign tvshow tags
        for name in tv:
            if hasattr(name, 'contents'):
                name = name.contents[0]
            refine = simName(name)
            if len(refine) <= 1 or refine.lower() in allStopWords:                 #remove single word tv show name that is a stop word
                continue
            t = checkName(refine, self.title)                                      #search video title
            c = checkName(refine, self.content)                                    #search video description
            if t or c :
                if len(self.tag['tv']) == 0:
                    self.tag['tv'].add(name)                                    #assign TV show tags to video
                    continue
                clean = set()
                include = False
                for item in self.tag['tv']:                                        #detecting the longest/maximal matching tv show name from text content
                    if simName(item) in name:                                      
                        clean.add(item)
                    else:
                        if refine in item:
                            include = True
                for rem in clean:
                    self.tag['tv'].remove(rem)                                   #remove inappropriate TV show tags
                if include == False: self.tag['tv'].add(name)                    #assign TV show tags to video

    def similarVideo(self, videoset,n):
        self.close = []
        for compare in videoset:
            if self == compare: continue
            sim1 = len(self.tag['actor'].intersection(compare.tag['actor']))                            #count of common actor tags
            sim2 = len(self.tag['movie'].intersection(compare.tag['movie']))                            #count of common movie tags
            sim3 = len(self.tag['tv'].intersection(compare.tag['tv']))                                  #count of common tv show tags
            sim4 = len(self.cat.intersection(compare.cat))/float(len(self.cat.union(compare.cat)))      #Jaccard Similarity of video category
            sim = sim1 + sim2 + sim3 + sim4                                                             #compute total relation strength measurement of each pair of video
            if len(self.close) < n:
                self.close.append((compare, sim))
                self.close.sort(key = lambda x : x[1], reverse = True)
            else:
                if sim > self.close[-1][1]:                                                             #record the top 3 related videos by total relation strength measurement
                    self.close.pop()
                    self.close.append((compare,sim))                                                
                    self.close.sort(key = lambda x : x[1], reverse = True)


                
#read in json youtube videos information data           
def readVideo(directory):
    with open(directory) as readin:
        jsondata = json.load(readin)
    return jsondata


#adding actor, movie, and tv show tags to each of the 474 youtube videos
def addTag(indata,filmactor, tvactor, filmactress, tvactress, film, tv):
    videoset = []
    tagvideo = open('tag.csv', 'a')
    tagvideo.write('Actor,Movie,TV Show\n')
    for item in indata:
        record = video(item['title'], item['description'], item['categories'])
        record.tagActor(filmactor)                                                     #assign film actor tag
        record.tagActor(tvactor)                                                       #assign tv actor tag
        record.tagActor(filmactress)                                                   #assign film actress tag
        record.tagActor(tvactress)                                                     #assign tv actress tag
        record.tagFilm(film)                                                           #assign film tag
        record.tagTV(tv)                                                               #assign tv show tag
        videoset.append(record)                                                         
        for actor in record.tag['actor']:
            tagvideo.write(actor.encode('utf-8')+'::')
        tagvideo.write(',')
        for movie in record.tag['movie']:
            tagvideo.write(movie.encode('utf-8')+'::')
        tagvideo.write(',')
        for tvshow in record.tag['tv']:
            tagvideo.write(tvshow.encode('utf-8')+'::')
        tagvideo.write('\n')
    tagvideo.close()    
    return videoset


#find top 3 related video for each of the 474 youtube videos
def relate(videoset):
    out = open('output.txt', 'a')
    i = 1
    for item in videoset:                    #write a file to summerize the results
        item.similarVideo(videoset,3)
        out.write('Video '+str(i)+'. '+item.title.encode('utf-8')+':\n')
        out.write('1st.'+item.close[0][0].title.encode('utf-8')+'\n')
        out.write('2nd.'+item.close[1][0].title.encode('utf-8')+'\n')
        out.write('3rd.'+item.close[2][0].title.encode('utf-8')+'\n\n')
        i+= 1
    out.close()


def main():
    
    print 'Building up film actor vocabulary...'
    filmactor = fetchactor('male', 'film')                   #Build up film actor vocabulary from wikipedia
    print 'Film actor vocabulary built'
    print 'Building up TV actor vocabulary...'
    tvactor = fetchactor('male', 'television')              #build up tv show actor vocabulary from wikipedia
    print 'TV actor vocabulary build'
    print 'Building up film actress vocabulary...'
    filmactress = fetchactor('female', 'film')               #build up film actress vocabulary from wikipedia
    print 'Film actress vocabulary built'
    print 'Building up TV actress vocabulary...'
    tvactress = fetchactor('female', 'television')           #build up tv show actress vocabulary from wikipedia
    print 'TV actress vocabulary built'
    print 'Building up movie vocabulary...'
    film = fetchfilm(1980, 2015)                             #build up movie vocabulary from wikipedia
    print 'Movie vocabulary built'
    print 'Building up TV vocabulary...'
    tv = fetchtv(1980, 2010)                                #build up tv show vocabulary from wikipedia
    print 'TV vocabulary built'

    jsondata = readVideo('CodeAssignmentDataSet.json')           #read input data
    print 'Input Video Data read'
    print 'Assigning tags to input Video...'
    videoset = addTag(jsondata,filmactor, tvactor, filmactress, tvactress, film, tv)           #assign tags to each video and write results to tag.csv
    print 'Actor, Movie, TV show tags are assigned to each Video'
    relate(videoset)                                                                    #found top 3 related video and write results to output.txt
    print 'Related Video Outputed!'

if __name__ == '__main__':
    main() 
