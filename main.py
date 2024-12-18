import pygame
import random
import math

class RoboMiekka:
    def __init__(self, robo_x, robo_y):
        self.robo_x = robo_x
        self.robo_y = robo_y
        self.halkaisija = 75
        self.lyonti_paalla = False
        self.kulma = 0
        self.osutut_hirviot = [] #sisältää osutut hirviot, jotta miekka ei osu monta kertaa per isku

    def robo_sijainti(self, robo_x, robo_y):
        self.robo_x = robo_x
        self.robo_y = robo_y

    def luo_lyonti(self, kulma):
        miekan_rata = math.pi / 2
        self.kulma = kulma
        self.kulma_alku = kulma - miekan_rata / 2
        self.lyonti_paalla = True
        self.kulma_loppu = kulma + miekan_rata /2
        self.osutut_hirviot = []

    def miekan_sijainti(self):
        if self.lyonti_paalla:
            self.kulma_alku += 0.2
            if self.kulma_alku > self.kulma_loppu:
                self.lyonti_paalla = False
                return None
            miekan_alku_x = self.robo_x + (self.halkaisija -40) * math.cos(self.kulma_alku)
            miekan_alku_y = self.robo_y + (self.halkaisija -40) * math.sin(self.kulma_alku)
            miekan_paa_x = self.robo_x + self.halkaisija * math.cos(self.kulma_alku)
            miekan_paa_y = self.robo_y + self.halkaisija * math.sin(self.kulma_alku)
            
            return (miekan_alku_x , miekan_alku_y), (miekan_paa_x, miekan_paa_y)
        return None
    
class Hirvio:
    def __init__(self, nayton_leveys, nayton_korkeus):
        self.kuva = pygame.image.load("hirvio.png")
        self.nopeus_x = 0
        self.nopeus_y = 0
        self.nayton_leveys = nayton_leveys
        self.nayton_korkeus = nayton_korkeus
        self.x, self.y = self.luo_aloituspaikka()
        self.hp = 1

    def luo_aloituspaikka(self): #Luo satunnaisen paikan ruudun ulkopuolella
        vasen_x, oikea_x = -100, self.nayton_leveys + 100
        yla_y, ala_y = -100, self.nayton_korkeus + 100

        aloituspaikka = random.choice(["vasen", "oikea", "ylos", "alas"])
        if aloituspaikka == "vasen":
            x = random.randint(vasen_x, -20)
            y = random.randint(0, self.nayton_korkeus - self.kuva.get_height())
        elif aloituspaikka == "oikea":
            x = random.randint(self.nayton_leveys + 20, oikea_x)
            y = random.randint(0, self.nayton_korkeus - self.kuva.get_height())
        elif aloituspaikka == "ylos":
            x = random.randint(0, self.nayton_leveys - self.kuva.get_width())
            y = random.randint(yla_y, -30)
        else:
            x = random.randint(0, self.nayton_leveys -1)
            y = random.randint(self.nayton_korkeus +20, ala_y)

        return x, y
    
    def hirvio_suunta(self, robo_keskipiste_x, robo_keskipiste_y): #antaa robon suunnan hirviöille
        hirvio_laatikko = self.kuva.get_rect()
        hirvio_laatikko.topleft = (self.x, self.y)
        hirvio_ylä = hirvio_laatikko.top
        hirvio_ala = hirvio_laatikko.bottom
        hirvio_vasen = hirvio_laatikko.left
        hirvio_oikea = hirvio_laatikko.right

        if robo_keskipiste_x < hirvio_vasen:
            self.nopeus_x = -1
        elif robo_keskipiste_x > hirvio_oikea:
            self.nopeus_x = 1
        else:
            self.nopeus_x = 0

        if robo_keskipiste_y < hirvio_ylä:
            self.nopeus_y = -1
        elif robo_keskipiste_y > hirvio_ala:
            self.nopeus_y = 1
        else:
            self.nopeus_y = 0
    
    def liiku_hirvio(self):
        self.x += self.nopeus_x
        self.y += self.nopeus_y

    def hirviot_paallekkain(self, muut_hirviot): 
        for muu_hirvio in muut_hirviot:
            if self != muu_hirvio:
                if (self.x <= muu_hirvio.x - 5 + muu_hirvio.kuva.get_width() and
                    self.x + self.kuva.get_width() >= muu_hirvio.x and 
                    self.y <= muu_hirvio.y - 5 + muu_hirvio.kuva.get_height() and
                    self.y + self.kuva.get_height() >= muu_hirvio.y):
                    return True
        return False

    def osuuko_hirvioon(self, miekan_isku):
        if miekan_isku != None:
            alku_x, alku_y  = miekan_isku[0]
            loppu_x, loppu_y = miekan_isku[1]
            keski_x = (alku_x + loppu_x) /2
            keski_y = (alku_y + loppu_y) /2
            if (self.x < loppu_x < self.x + self.kuva.get_width() and
                self.y < loppu_y < self.y + self.kuva.get_height()):
                return True
            if (self.x < alku_x < self.x + self.kuva.get_width() and
                self.y < alku_y < self.y + self.kuva.get_height()):
                return True
            if (self.x < keski_x < self.x + self.kuva.get_width() and
                self.y < keski_y < self.y + self.kuva.get_height()):
                return True
        return False  

