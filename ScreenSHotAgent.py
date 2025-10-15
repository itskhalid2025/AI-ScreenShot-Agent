"""
AI Screenshot Agent with Google Gemini Integration

Author: Mohammed Khalid
Version: 1.0.0
Created: 2025
License: MIT

Description:
    This application is an automated screenshot capture and analysis tool that integrates
    with Google Gemini AI and Telegram for real-time image analysis and sharing. It allows
    users to capture multiple screenshots using keyboard shortcuts, automatically upload
    them to Telegram, and receive AI-powered analysis of the content.

Features:
    - Keyboard-controlled screenshot capture (Caps Lock to start/stop, Right Shift to capture)
    - Automatic image upload to Telegram
    - AI-powered analysis using Google Gemini 1.5 Flash
    - Support for code analysis, question answering, and MCQ/MSQ solving
    - Batch processing of multiple screenshots
    - Local storage of captured images

Use Cases:
    - Educational: Capture exam questions and get instant answers
    - Development: Analyze code snippets and get improvement suggestions
    - Documentation: Capture and analyze technical diagrams or documentation
    - Research: Collect and analyze visual information

Requirements:
    - Python 3.7+
    - PIL (Pillow)
    - keyboard
    - requests
    - Active internet connection
    - Telegram Bot Token and Chat ID
    - Google Gemini API Key

Setup:
    1. Install dependencies: pip install pillow keyboard requests
    2. Create a Telegram bot via @BotFather and get the token
    3. Get your Telegram Chat ID
    4. Obtain Google Gemini API key from Google AI Studio
    5. Configure the tokens and paths in the Configuration section below

Usage:
    1. Run the script: python screenshot_agent.py
    2. Press Caps Lock to start collecting screenshots
    3. Press Right Shift to capture additional screenshots
    4. Press Caps Lock again to submit and process all captured screenshots
    5. View results in your Telegram chat

Notes:
    - Screenshots are saved locally before being processed
    - AI analysis results are sent as text messages after images
    - Rate limiting is implemented to prevent Telegram API throttling
    - Long messages are automatically split into chunks

Author Contact:
    Mohammed Khalid
    GitHub: [Your GitHub Profile]
    Email: [Your Email]
"""

import os
import time
import base64
import requests
from PIL import ImageGrab
import keyboard

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================
# Configure these values before running the script

# Telegram Bot Configuration
# Get your bot token from @BotFather on Telegram
TELEGRAM_TOKEN = ""  # Example: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Your Telegram Chat ID
# Get this by messaging @userinfobot on Telegram
TELEGRAM_CHAT_ID = ""  # Example: "123456789"

# Google Gemini API Configuration
# Get your API key from https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = ""  # Example: "AIzaSyABC123..."

# Screenshot Storage Location
# Change this to your preferred folder path
SCREENSHOT_FOLDER = r"Your Choice"  # Example: r"C:\Users\YourName\Screenshots"

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

# List to store base64 encoded screenshot data for API submission
screenshots = []

# List to store file paths of saved screenshots
screenshot_paths = []

# Flag to track whether we're currently collecting screenshots
is_collecting = False

# ============================================================================
# INITIALIZATION
# ============================================================================

# Create screenshot folder if it doesn't exist
# This ensures the script won't fail when trying to save the first screenshot
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

# ============================================================================
# SCREENSHOT CAPTURE FUNCTIONS
# ============================================================================

