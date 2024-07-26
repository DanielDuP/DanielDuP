from danieldup import render_currently_reading, render_proportional_languages
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    render_currently_reading.render()
    render_proportional_languages.render()


if __name__ == "__main__":
    main()
