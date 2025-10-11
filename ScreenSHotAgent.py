import os
import time
import base64
import requests
from PIL import ImageGrab
import keyboard

# Configuration
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
GOOGLE_API_KEY = ""

SCREENSHOT_FOLDER = r"Your Choice"

# Global variables
screenshots = []
screenshot_paths = []
is_collecting = False

# Create screenshot folder if it doesn't exist
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

def take_screenshot():
    """Take a screenshot and return base64 data"""
    try:
        screenshot = ImageGrab.grab()
        
        # Generate filename with timestamp
        timestamp = int(time.time())
        filename = f"screenshot_{timestamp}_{len(screenshots) + 1}.png"
        filepath = os.path.join(SCREENSHOT_FOLDER, filename)
        
        # Save screenshot to folder
        screenshot.save(filepath)
        print(f"📷 Screenshot saved: {filepath}")
        
        # Convert to base64 for API
        with open(filepath, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode('utf-8')
        
        return base64_string, screenshot.size, filepath
        
    except Exception as e:
        print(f"❌ Screenshot error: {e}")
        return None, None, None

def send_image_to_telegram(image_path, caption=""):
    """Send image to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption
            }
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                print(f"✅ Image sent: {os.path.basename(image_path)}")
                return True
            else:
                print(f"❌ Image send error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Image send error: {e}")
        return False

def send_images_to_telegram(image_paths):
    """Send multiple images to Telegram with captions"""
    print(f"📤 Sending {len(image_paths)} images to Telegram...")
    
    for i, image_path in enumerate(image_paths, 1):
        caption = f"Screenshot {i}/{len(image_paths)} - {os.path.basename(image_path)}"
        success = send_image_to_telegram(image_path, caption)
        
        if success:
            time.sleep(1)  # Delay between image sends to avoid rate limits
        else:
            print(f"❌ Failed to send image {i}")
    
    print("✅ All images sent!")

def analyze_with_google_gemini(images_base64):
    """Analyze screenshots using Google Gemini API"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        # Prepare the request
        contents = [{
            "parts": [
                {
                        "text": "Analyze this screenshot. If you see code, explain it and provide improvements and provide the code as per the needs mentioned. If you see questions, answer them comprehensively. Be detailed and practical then choose the option from the MCQ or MSQ which is the most appropriate answer or else if its a fill in blanks then provide the suitable answer, at last give all the answer with their question number ."
                }
            ]
        }]
        
        # Add images
        for img_base64 in images_base64:
            contents[0]["parts"].append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": img_base64
                }
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192
            }
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Gemini API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Gemini analysis error: {str(e)}"

def send_text_to_telegram(message):
    """Send text message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        # Split long messages
        max_length = 4000
        if len(message) > max_length:
            chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            for i, chunk in enumerate(chunks):
                payload = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'text': f"Part {i+1}/{len(chunks)}:\n{chunk}"
                }
                response = requests.post(url, data=payload)
                if response.status_code != 200:
                    print(f"❌ Telegram error for chunk {i+1}: {response.text}")
                time.sleep(1)  # Delay between chunks
        else:
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
        print(f"❌ Telegram error: {e}")

def process_screenshots():
    """Process collected screenshots"""
    global screenshots, screenshot_paths
    
    if not screenshots:
        print("❌ No screenshots to process")
        return
    
    print(f"🔄 Processing {len(screenshots)} screenshots...")
    
    # Step 1: Send images first
    send_images_to_telegram(screenshot_paths)
    
    # Step 2: Analyze with Google Gemini
    print(f"🤖 Analyzing screenshots with Google Gemini...")
    analysis = analyze_with_google_gemini(screenshots)
    
    # Step 3: Create and send analysis text
    summary = f"🔍 AI Analysis Results:\n"
    summary += f"📊 Screenshots analyzed: {len(screenshots)}\n"
    summary += f"🕐 Analysis time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += f"📁 Saved to: {SCREENSHOT_FOLDER}\n\n"
    summary += "=" * 50 + "\n"
    summary += "📋 DETAILED ANALYSIS:\n"
    summary += "=" * 50 + "\n"
    summary += analysis
    
    # Send analysis text
    send_text_to_telegram(summary)
    
    print("✅ Processing complete!")
    print(f"📁 Screenshots saved in: {SCREENSHOT_FOLDER}")
    
    # Clear screenshots for next batch
    screenshots.clear()
    screenshot_paths.clear()

# Print setup instructions
print("🤖 AI Screenshot Agent Started!")
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

# Main loop
try:
    while True:
        # Check for Caps Lock key press
        if keyboard.is_pressed('caps lock'):
            if not is_collecting:
                # Start collecting
                is_collecting = True
                screenshots.clear()
                screenshot_paths.clear()
                print("🚀 Started collecting screenshots!")
                print("📸 Press Right Shift for more screenshots, Caps Lock again to submit.")
                
                # Take initial screenshot
                base64_img, size, filepath = take_screenshot()
                if base64_img:
                    screenshots.append(base64_img)
                    screenshot_paths.append(filepath)
                    print(f"📷 Screenshot 1 taken ({size[0]}x{size[1]})")
                
                # Wait for key release
                while keyboard.is_pressed('caps lock'):
                    time.sleep(0.1)
                    
            else:
                # Submit screenshots
                print(f"🔄 Submitting {len(screenshots)} screenshots for processing...")
                process_screenshots()
                is_collecting = False
                
                # Wait for key release
                while keyboard.is_pressed('caps lock'):
                    time.sleep(0.1)
        
        # Check for Right Shift key press (only when collecting)
        elif keyboard.is_pressed('right shift') and is_collecting:
            base64_img, size, filepath = take_screenshot()
            if base64_img:
                screenshots.append(base64_img)
                screenshot_paths.append(filepath)
                print(f"📷 Screenshot {len(screenshots)} taken ({size[0]}x{size[1]})")
            
            # Wait for key release
            while keyboard.is_pressed('right shift'):
                time.sleep(0.1)
        
        # Small delay to prevent high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n👋 Shutting down...")
    print("✅ Screenshot Agent stopped!")