class PikkuHirvio(Hirvio):
    def __init__(self, nayton_leveys, nayton_korkeus):
        super().__init__(nayton_leveys, nayton_korkeus)
        self.kuva = pygame.transform.scale(self.kuva, (self.kuva.get_width() * 0.6, self.kuva.get_height() * 0.6))

class PomoHirvio(Hirvio):
    def __init__(self, nayton_leveys, nayton_korkeus):
        super().__init__(nayton_leveys, nayton_korkeus)
        self.kuva.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MIN) #Muuttaa Pomon värin
        self.kuva =  pygame.transform.scale(self.kuva, (self.kuva.get_width() * 1.5, self.kuva.get_height() * 1.5))
        self.hp = 30
        self.osuma_aika = 0
        self.aloitus_aika = 50
        self.syoksy_aika = 10
        self.vaihe = None

        self.syntymä_aika = pygame.time.get_ticks()
        self.syoksy_vali = 5000
        self.viime_syoksy = self.syntymä_aika

    def liiku_hirvio(self):
        self.x += self.nopeus_x *2
        self.y += self.nopeus_y *2
    
    def osuma_kuva(self, naytto): #Pomohirvio välähtää, kun saa osuman
        if self.osuma_aika > 0:
            osuma_kuva = self.kuva.copy()
            osuma_kuva.fill((200, 200, 255), special_flags=pygame.BLEND_RGBA_SUB)
            naytto.blit(osuma_kuva, (self.x, self.y))
            self.osuma_aika -= 1
        else:
            naytto.blit(self.kuva, (self.x, self.y))
 
    def syoksy_seuraus(self, robo_keskipiste_x, robo_keskipiste_y): #seuraa syoksyn ajoitusta ja alustaa syoksyajan ja tärinäajan.
        aika = pygame.time.get_ticks()

        if self.vaihe == None and aika - self.viime_syoksy >= self.syoksy_vali:
            self.vaihe = "tarisee"
            self.aloitus_aika = 50
            self.syoksy_aika = 10
            self.viime_syoksy = aika
            self.hirvio_suunta(robo_keskipiste_x, robo_keskipiste_y)
           
        if self.vaihe == "tarisee":
            self.aloitus_aika -=1
            self.x += random.randint(-5, 5)
            self.y += random.randint(-5, 5)
            if self.aloitus_aika <=0:
                self.vaihe = "syoksyy"
                self.nopeus_x *= 30
                self.nopeus_y *= 30
  
        elif self.vaihe == "syoksyy":
            self.x += self.nopeus_x
            self.y += self.nopeus_y
            self.syoksy_aika -=1
            if self.syoksy_aika <= 0:
                self.vaihe = None


