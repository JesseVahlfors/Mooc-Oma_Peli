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

    def robo_sijainti(self, robo_x, robo_y):
        self.robo_x = robo_x
        self.robo_y = robo_y

    def luo_lyonti(self, kulma):
        miekan_rata = math.pi / 2
        self.kulma = kulma
        self.kulma_alku = kulma - miekan_rata / 2
        self.lyonti_paalla = True
        self.kulma_loppu = kulma + miekan_rata /2

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

    def luo_aloituspaikka(self):
        #kuvan ulkopuoliset koordinaatit
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
    
    def hirvio_suunta(self, robo_keskipiste_x, robo_keskipiste_y):
        hirvio_keskipiste_x = self.x + self.kuva.get_width()/2
        hirvio_keskipiste_y = self.y + self.kuva.get_height()/2

        if robo_keskipiste_x < hirvio_keskipiste_x:
            self.nopeus_x = -1
        elif robo_keskipiste_x > hirvio_keskipiste_x:
            self.nopeus_x = 1
        else:
            self.nopeus_x = 0

        if robo_keskipiste_y < hirvio_keskipiste_y:
            self.nopeus_y = -1
        elif robo_keskipiste_y > hirvio_keskipiste_y:
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

class PikkuHirvio(Hirvio):
    def __init__(self, nayton_leveys, nayton_korkeus):
        super().__init__(nayton_leveys, nayton_korkeus)
        self.kuva = pygame.transform.scale(self.kuva, (self.kuva.get_width() * 0.6, self.kuva.get_height() * 0.6))


class Robo_Survivor:
    def __init__(self):
        pygame.init()

        self.nayton_leveys, self.nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))

        #Kirja liike tapahtumille ja robon nopeus
        self.liikkeet = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False,}
        self.robo_nopeus = 3

        pygame.display.set_caption("Robo Survivor")

        self.kello = pygame.time.Clock()

        self.robo()
        self.robo_miekka = RoboMiekka(self.robo_keskipiste_x, self.robo_keskipiste_y)
        self.silmukka()

    def robo(self):
        kuva = pygame.image.load("robo.png")
        self.robo_kuva = pygame.transform.scale(kuva, (kuva.get_width() * 0.6, kuva.get_height() * 0.6))
        self.robo_x = 320 - self.robo_kuva.get_width()/2 #robon aloituspiste keskelle ruutua
        self.robo_y = 240 - self.robo_kuva.get_height()/2
        self.robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2
        self.robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key in self.liikkeet:
                    self.liikkeet[tapahtuma.key] = True
                if tapahtuma.key == pygame.K_F2:
                    self.silmukka()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key in self.liikkeet:
                    self.liikkeet[tapahtuma.key] = False
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #laskee kulman hiiren ja robon välille
                kulma = math.atan2(mouse_y - self.robo_keskipiste_y, mouse_x - self.robo_keskipiste_x)
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
        #päivittää keskipisteen kun robo liikkuu
        self.robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2
        self.robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2
        
    
    def osuuko_roboon(self, hirvio):
        if (
            hirvio.x <= self.robo_x + self.robo_kuva.get_width() and
            hirvio.x + hirvio.kuva.get_width() >= self.robo_x and 
            hirvio.y <= self.robo_y + self.robo_kuva.get_height() and
            hirvio.y + hirvio.kuva.get_height() >= self.robo_y
        ):
            return True
        return False
        
    def osuuko_hirvioon(self, miekan_isku, hirvio):
        if miekan_isku != None:
            alku_x, alku_y  = miekan_isku[0]
            loppu_x, loppu_y = miekan_isku[1]
            keski_x = (alku_x + loppu_x) /2
            keski_y = (alku_y + loppu_y) /2
            if (hirvio.x < loppu_x < hirvio.x + hirvio.kuva.get_width() and
                hirvio.y < loppu_y < hirvio.y + hirvio.kuva.get_height()):
                return True
            if (hirvio.x < alku_x < hirvio.x + hirvio.kuva.get_width() and
                hirvio.y < alku_y < hirvio.y + hirvio.kuva.get_height()):
                return True
            if (hirvio.x < keski_x < hirvio.x + hirvio.kuva.get_width() and
                hirvio.y < keski_y < hirvio.y + hirvio.kuva.get_height()):
                return True
        return False
    
    def silmukka(self):   
        self.hirviot = [PikkuHirvio(self.nayton_leveys, self.nayton_korkeus) for _ in range(15)]
        while True:
            self.tutki_tapahtumat()
            self.liiku_robo()
            self.naytto.fill((100,100,100))
            miekan_isku = self.robo_miekka.miekan_sijainti()
            for hirvio in self.hirviot:
                hirvio.hirvio_suunta(self.robo_keskipiste_x, self.robo_keskipiste_y)
                hirvio.liiku_hirvio()

                if hirvio.hirviot_paallekkain(self.hirviot):
                    hirvio.x, hirvio.y = hirvio.luo_aloituspaikka()

                if self.osuuko_roboon(hirvio):
                    hirvio.x, hirvio.y = hirvio.luo_aloituspaikka()
                    
                if self.osuuko_hirvioon(miekan_isku, hirvio):
                    hirvio.x, hirvio.y = hirvio.luo_aloituspaikka()

                self.naytto.blit(hirvio.kuva, (hirvio.x, hirvio.y))
                
            self.robo_miekka.robo_sijainti(self.robo_keskipiste_x, self.robo_keskipiste_y)
            if miekan_isku:
                pygame.draw.line(self.naytto, (255, 255, 255), miekan_isku[0], miekan_isku[1], 3)
            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_y))
            pygame.display.flip()
            self.kello.tick(60)    

Robo_Survivor()