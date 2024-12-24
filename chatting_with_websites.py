# Pratham Agarwal 
# pagarwal5_be21@thapar.edu
# +91 8006058885 

# first do !pip install -r requirements.txt

# Imports

import requests
from bs4 import BeautifulSoup
import re
import string
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage



load_dotenv()

# Scrapping
url=input("Enter The URL You need to scrape, Or leave it blank for default botpenguin site: ")

if len(url)==0:
    url = "https://botpenguin.com/"  


def scrape(url):
    response = requests.get(url)

    if response.status_code == 200:

        content = response.text
        

        soup = BeautifulSoup(content, 'html.parser')

        text = soup.get_text(separator="\n", strip=True)
        
        
        with open('output.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(text)
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    
    return text


# Pipeline

def remove_html_tags(text):
  pattern=re.compile('<.*?>')
  return pattern.sub(r'',text)

def remove_punc(text):
    return text.translate(str.maketrans('','',string.punctuation))


def chat_conversion(text):
    chat_words = {
    "2F4U": "Too Fast For You",
    "4YEO FYEO": "For Your Eyes Only",
    "AAMOF": "As a Matter of Fact",
    "ACK": "Acknowledgment",
    "AFAIK": "As far as I know",
    "AFAIR": "As far as I remember / recall",
    "AFK": "Away from Keyboard",
    "AKA": "Also known as",
    "B2K BTK": "Back to Keyboard",
    "BTT": "Back to Topic",
    "BTW": "By the Way",
    "B/C": "Because",
    "C&P": "Copy and Paste",
    "CU": "See you",
    "CYS": "Check your Settings",
    "DIY": "Do it Yourself",
    "EOBD": "End of Business Day",
    "EOD": "End of Discussion",
    "EOM": "End of Message",
    "EOT": "End of Thread/Text/ Transmission",
    "FAQ": "Frequently asked Questions",
    "FACK": "Full Acknowledge",
    "FKA": "Formerly known as",
    "FWIW": "For what it's Worth",
    "FYI": "For your Information",
    "JFYI": "Just For your Information",
    "FTW": "Fuck the World / For the Win",
    "HF": "Have fun",
    "HTH": "Hope this Helps",
    "IDK": "I don't know",
    "IIRC": "If I Recall / Remember Correctly",
    "IMHO": "In my Humble Opinion",
    "IMO": "In my Opinion",
    "IMNSHO": "In my not so Humble / Honest Opinion",
    "IOW": "In other Words",
    "ITT": "In this Thread",
    "LOL": "Laughing out loud",
    "DGMW": "Don't get me wrong",
    "MMW": "Mark my Words",
    "N/A": "Not Available / Applicable",
    "NaN": "Not a Number",
    "NNTR": "No need to Reply",
    "noob": "Newbie",
    "n00b": "Newbie",
    "NOYB": "None of your Business",
    "NRN": "No Reply Necessary",
    "OMG": "Oh my God",
    "OP": "Original Poster, Original Post",
    "OT": "Off Topic",
    "OTOH": "On the other Hand",
    "PEBKAC": "Problem exists between Keyboard and Chair",
    "POV": "Point of View",
    "ROTFL": "Rolling on the Floor Laughing",
    "RSVP": "Repondez s'il vous plait (French: Please reply)",
    "RTFM": "Read the fine Manual",
    "SCNR": "Sorry, could not Resist",
    "SFLR": "Sorry, for late Reply",
    "SPOC": "Single Point of Contact",
    "TBA": "To be Announced",
    "TBC": "To be Continued / To be Confirmed",
    "TIA": "Thanks in Advance",
    "THX": "Thanks",
    "TNX": "Thanks",
    "TQ": "Thank You",
    "TYVM": "Thank You Very Much",
    "TYT": "Take your Time",
    "TTYL": "Talk to you Later",
    "w00t": "Whoomp, there it is; Meaning \"Hooray\"",
    "WFM": "Works for Me",
    "WRT": "With Regard to",
    "WTH": "What the Hell / What the Heck",
    "WTF": "What the Fuck",
    "YMMD": "You made my Day",
    "YMMV": "Your Mileage may vary",
    "YAM": "Yet Another Meeting",
    "ICYMI": "In Case you missed it",
    "2moro": "Tomorrow",
    "2nte": "Tonight",
    "AEAP": "As Early as Possible",
    "ALAP": "As Late as Possible",
    "ASAP": "As Soon as Possible",
    "ASLA": "Age / Sex / Location?",
    "B3": "Blah, Blah, Blah",
    "B4YKI": "Before You Know it",
    "BAE": "Before Anyone else",
    "BMBAE": "Be My BAE",
    "BFF": "Best Friends, Forever",
    "BM&Y": "Between Me and You",
    "BRB": "Be right Back",
    "BRT": "Be right There",
    "BTAM": "Be that as it May",
    "C-P": "Sleepy",
    "CTN": "Cannot talk now",
    "CUS": "See You Soon",
    "CWOT": "Complete Waste of Time",
    "CYT": "See You Tomorrow",
    "E123": "Easy as 1, 2, 3",
    "EM?": "Excuse Me?",
    "EOD": "End of Day",
    "F2F": "Face to Face",
    "FC": "Fingers Crossed",
    "FOAF": "Friend of a Friend",
    "GR8": "Great",
    "HAK": "Hugs and Kisses",
    "IDC": "Don't Care",
    "IDK": "Don't Know",
    "ILU": "I Love You",
    "ILY": "I Love You",
    "IMU": "I Miss You",
    "IRL": "In Real Life",
    "J/K": "Just Kidding",
    "JC": "Just Checking",
    "JTLYK": "Just to Let You Know",
    "KFY": "Kiss for You",
    "KMN": "Kill Me Now",
    "KPC": "Keeping Parents Clueless",
    "L8R": "Later",
    "MoF": "Male or Female",
    "MTFBWY": "May the Force be with You",
    "MYOB": "Mind Your Own Business",
    "N-A-Y-L": "In a While",
    "NAZ": "Name, Address, ZIP",
    "NC": "No Comment",
    "NIMBY": "Not in my Backyard",
    "NM": "Never Mind / Nothing Much",
    "NP": "No Problem",
    "NSFW": "Not Safe for Work",
    "NTIM": "Not that it Matters",
    "NVM": "Never Mind",
    "OATUS": "On a totally Unrelated Subject",
    "OIC": "Oh, I See",
    "OMW": "On My Way",
    "OTL": "Out to Lunch",
    "OTP": "On the Phone/One Time password",
    "P911": "Parent Alert",
    "PAL": "Parents are Listening",
    "PAW": "Parents are Watching",
    "PIR": "Parent in Room",
    "POS": "Parent over Shoulder",
    "PROP(S)": "Proper Respect / Proper Recognition",
    "QT": "Cutie",
    "RN": "Right Now",
    "RU": "Are You",
    "SEPS": "Someone else's Problem",
    "SITD": "Still in the Dark",
    "SLAP": "Sounds like a Plan",
    "SMIM": "Send Me an Instant Message",
    "SO": "Significant Other",
    "TMI": "Too Much Information",
    "UR": "Your / You are",
    "W8": "Wait",
    "WB": "Welcome Back",
    "WYCM": "Will You Call Me?",
    "WYWH": "Wish You Were Here",
    "XOXOXOX": "Hugs, Kisses, LOVE"
}
    new_text=[]
    for w in text.split():
        if w.upper() in chat_words:
            new_text.append(chat_words[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)


def pipeline(text):
    text=remove_html_tags(text)
    text=remove_punc(text)
    text=chat_conversion(text)
    text=text.replace(r"\n","")
    return text


def chat(text):
    model=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    messages = [
        SystemMessage(f"You are a helpful AI Chatbot. Based on the context provided below about the site, you need to answer the questions carefully. Here is the site content: {text}.")
    ]

    while True:
        input_from_user = input("\n\nWhat do you want to ask?\nType 'exit' to quit.\n")
        if input_from_user.lower() == "exit":
            break
        
        # Add the user's message to the conversation history
        messages.append(HumanMessage(input_from_user))
        print("You said: ", input_from_user)

        # Get the model's response
        result = model.invoke(messages)

        # Print the model's answer
        print(f"Answer: {result.content}")

        # Add the model's response to the conversation history
        messages.append(AIMessage(result.content))


text=scrape(url)
text=pipeline(text)
chat(text)
    
