from time import time_ns
from playsound import playsound

# Variables
TIME_OVERRIDE = 1 # Multiplier for time spent during wait calls. Change this if the music goes out of sync.

# Main frame
mainFrame = [("-"*55) + "  " + ("-"*55)] + ["| %s||  %s|"] * 15 + ["| %s|  " + ("-"*55)] + ["| %s|%s"] * 13 + [("-"*55)]

# Text arrays
mainText = [""] * 29
credits = [""] * 15
image = [""] * 20
textWait = 0
creditsWait = 0
imageWait = 0

# Main display function
def display():
    global mainText, credits, image
    print(mainFrame[0])
    for i in range(15): print(mainFrame[i+1] % (mainText[i].ljust(52), credits[i].ljust(54)))
    print(mainFrame[16] % mainText[15].ljust(52))
    for i in range(16,29): print(mainFrame[i+1] % (mainText[i].ljust(52), image[i-16]))
    print(mainFrame[30] + image[13])
    for i in range(14, 20): print((" "*55) + image[i])
    print("\033[0;0H\033[?25l", end="") # Resets and hides cursor

def bakeInstructions(instructions):
    bakedInstructions = []
    for instruction in instructions:
        try:
            if instruction[0] == "p":
                splitInstruction = instruction.split("§")
                bakedInstructions.append(["p", int(splitInstruction[1]), splitInstruction[2]])
            elif instruction[0] == "s":
                splitInstruction = instruction.split("§")
                printToFrame = ["p", int(splitInstruction[1])]
                wait = ["w", int(int(splitInstruction[2]) * 1_000_000 * TIME_OVERRIDE)]
                progressingText = splitInstruction[3]
                for letter in splitInstruction[4]:
                    progressingText += letter
                    bakedInstructions.append(printToFrame + [progressingText])
                    bakedInstructions.append(wait)
                bakedInstructions.pop()
            elif instruction[0] == "w":
                bakedInstructions.append(["w",int(int(instruction[2:]) * 1_000_000 * TIME_OVERRIDE)])
            elif instruction[0] == "d":
                bakedInstructions.append(["d", int(instruction[2:])])
            elif instruction[0] == "#": pass
            else:
                bakedInstructions.append(instruction)
        except:
            print("Error at instruction " + instruction)
            quit()
    return bakedInstructions

def executeText(instruction):
    global textWait, mainText, image

    if instruction[0] == "p":
        mainText[instruction[1]] = instruction[2]
    elif instruction[0] == "w":
        textWait = time_ns() + instruction[1]
    elif instruction[0] == "u":
        for i in range(len(mainText)-1): mainText[i] = mainText[i+1]
        mainText[-1] = ""
    elif instruction[0] == "c":
        for i in range(len(mainText)): mainText[i] = ""
    elif instruction[0] == "d":
        for i in range(len(mainText)): image = images[instruction[1]]
    elif instruction[0] == "m":
        playsound("audio.wav", block=False)
        print("\033c\033[38;2;193;156;0m", end="") # Resets screen in case of error

def executeCredits(instruction):
    global creditsWait, credits

    if instruction[0] == "p":
        credits[instruction[1]] = instruction[2]
    elif instruction[0] == "w":
        creditsWait = time_ns() + instruction[1]
    elif instruction[0] == "u":
        for i in range(len(credits)-1):
            credits[i] = credits[i+1]
        credits[-1] = ""

def main():
    global textInstructions, creditsInstructions, textWait, creditsWait, imageWait

    print("\033[38;2;193;156;0m\033[?25l", end="") # Sets colour and hides cursor

    bakedText = bakeInstructions(textInstructions)
    bakedCredits = bakeInstructions(creditsInstructions)

    textIndex = 0
    creditsIndex = 0
    
    # Main loop
    scheduleDisplay = True
    while True:
        current = time_ns()
        if current >= textWait:
            if len(bakedText) == textIndex: textWait = 2**63-1
            else: executeText(bakedText[textIndex])
            textIndex += 1
            scheduleDisplay = True
        if current >= creditsWait:
            if len(bakedCredits) == creditsIndex: creditsWait = 2**63-1
            else: executeCredits(bakedCredits[creditsIndex])
            creditsIndex += 1
            scheduleDisplay = True
        if scheduleDisplay:
            display()
            scheduleDisplay = False

