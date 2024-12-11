import pygame
import random

class Robo_Survivor:
    def __init__(self):
        pygame.init()

        self.nayton_leveys, self.nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))

        self.liikkeet = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False,}
        self.nopeus = 2

        pygame.display.set_caption("Robo Survivor")

        self.kello = pygame.time.Clock()

        self.robo()
        self.silmukka()

    def robo(self):
        self.robo_kuva = pygame.image.load("robo.png")
        self.robo_x = 320 - self.robo_kuva.get_width()/2
        self.robo_y = 240 - self.robo_kuva.get_height()/2
        self.robo_suunta = (0,0)

    def hirvio(self):
        x, y = self.luo_aloituspaikka()

        hirvio_data = {
        "kuva": pygame.image.load("hirvio.png"),
        "x": x,
        "y": y,  
        "nopeus_x": 0,
        "nopeus_y": 0,  # Moves downward
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
            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku_robo(self):
        if self.liikkeet[pygame.K_LEFT]:
            self.robo_x -= self.nopeus
        if self.liikkeet[pygame.K_RIGHT]:
            self.robo_x += self.nopeus
        if self.liikkeet[pygame.K_UP]:
            self.robo_y -= self.nopeus
        if self.liikkeet[pygame.K_DOWN]:
            self.robo_y += self.nopeus
        


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
        hirviot = [self.hirvio() for _ in range(10)]
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
            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_y))
            pygame.display.flip()
            self.kello.tick(60)    

Robo_Survivor()