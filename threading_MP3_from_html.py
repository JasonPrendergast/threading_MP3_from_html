import speech_recognition as sr
import queue as Queue
import threading, time, random
from gtts import gTTS
import os
from lxml import html
import requests
import re
#
#Threading tts google api returning a lower case string
#output = qTextinput
#
class Listening:
    def __init__(self,sr,r):
        self.sr=sr
        self.r=r
        self.nextTime=0


    def run(self):
        while (exitflag==0):
            if(self.nextTime<time.clock()):
                with self.sr.Microphone() as source:
                    print('Listening')
                    audio = self.r.listen(source)
                try:
                    current_action =' '+ r.recognize_google(audio)
                    qTextinput.put(current_action)
                    self.nextTime+=(random.random())/10
               
                
                except:
                    with print_lock:
                       print('fail_listen')
                    self.nextTime+=(random.random())/10
                    pass

#
#class split string use first words to discard or create action
#Looking for keywords as first word this can be list can be changed to
#add more commands:
# OS = computer
#Wiki = who and what
#google = search
#
class qtextinput_Consumer:
    def __init__(self):
        self.nextTime=0

        
    def __del__(self):
        print('deleted')
        
    def run(self):
        while (exitflag==0):
            #print('in exitflag')

            if(self.nextTime<time.clock() and not qTextinput.empty()):
                try:
                    
                    temp = str(qTextinput.get()).split()
                    #with print_lock:
                       # print(str(temp))
 
                    if temp[0]=='make':
                        if temp[1]=='youtube':
                            qGetHTML.put(temp)
                            self.nextTime+=(random.random())/10
                except:
                    with print_lock:
                        print('fail qtextinput_Consumer')
                    self.nextTime+=(random.random())/10
                    pass
#
#class qGetHTML_Consumer output = title text and main text
#

class qGetHTML_Consumer:
    def __init__(self):
        self.nextTime=0
        self.incomingarray=[]
        self.page = ''
        #self.tree=html.fromstring()

        
    def __del__(self):
        print('deleted')
        
    def run(self):
        while (exitflag==0):
            #print('in exitflag')

            if(self.nextTime<time.clock() and not qGetHTML.empty()):
                try:
                    self.incomingarray=qGetHTML.get()
                    self.page = requests.get(self.incomingarray[2])
                    tree = html.fromstring(self.page.content)
                    title=tree.xpath('//h1[@class="pub-c-title__text pub-c-title__text--long"]/text()')
                    content=tree.xpath('//div[@class="govspeak"]/blockquote/p/text()')
                    if len(content) == 0:
                        content=tree.xpath('//div[@class="govspeak"]/p/text()')

                    
                    with print_lock:
                       # print(self.localtextarray[0])
                        #print(self.localtextarray[1])
                        #print(self.incomingarray[2])
                        #print(content)
                        print('qGetHTML')
                       # print(str())
                    qClean_content_for_tts.put(content)
                    qClean_title_for_tts.put(title)
                    self.nextTime+=(random.random())*10/1
                    
                except:
                    with print_lock:
                        print('fail qGetHTML _Consumer')
                    self.nextTime+=(random.random())*10/1
                    pass


class qClean_content_for_tts_Consumer:
    def __init__(self):
        self.nextTime=0
        self.content=''
        self.title=''
        self.temp=''

        
    def __del__(self):
        with print_lock:
            print('deleted')
        
    def run(self):
        while (exitflag==0):
            
            if(self.nextTime<time.clock() and not qClean_content_for_tts.empty() and not qClean_title_for_tts.empty()):
                try:
                    self.content = qClean_content_for_tts.get()
                    self.title=qClean_title_for_tts.get()
                    #re clean content
                    self.content = re.sub(r'\\n','',str(self.content))
                    self.content = re.sub(r'\', \'','',str(self.content))
                    self.content = re.sub(r'\\','',str(self.content))
                    for sent in self.content:
                        self.temp += str(sent)
                    self.content = self.temp

                    #re clean title
                    self.title = re.sub(r'\\n','',str(self.title))
                    self.title = re.sub(r'\\','',str(self.title))
                    self.title=self.title.split()
                    self.title= str(self.title)

                    with print_lock:
                        #print(self.content)
                        print('qClean_content_for_tts')
                        
                    qCreateaudio_from_text.put([self.content,self.title])
                    
                    self.nextTime+=(random.random())/10
                    
                except:
                    with print_lock:
                        print('fail qClean_content_for_tts _Consumer')
                        self.nextTime+=(random.random())/10
                    pass



