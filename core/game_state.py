# game_state.py
import pygame
from settings import (
    GRID_SIZE, GRID_COLS, GRID_ROWS,
    BAT_SPRITESHEET_PATH, BAT_ANIMATION_SPEED, BAT_SPRITE_NATIVE_WIDTH, BAT_SPRITE_NATIVE_HEIGHT, BAT_FLAP_FRAMES_COUNT,
    HUMAN_SPRITESHEET_PATH, HUMAN_ANIMATION_SPEED, HUMAN_SPRITE_NATIVE_WIDTH, HUMAN_SPRITE_NATIVE_HEIGHT,
    HUMAN_WALK_DOWN_FRAMES_COUNT, HUMAN_WALK_UP_FRAMES_COUNT, HUMAN_WALK_RIGHT_FRAMES_COUNT, HUMAN_ANIMATION_OFFSETS,
    RAT_SPRITESHEET_PATH, RAT_ANIMATION_SPEED, RAT_SPRITE_NATIVE_WIDTH, RAT_SPRITE_NATIVE_HEIGHT,
    RAT_ANIMATION_FRAMES_PER_DIRECTION, RAT_ANIMATION_ROW_OFFSETS
)

class GameState:
    def __init__(self, tile_properties_grid):
        self.tile_properties_grid = tile_properties_grid
        self.current_form = 'human'
        self.forms = ['human', 'bat', 'rat']
        self.player_grid_pos = (GRID_COLS // 2, GRID_ROWS // 2)
        self.player_pixel_pos = [0, 0]
        self.target_pos = None
        self.path = []
        self.is_moving = False
        self.current_target_pixel = None
        self.movement_speed = 8 * GRID_SIZE
        self._init_animation_attributes()
        self._load_all_sprites()
        self.reset_player_state()

    def _init_animation_attributes(self):
        self.bat_frames = []
        self.bat_animation_speed = BAT_ANIMATION_SPEED
        self.bat_current_frame_index = 0
        self.bat_animation_timer = 0.0
        self.human_animations = {}
        self.human_animation_speed = HUMAN_ANIMATION_SPEED
        self.human_current_animation_name = "idle_down"
        self.human_current_frame_index = 0
        self.human_animation_timer = 0.0
        self.human_facing_direction = "down"
        self.rat_animations = {}
        self.rat_animation_speed = RAT_ANIMATION_SPEED
        self.rat_current_animation_name = "idle_down"
        self.rat_current_frame_index = 0
        self.rat_animation_timer = 0.0
        self.rat_facing_direction = "down"

    def _load_all_sprites(self):
        self._load_bat_sprites()
        self._load_human_sprites()
        self._load_rat_sprites()

    def _load_bat_sprites(self):
        try:
            spritesheet = pygame.image.load(BAT_SPRITESHEET_PATH).convert_alpha()
            for i in range(BAT_FLAP_FRAMES_COUNT):
                rect = pygame.Rect(i * BAT_SPRITE_NATIVE_WIDTH, 0, BAT_SPRITE_NATIVE_WIDTH, BAT_SPRITE_NATIVE_HEIGHT)
                frame = spritesheet.subsurface(rect)
                self.bat_frames.append(pygame.transform.scale(frame, (GRID_SIZE, GRID_SIZE)))
            if not self.bat_frames: print(f"Warning: Bat sprites loaded 0 frames.")
        except Exception as e:
            print(f"Error loading bat sprites from '{BAT_SPRITESHEET_PATH}': {e}")

    def _load_human_sprites(self):
        try:
            spritesheet = pygame.image.load(HUMAN_SPRITESHEET_PATH).convert_alpha()
            configs = {
                "walk_down": (HUMAN_ANIMATION_OFFSETS["walk_down"], HUMAN_WALK_DOWN_FRAMES_COUNT),
                "walk_up": (HUMAN_ANIMATION_OFFSETS["walk_up"], HUMAN_WALK_UP_FRAMES_COUNT),
                "walk_right": (HUMAN_ANIMATION_OFFSETS["walk_right"], HUMAN_WALK_RIGHT_FRAMES_COUNT),
            }
            for name, ((r_offset, c_start), count) in configs.items():
                frames = []
                for i in range(count):
                    rect = pygame.Rect(
                        (c_start + i) * HUMAN_SPRITE_NATIVE_WIDTH, r_offset * HUMAN_SPRITE_NATIVE_HEIGHT,
                        HUMAN_SPRITE_NATIVE_WIDTH, HUMAN_SPRITE_NATIVE_HEIGHT
                    )
                    frame = spritesheet.subsurface(rect)
                    frames.append(pygame.transform.scale(frame, (GRID_SIZE, GRID_SIZE)))
                self.human_animations[name] = frames
            if "walk_right" in self.human_animations and self.human_animations["walk_right"]:
                self.human_animations["walk_left"] = [pygame.transform.flip(f, True, False) for f in self.human_animations["walk_right"]]
            else: print(f"Warning: 'walk_right' for human missing, cannot create 'walk_left'.")
            for direction in ["down", "up", "right", "left"]:
                if f"walk_{direction}" in self.human_animations and self.human_animations[f"walk_{direction}"]:
                    self.human_animations[f"idle_{direction}"] = [self.human_animations[f"walk_{direction}"][0]]
                else: print(f"Warning: 'walk_{direction}' for human missing, cannot create 'idle_{direction}'.")
            if not self.human_animations: print(f"Warning: Human animations dictionary is empty.")
            self.human_current_animation_name = f"idle_{self.human_facing_direction}" 
        except Exception as e:
            print(f"Error loading human sprites from '{HUMAN_SPRITESHEET_PATH}': {e}")

    def _load_rat_sprites(self):
        try:
            spritesheet = pygame.image.load(RAT_SPRITESHEET_PATH).convert_alpha()
            for direction_suffix, row_index in RAT_ANIMATION_ROW_OFFSETS.items():
                animation_name_walk = f"walk_{direction_suffix}"
                animation_name_idle = f"idle_{direction_suffix}"
                frames = []
                for i in range(RAT_ANIMATION_FRAMES_PER_DIRECTION):
                    rect = pygame.Rect(
                        i * RAT_SPRITE_NATIVE_WIDTH, row_index * RAT_SPRITE_NATIVE_HEIGHT,
                        RAT_SPRITE_NATIVE_WIDTH, RAT_SPRITE_NATIVE_HEIGHT
                    )
                    frame = spritesheet.subsurface(rect)
                    frames.append(pygame.transform.scale(frame, (GRID_SIZE, GRID_SIZE)))
                self.rat_animations[animation_name_walk] = frames
                if frames: self.rat_animations[animation_name_idle] = [frames[0]]
            if not self.rat_animations: print(f"Warning: Rat animations dictionary is empty.")
            self.rat_current_animation_name = f"idle_{self.rat_facing_direction}"
        except Exception as e:
            print(f"Error loading rat sprites from '{RAT_SPRITESHEET_PATH}': {e}")

    def find_walkable_position(self, form_to_check):
        walkable_key = f"{form_to_check}_walkable"
        for r, row_data in enumerate(self.tile_properties_grid):
            for c, tile_props in enumerate(row_data):
                if tile_props.get(walkable_key, False): return (c, r)
        print(f"Warning: No walkable start for '{form_to_check}'. Fallback.")
        return (GRID_COLS // 2, GRID_ROWS // 2)

    def reset_player_state(self):
        self.player_grid_pos = self.find_walkable_position(self.current_form)
        self.player_pixel_pos = [
            self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        ]
        self.cancel_movement()
        self._reset_current_form_animation_state()

    def _reset_current_form_animation_state(self):
        if self.current_form == 'bat':
            self.bat_current_frame_index = 0
            self.bat_animation_timer = 0.0
        elif self.current_form == 'human':
            self.human_facing_direction = "down"
            self.human_current_animation_name = "idle_down"
            self.human_current_frame_index = 0
            self.human_animation_timer = 0.0
        elif self.current_form == 'rat':
            self.rat_facing_direction = "down"
            self.rat_current_animation_name = "idle_down"
            self.rat_current_frame_index = 0
            self.rat_animation_timer = 0.0

    def set_form(self, new_form):
        if new_form in self.forms and self.current_form != new_form:
            print(f"Switching form: {self.current_form} -> {new_form}")
            self.current_form = new_form
            current_grid_x, current_grid_y = self.player_pos
            if not self.is_walkable(current_grid_x, current_grid_y):
                print(f"Warning: Pos ({current_grid_x},{current_grid_y}) not walkable for {new_form}. Relocating.")
                self.player_grid_pos = self.find_walkable_position(self.current_form)
                self.player_pixel_pos = [
                    self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
                    self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
                ]
            self.cancel_movement()
            self._reset_current_form_animation_state()
        elif new_form not in self.forms:
            print(f"Warning: Unknown form '{new_form}'.")

    def get_current_player_sprite(self):
        sprite = None
        try:
            if self.current_form == 'bat':
                if self.bat_frames: sprite = self.bat_frames[self.bat_current_frame_index]
            elif self.current_form == 'human':
                anim_frames = self.human_animations.get(self.human_current_animation_name)
                if anim_frames: sprite = anim_frames[self.human_current_frame_index]
            elif self.current_form == 'rat':
                anim_frames = self.rat_animations.get(self.rat_current_animation_name)
                if anim_frames: sprite = anim_frames[self.rat_current_frame_index]
        except IndexError:
            print(f"IndexError in get_current_player_sprite for {self.current_form}: anim='{getattr(self, f'{self.current_form}_current_animation_name', 'N/A')}', index={getattr(self, f'{self.current_form}_current_frame_index', 'N/A')}, frames_len={len(anim_frames) if 'anim_frames' in locals() and anim_frames else 'N/A'}")
            if self.current_form == 'human' and anim_frames: self.human_current_frame_index = 0 
            elif self.current_form == 'rat' and anim_frames: self.rat_current_frame_index = 0
            if anim_frames : sprite = anim_frames[0]

        if sprite is None:
            pass
        return sprite

    def _update_animation_logic(self, dt):
        """Inti logika update animasi untuk human dan rat."""
        form_attrs = None
        if self.current_form == 'bat':
            if not self.bat_frames: return
            self.bat_animation_timer += dt
            if self.bat_animation_timer >= self.bat_animation_speed:
                self.bat_animation_timer -= self.bat_animation_speed
                self.bat_current_frame_index = (self.bat_current_frame_index + 1) % len(self.bat_frames)
            return

        elif self.current_form == 'human':
            form_attrs = {
                "animations": self.human_animations, "current_name_attr": "human_current_animation_name",
                "frame_index_attr": "human_current_frame_index", "timer_attr": "human_animation_timer",
                "speed": self.human_animation_speed, "facing_direction": self.human_facing_direction
            }
        elif self.current_form == 'rat':
            form_attrs = {
                "animations": self.rat_animations, "current_name_attr": "rat_current_animation_name",
                "frame_index_attr": "rat_current_frame_index", "timer_attr": "rat_animation_timer",
                "speed": self.rat_animation_speed, "facing_direction": self.rat_facing_direction
            }
        
        if not form_attrs or not form_attrs["animations"]: return

        current_anim_name_on_attr = getattr(self, form_attrs["current_name_attr"])
        
        base_anim_type = "walk" if self.is_moving else "idle"
        desired_anim_name = f"{base_anim_type}_{form_attrs['facing_direction']}"

        if desired_anim_name not in form_attrs["animations"]:
            desired_anim_name = f"idle_down" 
            if desired_anim_name not in form_attrs["animations"]:
                return
        
        if current_anim_name_on_attr != desired_anim_name:
            setattr(self, form_attrs["frame_index_attr"], 0)
            setattr(self, form_attrs["timer_attr"], 0.0)
        
        setattr(self, form_attrs["current_name_attr"], desired_anim_name)
        
        animation_frames = form_attrs["animations"].get(desired_anim_name, [])
        if not animation_frames: 
            return

        current_timer = getattr(self, form_attrs["timer_attr"])
        new_timer = current_timer + dt
        
        current_frame_idx = getattr(self, form_attrs["frame_index_attr"])
        new_frame_idx = current_frame_idx

        if new_timer >= form_attrs["speed"]:
            new_timer -= form_attrs["speed"]
            new_frame_idx = (current_frame_idx + 1) % len(animation_frames)
        
        setattr(self, form_attrs["timer_attr"], new_timer)
        setattr(self, form_attrs["frame_index_attr"], new_frame_idx)

    def update_player_position(self, dt):
        if self.is_moving and self.current_target_pixel:
            dx = self.current_target_pixel[0] - self.player_pixel_pos[0]
            dy = self.current_target_pixel[1] - self.player_pixel_pos[1]
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                new_dir = ""
                if abs(dx) > abs(dy): new_dir = "right" if dx > 0 else "left"
                else: new_dir = "down" if dy > 0 else "up"
                
                if self.current_form == 'human' and self.human_facing_direction != new_dir:
                    self.human_facing_direction = new_dir
                    self.human_current_frame_index = 0
                elif self.current_form == 'rat' and self.rat_facing_direction != new_dir:
                    self.rat_facing_direction = new_dir
                    self.rat_current_frame_index = 0
        
        self._update_animation_logic(dt)

        if not self.is_moving and not self.path: return
        if not self.is_moving and self.path:
            next_pos = self.path[0]
            if not self.is_walkable(next_pos[0], next_pos[1]):
                self.cancel_movement(); print(f"Path Error: Next {next_pos} not walkable for {self.current_form}.")
                return
            self.current_target_pixel = (next_pos[0]*GRID_SIZE+GRID_SIZE//2, next_pos[1]*GRID_SIZE+GRID_SIZE//2)
            self.is_moving = True

        if self.is_moving and self.current_target_pixel:
            dx_target = self.current_target_pixel[0] - self.player_pixel_pos[0]
            dy_target = self.current_target_pixel[1] - self.player_pixel_pos[1]
            dist = (dx_target**2 + dy_target**2)**0.5
            if dist < max(2, self.movement_speed * dt * 0.6): # Toleransi pencapaian
                self.player_pixel_pos = list(self.current_target_pixel)
                self.player_grid_pos = self.player_pos
                if self.path: self.path.pop(0)
                if not self.path:
                    self.is_moving = False; self.target_pos = None; self.current_target_pixel = None
                    self._update_animation_logic(0) # Update ke idle
                else:
                    next_pos = self.path[0]
                    if not self.is_walkable(next_pos[0], next_pos[1]):
                        self.cancel_movement(); print(f"Path Error: Next {next_pos} not walkable (mid-path).")
                        return
                    self.current_target_pixel = (next_pos[0]*GRID_SIZE+GRID_SIZE//2, next_pos[1]*GRID_SIZE+GRID_SIZE//2)
            else:
                if dist > 0:
                    self.player_pixel_pos[0] += (dx_target / dist) * self.movement_speed * dt
                    self.player_pixel_pos[1] += (dy_target / dist) * self.movement_speed * dt
                
    def is_walkable(self, x, y):
        if not (0 <= y < len(self.tile_properties_grid) and 0 <= x < len(self.tile_properties_grid[0])): return False
        return self.tile_properties_grid[y][x].get(f"{self.current_form}_walkable", False)

    @property
    def player_pos(self):
        return (int(self.player_pixel_pos[0]//GRID_SIZE), int(self.player_pixel_pos[1]//GRID_SIZE))

    def cancel_movement(self):
        self.path = []; self.target_pos = None; self.is_moving = False; self.current_target_pixel = None
        self._update_animation_logic(0)