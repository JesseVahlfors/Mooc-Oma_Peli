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
        self.kulma = kulma - miekan_rata / 2
        self.lyonti_paalla = True
        self.kulma_loppu = kulma + miekan_rata /2

    def miekan_sijainti(self):
        if self.lyonti_paalla:
            self.kulma += 0.1
            if self.kulma > self.kulma_loppu:
                self.lyonti_paalla = False
                return None
            miekan_alku_x = self.robo_x + (self.halkaisija -50) * math.cos(self.kulma)
            miekan_alku_y = self.robo_y + (self.halkaisija -50) * math.sin(self.kulma)
            miekan_paa_x = self.robo_x + self.halkaisija * math.cos(self.kulma)
            miekan_paa_y = self.robo_y + self.halkaisija * math.sin(self.kulma)
            
            return (miekan_alku_x , miekan_alku_y), (miekan_paa_x, miekan_paa_y)
        
        return None


class Robo_Survivor:
    def __init__(self):
        pygame.init()

        self.nayton_leveys, self.nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        #Kirja liike tapahtumille ja robon nopeus
        self.liikkeet = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False,}
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


    def hirvio(self):
        x, y = self.luo_aloituspaikka()
        kuva = pygame.image.load("hirvio.png")
        hirvio_data = {
        "kuva": pygame.transform.scale(kuva, (kuva.get_width() * 0.6, kuva.get_height() * 0.6)),
        "x": x,
        "y": y,  
        "nopeus_x": 0,
        "nopeus_y": 0,
        }
        return hirvio_data

    def luo_aloituspaikka(self):
        hirvio_kuva = pygame.image.load("hirvio.png")
        #kuvan ulkopuoliset koordinaatit
        vasen_x = -100
        oikea_x = self.nayton_leveys + 100
        yla_y = -100
        ala_y = self.nayton_korkeus + 100

        aloituspaikka = random.choice(["vasen", "oikea", "ylos", "alas"])

        if aloituspaikka == "vasen":
            x = random.randint(vasen_x, -1)
            y = random.randint(0, self.nayton_korkeus - hirvio_kuva.get_height())
        elif aloituspaikka == "oikea":
            x = random.randint(self.nayton_leveys, oikea_x)
            y = random.randint(0, self.nayton_korkeus - hirvio_kuva.get_height())
        elif aloituspaikka == "ylos":
            x = random.randint(0, self.nayton_leveys -hirvio_kuva.get_width())
            y = random.randint(yla_y, -1)
        elif aloituspaikka == "alas":
            x = random.randint(0, self.nayton_leveys -1)
            y = random.randint(self.nayton_korkeus, ala_y)

        return x, y
    

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
                kulma = math.atan2(mouse_y - self.robo_keskipiste_y, mouse_x - self.robo_keskipiste_x)
                self.robo_miekka.luo_lyonti(kulma)

            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku_robo(self):
        if self.liikkeet[pygame.K_LEFT]:
            self.robo_x -= self.robo_nopeus
        if self.liikkeet[pygame.K_RIGHT]:
            self.robo_x += self.robo_nopeus
        if self.liikkeet[pygame.K_UP]:
            self.robo_y -= self.robo_nopeus
        if self.liikkeet[pygame.K_DOWN]:
            self.robo_y += self.robo_nopeus

        self.robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2
        self.robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2
        
        


    def hirvio_suunta(self, hirvio):
        robo_keskipiste_x = self.robo_x + self.robo_kuva.get_width()/2
        robo_keskipiste_y = self.robo_y + self.robo_kuva.get_height()/2
        hirvio_keskipiste_x = hirvio["kuva"].get_width()/2
        hirvio_keskipiste_y = hirvio["kuva"].get_height()/2
        suunta_x = 0
        suunta_y = 0

        if robo_keskipiste_x < hirvio["x"] + hirvio_keskipiste_x:
            suunta_x = -1
        elif robo_keskipiste_x > hirvio["x"] + hirvio_keskipiste_x:
            suunta_x = 1
        else:
            suunta_x = 0

        if robo_keskipiste_y < hirvio["y"] + hirvio_keskipiste_y:
            suunta_y = -1
        elif robo_keskipiste_y > hirvio["y"] + hirvio_keskipiste_y:
            suunta_y = 1
        else:
            suunta_y = 0
        
        return suunta_x, suunta_y
        
    
        
    
    def silmukka(self):   
        hirviot = [self.hirvio() for _ in range(15)]
        while True:
            uusi_x, uusi_y = self.luo_aloituspaikka()
            self.tutki_tapahtumat()
            self.liiku_robo()
            self.naytto.fill((100,100,100))

            for hirvio in hirviot:
                hirvio["nopeus_x"], hirvio["nopeus_y"]  = self.hirvio_suunta(hirvio)    
                hirvio["y"] += hirvio["nopeus_y"]
                hirvio["x"] += hirvio["nopeus_x"]

                """ if self.hirvio_y >= self.nayton_korkeus - self.hirvio_kuva.get_width():
                    peli_loppu = True """
                if (hirvio["x"]<= self.robo_x + self.robo_kuva.get_width() and
                hirvio["x"] + hirvio["kuva"].get_width() >= self.robo_x and 
                hirvio["y"] <= self.robo_y + self.robo_kuva.get_height() and
                hirvio["y"] + hirvio["kuva"].get_height() >= self.robo_y):
                    hirvio["x"] = uusi_x
                    hirvio["y"] = uusi_y

                
                self.naytto.blit(hirvio["kuva"], (hirvio["x"], hirvio["y"]))
            
            self.robo_miekka.robo_sijainti(self.robo_keskipiste_x, self.robo_keskipiste_y)
            miekan_isku = self.robo_miekka.miekan_sijainti()
            if miekan_isku:
                pygame.draw.line(self.naytto, (255, 255, 255), miekan_isku[0], miekan_isku[1], 3)
            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_y))
            pygame.display.flip()
            self.kello.tick(60)    

Robo_Survivor()