class Robo_Survivor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Robo Survivor")
        self.pisteet = 0
        self.fontti = pygame.font.SysFont(None, 30)
        self.nayton_leveys, self.nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        self.kello = pygame.time.Clock()
        self.voitto = False

        self.liikkeet = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False,}  #Kirja liike tapahtumille ja robon nopeus
        self.robo_nopeus = 3

        self.robo()
        self.robo_miekka = RoboMiekka(self.robo_keskipiste_x, self.robo_keskipiste_y)
        self.piirrä_aloitusruutu()

    def robo(self):
        kuva = pygame.image.load("robo.png")
        self.robo_kuva = pygame.transform.scale(kuva, (kuva.get_width() * 0.6, kuva.get_height() * 0.6)) # kuva pienennetään 60 prosenttiin
        self.robo_x = 320 - self.robo_kuva.get_width()/2 #robon aloituspiste keskelle ruutua
        self.robo_y = 240 - self.robo_kuva.get_height()/2
        self.robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2
        self.robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2
        self.robo_elamat = 3

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key in self.liikkeet:
                    self.liikkeet[tapahtuma.key] = True
                if tapahtuma.key == pygame.K_F2:
                    self.peli_silmukka()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key in self.liikkeet:
                    self.liikkeet[tapahtuma.key] = False
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                kulma = math.atan2(mouse_y - self.robo_keskipiste_y, mouse_x - self.robo_keskipiste_x) #laskee kulman hiiren ja robon välille
                self.robo_miekka.luo_lyonti(kulma)
            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku_robo(self):
        if self.liikkeet[pygame.K_a]:
            self.robo_x -= self.robo_nopeus
        if self.liikkeet[pygame.K_d]:
            self.robo_x += self.robo_nopeus
        if self.liikkeet[pygame.K_w]:
            self.robo_y -= self.robo_nopeus
        if self.liikkeet[pygame.K_s]:
            self.robo_y += self.robo_nopeus

        self.robo_x = max(0, min(self.nayton_leveys - self.robo_kuva.get_width(), self.robo_x))
        self.robo_y = max(0, min(self.nayton_korkeus - self.robo_kuva.get_height(), self.robo_y))

        self.robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2 #päivittää robon keskipisteen
        self.robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2

    def osuuko_roboon(self, hirvio):
        robo_oikea = self.robo_x + self.robo_kuva.get_width()
        robo_ala = self.robo_y + self.robo_kuva.get_height()
        hirvio_oikea = hirvio.x + hirvio.kuva.get_width()
        hirvio_ala = hirvio.y + hirvio.kuva.get_height()

        if (
            hirvio.x +10 <= robo_oikea and
            hirvio_oikea -10 >= self.robo_x and 
            hirvio.y +10 <= robo_ala and
            hirvio_ala -10 >= self.robo_y
        ):
            return True
        return False
    
    def piirrä_aloitusruutu(self):
        aloitus_fontti = pygame.font.Font(None, 30)
        teksti_lista = ["ROBO SURVIVOR","WASD - näppäimet liikuttavat Roboa","Hiiren vasemmalla napilla lyöt miekalla kursorin suuntaan","Paina F2 aloittaaksesi tai ESC lopettaaksesi"]
        aloitus_teksti = aloitus_fontti.render(f"ROBO SURVIVOR", True, (255,255,255))
        aloitus_teksti_laatikko = aloitus_teksti.get_rect(center=(self.nayton_leveys // 2, self.nayton_korkeus // 2))
        while True:
            self.naytto.fill((0,0,0))
            self.tutki_tapahtumat()
            rivi_y = self.nayton_korkeus // 2
            for rivi in teksti_lista:
                aloitus_teksti = aloitus_fontti.render(rivi, True, (255, 255, 255))
                aloitus_teksti_laatikko = aloitus_teksti.get_rect(center=(self.nayton_leveys // 2, rivi_y))
                self.naytto.blit(aloitus_teksti, aloitus_teksti_laatikko)
                rivi_y += 50
            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_x -200))
            pygame.display.flip()
            self.kello.tick(60)

    def piirra_elamat(self, fontti):
        elama = pygame.image.load("kolikko.png")
        elama = pygame.transform.scale(elama, (elama.get_width() * 0.5, elama.get_height() * 0.5))
        elamat_teksti = fontti.render(f"Elämät ", True, (255,255,255))
        elamat_laatikko = elamat_teksti.get_rect()
        elamat_laatikko.topleft = (10, 10)
        self.naytto.blit(elamat_teksti, elamat_laatikko)

        elama_x = elamat_laatikko.right +10
        elama_y = elamat_laatikko.top
        for i in range(self.robo_elamat):
            self.naytto.blit(elama, (elama_x, elama_y))
            elama_x += 30

    def piirra_havio(self):
        havio_fontti = pygame.font.Font(None, 30)
        havio_teksti = havio_fontti.render("Robo hajosi :(", True, (255,255,255))
        havio_teksti_laatikko = havio_teksti.get_rect(center=(self.nayton_leveys // 2, self.nayton_korkeus // 2))
        havio_teksti2 = havio_fontti.render("Paina F2 yrittääksesi uudelleen tai ESC lopettaaksesi", True, (255,255,255))
        havio_teksti2_laatikko = havio_teksti2.get_rect(center=(self.nayton_leveys // 2, self.nayton_korkeus // 2 + 50))
        self.naytto.fill((0,0,0))
        self.naytto.blit(havio_teksti, havio_teksti_laatikko)
        self.naytto.blit(havio_teksti2, havio_teksti2_laatikko)

    def piirra_voitto(self):
        voitto_fontti = pygame.font.Font(None, 30)
        voitto_teksti = voitto_fontti.render(f"Onneksi olkoon! Läpäisit pelin. Hirviöitä tuhottu {self.pisteet} ", True, (255,255,255))
        voitto_teksti_laatikko = voitto_teksti.get_rect(center=(self.nayton_leveys // 2, self.nayton_korkeus // 2))
        voitto_teksti2 = voitto_fontti.render("Paina F2 yrittääksesi uudelleen tai ESC lopettaaksesi", True, (255,255,255))
        voitto_teksti2_laatikko = voitto_teksti2.get_rect(center=(self.nayton_leveys // 2, self.nayton_korkeus // 2 + 50))
        self.naytto.fill((0,0,0))
        self.naytto.blit(voitto_teksti, voitto_teksti_laatikko)
        self.naytto.blit(voitto_teksti2, voitto_teksti2_laatikko)

    def pomo_generaattori(self):
        yield PomoHirvio(self.nayton_leveys, self.nayton_korkeus)
        
    def peli_silmukka(self):
        self.robo_elamat = 3
        self.voitto = False 
        hirvio_generaattori = (PikkuHirvio(self.nayton_leveys, self.nayton_korkeus) for _ in range(100))  #generaattorilla voin määrätä hirviöiden kokonaismäärän
        self.hirviot = [next(hirvio_generaattori) for _ in range(15)] #generoi halutun määrän hirviöitä kentälle
        pomo_generaattori = self.pomo_generaattori()
        kosketus_aika = 0

        while True:
            self.naytto.fill((100,100,100))
            self.piirra_elamat(self.fontti)
            self.tutki_tapahtumat()
            self.liiku_robo()

            miekan_isku = self.robo_miekka.miekan_sijainti()

            for hirvio in self.hirviot:
                if hirvio.hirviot_paallekkain(self.hirviot):
                    hirvio.x, hirvio.y = hirvio.luo_aloituspaikka()

                if self.osuuko_roboon(hirvio): #selvittää osuuko hirvio roboon ja vähentää hp:ta jos ei ole koskettu sekunnin sisällä
                    aika = pygame.time.get_ticks()
                    kuolemattomuus_aika = 1000
                    if aika - kuolemattomuus_aika > kosketus_aika:
                        self.robo_elamat -= 1
                        kosketus_aika = aika
                    if not isinstance(hirvio, PomoHirvio):
                        hirvio.x, hirvio.y = hirvio.luo_aloituspaikka()

                if miekan_isku and hirvio not in self.robo_miekka.osutut_hirviot:  #Miekkalyönti voi osua vain kerran per hirviö 
                    if hirvio.osuuko_hirvioon(miekan_isku):
                        hirvio.hp -= 1
                        self.robo_miekka.osutut_hirviot.append(hirvio)
                        hirvio.osuma_aika = 5
                    
                if hirvio.hp <= 0:
                    self.hirviot.remove(hirvio)
                    self.pisteet +=1
                    try:
                        self.hirviot.append(next(hirvio_generaattori)) #Pitää hirviö määrän samana, kun hirviöitä riittää.
                    except StopIteration:
                        pass

                if len(self.hirviot) == 0:
                    try:
                        self.hirviot.append(next(pomo_generaattori)) #Luo Pomon, kun viimeinen pikkuhirviö tuhoutuu
                    except StopIteration:
                       self.voitto = True

                if isinstance(hirvio, PomoHirvio): #Pomo hirvion käytös
                    hirvio.osuma_kuva(self.naytto)
                    hirvio.syoksy_seuraus(self.robo_keskipiste_x, self.robo_keskipiste_y)
                    if not hirvio.vaihe in {"tarisee","syoksyy"}:
                        hirvio.hirvio_suunta(self.robo_keskipiste_x, self.robo_keskipiste_y)
                        hirvio.liiku_hirvio()
          
                else:
                    self.naytto.blit(hirvio.kuva, (hirvio.x, hirvio.y))
                    hirvio.hirvio_suunta(self.robo_keskipiste_x, self.robo_keskipiste_y)
                    hirvio.liiku_hirvio()

            self.robo_miekka.robo_sijainti(self.robo_keskipiste_x, self.robo_keskipiste_y) #miekka seuraa roboa
            if miekan_isku:
                pygame.draw.line(self.naytto, (125, 249, 255), miekan_isku[0], miekan_isku[1], 4)
            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_y))
            if self.robo_elamat <= 0:
                self.piirra_havio()
            if self.voitto == True:
                self.piirra_voitto()
              
            pygame.display.flip()
            self.kello.tick(60)    

Robo_Survivor()