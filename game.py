import pygame

#image_path = '/data/data/com.Muhammed.myapp/files/app/'

clock = pygame.time.Clock()


pygame.init()
screen = pygame.display.set_mode((888,500))#, flags=pygame.NOFRAME)
pygame.display.set_caption('Pygame for OneCode')
icon = pygame.image.load('Media/icon.png').convert_alpha()
pygame.display.set_icon(icon)
backgraund = pygame.image.load('Media/backgraund main.png').convert_alpha()


#Player
hero_left = [
	pygame.image.load("Media/Player/Left/1.png").convert_alpha(),
	pygame.image.load('Media/Player/Left/2.png').convert_alpha(),
	pygame.image.load('Media/Player/Left/3.png').convert_alpha(),
	pygame.image.load('Media/Player/Left/4.png').convert_alpha()]
hero_right = [
	pygame.image.load('Media/Player/Right/1.png').convert_alpha(),
	pygame.image.load('Media/Player/Right/2.png').convert_alpha(),
	pygame.image.load('Media/Player/Right/3.png').convert_alpha(),
	pygame.image.load('Media/Player/Right/4.png').convert_alpha()]

player_speed = 9
player_x = 50
player_y = 360

#Jump
is_jump = False
jump_count = 8

#Music
pygame.mixer.music.load("sound/main.mp3")
pygame.mixer.music.play(-1)
game_over_sound = pygame.mixer.Sound('sound/Game Over.mp3')
over_sound = True

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

#Fonts
label_black = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
label_bold = pygame.font.Font('fonts/Roboto-Bold.ttf', 60)
label_bold_quit = pygame.font.Font('fonts/Roboto-Bold.ttf', 30)
label_bull =  pygame.font.Font('fonts/Roboto-Bold.ttf', 20)

#Надпись
lose_label = label_black.render('Game Over', False, (193,196,199))
restart_label = label_bold.render('Restart', False, (253,0,0))
quit_label = label_bold_quit.render('quit', True, (0,0,0))

restart_label_rect = restart_label.get_rect(topleft=(340, 200))
quit_label_rect = quit_label.get_rect(topleft=(400, 300))

#Bullets
bullets_left = 5
bullet = pygame.image.load('Media/arrow.png').convert_alpha()
bullets = []
bul_sum = pygame.image.load('Media/arrow x.png').convert_alpha()

#Ghosts
ghost = pygame.image.load('Media/ghost.png').convert_alpha()
ghost_list_in_game = []

cadr = 0
bg_x = 0

hero_st = 'right'

gameplay = True

running = True
while running:
	
	screen.blit(backgraund, (bg_x,0))
	screen.blit(backgraund, (bg_x + 888,0))
	screen.blit(bul_sum, (0,0))

	mouse = pygame.mouse.get_pos()
	

	if gameplay:
		_x_ = label_black.render(str(bullets_left), False, (255,0,0))
		screen.blit(_x_, (57, 10))
		player_react = hero_left[0].get_rect(topleft=(player_x, player_y))

		if ghost_list_in_game:
			for (i, el) in enumerate(ghost_list_in_game):
				screen.blit(ghost, el)
				el.x -= 10

				if el.x < -10:
					ghost_list_in_game.pop(i)
					bullets_left += 1

				if player_react.colliderect(el):
					gameplay = False


		keys = pygame.key.get_pressed()

	

		if keys[pygame.K_LEFT] and player_x > 5:
			hero_st = 'left'
			player_x -= player_speed
		elif keys[pygame.K_RIGHT] and player_x < 835:
			hero_st = 'right'
			player_x += player_speed
	
		if hero_st == 'left':
			screen.blit(hero_left[cadr], (player_x,player_y))
		elif hero_st == 'right':
			screen.blit(hero_right[cadr], (player_x,player_y))
	
		if not is_jump:
			if keys[pygame.K_UP]:
				is_jump = True
		else:
			if jump_count >= -8:
				if jump_count > 0:
					player_y -= (jump_count ** 2) / 2
				else:
					player_y += (jump_count ** 2) / 2
				jump_count -= 1
			else:
				is_jump = False
				jump_count = 8


		if cadr == 3:
				cadr = 0
		else:
			cadr += 1

		bg_x -= 2
		if bg_x == -888:
			bg_x = 0

		

		if bullets:
			for (i, el) in enumerate(bullets):
				screen.blit(bullet, (el.x, el.y))
				el.x += 15
				if el.x > 888:
					bullets.pop(i)

				if ghost_list_in_game:
					for (index, ghost_el) in enumerate(ghost_list_in_game):
						if el.colliderect(ghost_el):
							ghost_list_in_game.pop(index)
							bullets.pop(i)


	else:
		pygame.mixer.music.stop()

		screen.fill((87, 88, 89))
		screen.blit(lose_label, (340,100))
		screen.blit(restart_label, restart_label_rect)
		screen.blit(quit_label, quit_label_rect)

		if over_sound:
			game_over_sound.play()
			over_sound = False

		#mouse = pygame.mouse.get_pos()
		if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
			gameplay = True
			player_x = 50
			ghost_list_in_game.clear()
			pygame.mixer.music.play(-1)
			over_sound = True
			bullets.clear()
			bullets_left = 5
		elif quit_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
			pygame.quit()
			break
		
	pygame.display.update()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
		if event.type == ghost_timer:
			ghost_list_in_game.append(ghost.get_rect(topleft=(800,360)))
		if gameplay and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bullets_left > 0:
			bullets.append(bullet.get_rect(topleft=(player_x + 45, player_y + 15)))
			bullets_left -= 1

	if running == False:
		break
	clock.tick(15)
