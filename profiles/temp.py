
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

WIDTH = 1000
HEIGHT = 600

BG = "#10131C"
CARD = "#191E2B"
GREEN = "#A3FF68"
PURPLE = "#9B8CFF"
WHITE = "#FFFFFF"
GRAY = "#A0A7B8"


def load_font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / name

    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default(size=size)


def fit_text(draw, text, font, width):
    text = str(text or "Not provided")

    if draw.textbbox((0, 0), text, font=font)[2] <= width:
        return text

    while text and draw.textbbox(
        (0, 0), text + "...", font=font
    )[2] > width:
        text = text[:-1]

    return text.rstrip() + "..."


def render_and_return_image(
    username,
    name,
    bio,
    public_repos,
    followers
):

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    # Background decorative circles
    draw.ellipse(
        (760, -160, 1120, 200),
        fill="#22233D"
    )

    draw.ellipse(
        (-160, 430, 170, 760),
        fill="#172A2B"
    )

    # Main card
    draw.rounded_rectangle(
        (45, 40, 955, 560),
        radius=28,
        fill=CARD
    )

    # Top navigation
    draw.text(
        (85, 72),
        "DEV / PROFILE",
        fill=GREEN,
        font=load_font(17, True)
    )

    draw.text(
        (760, 76),
        "GITHUB DEVELOPER",
        fill=GRAY,
        font=load_font(12, True)
    )

    draw.line(
        (85, 115, 915, 115),
        fill="#303747",
        width=2
    )

    # Left profile panel
    # Avatar background
    draw.ellipse(
        (105, 155, 295, 345),
        fill="#30304C"
    )

    draw.ellipse(
        (115, 165, 285, 335),
        fill=PURPLE
    )

    # Initials
    initials = "".join(
        word[0] for word in str(name or username).split()[:2]
    ).upper()

    font = load_font(55, True)
    box = draw.textbbox((0, 0), initials, font=font)

    x = 200 - (box[2] - box[0]) // 2
    y = 250 - (box[3] - box[1]) // 2 - box[1]

    draw.text(
        (x, y),
        initials,
        fill=WHITE,
        font=font
    )

    # Online status
    draw.ellipse(
        (255, 305, 285, 335),
        fill=GREEN
    )

    # Profile name
    draw.text(
        (95, 375),
        fit_text(
            draw, name, load_font(27, True), 300
        ),
        fill=WHITE,
        font=load_font(27, True)
    )

    draw.text(
        (95, 420),
        fit_text(
            draw, "@" + username, load_font(16), 300
        ),
        fill=GREEN,
        font=load_font(16)
    )

    # Bio
    draw.text(
        (95, 470),
        "ABOUT DEVELOPER",
        fill=GRAY,
        font=load_font(11, True)
    )

    draw.text(
        (95, 495),
        fit_text(
            draw, bio, load_font(14), 300
        ),
        fill=WHITE,
        font=load_font(14)
    )

    # Vertical separator
    draw.line(
        (440, 145, 440, 515),
        fill="#303747",
        width=2
    )

    # Right section heading
    draw.text(
        (490, 155),
        "OVERVIEW",
        fill=GRAY,
        font=load_font(13, True)
    )

    draw.text(
        (490, 185),
        "Developer Statistics",
        fill=WHITE,
        font=load_font(27, True)
    )

    # Repository card
    draw.rounded_rectangle(
        (490, 245, 685, 355),
        radius=18,
        fill="#242D38"
    )

    draw.text(
        (515, 265),
        "01",
        fill=GREEN,
        font=load_font(12, True)
    )

    draw.text(
        (515, 290),
        str(public_repos),
        fill=WHITE,
        font=load_font(32, True)
    )

    draw.text(
        (515, 330),
        "Repositories",
        fill=GRAY,
        font=load_font(13)
    )

    # Followers card
    draw.rounded_rectangle(
        (710, 245, 905, 355),
        radius=18,
        fill="#29263E"
    )

    draw.text(
        (735, 265),
        "02",
        fill=PURPLE,
        font=load_font(12, True)
    )

    draw.text(
        (735, 290),
        str(followers),
        fill=WHITE,
        font=load_font(32, True)
    )

    draw.text(
        (735, 330),
        "Followers",
        fill=GRAY,
        font=load_font(13)
    )

    # Developer badge
    draw.rounded_rectangle(
        (490, 390, 905, 475),
        radius=18,
        fill="#242D38"
    )

    draw.text(
        (515, 407),
        "DEVELOPER STATUS",
        fill=GRAY,
        font=load_font(11, True)
    )

    draw.text(
        (515, 432),
        "Building. Learning. Creating.",
        fill=GREEN,
        font=load_font(17, True)
    )

    # Footer
    draw.line(
        (85, 525, 915, 525),
        fill="#303747",
        width=1
    )

    draw.text(
        (85, 535),
        "MY GITHUB PROFILE",
        fill=GRAY,
        font=load_font(11)
    )

    draw.text(
        (820, 535),
        "2026",
        fill=GREEN,
        font=load_font(11, True)
    )

    return image


# Generate profile
img = render_and_return_image(
    username="ASMIT_SHARMA",
    name="Asmit Sharma",
    bio="Computer Science Student | Python Developer",
    public_repos=8,
    followers=6969
)

# Save image
img.save("github_profile_dark.png")

print("Profile image generated successfully!")
