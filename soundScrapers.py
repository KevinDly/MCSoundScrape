from bs4 import BeautifulSoup
import requests, re, os

def buildSoundData(header, td, mobName, dir = ''):
    data = {}
    sounds = td.find_all("span", class_="sound")
    for sound in sounds:
        source = sound.find("audio").get("src")
        r = requests.get(source, allow_redirects = True)
        regex = re.compile(".*\.ogg")
        #Download sounds
        #TODO: 
        linkSplit = source.rsplit('/')
        name = list(filter(regex.match, linkSplit))[0]
        data[header] = name
        
        if dir != None:
            directory = dir + mobName
            if not os.path.isdir(directory):
                os.mkdir(directory)
            filepath = directory + '/' + name
            open(filepath, 'wb').write(r.content)
            data[header] = filepath
    return data
    
def buildTextData(header, td, dir = ''):
    data = {}
    data[header] = td.text
    return data
    
def packageData(header, td, mobName, dir = ''):
    if(header == "Sound"):
        return buildSoundData(header, td, mobName, dir = dir)
    else:
        return buildTextData(header, td, dir = dir)
        

def scrapeSound(URL, dir = ''):
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table", class_="wikitable")
    soundTables = []
    
    linkSplit = page.url.split('/')
    mobName = linkSplit[len(linkSplit) - 1]
    
    ##Find all the sound tables on the page
    #Grab all the tables
    for table in tables:
        #Check the first row of the table
        trs = table.find_all("tr")
        #Check the first head of the row
        ths = trs[0].find_all("th")
        
        #If the head has sound, it's a sound table.
        
        if "Sound" in ths[0].contents:
            soundTables.append(table);
            
            
    #Grab the data
    for table in soundTables:
        trs = table.find_all("tr")
        headers = []
        for header in trs[0]:
            headers.append(header.text)
        del trs[0]
        
        dicts = []
        for tr in trs:
            tds = tr.find_all("td")
            #Grab the sounds and download them
            
            for num in range(len(tds)):
                header = headers[num]
                td = tds[num]
                dicts.append(packageData(header, td, mobName, dir = dir))
                
        print(dicts)
