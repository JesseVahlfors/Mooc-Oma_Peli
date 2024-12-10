import pygame
import random

class Robo_Survivor:
    def __init__(self):
        pygame.init()

        self.nayton_leveys, self.nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))

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
        x, y, nopeus_x, nopeus_y = self.luo_aloituspaikka()

        hirvio_data = {
        "kuva": pygame.image.load("hirvio.png"),
        "x": x,
        "y": y,  
        "nopeus_x": nopeus_x,
        "nopeus_y": nopeus_y,  # Moves downward
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
            nopeus_x = 1
            nopeus_y = 0
        elif aloituspaikka == "oikea":
            x = random.randint(self.nayton_leveys, oikea_x)
            y = random.randint(0, self.nayton_korkeus - hirvio_kuva.get_height())
            nopeus_x = -1
            nopeus_y = 0
        elif aloituspaikka == "ylos":
            x = random.randint(0, self.nayton_leveys -hirvio_kuva.get_width())
            y = random.randint(yla_y, -1)
            nopeus_x = 0
            nopeus_y = 1
        elif aloituspaikka == "alas":
            x = random.randint(0, self.nayton_leveys -1)
            y = random.randint(self.nayton_korkeus, ala_y)
            nopeus_x = 0
            nopeus_y = -1

        return x, y, nopeus_x, nopeus_y
    

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_F2:
                    self.silmukka()
            if tapahtuma.type == pygame.QUIT:
                exit()
    
    def silmukka(self):   
        hirviot = [self.hirvio() for _ in range(10)]
        while True:
            uusi_x, uusi_y, uusi_nopeus_x, uusi_nopeus_y = self.luo_aloituspaikka()
            self.tutki_tapahtumat()
            self.naytto.fill((100,100,100))

            for hirvio in hirviot:    
                hirvio["y"] += hirvio["nopeus_y"]
                hirvio["x"] += hirvio["nopeus_x"]

                """ if self.hirvio_y >= self.nayton_korkeus - self.hirvio_kuva.get_width():
                    peli_loppu = True """
                if (hirvio["x"]<= self.robo_x + self.robo_kuva.get_width() and
                hirvio["x"] + hirvio["kuva"].get_width() >= self.robo_x and 
                hirvio["y"] <= self.robo_y + self.robo_kuva.get_width() and
                hirvio["y"] + hirvio["kuva"].get_height() >= self.robo_y):
                    hirvio["x"] = uusi_x
                    hirvio["y"] = uusi_y
                    hirvio["nopeus_x"] = uusi_nopeus_x
                    hirvio["nopeus_y"] = uusi_nopeus_y

            
                self.naytto.blit(hirvio["kuva"], (hirvio["x"], hirvio["y"]))

            self.naytto.blit(self.robo_kuva, (self.robo_x, self.robo_y))

            pygame.display.flip()
            self.kello.tick(60)    

Robo_Survivor()