#
# Instruction Legend:
#
# Print§Line§Text
# Slow§Line§TimeInMs§PreviousText§ProgressingText
# Wait§TimeInMs
# Draw§imageIndex
# Clear
# Up
# Music
#

textInstructions = '''
s§0§75§§Forms FORM-29827281-12:
w§75
s§1§75§§Test Assessment Report
w§3000
m
s§5§75§§This was a triumph.
w§2500
s§6§75§§I'm making a note here:
w§500
s§7§75§§HUGE SUCCESS.
w§2100
s§8§100§§It's hard to overstate
w§150
s§9§150§§my satisfaction.
w§2700
d§0
s§10§75§§Aperture Science
w§2500
s§11§75§§We do what we must
w§400
s§12§75§§because
w§400
s§12§75§because §we can.
w§2000
s§13§100§§For the good of all of us.
d§1
w§100
s§14§70§§Except the ones who are dead.
w§900
d§0
s§16§70§§But there's no sense crying
w§150
s§17§85§§over every mistake.
w§250
s§18§75§§You just keep on trying
w§150
s§19§85§§till you run out of cake.
d§2
w§150
s§20§80§§And the Science gets done.
w§150
s§21§80§§And you make a neat gun.
d§0
w§150
s§22§80§§For the people who are
w§150
s§23§80§§still alive.
w§2000
c
s§0§40§§Forms FORM-55551-5:
w§40
s§1§40§§Personnel File Addendum:
w§500
s§3§75§§Dear <<Subject Name Here>>,
w§85
s§5§85§§I'm not even angry.
w§2750
s§6§85§§I'm being so sincere right now.
w§2750
s§7§85§§Even though you
d§3
s§7§85§Even though you§ broke my heart.
w§250
s§8§85§§And killed me.
w§2750
d§4
s§9§70§§And tore me to pieces.
w§2100
s§10§85§§And threw every piece
w§500
s§10§100§And threw every piece §into
w§500
d§5
s§10§100§And threw every piece into §a fire.
w§2200
s§11§75§§As they burned it hurt because
w§700
d§6
s§12§75§§I was so happy for you!
w§800
s§13§85§§Now these points of data
w§75
s§14§85§§make a beautiful line.
w§200
s§15§80§§And we're out of beta.
w§75
s§16§80§§We're releasing on time.
d§4
w§200
s§17§80§§So I'm GLaD. I got burned.
d§2
w§200
s§18§60§§Think of all the things we learned
w§75
d§0
s§19§60§§for the people who are
w§75
s§20§60§§still
w§75
s§20§150§still §alive.
w§2000
c
s§0§40§§Forms FORM-55551-6:
w§40
s§1§40§§Personnel File Addendum Addendum:
w§300
s§3§150§§One last thing:
w§175
s§5§75§§Go ahead and leave me.
w§2450
s§6§75§§I think
w§75
s§6§130§I think §I prefer to stay inside.
w§1750
s§7§100§§Maybe you'll find someone else
w§100
s§8§100§§to help you.
w§2800
s§9§75§§Maybe
d§7
s§9§75§Maybe§ Black
w§75
s§9§200§Maybe Black §Mesa
w§220
s§9§400§Maybe Black Mesa§...
w§1500
s§10§40§§THAT WAS A JOKE.
w§1600
s§10§40§THAT WAS A JOKE. §FAT CHANCE.
w§2000
s§11§300§§Anyway
w§75
d$8
s§11§80§Anyway§, this cake is great.
w§75
s§12§80§§It's so delicious and moist.
§1200
d§9
s§13§80§§Look at me still talking
w§80
d§1
s§14§65§§when there's Science to do.
w§60
d§0
s§15§70§§When I look out there,
w§60
s§16§85§§it makes me GLaD I'm not you.
w§65
d§2
s§17§70§§I've experiments to run.
w§90
d§4
s§18§65§§There is research to be done.
w§60
d§0
s§19§80§§On the people who are
w§80
s§20§75§§Still
w§80
s§20§300§Still §alive.
w§500
c
s§3§65§§PS: And believe me I am
w§75
s§4§80§§still alive.
w§1500
s§5§55§§PPS:
w§50
s§5§65§PPS: §I'm doing Science and I'm
w§75
s§6§80§§still alive.
w§1400
s§7§55§§PPPS:
w§50
s§7§65§PPPS: §I feel FANTASTIC and I'm
w§75
s§8§80§§still alive.
w§600
s§10§65§§FINAL THOUGHT:
w§60
s§11§65§§While you're dying I'll be
w§60
s§12§80§§still alive.
w§500
s§14§45§§FINAL THOUGHT PS:
w§60
s§15§65§§And when you're dead I will be
w§60
s§16§80§§still alive.
w§700
s§19§120§§STILL ALIVE
w§200
c
w§5000
s§0§40§§Forms FORM-55551-7:
w§40
s§1§40§§Personnel File Addendum Addendum Addendum:
w§300
s§3§50§§Recreated by:
w§300
s§3§300§Recreated by: §mgmgmg
'''.split("\n")
textInstructions.pop(0)
textInstructions.pop(-1)

