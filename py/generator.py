#! /usr/bin/env python3

import random
import json
import csv

class Studienfach:
	def __init__(self, abschluss, fach, fsem):
		self.abschluss = abschluss
		self.fach = fach
		self.fsem = fsem
	
	def __str__(self):
		return "{}	{}	{}".format(self.abschluss, self.fach, self.fsem)

class Stud:
	def __init__(self, vorname, nachname, geburtsdatum, strasse, plzort, weiblich, matrikelnummer, studienfaecher, sternchen, fakultaet, mehrfachausfertigung, beurlaubt, ausweistyp, mitglied_studierendenschaft):
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
		self.ausweistyp = ausweistyp
		self.mitglied_studierendenschaft = mitglied_studierendenschaft
		
class Ausweis:
	def __init__(self, stud, semester, nummer, loecher, ausfertigung):
		self.stud = stud
		self.semester = semester
		self.nummer = nummer
		self.loecher = loecher
		self.ausfertigung = ausfertigung
	
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	
	def typ(self):
		if(self.stud.ausweistyp == "regulaer"):
			return "Studentinnen-" if self.stud.weiblich else "Studenten-"
		if(self.stud.ausweistyp == "weiterbildung"):
			return "Weiterbildungs-"
		if(self.stud.ausweistyp == "zweithoerer"):
			return "Zweithörerinnen-" if self.stud.weiblich else "Zweithörer-"
	
	def __str__(self):
		s = """{typ}   AUSWEIS
{semester}			[{ausfertigung}]
{stud.vorname} {stud.nachname}
{stud.geburtsdatum}		{stud.matrikelnummer}
{stud.strasse}
{stud.plzort}

			{nummer}

--------

""".format(stud = self.stud, typ=self.typ(), semester= self.semester, loecher = self.loecher, nummer = self.nummer, ausfertigung = self.ausfertigung)
		t = ""
		for i in range(len(self.stud.studienfaecher)):
			t += str(self.stud.studienfaecher[i])
			if(i == self.stud.sternchen):
				t += "*"
			t += "\n"
		
		u = """
[{stud.fakultaet} {loecher[gremien]}] [{loecher[sp]}]

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
	
	return random.randint(1900000,3199999)

def randgebdat():
	d = random.randint(1,28)
	m = random.randint(1,12)
	y = int(max(min(random.gauss(1994, 4), 1999),1970))
	return "{0:02d}.{1:02d}.{2:02d}".format(d,m,y)

def randomfaecher(fakultaet, faecher, double=False):
	abschluss = random.choice(list(faecher[str(fakultaet)].keys()))
	retval = []
	
	if(fakultaet == 5 and abschluss == "Bachelor of Arts" and len(faecher[str(fakultaet)][abschluss]) > 1):
		sfaecher = random.sample(faecher[str(fakultaet)][abschluss], 2)
		fsemester = random.randint(1, 13)
		
		retval.append(Studienfach(abschluss, sfaecher[0], fsemester))
		retval.append(Studienfach("", sfaecher[1], (fsemester if random.random() < 0.8 else random.randint(1, 13))))
		  
	elif(fakultaet == 8 and abschluss != "Promotion" and len(faecher[str(fakultaet)][abschluss]) > 1):
		sfaecher = random.sample(faecher[str(fakultaet)][abschluss], 2)
		sfaecher.append("Bildungswissenschaften")
		
		fsemester = random.randint(1, 13)
		retval.append(Studienfach(abschluss, sfaecher[0], fsemester))
		retval.append(Studienfach("", sfaecher[1], (fsemester if random.random() < 0.8 else random.randint(1, 13))))
		retval.append(Studienfach("", sfaecher[2], (fsemester if random.random() < 0.8 else random.randint(1, 13))))
		  
	else:
		sfaecher = random.sample(faecher[str(fakultaet)][abschluss], 1)
		fsemester = random.randint(1, 13)
		retval.append(Studienfach(abschluss, sfaecher[0], fsemester))
	
	if (not double) and (random.random() < 0.2):
		retval += randomfaecher(random.randint(0,9), faecher, double=True)
	return retval
	
	

vornamen_weiblich = []
vornamen_nicht_weiblich = []
nachnamen = []
strassennamen = []
plzorte = []
faecher = {}

twobools = {'a':{'sp':False,'gremien':False},'b':{'sp':True,'gremien':True},'c':{'sp':True,'gremien':False},'d':{'sp':False,'gremien':True}}
ma_map = {1:"", 2:"Zweitschrift", 3:"Drittschrift", 4:"Viertschrift", 5:"Fünftschrift"}

semesters = {"Wintersemester 2016/2017":95,"Sommersemester 2016":4,"Wintersemester 2015/2016":1}
#fakultaeten = {0:119,1:321,2:1014,3:4352,4:3053,5:9574,6:11052,7:3665,8:1593,9:1440}
fakultaeten = {0:1,1:1,2:1,3:1,4:2,5:2,6:2,7:1,8:1,9:1}
loecher = {'a':90,'b':8,'c':1,'d':1}
mehrfachausfertigungen = {1:90,2:5,3:3,4:1,5:1}
briefwahl = {'a':95,'b':1,'c':3,'d':1}

with open('../data/nachnamen.txt', "r") as f:
	for line in f:
		nachnamen.append(line.strip())
with open('../data/plz-ort.txt', "r") as f:
	for line in f:
		plzorte.append(line.strip())
with open('../data/strassen.txt', "r") as f:
	for line in f:
		strassennamen.append(line.strip())
with open('../data/vornamen_frau.txt', "r") as f:
	for line in f:
		vornamen_weiblich.append(line.strip())
with open('../data/vornamen_mann.txt', "r") as f:
	for line in f:
		vornamen_nicht_weiblich.append(line.strip())
with open("../data/faecher.json", "r") as f:
	faecher = json.load(f)

negativliste = []

for i in range(10000):
	r_weiblich = (random.random() < 0.5)
	r_wohnort = (random.random() < 0.25)
	r_hausnummerbuchstabe = (random.random() < 0.1)
	r_mehrfachausfertigung = (random.random() < 0.75)
	r_ausweistyp = random.random()
	mitglied_studierendenschaft = True
	ausweistyp = ""
	if(r_ausweistyp < 0.05):
		ausweistyp = "weiterbildung"
		mitglied_studierendenschaft = (random.random() < 0.2)
	elif(r_ausweistyp < 0.15):
		ausweistyp = "zweithoerer"
	else:
		ausweistyp = "regulaer"
		
	vorname = random.choice(vornamen_weiblich) if r_weiblich else random.choice(vornamen_nicht_weiblich)
	nachname = random.choice(nachnamen)
	
	if(i < 50):
		if not r_weiblich:
			vorname = "Marcel"
		nachname = "Heinen"
	
	geburtsdatum = randgebdat()
	strasse = random.choice(strassennamen)
	hausnummer = int(random.expovariate(0.1))
	zusatz_hausnummer = random.choice(('a','b','c','d','e')) if r_hausnummerbuchstabe else ''
	plzort = random.choice(plzorte) if r_wohnort else "{} Bonn".format(random.randint(53111,53229))
	beurlaubt = (random.random() < 0.1)
	
	matrikelnummer = randmatnr()
	weiblich = r_weiblich
	mehrfachausfertigung = randomvalue(mehrfachausfertigungen)
	ma_ausweis = mehrfachausfertigung if r_mehrfachausfertigung else random.randint(1,mehrfachausfertigung)
	semester = randomvalue(semesters)
	fakultaet = randomvalue(fakultaeten)
	
	sfaecher = randomfaecher(fakultaet, faecher)
	sternchen = random.randrange(len(sfaecher))
	
	loch = twobools[randomvalue(loecher)]
	
	print(plzort)
	
	studi = Stud(vorname, nachname, geburtsdatum, "{} {}{}".format(strasse,hausnummer,zusatz_hausnummer), plzort, weiblich, matrikelnummer, sfaecher, 0, fakultaet, mehrfachausfertigung, beurlaubt, ausweistyp, mitglied_studierendenschaft)
	
	ausweisnr = random.randint(1000000,3000000)
	
	ausweis = Ausweis(studi, semester, ausweisnr, loch, ma_ausweis)
	
	bw = twobools[randomvalue(briefwahl)]
	
	if(bw['sp'] or bw['gremien'] or mehrfachausfertigung > 1 or (ausweistyp == "weiterbildung" and not weiblich) or not mitglied_studierendenschaft):
		if(ausweistyp != "zweithoerer"):
			negativliste.append((studi, bw))
	
	#print(ausweis)
	
	with open("json/{}.json".format(i), "w") as f:
		print(ausweis.toJSON(), file=f)


i = 1
negativliste_s = []
for entry in sorted(negativliste, key=lambda x: "{}{}{}".format(x[0].nachname, x[0].vorname, x[0].matrikelnummer)):
		
		ma = ma_map[entry[0].mehrfachausfertigung]
		
		bw = ""
		wbgs = ""
		wbgf = ""
		wbggb = ""
		wbsp = ""
		if(entry[1]['sp'] and entry[1]['gremien']):
			bw = "Briefwahl"
			wbg = "Nein"
			wbsp = "Nein"
		elif(entry[1]['sp']):
			bw = "Briefwahl SP"
			wbsp = "Nein"
		elif(entry[1]['gremien']):
			bw = "Briefwahl G"
			wbgs = "Nein"
		
		if(entry[0].ausweistyp == "weiterbildung" and not entry[0].weiblich):
			wbggb = "Nein"
		if(not entry[0].mitglied_studierendenschaft):
			wbsp = "Nein"
		
		if(entry[0].beurlaubt):
			if (random.random() < 0.5):
				wbgs = "Nein"
				wbsp = "Nein"
		
		negativliste_s.append([i, entry[0].matrikelnummer, entry[0].nachname, entry[0].vorname, wbgs, wbgf, wbggb, wbsp, ma, bw])
		i+= 1
with open("json/negativliste.json", "w") as f:
	json.dump(negativliste_s, f)