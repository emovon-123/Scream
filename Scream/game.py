"""
Scream - Voice-Controlled Side-Scrolling Jumping Game
Control character jumping with voice or spacebar
"""

import pygame
import sys
import numpy as np
from typing import Tuple, List
import os

# Try importing PyAudio
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    print("Warning: PyAudio not installed, voice control unavailable")
    print("Game will use keyboard control (Spacebar)")
    AUDIO_AVAILABLE = False
    # Create virtual pyaudio constants
    class FakePyAudio:
        paInt16 = 16
    pyaudio = type('obj', (object,), {'paInt16': 16})

# Game configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 5
PIPE_GAP = 200
PIPE_WIDTH = 80
GROUND_HEIGHT = 50

# Sound detection configuration
CHUNK = 1024
try:
    FORMAT = pyaudio.paInt16
except:
    FORMAT = 16
CHANNELS = 1
RATE = 44100
SOUND_THRESHOLD = 300  # Sound threshold (much lower for easier triggering)
SILENT_TIME = 5  # Silent time (frames)

# Colors (black and white style)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


class Bird:
    """Player character"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.velocity = 0
        self.width = 60
        self.height = 60
        self.alive = True
        self.rotation = 0
        
        # GIF animation related
        self.frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5  # Animation playback speed
        
        # Try loading character GIF
        try:
            gif_path = "Character/sheets/DinoSprites_vita.gif"
            if os.path.exists(gif_path):
                from PIL import Image, ImageSequence
                # Use PIL to read GIF
                img = Image.open(gif_path)
                for frame in ImageSequence.Iterator(img):
                    # Convert to RGBA mode
                    frame = frame.convert('RGBA')
                    # Convert to pygame Surface
                    frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, 'RGBA')
                    # Scale
                    frame_surface = pygame.transform.scale(frame_surface, (60, 60))
                    self.frames.append(frame_surface)
                print(f"Successfully loaded {len(self.frames)} frame GIF animation")
        except Exception as e:
            print(f"Failed to load character GIF: {e}")
            self.frames = []
        
        # Try loading shadow
        try:
            shadow_path = "Character/misc/shadow_2.png"
            if os.path.exists(shadow_path):
                self.shadow = pygame.image.load(shadow_path)
                self.shadow = pygame.transform.scale(self.shadow, (40, 15))
            else:
                self.shadow = None
        except:
            self.shadow = None
    
    def update(self, volume_normalized=0.0):
        """Update character position
        
        Args:
            volume_normalized: Normalized volume value between 0-1
        """
        if volume_normalized > 0:
            # When sound exists, move upward based on normalized volume
            # volume_normalized range is 0-2, used directly to control height
            self.velocity = -volume_normalized * 8  # Higher volume = faster upward movement
        else:
            # No sound = normal gravity falling
            self.velocity += GRAVITY
        
        self.y += self.velocity
        
        # Update GIF animation
        if self.frames:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
        
        # Boundary check
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        
        if self.y + self.height > WINDOW_HEIGHT - GROUND_HEIGHT:
            self.y = WINDOW_HEIGHT - GROUND_HEIGHT - self.height
            self.alive = False
    
    def jump(self):
        """Jump"""
        self.velocity = JUMP_STRENGTH
    
    def draw(self, screen):
        """Draw character"""
        # Draw shadow
        if self.shadow:
            shadow_y = WINDOW_HEIGHT - GROUND_HEIGHT - 20
            screen.blit(self.shadow, (self.x + 10, shadow_y))
        
        # If GIF animation exists, draw current frame (no rotation)
        if self.frames:
            current_sprite = self.frames[self.current_frame]
            screen.blit(current_sprite, (self.x, self.y))
        else:
            # Fallback: draw white circle
            pygame.draw.circle(screen, WHITE, (int(self.x + self.width/2), 
                                                int(self.y + self.height/2)), 
                              self.width // 2)
            # Add eyes
            pygame.draw.circle(screen, BLACK, (int(self.x + self.width/2 - 8), 
                                               int(self.y + self.height/2 - 8)), 4)
            pygame.draw.circle(screen, BLACK, (int(self.x + self.width/2 + 8), 
                                               int(self.y + self.height/2 - 8)), 4)
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Pipe:
    """Obstacle (black and white style)"""
    
    def __init__(self, x: int, speed: float = PIPE_SPEED):
        self.x = x
        self.gap_y = np.random.randint(150, WINDOW_HEIGHT - GROUND_HEIGHT - 150)
        self.gap_height = PIPE_GAP
        self.width = PIPE_WIDTH
        self.passed = False
        self.speed = speed
    
    def update(self):
        """Update pipe position"""
        self.x -= self.speed
    
    def draw(self, screen):
        """Draw pipe"""
        # Top pipe
        pygame.draw.rect(screen, WHITE, 
                        (self.x, 0, self.width, self.gap_y))
        # Bottom pipe
        bottom_pipe_y = self.gap_y + self.gap_height
        pygame.draw.rect(screen, WHITE, 
                        (self.x, bottom_pipe_y, self.width, 
                         WINDOW_HEIGHT - GROUND_HEIGHT - bottom_pipe_y))
    
    def get_rects(self) -> List[pygame.Rect]:
        """Get collision rectangle list"""
        return [
            pygame.Rect(self.x, 0, self.width, self.gap_y),
            pygame.Rect(self.x, self.gap_y + self.gap_height, self.width, 
                       WINDOW_HEIGHT - GROUND_HEIGHT - (self.gap_y + self.gap_height))
        ]
    
    def collision(self, bird_rect: pygame.Rect) -> bool:
        """Detect collision with bird"""
        for pipe_rect in self.get_rects():
            if bird_rect.colliderect(pipe_rect):
                return True
        return False


class SoundDetector:
    """Sound detector"""
    
    def __init__(self):
        self.audio = None
        self.stream = None
        self.silent_count = 0
        self.available = False
        self.current_volume = 0.0  # Current volume value
        
        if AUDIO_AVAILABLE:
            self.init_audio()
        else:
            print("Voice detection unavailable, using keyboard control")
    
    def init_audio(self):
        """Initialize audio stream"""
        if not AUDIO_AVAILABLE:
            return
        
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            self.available = True
            print("Microphone initialized successfully!")
        except Exception as e:
            print(f"Microphone initialization failed: {e}")
            print("Will use keyboard control (Spacebar)")
            self.stream = None
            self.available = False
    
    def detect_sound(self) -> float:
        """Detect sound and return volume value (normalized 0-1)"""
        if not self.available or self.stream is None:
            return 0.0
        
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            self.current_volume = volume  # Save current volume
            
            # Normalize volume to 0-1 range
            # Below threshold is 0, above threshold is proportionally mapped
            if volume < SOUND_THRESHOLD:
                normalized = 0.0
            else:
                # When volume exceeds threshold, map to 0-2 range (2x threshold for height)
                normalized = min(2.0, (volume - SOUND_THRESHOLD) / SOUND_THRESHOLD)
            
            self.silent_count = 0 if normalized > 0 else self.silent_count + 1
            return normalized
        except:
            return 0.0
    
    def get_volume(self) -> float:
        """Get current volume (for debugging)"""
        return self.current_volume
    
    def cleanup(self):
        """Clean up resources"""
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass


class Button:
    """Button class"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
    
    def draw(self, screen, font):
        """Draw button"""
        color = WHITE if not self.hover else GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        """Check mouse hover"""
        self.hover = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos):
        """Check if clicked"""
        return self.rect.collidepoint(pos)