def take_screenshot():
    """
    Capture a screenshot of the entire screen and save it locally.
    
    This function:
    1. Captures the full screen using PIL's ImageGrab
    2. Generates a unique filename with timestamp
    3. Saves the image to the configured folder
    4. Converts the image to base64 for API transmission
    
    Returns:
        tuple: (base64_string, image_size, filepath) on success
               (None, None, None) on failure
    
    Example:
        base64_img, size, path = take_screenshot()
        if base64_img:
            print(f"Screenshot saved: {path}, Size: {size}")
    """
    try:
        # Capture the entire screen
        screenshot = ImageGrab.grab()
        
        # Generate a unique filename using timestamp and sequence number
        # Format: screenshot_1234567890_1.png
        timestamp = int(time.time())
        filename = f"screenshot_{timestamp}_{len(screenshots) + 1}.png"
        filepath = os.path.join(SCREENSHOT_FOLDER, filename)
        
        # Save the screenshot to the designated folder
        screenshot.save(filepath)
        print(f"📷 Screenshot saved: {filepath}")
        
        # Convert the image to base64 encoding for API transmission
        # This allows us to send the image data in JSON format
        with open(filepath, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode('utf-8')
        
        return base64_string, screenshot.size, filepath
        
    except Exception as e:
        # Handle any errors during screenshot capture
        print(f"❌ Screenshot error: {e}")
        return None, None, None

# ============================================================================
# TELEGRAM INTEGRATION FUNCTIONS
# ============================================================================

def send_image_to_telegram(image_path, caption=""):
    """
    Upload a single image to Telegram using the Bot API.
    
    This function sends an image file to your Telegram chat with an optional caption.
    It uses the sendPhoto endpoint of the Telegram Bot API.
    
    Args:
        image_path (str): Full path to the image file to send
        caption (str): Optional text caption to display with the image
    
    Returns:
        bool: True if image was sent successfully, False otherwise
    
    Example:
        success = send_image_to_telegram("/path/to/image.png", "Screenshot 1")
        if success:
            print("Image uploaded successfully!")
    
    Notes:
        - Maximum file size: 10MB for photos
        - Supported formats: JPG, PNG, GIF
        - API Reference: https://core.telegram.org/bots/api#sendphoto
    """
    try:
        # Construct the Telegram API endpoint URL
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        
        # Open and send the image file
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption
            }
            
            # Make the POST request to Telegram API
            response = requests.post(url, files=files, data=data)
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"✅ Image sent: {os.path.basename(image_path)}")
                return True
            else:
                print(f"❌ Image send error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        # Handle any errors during image transmission
        print(f"❌ Image send error: {e}")
        return False

def send_images_to_telegram(image_paths):
    """
    Send multiple images to Telegram sequentially with captions.
    
    This function iterates through a list of image paths and sends each one
    to Telegram with a numbered caption. It includes delays between sends to
    avoid hitting Telegram's rate limits.
    
    Args:
        image_paths (list): List of full file paths to images
    
    Example:
        paths = ["/path/img1.png", "/path/img2.png"]
        send_images_to_telegram(paths)
    
    Notes:
        - Includes 1-second delay between images to prevent rate limiting
        - Telegram rate limit: ~30 messages per second per chat
        - Failed sends are logged but don't stop the process
    """
    print(f"📤 Sending {len(image_paths)} images to Telegram...")
    
    # Iterate through all image paths and send each one
    for i, image_path in enumerate(image_paths, 1):
        # Create a descriptive caption with sequence number
        caption = f"Screenshot {i}/{len(image_paths)} - {os.path.basename(image_path)}"
        success = send_image_to_telegram(image_path, caption)
        
        if success:
            # Wait between sends to avoid rate limiting
            time.sleep(1)
        else:
            print(f"❌ Failed to send image {i}")
    
    print("✅ All images sent!")

def send_text_to_telegram(message):
    """
    Send a text message to Telegram, automatically splitting long messages.
    
    Telegram has a message length limit of 4096 characters. This function
    automatically splits longer messages into chunks and sends them sequentially.
    
    Args:
        message (str): Text message to send (any length)
    
    Example:
        send_text_to_telegram("Analysis results: ...")
    
    Notes:
        - Maximum message length: 4096 characters (Telegram limit)
        - This function uses 4000 chars to be safe
        - Long messages are split and numbered
        - 1-second delay between chunks
    """
    try:
        # Construct the Telegram API endpoint URL
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        # Split long messages into chunks to respect Telegram's limits
        max_length = 4000
        if len(message) > max_length:
            # Split message into chunks of max_length characters
            chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            
            # Send each chunk separately with part numbers
            for i, chunk in enumerate(chunks):
                payload = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'text': f"Part {i+1}/{len(chunks)}:\n{chunk}"
                }
                response = requests.post(url, data=payload)
                
                if response.status_code != 200:
                    print(f"❌ Telegram error for chunk {i+1}: {response.text}")
                
                time.sleep(1)  # Delay between chunks to avoid rate limiting
        else:
            # Send the message directly if it's short enough
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }
            response = requests.post(url, data=payload)
            
            if response.status_code != 200:
                print(f"❌ Telegram error: {response.text}")
            else:
                print("✅ Text message sent to Telegram!")
                
    except Exception as e:
        # Handle any errors during message transmission
        print(f"❌ Telegram error: {e}")