#use tts to create audio
#inpur =  main text qCreateaudio_from_text
#output = audio'+str(self.title)+'.mp3
#
class qCreateaudio_from_text_Consumer:
    def __init__(self):
        self.nextTime=0
        self.incomingarray=[]
        self.title=''
        self.content=''
        

        
    def __del__(self):
        with print_lock:
            print('deleted')
        
    def run(self):
        while (exitflag==0):
            
            if(self.nextTime<time.clock() and not qCreateaudio_from_text.empty()):
                try:
                    self.incomingarray = qCreateaudio_from_text.get()
                    self.content=self.incomingarray[0]
                    self.title=str(self.incomingarray[1])
                    tts = gTTS(text=str(self.content), lang="en-uk")
                    for ch in [',','-',')','(','/','\\','[',']','{','}','&','#','\'','"','1','2','3','4','5','6','7','8','9','0','',')','(','*','&','^','%','$','£','@','"','!','?','.','=','+','_','']:
                        if ch in self.title:
                            self.title=self.title.replace(ch,"")

                    tts.save('audio'+str(self.title)+'.mp3')
                   # os.system('mpg321 audio'+self.title+'.mp3')
                    
                    

                    with print_lock:
                        print('qCreateaudio_from_text')
                        #print(str())
                    self.nextTime+=(random.random())/10
                    #qTTSaudio.put(tts)
                    
                except:
                    with print_lock:
                        print('fail qCreateaudio_from_text _Consumer')
                    self.nextTime+=(random.random())/10
                    pass

if __name__ == "__main__":
    global exitflag
    exitflag=0
    testing=1
    r = sr.Recognizer()
    print_lock = threading.Lock()
    #
    #Creating queues
    #
    qTextinput=Queue.Queue(20)
    qGetHTML=Queue.Queue(20)
    qClean_content_for_tts=Queue.Queue(20)
    qClean_title_for_tts=Queue.Queue(20)
    qCreateaudio_from_text=Queue.Queue(20)
    qTTSaudio=Queue.Queue(20)
    
    if testing ==1:
        #qTextinput.put('make youtube https://www.gov.uk/government/speeches/annual-human-rights-day-reception-2017-lord-ahmads-speech')
        qTextinput.put('make youtube https://www.gov.uk/government/news/mark-field-statement-at-un-security-council-north-korea-meeting')

    #
    #Threading tts google api returning a lower case string
    #Input WORLD DATA in the form of sound from the microphone
    #output = qTextinput
    #
    p=Listening(sr,r)
    pt=threading.Thread(target=p.run,args=())
    pt.start()

    #
    #Threading split string use first words to discard or create action
    #Looking for keywords as first word this can be list can be changed to
    #add more commands:
    # OS = computer
    #Wiki = who and what
    #google = search
    #make youtube vidio output = string array qGetHTML
    #
    #input = string qTextinput
    #output = string array in related action queue
    #
    qtextinput_c=qtextinput_Consumer()
    qtextinput_ct=threading.Thread(target=qtextinput_c.run,args=())
    qtextinput_ct.start()

    #
    #Scape that html
    #
    #input = string array with element 2 as url qGetHTML
    #output = content html qClean_content_for_tts 
    #planned output = title as well
    #
    qGetHTML_c=qGetHTML_Consumer()
    qGetHTML_ct=threading.Thread(target=qGetHTML_c.run,args=())
    qGetHTML_ct.start()

    #
    #Scrub content to text format I want
    #inpur = HTML from qClean_content_for_tts
    #output = main text qCreateaudio_from_text
    #
    qClean_content_for_tts_c=qClean_content_for_tts_Consumer()
    qClean_content_for_tts_ct=threading.Thread(target=qClean_content_for_tts_c.run,args=())
    qClean_content_for_tts_ct.start()
    
    #use tts to create audio
    #inpur =  main text qCreateaudio_from_text
    #output = qTTSaudio
    #
    qCreateaudio_from_text_c=qCreateaudio_from_text_Consumer()
    qCreateaudio_from_text_ct=threading.Thread(target=qCreateaudio_from_text_c.run,args=())
    qCreateaudio_from_text_ct.start()
    
    while (exitflag==0):
        time.sleep(10)
        
    print('ending')
    
    
