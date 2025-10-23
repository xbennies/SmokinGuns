from gun import Gun

PISTOL = Gun(name="Pistol",
            cooldown=300,
            bullet_speed = 10,
            bullet_lifetime = 800,
            bullet_size = (4, 10),
            bullet_color = (255,255,0))

SHOTGUN = Gun(name="Shotgun",
            cooldown=800,
            bullet_speed = 12,
            bullet_lifetime = 300,
            bullet_size = (8, 8),
            bullet_color = (200,200,0))

RIFLE = Gun(name="Rifle",
            cooldown=100,
            bullet_speed = 15,
            bullet_lifetime = 1200,
            bullet_size = (3, 12),
            bullet_color = (255,165,0))