# ============================================================================
# AI ANALYSIS FUNCTIONS
# ============================================================================

def analyze_with_google_gemini(images_base64):
    """
    Analyze multiple screenshots using Google Gemini 1.5 Flash AI model.
    
    This function sends all captured screenshots to Google's Gemini AI for analysis.
    The AI is configured to:
    - Explain and improve code if detected
    - Answer questions comprehensively
    - Solve MCQs/MSQs and provide answers with question numbers
    - Fill in blanks appropriately
    
    Args:
        images_base64 (list): List of base64-encoded image strings
    
    Returns:
        str: AI analysis text or error message
    
    Example:
        analysis = analyze_with_google_gemini([img1_base64, img2_base64])
        print(analysis)
    
    API Details:
        - Model: gemini-1.5-flash (fast and efficient)
        - Temperature: 0.7 (balanced creativity/accuracy)
        - Max Output Tokens: 8192 (supports long responses)
    
    Notes:
        - Can process multiple images in a single request
        - Supports various content types: code, text, diagrams, questions
        - API Reference: https://ai.google.dev/docs
    """
    try:
        # Construct the Gemini API endpoint URL with API key
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        # Prepare the request content with analysis instructions
        contents = [{
            "parts": [
                {
                    "text": """Analyze this screenshot. If you see code, explain it and provide improvements and provide the code as per the needs mentioned. If you see questions, answer them comprehensively. Be detailed and practical then choose the option from the MCQ or MSQ which is the most appropriate answer or else if its a fill in blanks then provide the suitable answer, at last give all the answer with their question number."""
                }
            ]
        }]
        
        # Add all images to the request
        # Each image is embedded as inline data with base64 encoding
        for img_base64 in images_base64:
            contents[0]["parts"].append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": img_base64
                }
            })
        
        # Configure generation parameters
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,  # Controls randomness (0.0-1.0)
                "maxOutputTokens": 8192  # Maximum length of response
            }
        }
        
        # Send the request to Gemini API
        response = requests.post(url, json=payload)
        
        # Parse and return the AI's analysis
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Gemini API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        # Handle any errors during AI analysis
        return f"❌ Gemini analysis error: {str(e)}"

# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================

def process_screenshots():
    """
    Process all collected screenshots: upload to Telegram and analyze with AI.
    
    This is the main orchestration function that:
    1. Sends all screenshot images to Telegram
    2. Analyzes screenshots using Google Gemini AI
    3. Formats and sends the AI analysis results
    4. Clears the screenshot buffers for the next batch
    
    Process Flow:
        Screenshots → Telegram Upload → AI Analysis → Results to Telegram
    
    Global Variables Modified:
        - screenshots: Cleared after processing
        - screenshot_paths: Cleared after processing
    
    Example Output in Telegram:
        1. All screenshot images with captions
        2. AI analysis summary with:
           - Number of screenshots analyzed
           - Timestamp
           - Storage location
           - Detailed analysis results
    """
    global screenshots, screenshot_paths
    
    # Validate that we have screenshots to process
    if not screenshots:
        print("❌ No screenshots to process")
        return
    
    print(f"🔄 Processing {len(screenshots)} screenshots...")
    
    # Step 1: Send all images to Telegram first
    # Users can see the actual screenshots while waiting for AI analysis
    send_images_to_telegram(screenshot_paths)
    
    # Step 2: Send screenshots to Google Gemini for AI analysis
    print(f"🤖 Analyzing screenshots with Google Gemini...")
    analysis = analyze_with_google_gemini(screenshots)
    
    # Step 3: Create a formatted summary with metadata and analysis
    summary = f"🔍 AI Analysis Results:\n"
    summary += f"📊 Screenshots analyzed: {len(screenshots)}\n"
    summary += f"🕐 Analysis time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += f"📁 Saved to: {SCREENSHOT_FOLDER}\n\n"
    summary += "=" * 50 + "\n"
    summary += "📋 DETAILED ANALYSIS:\n"
    summary += "=" * 50 + "\n"
    summary += analysis
    
    # Step 4: Send the formatted analysis to Telegram
    send_text_to_telegram(summary)
    
    print("✅ Processing complete!")
    print(f"📁 Screenshots saved in: {SCREENSHOT_FOLDER}")
    
    # Step 5: Clear the screenshot buffers for the next batch
    screenshots.clear()
    screenshot_paths.clear()

# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

# Display startup information and usage instructions
print("🤖 AI Screenshot Agent Started!")
print("=" * 50)
print(f"Author: Mohammed Khalid")
print(f"Version: 1.0.0")
print("=" * 50)
print(f"📁 Screenshots folder: {SCREENSHOT_FOLDER}")
print(f"💬 Telegram Chat ID: {TELEGRAM_CHAT_ID}")
print(f"🔑 Using Google Gemini API")
print("=" * 50)
print("🎮 Controls:")
print("  Caps Lock → Start/Stop screenshot collection")
print("  Right Shift → Take screenshot (while collecting)")
print("  Ctrl+C → Exit")
print("=" * 50)
print("📤 Process: Images sent first → Then AI analysis")
print("✅ Ready! Press Caps Lock to start taking screenshots...")

# Main event loop for keyboard monitoring and screenshot capture
try:
    while True:
        # ====================================================================
        # CAPS LOCK: Toggle screenshot collection mode
        # ====================================================================
        # First press: Start collecting screenshots
        # Second press: Submit collected screenshots for processing
        
        if keyboard.is_pressed('caps lock'):
            if not is_collecting:
                # ============================================================
                # START COLLECTION MODE
                # ============================================================
                is_collecting = True
                screenshots.clear()
                screenshot_paths.clear()
                print("🚀 Started collecting screenshots!")
                print("📸 Press Right Shift for more screenshots, Caps Lock again to submit.")
                
                # Capture the first screenshot immediately
                base64_img, size, filepath = take_screenshot()
                if base64_img:
                    screenshots.append(base64_img)
                    screenshot_paths.append(filepath)
                    print(f"📷 Screenshot 1 taken ({size[0]}x{size[1]})")
                
                # Wait for key release to avoid multiple triggers
                while keyboard.is_pressed('caps lock'):
                    time.sleep(0.1)
                    
            else:
                # ============================================================
                # SUBMIT AND PROCESS SCREENSHOTS
                # ============================================================
                print(f"🔄 Submitting {len(screenshots)} screenshots for processing...")
                process_screenshots()
                is_collecting = False
                
                # Wait for key release to avoid multiple triggers
                while keyboard.is_pressed('caps lock'):
                    time.sleep(0.1)
        
        # ====================================================================
        # RIGHT SHIFT: Capture additional screenshot (only while collecting)
        # ====================================================================
        elif keyboard.is_pressed('right shift') and is_collecting:
            base64_img, size, filepath = take_screenshot()
            if base64_img:
                screenshots.append(base64_img)
                screenshot_paths.append(filepath)
                print(f"📷 Screenshot {len(screenshots)} taken ({size[0]}x{size[1]})")
            
            # Wait for key release to avoid multiple captures
            while keyboard.is_pressed('right shift'):
                time.sleep(0.1)
        
        # Small delay to prevent high CPU usage
        # This makes the loop check for keypresses ~10 times per second
        time.sleep(0.1)

except KeyboardInterrupt:
    # Graceful shutdown when user presses Ctrl+C
    print("\n👋 Shutting down...")
    print("✅ Screenshot Agent stopped!")
    print(f"Author: Mohammed Khalid | Thank you for using AI Screenshot Agent!")

# ============================================================================
# END OF SCRIPT
# ============================================================================
