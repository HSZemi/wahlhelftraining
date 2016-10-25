#! /usr/bin/env python3

import random
import json

class Studienfach:
	def __init__(self, abschluss, fach, fsem):
		self.abschluss = abschluss
		self.fach = fach
		self.fsem = fsem
	
	def __str__(self):
		return "{}	{}	{}".format(self.abschluss, self.fach, self.fsem)

class Stud:
	def __init__(self, vorname, nachname, geburtsdatum, strasse, plzort, weiblich, matrikelnummer, studienfaecher, sternchen, fakultaet, mehrfachausfertigung, beurlaubt):
		self.vorname = vorname
		self.nachname = nachname
		self.geburtsdatum = geburtsdatum
		self.matrikelnummer = matrikelnummer
		self.strasse = strasse
		self.plzort = plzort
		self.weiblich = weiblich
		self.studienfaecher = studienfaecher
		self.sternchen = min(len(self.studienfaecher), sternchen)
		self.fakultaet = fakultaet
		self.mehrfachausfertigung = mehrfachausfertigung
		self.beurlaubt = beurlaubt
		
class Ausweis:
	def __init__(self, stud, semester, nummer, loecher, ausfertigung):
		self.stud = stud
		self.semester = semester
		self.nummer = nummer
		self.loecher = loecher
		self.ausfertigung = ausfertigung
	
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	
	def __str__(self):
		s = """{stud.weiblich}   AUSWEIS
{semester}			[{ausfertigung}]
{stud.vorname} {stud.nachname}
{stud.geburtsdatum}		{stud.matrikelnummer}
{stud.strasse}
{stud.plzort}

			{nummer}

--------

""".format(stud = self.stud, semester= self.semester, loecher = self.loecher, nummer = self.nummer, ausfertigung = ausfertigung)
		t = ""
		for i in range(len(self.stud.studienfaecher)):
			t += str(self.stud.studienfaecher[i])
			if(i == self.stud.sternchen):
				t += "*"
			t += "\n"
		
		u = """
[{stud.fakultaet} {loecher[0]}] [{loecher[1]}]

++++++++++

""".format(stud = self.stud, semester= self.semester, loecher = self.loecher, nummer = self.nummer)
		return (s+t+u)


def randomvalue(inputdict):
	choicelist = []
	for key in inputdict:
		for i in range(inputdict[key]):
			choicelist.append(key)
	return random.choice(choicelist)

def randmatnr():
	selector = random.randrange(10)
	if selector > 8:
		return random.randint(11111,19999)
	
	if selector > 7:
		return random.randint(111111,199999)
	
	return random.randint(1900000,2999999)

def randgebdat():
	d = random.randint(1,28)
	m = random.randint(1,12)
	y = int(max(min(random.gauss(1994, 4), 1999),1970))
	return "{0:02d}.{1:02d}.{2:02d}".format(d,m,y)

vornamen_weiblich = []
vornamen_nicht_weiblich = []
nachnamen = []
strassennamen = []
plzort = []

twobools = {'a':{'sp':False,'gremien':False},'b':{'sp':True,'gremien':True},'c':{'sp':True,'gremien':False},'d':{'sp':False,'gremien':True}}
ma_map = {1:"", 2:"Zweitschrift", 3:"Drittschrift", 4:"Viertschrift", 5:"Fünftschrift"}

semesters = {"Wintersemester 2016/2017":95,"Sommersemester 2016":4,"Wintersemester 2015/2016":1}
fakultaeten = {0:119,1:321,2:1014,3:4352,4:3053,5:9574,6:11052,7:3665,8:1593,9:1440}
loecher = {'a':90,'b':8,'c':1,'d':1}
mehrfachausfertigungen = {1:90,2:5,3:3,4:1,5:1}
briefwahl = {'a':95,'b':1,'c':3,'d':1}

with open('../data/nachnamen.txt', "r") as f:
	for line in f:
		nachnamen.append(line.strip())
with open('../data/plz-ort.txt', "r") as f:
	for line in f:
		plzort.append(line.strip())
with open('../data/strassen.txt', "r") as f:
	for line in f:
		strassennamen.append(line.strip())
with open('../data/vornamen_frau.txt', "r") as f:
	for line in f:
		vornamen_weiblich.append(line.strip())
with open('../data/vornamen_mann.txt', "r") as f:
	for line in f:
		vornamen_nicht_weiblich.append(line.strip())


negativliste = []

for i in range(30000):
	r1 = (random.random() < 0.5)
	r2 = (random.random() < 0.25)
	r3 = (random.random() < 0.1)
	r4 = (random.random() < 0.75)
	v = random.choice(vornamen_weiblich) if r1 else random.choice(vornamen_nicht_weiblich)
	n = random.choice(nachnamen)
	g = randgebdat()
	s = random.choice(strassennamen)
	h = int(random.expovariate(0.1))
	z = random.choice(('a','b','c','d','e')) if r3 else ''
	p = random.choice(plzort) if r2 else "{} Bonn".format(random.randint(53111,53229))
	beurlaubt = (random.random() < 0.1)
	
	matrikelnummer = randmatnr()
	weiblich = r1
	mehrfachausfertigung = randomvalue(mehrfachausfertigungen)
	ma_ausweis = mehrfachausfertigung if r4 else random.randint(1,mehrfachausfertigung)
	semester = randomvalue(semesters)
	fakultaet = randomvalue(fakultaeten)
	
	sfach = Studienfach("Master of Disaster","Katastrophenmanagement",0)
	
	loch = twobools[randomvalue(loecher)]
	
	studi = Stud(v, n, g, "{} {}{}".format(s,h,z), p, weiblich, matrikelnummer, [sfach], 0, fakultaet, mehrfachausfertigung, beurlaubt)
	
	ausweisnr = random.randint(1000000,3000000)
	
	ausweis = Ausweis(studi, semester, ausweisnr, loch, ma_ausweis)
	
	bw = twobools[randomvalue(briefwahl)]
	
	if(bw['sp'] or bw['gremien'] or mehrfachausfertigung > 1):
		negativliste.append((studi, bw))
	
	
	
	with open("json/{}.json".format(i), "w") as f:
		print(ausweis.toJSON(), file=f)


i = 1
negativliste_s = []
for entry in sorted(negativliste, key=lambda x: "{}{}{}".format(x[0].nachname, x[0].vorname, x[0].matrikelnummer)):
		
		ma = ma_map[entry[0].mehrfachausfertigung]
		
		bw = ""
		wbg = ""
		wbsp = ""
		if(entry[1]['sp'] and entry[1]['gremien']):
			bw = "Briefwahl"
			wbg = "Nein"
			wbsp = "Nein"
		elif(entry[1]['sp']):
			bw = "Briefwahl SP"
			wbsp = "Nein"
		elif(entry[1]['gremien']):
			bw = "Briefwahl Gremien"
			wbg = "Nein"
		
		if(entry[0].beurlaubt):
			if (random.random() < 0.5):
				wbg = "Nein"
				wbsp = "Nein"
		
		negativliste_s.append([i, entry[0].matrikelnummer, entry[0].nachname, entry[0].vorname, wbg, wbsp, ma, bw])
		i+= 1
with open("json/negativliste.json", "w") as f:
	json.dump(negativliste_s, f)