class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Scream - Voice-Controlled Jumping Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Sound detector
        self.sound_detector = SoundDetector()
        
        # Buttons
        self.start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 80, 200, 50, "START")
        self.restart_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 80, 200, 50, "RESTART")
        
        # Game state
        self.reset_game()
        
        # Load background image
        self.background = None
        try:
            bg_path = "Character/background/Background.png"
            if os.path.exists(bg_path):
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
                print("Background image loaded successfully")
        except Exception as e:
            print(f"Failed to load background image: {e}")
    
    def reset_game(self):
        """Reset game"""
        self.bird = Bird(100, WINDOW_HEIGHT // 2)
        self.pipes: List[Pipe] = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.pipe_timer = 0
        self.last_volume = 0.0
        self.show_volume = True
        self.current_speed = PIPE_SPEED  # Current pipe speed
        self.sound_test_mode = True  # Sound test mode
        self.sound_test_started = False
    
    def handle_events(self):
        """Handle events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if not self.game_started:
                        if self.start_button.is_clicked(mouse_pos):
                            # Click start button, exit sound test mode, enter game
                            self.sound_test_mode = False
                            self.game_started = True
                    elif self.game_over and self.restart_button.is_clicked(mouse_pos):
                        self.reset_game()
            
            if event.type == pygame.MOUSEMOTION:
                if not self.game_started:
                    # Also show button hover effect in sound test mode
                    self.start_button.check_hover(mouse_pos)
                elif self.game_over:
                    self.restart_button.check_hover(mouse_pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and self.game_started:
                    # Spacebar simulates sound input
                    self.bird.velocity = JUMP_STRENGTH
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        """Update game state"""
        if not self.game_started or self.game_over:
            return
        
        # Adjust speed based on score: increase 0.1 speed per point
        self.current_speed = PIPE_SPEED + self.score * 0.1
        
        # Detect sound and get normalized volume value
        volume_normalized = self.sound_detector.detect_sound()
        
        # Update character position based on normalized volume (smooth control)
        self.bird.update(volume_normalized)
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Detect collision
            if pipe.collision(self.bird.get_rect()):
                self.game_over = True
            
            # Score
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
        
        # Remove pipes off screen
        self.pipes = [p for p in self.pipes if p.x + p.width > 0]
        
        # Generate new pipe (using current speed)
        self.pipe_timer += 1
        if self.pipe_timer > 100:
            self.pipes.append(Pipe(WINDOW_WIDTH, self.current_speed))
            self.pipe_timer = 0
    
    def draw(self):
        """Draw game screen"""
        # Draw background (if exists)
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        if not self.game_started:
            if self.sound_test_mode:
                # Sound test interface
                self.draw_sound_test()
            else:
                # Show start interface
                text = self.big_font.render("SCREAM", True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
                self.screen.blit(text, text_rect)
                
                # Show start button
                self.start_button.draw(self.screen, self.font)
        else:
            # Draw pipes
            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            # Draw ground
            pygame.draw.rect(self.screen, WHITE, 
                          (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))
            pygame.draw.rect(self.screen, BLACK, 
                          (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, 5))
            
            # Draw bird
            self.bird.draw(self.screen)
            
            # Display score and volume in top-right corner
            score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
            self.screen.blit(score_text, score_rect)
            
            # Display volume (if sound function available)
            if self.sound_detector.available and self.show_volume:
                volume = self.sound_detector.get_volume()
                self.last_volume = volume
                # Volume display, including threshold line
                volume_text = self.font.render(f"VOL: {int(volume)}/{SOUND_THRESHOLD}", True, 
                                                (255, 255, 0) if volume < SOUND_THRESHOLD else (0, 255, 0))
                volume_rect = volume_text.get_rect(topright=(WINDOW_WIDTH - 10, 50))
                self.screen.blit(volume_text, volume_rect)
            
            # Game over interface
            if self.game_over:
                # Semi-transparent background
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.big_font.render("GAME OVER", True, WHITE)
                final_score_text = self.font.render(f"FINAL SCORE: {self.score}", True, WHITE)
                
                game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60))
                score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                
                self.screen.blit(game_over_text, game_over_rect)
                self.screen.blit(final_score_text, score_rect)
                
                # Display restart button
                self.restart_button.draw(self.screen, self.font)
        
        pygame.display.flip()
    
    def draw_sound_test(self):
        """Draw cover (including sound detection progress bar)"""
        # Continuously detect sound to update volume value
        volume_normalized = self.sound_detector.detect_sound()
        
        # Get current volume
        current_volume = self.sound_detector.get_volume()
        
        # Game title
        title = self.big_font.render("SCREAM", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 120))
        self.screen.blit(title, title_rect)
        
        # Sound detection progress bar
        bar_x = WINDOW_WIDTH // 2 - 200
        bar_y = 220
        bar_width = 400
        bar_height = 40
        
        # Calculate volume percentage (max display 3000)
        max_volume = 3000
        volume_percent = min(current_volume / max_volume, 1.0)
        
        # Draw background bar
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Draw volume bar
        bar_fill_width = int(bar_width * volume_percent)
        
        # Set color based on volume
        if volume_percent < 0.3:
            bar_color = (255, 0, 0)  # Red
        elif volume_percent < 0.6:
            bar_color = (255, 255, 0)  # Yellow
        else:
            bar_color = (0, 255, 0)  # Green
        
        pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, bar_fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Display threshold marker line
        threshold_percent = SOUND_THRESHOLD / max_volume
        threshold_x = bar_x + int(bar_width * threshold_percent)
        pygame.draw.line(self.screen, WHITE, 
                        (threshold_x, bar_y - 10),
                        (threshold_x, bar_y + bar_height + 10), 2)
        
        # Display start button (removed middle UI)
        self.start_button.draw(self.screen, self.font)
    
    def run(self):
        """Run game main loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Clean up resources
        self.sound_detector.cleanup()
        pygame.quit()
        sys.exit()


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