creditsInstructions = '''
w§1725
w§75
w§1650
w§3000
w§1425
s§-1§69§§>LIST PERSONNEL
u
w§60
u
w§60
u
w§60
s§-1§69§§Gautam Babbar
u
w§60
s§-1§69§§Ted Backman
u
w§60
s§-1§69§§Kelly Bailey
u
w§60
s§-1§69§§Jeff Ballinger
u
w§60
s§-1§69§§Aaron Barber
u
w§60
s§-1§69§§Jeep Barnett
u
w§60
s§-1§69§§Dan Berger
u
w§60
s§-1§69§§Yahn Bernier
u
w§60
s§-1§69§§Ken Birdwell
u
w§60
s§-1§69§§Derrick Birum
u
w§60
s§-1§69§§Mike Blaszczak
u
w§60
s§-1§69§§Iestyn Bleasdale-Shepherd
u
w§60
s§-1§69§§Chris Bokitch
u
w§60
s§-1§69§§Steve Bond
u
w§60
s§-1§69§§Matt Boone
u
w§60
s§-1§69§§Antoine Bourdon
u
w§60
s§-1§69§§Jamaal Bradley
u
w§60
s§-1§69§§Charlie Brown
u
w§60
s§-1§69§§Chralie Burgin
u
w§60
s§-1§69§§Adrew Burke
u
w§60
s§-1§69§§Augusta Butlin
u
w§60
s§-1§69§§Julie Caldwell
u
w§60
s§-1§69§§Dario Casali
u
w§60
s§-1§69§§Chris Chin
u
w§60
s§-1§69§§Jess Cliffe
u
w§60
s§-1§69§§Phil Co
u
w§60
s§-1§69§§John Cook
u
w§60
s§-1§69§§Christen Coomer
u
w§60
s§-1§69§§Greg Coomer
u
w§60
s§-1§69§§Scott Dalton
u
w§60
s§-1§69§§Kerry Davis
u
w§60
s§-1§69§§Jason Deakins
u
w§60
s§-1§69§§Ariel Diaz
u
w§60
s§-1§69§§Quintin Doroquez
u
w§60
s§-1§69§§Jim Dose
u
w§60
s§-1§69§§Chris Douglass
u
w§60
s§-1§69§§Laura Dubuk
u
w§60
s§-1§69§§Mike Dunkle
u
w§60
s§-1§69§§Mike Durand
u
w§60
s§-1§69§§Mike Dussault
u
w§60
s§-1§69§§Dhabih Eng
u
w§60
s§-1§69§§Katie Engel
u
w§60
s§-1§69§§Chet Faliszek
u
w§60
s§-1§69§§Adrian Finol
u
w§60
s§-1§69§§Bill Fletcher
u
w§60
s§-1§69§§Moby Francke
u
w§60
s§-1§69§§Stephane Gaudette
u
w§60
s§-1§69§§Kethy Gehrig
u
w§60
s§-1§69§§Vitality Genkin
u
w§60
s§-1§69§§Paul Grahm
u
w§60
s§-1§69§§Chris Green
u
w§60
s§-1§69§§Chris Grinstead
u
w§60
s§-1§69§§John Guthrie
u
w§60
s§-1§69§§Aaron Halifax
u
w§60
s§-1§69§§Reagan Halifax
u
w§60
s§-1§69§§Leslie Hall
u
w§60
s§-1§69§§Jeff Hameluck
u
w§60
s§-1§69§§Joe Han
u
w§60
s§-1§69§§Don Holden
u
w§60
s§-1§69§§Jason Holtman
u
w§60
s§-1§69§§Gray Horsfield
u
w§60
s§-1§69§§Keith Huggins
u
w§60
s§-1§69§§Jim Hughes
u
w§60
s§-1§69§§Jon Huising
u
w§60
s§-1§69§§Brian Jacobson
u
w§60
s§-1§69§§Lars Jensvold
u
w§60
s§-1§69§§Erik Johnson
u
w§60
s§-1§69§§Jakob Jungles
u
w§60
s§-1§69§§Rich Kaethler
u
w§60
s§-1§69§§Steve Kalning
u
w§60
s§-1§69§§Aaron Kearly
u
w§60
s§-1§69§§Likka Keranen
u
w§60
s§-1§69§§David Kircher
u
w§60
s§-1§69§§Eric Kirchmer
u
w§60
s§-1§69§§Scott Klintworth
u
w§60
s§-1§69§§Alden Kroll
u
w§60
s§-1§69§§Marc Laidlaw
u
w§60
s§-1§69§§Jeff Lane
u
w§60
s§-1§69§§Tim Larkin
u
w§60
s§-1§69§§Dan LeFree
u
w§60
s§-1§69§§Isabelle LeMay
u
w§60
s§-1§69§§Tom Leonard
u
w§60
s§-1§69§§Jeff Lind
u
w§60
s§-1§69§§Doug Lombardi
u
w§60
s§-1§69§§Bianca Loomis
u
w§60
s§-1§69§§Richard Lord
u
w§60
s§-1§69§§Realm Lovejoy
u
w§60
s§-1§69§§Randy Lundeen
u
w§60
s§-1§69§§Scott Lynch
u
w§60
s§-1§69§§Ido Magal
u
w§60
s§-1§69§§Nick Maggiore
u
w§60
s§-1§69§§John McCaskey
u
w§60
s§-1§69§§Patrick McClard
u
w§60
s§-1§69§§Steve McClure
u
w§60
s§-1§69§§Hamish McKenzie
u
w§60
s§-1§69§§Gary McTaggart
u
w§60
s§-1§69§§Jason Mitchell
u
w§60
s§-1§69§§Mike Morasky
u
w§60
s§-1§69§§John Morello II
u
w§60
s§-1§69§§Bryn Moslow
u
w§60
s§-1§69§§Arsenio Navarro
u
w§60
s§-1§69§§Gabe Newell
u
w§60
s§-1§69§§Milton Ngan
u
w§60
s§-1§69§§Jake Nicholson
u
w§60
s§-1§69§§Martin Otten
u
w§60
s§-1§69§§Nick Papineau
u
w§60
s§-1§69§§Karen Prell
u
w§60
s§-1§69§§Bay Raitt
u
w§60
s§-1§69§§Tristan Reidford
u
w§60
s§-1§69§§Alfred Reynolds
u
w§60
s§-1§69§§Matt Rhoten
u
w§60
s§-1§69§§Garret Rickey
u
w§60
s§-1§69§§Dave Riller
u
w§60
s§-1§69§§Elan Ruskin
u
w§60
s§-1§69§§Matthew Russell
u
w§60
s§-1§69§§Jason Ruymen
u
w§60
s§-1§69§§David Swyer
u
w§60
s§-1§69§§Marc Scaparro
u
w§60
s§-1§69§§Wade Schin
u
w§60
s§-1§69§§Matthew Scott
u
w§60
s§-1§69§§Aaron Seeler
u
w§60
s§-1§69§§Jennifer Seeley
u
w§60
s§-1§69§§Taylor Sherman
u
w§60
s§-1§69§§Eric Smith
u
w§60
s§-1§69§§Jeff Sorensen
u
w§60
s§-1§69§§David Speyrer
u
w§60
s§-1§69§§Jay Stelly
u
w§60
s§-1§69§§Jeremy Stone
u
w§60
s§-1§69§§Eric Strand
u
w§60
s§-1§69§§Kim Swift
u
w§60
s§-1§69§§Kelly Thornton
u
w§60
s§-1§69§§Eric Twelker
u
w§60
s§-1§69§§Carl Uhlman
u
w§60
s§-1§69§§Doug Valente
u
w§60
s§-1§69§§Bill Van Buren
u
w§60
s§-1§69§§Gabe Van Engel
u
w§60
s§-1§69§§Alex Vlachos
u
w§60
s§-1§69§§Robin Walker
u
w§60
s§-1§69§§Joshua Weier
u
w§60
s§-1§69§§Andrea Wicklund
u
w§60
s§-1§69§§Greg Winkler
u
w§60
s§-1§69§§Erik Wolpaw
u
w§60
s§-1§69§§Doug Wood
u
w§60
s§-1§69§§Matt T. Wood
u
w§60
s§-1§69§§Danika Wright
u
w§60
s§-1§69§§Matt Wright
u
w§60
s§-1§69§§Shawn Zabecki
u
w§60
s§-1§69§§Torsten Zabka
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§'Still Alive' by:
u
w§60
s§-1§69§§Johnathan Coulton
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Voices:
u
w§60
s§-1§69§§Ellen McLain - GlaDOS, Turrets
u
w§60
s§-1§69§§Mike Patton - THE ANGER SPHERE
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Voice Casting:
u
w§60
s§-1§69§§Shana Landsburg\\Teri Fiddleman
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Voice Recording:
u
w§60
s§-1§69§§Pure Audio, Seattle, WA
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Voice recording
u
w§60
s§-1§69§§scheduling and logistics:
u
w§60
s§-1§69§§Pat Cockburn, Pure Audio
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Translations:
u
w§60
s§-1§69§§SDL
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Crack Legal Team:
u
w§60
s§-1§69§§Liam Lavery
u
w§60
s§-1§69§§Karl Quackenbush
u
w§60
s§-1§69§§Kristen Boraas
u
w§60
s§-1§69§§Kevin Rosenfield
u
w§60
s§-1§69§§AlanBruggeman
u
w§60
s§-1§69§§Dennis Tessier
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Thanks for the use of their face:
u
w§60
s§-1§69§§Alesia Glidewell - Chell
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§Special thanks to everyone at:
u
w§60
s§-1§69§§Alienware
u
w§60
s§-1§69§§ATI
u
w§60
s§-1§69§§Dell
u
w§60
s§-1§69§§Falcon Northwest
u
w§60
s§-1§69§§Havok
u
w§60
s§-1§69§§SOFTIMAGE
u
w§60
s§-1§69§§and Don Kemmis, SLK Technologies
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
s§-1§69§§THANK YOU FOR PARTICIPATING
u
w§60
s§-1§69§§IN THIS
u
w§60
s§-1§69§§ENRICHMENT CENTER ACTIVITY!!
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
u
w§60
'''.split("\n")
creditsInstructions.pop(0)
creditsInstructions.pop(-1)

