
import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)
		return image
	def get_player(self, frame, width, height, scale, colour):
		border = (64 - width)/2
		vert_offset = 64-height
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, 
		(0, 0), 
		((border+frame*(width+2*border)), vert_offset, width, height)
		)
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)
		return image
	def get_icon(self,width,height,scale,colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), (0, 64*2, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)
		return image
	# def get_image(self, frame, width, height, scale, colour, border):
	# 	image = pygame.Surface((width, height)).convert_alpha()
	# 	# image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
	# 	image.blit(self.sheet, (border, border), ((frame * (width+(border*2)), 0, width, height)))
	# 	image = pygame.transform.scale(image, (width * scale, height * scale))
	# 	image.set_colorkey(colour)
	# 	return image