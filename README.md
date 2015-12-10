# nymph
nymph is a node class for data/text transmitting 
has n incoming edge for listening(receive) and 1 outgoing edge for talk(transmit)

Usage
terminalA
Alice_d=NymphData('Alice','192.168.*.*',8801)
Bob_d  =NymphData('Bob','192.168.*.*',8802)
Alice  =Nymph(Alice_d)

Alice.talkWith(Bob_d)
Alice.say("Hello World!")

terminalB
Alice_d=NymphData('Alice','192.168.*.*',8801)
Bob_d  =NymphData('Bob','192.168.*.*',8802)
Bob    =Nymph(Bob_d)

and if you want add some functionality you can inherit from nymph and override listen and sayformat