images = ['''
                       .,-:;//;:=,
                   . :H@@@MM@M#H/.,+%;,
                ,/X+ +M@@M@MM%=,-%HMMM@X/,
              -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
             ;@M@@M- XM@X;. -+xxxxxHHH@M@M#@/.
           ,%MM@@MH ,@%=            ,---=-=:=,.
           =@#@@@MX .,              -%HX$$%%%+;
          =-./@M@M$                  .;@MMMM@MM:
          X@/ -$MM/                    .+MM@@@M$
         ,@M@H: :@:                    . =x#@@@@-
         ,@@@MMX, .                    /H- ;@M@M=
         .H@@@@M@+,                    %MM+..%#$.
          /MMMM@MMH/.                  XM@MH; =;
           /%+%$XHH@$=              , .H@@@@MX,
            .=--------.           -%H.,@@@@@MX,
            .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
              =XMMM#MM@MM#H;,-+HMM@M+ /MMMX=
                =%@M@M#@$-.=$@MM@@@M; %M%=
                  ,:+$+-./H#MMMMMMM@= =,
                        =++%%%%+/:-.
''',
'''
                     =+$HM###@H%;,
                  /H##############M$,
                  ,@###############+
                   .H#############+
                    X############/
                     $##########/
                      %########/
                       /X/;;+X/

                        -XHHX-
                       ,######,
       #############X  .M####M.  X#############
       ##############-   -//-   -##############
       X##############%,      ,+##############X
       -##############X        X##############-
        %############%          %############%
         %##########;            ;##########%
          ;#######M=              =M#######;
           .+M###@,                ,@###M+.
              :XH.                  .HX:
''',
'''
                       =/;;/-
                      +:    //
                     /;      /;
                    -X        H.
      .//;;;:;;-,   X=        :+   .-;:=;:;%;.
      M-       ,=;;;#:,      ,:#;;;=,       ,@
      :%           :%.=/++++/=.$=           %=
       ,%;         %/:+/;,,/++:+/         ;+.
         ,+/.    ,;@+,        ,%H;,    ,/+,
            ;+;;/= @.  .H##X   -X :///+;
            ;+=;;;.@,  .XM@$.  =X.//;=%/.
         ,;:      :@%=        =$H:     .+%-
       ,%=         %;-///==///-//         =%.
      ;+           :%-;;;:;;;;-X-           +:
      @-      .-;;;;M-        =M/;;;-.      -X
       :;;::;;-.    %-        :+    ,.;;-;:==
                    ,X        H.
                     ;/      %=
                      //    +;
                       .////.
''',
'''
                                .,---.
                              ,/XM#MMMX;,
                            -%##########M%,
                           -@######%  $###@=
            .,--,         -H#######$   $###M:
         ,;$M###MMX;     .;##########$;HM###X=
       ,/@##########H=       ;###############+
      -+#############M/,       %#############+
      %M###############=       /#############:
      H################       .M############;.
      @###############M       ,@##########M:.
      X################,       -$=X######@:
      /@##################%-      +#####$-
      .:##################X      .X####+,
       ..H################/      -X####+.
        ,;X###############.        .MM/
           ,:+$H@M########M#$-     .$$=
                .,-=;+$@###X:      ;/=.
                       ../X$;     .::,
                           .,      ..
''',
'''
                 .+
                  /M;
                   H#@:              ;,
                   -###H-          -@/
                    %####$.  -;  .%#X
                     M#####+;#H :M#M.
      ..         .+/;%#########X###-
       -/%H%+;-,   +##############/
         .:$M###MH$%+############X  ,--=;-
             -/H#####################H+=.
                .+#################X.
              =%M####################H;.
                 /@###############+;;/%%;,
              -%###################$.
            ;H######################M=
         ,%#####MH$%;+#####M###-/@####%
       :$H%+;=-      -####X.,H#   -+M##@-
      .              ,###;    ;      =$##+
                     .#H,               :XH.
                      +                   .;-
''',
'''
                           -$-
                          .H##H,
                         +######+
                      .+#########H.
                    -$############@.
                  =M###############@  -X:
                .$##################:  @#@-
           ,;  .M###################;  H###;
         ;@#:  @###################@  ,#####:
       -M###.  M#################@.  ;######H
       M####-  +###############$   =@#######X
       M####$   -M###########+   :#########M,
        /####X-   =########%   :M########@/.
          ,;%H@X;   .$###X   :##MM@%+;:-
                       ..
         -/;:-,.             ,,-==+M########H
        -#################@HX%%+%%$%%%+:,,
           .-/H%%%+%%$H@###############M@+=:/+:
       /XHX%:#####MH%=    ,---:;;;;/%%XHM,:###$
       $@#MX %+;-                           .
''',
'''
                                           :X-
                                        :@###
                                      ;@####@
                                    ;M######X
                                  -@########$
                                .$##########@
                               =M############-
                              +##############$
                            .H############$=.
               ,/:         ,M##########M;.
            -+@###;       =##########M;
         =%M#######;     :#########M/
      -$M###########;   :#########/
       ,;X###########; =########$.
           ;H#########+#######M=
             ,+##############+
                /M#########@-
                  ;M######%
                    +####:
                     .$M-
''',
'''
                 .-;+$XHHHHHHX$+;-.
              ,;X@@x%/;=----=:/%X@@X/,
            =$@@%=.              .=+H@X:
          -XMX:                      =XMX=
         /@@:                          =H@+
        %@X,                            .$@$
       +@X,                               $@%
      -@@,                                 $@%
      %@%                                  .@=
      H@:                                  :@H
      H@:          :HHHHHHHHHHHHHHHHHX,    =@H
      %@%          ;@M@@@@@@@@@@@@@@@@H-   +@$
      =@@,         :@@@@@@@@@@@@@@@@@@@@= .@@:
       +@X         :@@@@@@@@@@@@@@@M@@@@@:%@%
        $@$,       ;@@@@@@@@@@@@@@@@M@@@@@@$.
         +@@HHHHHHH@@@@@@@@@@@@@@@@@@@@@@@+
          =X@@@@@@@@@@@@@@@@@@@@@@@@@@@@X=
            :$@@@@@@@@@@@@@@@@@@@@M@@@@$:
              ,.;$@@@@@@@@@@@@@@@@@@X/-
                  .-;+$XXHHHHHX$+;-.
''',
'''
                  ,:/+/-
                  /M/              .,-=;//;-
             .:/= ;MH/,    ,=/+%$XH@MM#@:
            -$##@+$###@H@MMM#######H:.    -/H#
       .,H@H@ X######@ -H#####@+-     -+H###@X
        .,@##H;      +XM##M/,     =%@###@X;-
      X%-  :M##########$.    .:%M###@%,
      M##H,   +H@@@$/-.  ,;$M###@%           -
      M####M=,,---,.-%%H####M$:          ,+@##
      @##################@/.         :%H##@$-
      M###############H.
      #################.
      ################H..;XM##M$=          .:+
      M##################@%=            =+@MH%
      @################M/.          =+H#X%=
      =+M##############M,       -/X#X+;.
        ..XM##########H=    ,/X#H+:,
           .=+HM######M+/+HM@+=.
               ,:/%XM####H/.
                    ..:=-
''',
'''
             #+ @      # #              M#@
       .    .X  X.%##@;# #   +@#######X. @#%  
         ,==.   ,######M+  -#####%M####M-    #
        :H##M%:=##+ .M##M,;#####/+#######% ,M#
       .M########=  =@#@.=#####M=M#######= ,M#
       :@@MMM##M.  -##M.,#######M#######. =  M
                   @##..###:.    .H####. @@ X,
         ############: ###,/####;  /##= @#. M
                 ,M## ;##,@#M;/M#M  @# X#% X#
      .%=   ######M## ##.M#:   ./#M ,M #M ,#$
      ##/         $## #+;#: #### ;#/ M M- @# :
      #+ #M@MM###M-;M #:$#-##$H# .#X @ + $#. #
            ######/.: #%=# M#:MM./#.-#  @#: H#
      +,.=   @###: /@ %#,@  ##@X #,-#@.##% .@#
      #####+;/##/ @##  @#,+       /#M    . X,
         ;###M#@ M###H .#M-     ,##M  ;@@; ###
         .M#M##H ;####X ,@#######M/ -M###$  -H
          .M###%  X####H  .@@MM@;  ;@#M@
            H#M    /@####/      ,++.  / ==-,
                     ,=/:, .+X@##H@#H  #####$=
''']
for i in range(len(images)):
    images[i] = images[i][1:-1].split("\n")
    for j in range(len(images[i])): images[i][j] = images[i][j].ljust(50)

# Executing the program
main()
