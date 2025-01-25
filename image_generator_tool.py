import openai
import requests
import os
from PIL import Image
from io import BytesIO

def get_image_description():
    print("Welcome to the Image Generator Tool!")
    print("Answer a few questions to generate your image.")

    # Collect user inputs
    subject = input("What is the subject of the image? (e.g., a cat, a mountain, a robot): ")
    style = input("What style should the image have? (e.g., realistic, cartoon, futuristic): ")
    colors = input("What dominant colors or color scheme should the image have? (e.g., blue and white, warm colors): ")
    background = input("What kind of background should the image have? (e.g., cityscape, forest, plain white): ")
    additional_details = input("Any additional details or features? (e.g., wearing sunglasses, in space, holding a cup of coffee): ")

    # Construct the image description
    description = (
        f"A {style} image of {subject}, with {colors} as the dominant colors, set against a {background} background. "
        f"It also features {additional_details}."
    )

    return description

def generate_image(description):
    print("Generating your image...")

    # Replace 'your-api-key' with your OpenAI API key
    openai.api_key = "your-api-key"

    try:
        # Use OpenAI's API to generate the image
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="1024x1024"
        )

        # Debugging: Check if the response contains the expected data
        print(f"API Response: {response}")

        image_url = response['data'][0]['url']
        print("Image successfully generated!")
        print(f"Image URL: {image_url}")

        return image_url

    except Exception as e:
        print("An error occurred while generating the image:", e)
        return None

def display_image(image_url):
    print("Downloading and displaying the image...")

    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()  # Check for request errors

        # Open the image with Pillow
        img = Image.open(BytesIO(response.content))
        img.show()  # Display the image

    except Exception as e:
        print("Failed to download and display the image:", e)

def save_image(image_url, save_path):
    print("Downloading the image...")
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for request errors

        # Save the image to the specified path
        with open(save_path, "wb") as image_file:
            image_file.write(response.content)

        print(f"Image successfully saved at: {save_path}")
    except Exception as e:
        print("Failed to download the image:", e)

if __name__ == "__main__":
    # Step 1: Get the image description
    description = get_image_description()

    # Step 2: Generate the image using the description
    image_url = generate_image(description)

    # Step 3: Provide the image URL or handle errors
    if image_url:
        # Ask the user if they want to display the image
        display_option = input("Do you want to view the image now? (yes/no): ").strip().lower()
        if display_option == "yes":
            display_image(image_url)
        
        # Ask the user if they want to save the image locally
        save_option = input("Do you want to save the image locally? (yes/no): ").strip().lower()
        if save_option == "yes":
            save_path = input("Enter the file path and name to save the image (e.g., output/image.png): ").strip()
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            save_image(image_url, save_path)
        else:
            print("You can view and download your image using the URL above.")
    else:
        print("Failed to generate the image. Please try again.")