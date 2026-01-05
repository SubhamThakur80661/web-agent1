import time
import json
import os
import random
from gtts import gTTS
import pygame
from playwright.sync_api import sync_playwright
from openai import OpenAI
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel


# ==========================================
MY_API_KEY = "Paste your api key here (groq) as client base is groq.com "
# ==========================================

if "PASTE_YOUR" in MY_API_KEY:
    print("\n❌ Error: Upar apni API Key paste karo!")
    exit()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=MY_API_KEY
)

TARGET_URL = "https://www.saucedemo.com/"

MAX_STEPS = 12

MISSION = """
1. Select 'Price (high to low)' from Sort Dropdown.
2. Add top 2 expensive items to Cart.
3. Go to Cart -> Click Checkout.
4. Fill Form: 'Tony', 'Stark', '10001'.
5. Click Continue -> Click Finish.
6. IF YOU SEE 'THANK YOU' -> STOP IMMEDIATELY.
"""

console = Console()

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', tld='co.in')
        filename = f"temp_voice_{random.randint(1,1000)}.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        if os.path.exists(filename): 
            try: os.remove(filename)
            except: pass
    except:
        pass

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(["script", "style", "svg", "head", "meta", "footer", "noscript", "img", "link"]):
        element.decompose()
    return soup.prettify()[:20000]

def highlight_element(page, selector):
    try:
        css = """
            .jarvis-glow {
                border: 2px solid #00ffcc !important;
                box-shadow: 0 0 15px #00ffcc !important;
                background-color: rgba(0, 255, 204, 0.2) !important;
                transition: all 0.3s ease;
            }
        """
        page.add_style_tag(content=css)
        page.eval_on_selector(selector, "el => el.classList.add('jarvis-glow')")
    except:
        pass

def get_next_action(page_content, previous_actions):
    system_prompt = f"""
    You are JARVIS. Mission: {MISSION}
    
    RULES:
    - If you see 'Checkout', CLICK IT.
    - If you see 'Zip/Postal Code', TYPE '10001'.
    - If you see 'Finish', CLICK IT.
    - If you see 'Thank you for your order', ACTION must be 'done'.
    
    Return JSON ONLY:
    {{
        "thought": "Short status.",
        "action": "click" | "type" | "scroll" | "select_option" | "done",
        "selector": "CSS selector",
        "value": "text_value" 
    }}
    """
    
    user_message = f"HTML:\n{page_content}\nHistory:\n{previous_actions}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        console.print(f"[bold red]❌ API ERROR: {e}[/bold red]")
        return {"action": "wait", "thought": "Signal weak."}

def run_agent():
    with sync_playwright() as p:
        console.rule("[bold cyan]🤖 JARVIS ONLINE[/bold cyan]")
        speak("System online.")
        
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # AUTO LOGIN
        try:
            page.goto(TARGET_URL)
            console.print("[yellow]⚡ Auto-Login...[/yellow]")
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")
            console.print("[bold green]✔ Login Done.[/bold green]")
            speak("Access granted.")
            time.sleep(1)
        except Exception as e:
            console.print(f"[red]Login Error: {e}[/red]")
            return

        action_history = []
        
        for step in range(MAX_STEPS):
            console.print(f"\n[bold green]--- STEP {step + 1} ---[/bold green]")
            
            try:
                page.wait_for_load_state("domcontentloaded")
                html = clean_html(page.content())
            except:
                html = ""

            with console.status("[bold cyan]Thinking...", spinner="dots12"):
                decision = get_next_action(html, action_history)
            
            thought = decision.get('thought')
            action = decision.get('action')
            selector = decision.get('selector')
            val = decision.get('value')

            console.print(Panel(thought, title="JARVIS", style="cyan"))
            speak(thought)
            
            if action == 'wait':
                time.sleep(2)
                continue

            try:
                if selector and action != 'done':
                    highlight_element(page, selector)

                if action == 'click':
                    page.click(selector)
                elif action == 'type':
                    page.fill(selector, val)
                elif action == 'select_option':
                    page.select_option(selector, value=val)
                elif action == 'scroll':
                    page.mouse.wheel(0, 500)
                elif action == 'done':
                    msg = "Mission accomplished."
                    speak(msg)
                    console.print(f"[bold green]✅ {msg}[/bold green]")
                    break
                
                action_history.append(f"{action} on {selector}")

            except Exception as e:
                console.print(f"[red]Retry: {e}[/red]")
                page.mouse.wheel(0, 300)

        console.rule("[bold red]🛑 FINISHED[/bold red]")
        input("Press Enter to close...")
        browser.close()

if __name__ == "__main__":
    run_agent()