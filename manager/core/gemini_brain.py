import google.generativeai as genai
import PIL.Image
import os
import json

class GeminiBrain:
    """
    The Intelligence behind the Controller Agent.
    Uses Gemini 2.5 Flash to analyze screenshots and make decisions.
    """

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_screen_with_dom(self, screenshot_path, dom_data):
        """Sends a screenshot and DOM bounding boxes to Gemini for exact coordinate clicking."""
        img = PIL.Image.open(screenshot_path)
        
        prompt = f"""
        You are an industrial automation manager. Look at this Google Colab screenshot and the provided DOM elements.
        DOM Elements: {json.dumps(dom_data)}
        
        Identify if there are any unknown errors or if the runtime is disconnected.
        If action is needed, return a JSON object using the exact x,y coordinates from the DOM elements list: 
        {{"action": "click" | "scroll" | "wait", "target": "description", "x": pixel_x, "y": pixel_y}}
        If everything is running perfectly, return: {{"action": "wait"}}
        """

        response = self.model.generate_content([prompt, img])
        
        try:
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            return {"action": "wait"}

    async def analyze_screen(self, screenshot_path):
        """(Deprecated) Sends a screenshot to Gemini and asks for the next action."""

    def generate_report(self, stats):
        """Generates a human-like report for Telegram."""
        prompt = f"Summarize these worker stats into a short, encouraging report for the boss: {stats}"
        response = self.model.generate_content(prompt)
        return response.text
