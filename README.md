#Flask development



## 1. Programvaror
Ni behöver installera en del programvaror
### 1.1 Virtualbox
Virtualbox är ett program som kan skapa virtuella maskiner på en dator,
er dator brukar kallas för host och i er host kan ni installer en eller flera guest's. Vi ska installera linux som guest.

Virtualbox hittar ni här https://www.virtualbox.org/

### 1.2 Vagrant

Vagrant kan användas för att skapa virtuella maskiner programmeringsmässigt, dvs vi slipper använda oss av virtualboxs GUI för att klicka och skriva.

Med vagrant skriver vi en Vagrantfile som innehåller allt det vi vill att maskinen ska göra.

### 1.3 requirements.txt

Det behövs också några python program för att administrera detta. Installera dessa med pip install -r requirements.txt som vanligt.

## 2. Testa

## 2.1 Checka ut

Vi kan använda git´s submodul för att checka ut allt på en gång.
Öppna en terminal gå till det stället du vill ha ditt projekt på och skriv/klistra in följande.

`git clone --recursive git@github.com:itgsodbojo/flask-development-.git`

Nu ska ni ha laddat ner två projekt från github.

- flask-development, som innehåller installationskript
- helloflask som är ett exemple på en applikation som ska installeras

## 2.1 Skapa en server

cd in till katalogen flask-development och skriv in följande i en terminal

`fab test_deploy`

om allt nu fungerar, det kommer ta ett tag första gången kommer följande att ske

- en linuxdistribution, ubuntu server att laddas ner
- det kommer att skapas en ny virtuell maskin
- på denna kommer en webserver, nginx skapas och konfigureras
- uwsgi som är ett program som sköter kommunikation till helloflask, installeras och konfigureras
- till sist kommer helloflask att installeras

Det var mycket det om ni öppnar en webläsare och går till 192.168.33.10 så hittar ni helloflask.

## 3. Gör det själv

Nu är det dags att göra allt själv.

... todo...
