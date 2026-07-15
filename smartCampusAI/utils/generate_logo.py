import os
from PIL import Image, ImageDraw

def generate_logo():
    """Generates a professional glassmorphic-styled logo for SmartCampusAI."""
    size = (512, 512)
    # Slate-950 dark background
    image = Image.new("RGBA", size, (9, 10, 15, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw futuristic glow circles
    for r in range(220, 170, -2):
        t = (220 - r) / 50.0
        # Color transition from Purple (#8b5cf6) to Blue (#3b82f6)
        r_col = int(139 + (59 - 139) * t)
        g_col = int(92 + (130 - 92) * t)
        b_col = int(246 + (246 - 246) * t)
        alpha = int(180 * (1 - t))
        draw.ellipse(
            [size[0]//2 - r, size[1]//2 - r, size[0]//2 + r, size[1]//2 + r],
            outline=(r_col, g_col, b_col, alpha),
            width=2
        )
        
    # Draw central stylized logo marks
    # Glowing ring
    draw.ellipse(
        [size[0]//2 - 160, size[1]//2 - 160, size[0]//2 + 160, size[1]//2 + 160],
        outline=(139, 92, 246, 255),
        width=10
    )
    
    # Outer accent arc (blue)
    draw.arc(
        [size[0]//2 - 190, size[1]//2 - 190, size[0]//2 + 190, size[1]//2 + 190],
        start=45, end=225,
        fill=(59, 130, 246, 255),
        width=6
    )
    
    # Inner accent arc (pink/purple)
    draw.arc(
        [size[0]//2 - 130, size[1]//2 - 130, size[0]//2 + 130, size[1]//2 + 130],
        start=225, end=45,
        fill=(217, 70, 239, 255),
        width=6
    )
    
    # Futuristic crosshair dashes
    draw.line([size[0]//2, 50, size[0]//2, 80], fill=(59, 130, 246, 255), width=4)
    draw.line([size[0]//2, 432, size[0]//2, 462], fill=(59, 130, 246, 255), width=4)
    draw.line([50, size[1]//2, 80, size[1]//2], fill=(217, 70, 239, 255), width=4)
    draw.line([432, size[1]//2, 462, size[1]//2], fill=(217, 70, 239, 255), width=4)
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Save the logo
    image.save("assets/logo.png")
    print("Professional logo generated successfully at assets/logo.png")

if __name__ == "__main__":
    generate_logo()
