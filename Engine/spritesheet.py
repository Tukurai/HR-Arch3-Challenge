import pygame
import xml.etree.ElementTree as ET


class Spritesheet:
    def __init__(self, filename, mask_layer_amount=0):
        self.file_name = filename
        self.sprite_sheet = self.load_sprite_sheet(filename)
        self.mask_layers = self.load_mask_layers(mask_layer_amount)
        self.sprite_atlas = self.load_atlas()

    def load_sprite_sheet(self, filename):
        print(f"Loaded [Spritesheet]:  {filename}")
        return pygame.image.load(filename).convert()

    def load_mask_layers(self, mask_layers_amount=1) -> dict[int, pygame.Surface]:
        mask_layers = {}
        for layer in range(mask_layers_amount):
            mask_file_name = self.file_name.replace(".png", f"_mask{layer}.png")
            mask_layers[layer] = pygame.image.load(mask_file_name).convert()
            print(f"Loaded [Mask Layer] :  {mask_file_name}")
        return mask_layers

    def load_atlas(self) -> dict:
        # Atlas XML has same base name as spritesheet
        tree = ET.parse(self.file_name.replace("png", "xml"))

        # Extract sprite data from XML Tree
        atlas = {}
        root = tree.getroot()
        for subtexture in root.findall("SubTexture"):
            name = subtexture.get("name")
            x = int(subtexture.get("x"))
            y = int(subtexture.get("y"))
            width = int(subtexture.get("width"))
            height = int(subtexture.get("height"))

            # Resulting atlas shape
            atlas[name] = {"x": x, "y": y, "w": width, "h": height}
        return atlas

    def create_sprite_from_sheet(self, x, y, w, h, sheet):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(sheet, (0, 0), (x, y, w, h))
        return sprite

    def get_sprite(self, name):
        x, y, w, h = self.find_sprite_coordinates(name)
        image = self.create_sprite_from_sheet(x, y, w, h, self.sprite_sheet)
        return image

    def get_mask_from_layer(self, name, mask_layer):
        x, y, w, h = self.find_sprite_coordinates(name)
        mask = self.create_sprite_from_sheet(x, y, w, h, self.mask_layers[mask_layer])
        return mask

    def get_mask_from_all_layers(self, name) -> dict:
        masks = {}
        if len(self.mask_layers) > 0:
            for layer in self.mask_layers:
                masks[layer] = self.get_mask_from_layer(name, layer)
        return masks

    def find_sprite_coordinates(self, name):
        sprite_cords = self.sprite_atlas[name]
        return (
            sprite_cords["x"],
            sprite_cords["y"],
            sprite_cords["w"],
            sprite_cords["h"],
        )


if __name__ == "__main__":
    pygame.init()
    DISPLAY_W, DISPLAY_H = 800, 300
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
    pygame.display.set_caption("Asphalt Carousel")
    running = True

    loaded_spritesheet = Spritesheet(
        "../Assets/Sprites/spritesheet_tiles.png", mask_layer_amount=1
    )
    names = [
        "road_asphalt01.png",
        "road_asphalt02.png",
        "road_asphalt03.png",
        "road_asphalt04.png",
        "road_asphalt05.png",
        "road_asphalt06.png",
        "road_asphalt07.png",
        "road_asphalt08.png",
        "road_asphalt09.png",
        "road_asphalt10.png",
        "road_asphalt11.png",
        "road_asphalt12.png",
        "road_asphalt13.png",
        "road_asphalt14.png",
        "road_asphalt15.png",
        "road_asphalt16.png",
        "road_asphalt17.png",
        "road_asphalt18.png",
        "road_asphalt19.png",
        "road_asphalt20.png",
        "road_asphalt21.png",
        "road_asphalt22.png",
        "road_asphalt23.png",
        "road_asphalt24.png",
        "road_asphalt25.png",
        "road_asphalt26.png",
        "road_asphalt27.png",
        "road_asphalt28.png",
        "road_asphalt29.png",
        "road_asphalt30.png",
        "road_asphalt31.png",
        "road_asphalt32.png",
        "road_asphalt33.png",
        "road_asphalt34.png",
        "road_asphalt35.png",
        "road_asphalt36.png",
        "road_asphalt37.png",
        "road_asphalt38.png",
        "road_asphalt39.png",
        "road_asphalt40.png",
        "road_asphalt41.png",
        "road_asphalt42.png",
        "road_asphalt43.png",
        "road_asphalt44.png",
        "road_asphalt45.png",
        "road_asphalt46.png",
        "road_asphalt47.png",
        "road_asphalt48.png",
        "road_asphalt49.png",
        "road_asphalt50.png",
        "road_asphalt51.png",
        "road_asphalt52.png",
        "road_asphalt53.png",
        "road_asphalt54.png",
        "road_asphalt55.png",
        "road_asphalt56.png",
        "road_asphalt57.png",
        "road_asphalt58.png",
        "road_asphalt59.png",
        "road_asphalt60.png",
        "road_asphalt61.png",
        "road_asphalt62.png",
        "road_asphalt63.png",
        "road_asphalt64.png",
        "road_asphalt65.png",
        "road_asphalt66.png",
        "road_asphalt67.png",
        "road_asphalt68.png",
        "road_asphalt69.png",
        "road_asphalt70.png",
        "road_asphalt71.png",
        "road_asphalt72.png",
        "road_asphalt73.png",
        "road_asphalt74.png",
        "road_asphalt75.png",
        "road_asphalt76.png",
        "road_asphalt77.png",
        "road_asphalt78.png",
        "road_asphalt79.png",
        "road_asphalt80.png",
        "road_asphalt81.png",
        "road_asphalt82.png",
        "road_asphalt83.png",
        "road_asphalt84.png",
        "road_asphalt85.png",
        "road_asphalt86.png",
        "road_asphalt87.png",
        "road_asphalt88.png",
        "road_asphalt89.png",
        "road_asphalt90.png",
    ]

    # Populate sprites
    asphalt_road_sprites = []
    for name in names:
        asphalt_road_sprites.append(loaded_spritesheet.get_sprite(name))

    # Populate masks
    asphalt_road_masks = []
    for name in names:
        asphalt_road_masks.append(loaded_spritesheet.get_mask_from_layer(name, 0))

    index = 0

    # --------- Text properties
    # Font and size
    font = pygame.font.Font(None, 56)
    # Color
    text_color = (255, 255, 255)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    index = (index + 1) % len(asphalt_road_sprites)
                if event.key == pygame.K_BACKSPACE:
                    index = (index - 1) % len(asphalt_road_sprites)

        # Make white background
        canvas.fill((0, 0, 0))
        # Place road sprite
        canvas.blit(asphalt_road_sprites[index], (50, DISPLAY_H - 200))
        # Place mask sprite
        canvas.blit(asphalt_road_masks[index], (200, DISPLAY_H - 200))

        # Get text and render it
        name_text_surface = font.render(names[index], True, text_color)
        instruction_text_surface = font.render(
            "Press spacebar to check names", True, text_color
        )
        # Place text on canvas
        canvas.blit(name_text_surface, (370, 100))
        canvas.blit(instruction_text_surface, (50, 250))

        window.blit(canvas, (0, 0))
        pygame.display.update()
