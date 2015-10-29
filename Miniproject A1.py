import requests
import logging
import xmltodict
from tkinter import *

#NS api wordt aangeroepen met de juist usernaam en wachtwoord vervolgens wordt met een get alle data gedownload
def callNSAPI(req,auth_details):
    try:
        response = requests.get(req,auth = auth_details)
        return response
    except BaseException:
        return logging.exception('')

filenaam = 'stations1.xml'
auth_details = ('walet.christian@gmail.com','q4kytt93Dq3A4IOX-mEBeT0Qx8a0WMSEBo6WQVZIuaPpdaHWWL0vCA')
nsapistations = callNSAPI('http://webservices.ns.nl/ns-api-stations-v2' ,auth_details)
data = nsapistations.content.decode("utf-8")

#Reisinformatie menu
def Gui2():
    global window2
    window2 = Tk()
    window2.config(bg = 'yellow')
    window2.geometry("784x590+300+300")

    #textbox van station
    L1 = Label( window2,text = " van station ")
    L1.pack(side = LEFT)
    L1.place(x=115, y=75, anchor=NW)
    global E1
    E1 = Entry(window2,bd=5)
    E1.pack(side= LEFT)
    E1.place(x=185, y=75, anchor=NW)

    #textbox naar station
    L2 = Label( window2,text = " naar station ")
    L2.pack(side = LEFT)
    L2.place(x=390, y=75, anchor=NW)
    global E2
    E2 = Entry(window2,bd=5)
    E2.pack(side= LEFT)
    E2.place(x=465, y=75, anchor=NW)


    buttonzoek = Button(window2,text = "zoek",width = 15,bd = 15 ,bg = 'blue' , foreground = 'white', command = beidefunctie)
    buttonzoek.place(relx=.4, rely=.3, anchor="sw")


#vertragingstijd
def callback():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)

    try:
        return "Vertraging: " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['AankomstVertraging'] + "\n"

    except:
        a = ("Geen vertraging" + "\n")
        return a


#aantal overstappen
def overstappen():

    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)

    try:
        return "Overstappen: " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['AantalOverstappen'] + "\n"

    except:
        nietoverstap = ("Error geen overstap info beschikbaar \n")
        return nietoverstap

#het traject
def traj():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    schrijf_xml(datainfo,infonaam)
    try:
        a = ("Traject: " + str(E1.get()) + " - " + str(E2.get()) + "\n")
        return a
    except:
        geentraject = ("Error geen traject info beschikbaar \n")
        return geentraject

#de actuele vertrektijden (incl. vertraging)
def vtt():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return ("Actuele vertrektijd:  " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['ActueleVertrekTijd'] + "\n")
    except:
        geenvertrektijden = ("Error geen vertrektijden beschikbaar \n")
        return geenvertrektijden

#de actuele aankomsttijden (incl. vertraging)
def att():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return ("Actuele aankomsttijd:  " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['ActueleAankomstTijd'] + "\n")
    except:
        geenaankomst = ("Error geen aankomsttijden beschikbaar \n" )
        return geenaankomst

#vervoerder
def ver():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return "Vervoerder:  " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['ReisDeel']['Vervoerder'] + "\n"
    except:
        geenvervoerder = ("Error geen vervoerder info beschikbaar \n")
        return geenvervoerder

#vervoerstype
def typ():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return ("Vervoertype:  " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['ReisDeel']['VervoerType'] + "\n")
    except:
        geentype = ("Geen vervoerstype info beschikbaar \n")
        return geentype

#status van het traject
def status():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return ("Status:  " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['ReisDeel']['Status'] + "\n")
    except:
        geenstatus = ("Geen status beschikbaar \n")
        return geenstatus

def sp():
    url = callNSAPI('http://webservices.ns.nl/ns-api-treinplanner?fromStation='+E2.get()+'&toStation='+ E1.get(),auth_details)
    infonaam = 'informatie.xml'
    datainfo = url.content.decode('utf-8')
    info_dict = verwerk_xml(infonaam)
    schrijf_xml(datainfo,infonaam)
    try:
        return ("Spoor: " + info_dict['ReisMogelijkheden']['ReisMogelijkheid'][0]['Spoor'] + "\n")
    except:
        geenspoor = ("Geen spoor informatie beschikbaar")
        return geenspoor

#roept beide functies voor de zoekknop
def beidefunctie():
    callback()
    textinfo()

#de textbox na het klikken van zoek
def textinfo():
    E4 = Text(window2,height =15 , width = 50,bg = 'blue',foreground = 'white')
    E4.place(x=200, y=200, anchor=NW)
    E4.pack
    E4.insert(END,traj())
    E4.insert(END,ver())
    E4.insert(END,typ())
    E4.insert(END,overstappen())
    E4.insert(END,status())
    E4.insert(END,callback())
    E4.insert(END,vtt())
    E4.insert(END,att())
    E4.insert(END,sp())

#schrijven van de xml
def schrijf_xml(response,infonaam):
    bestandinfo = open(infonaam,'w')
    bestandinfo.write(str(response))
    bestandinfo.close()

#de xml wordt geparse naar een dict
def verwerk_xml (infonaam):
    bestand = open(infonaam,'r')
    xml_string = bestand.read()       # informatie van de velden worden verwerkt om hier een url van te maken
    return xmltodict.parse(xml_string)


#Hoofdmenu
window = Tk()
p = PhotoImage(file="lol.png")
label = Label(window,image = p)
label.pack()
window.geometry("784x590+300+300")
button1 = Button(window,text = "Reisinformatie",width = 15,bd = 15 ,bg = 'blue' , foreground = 'white' ,command=Gui2)
button1.place(relx=.6, rely=.7, anchor="sw")



window.mainloop()



