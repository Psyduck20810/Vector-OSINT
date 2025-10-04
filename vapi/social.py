


import json
import requests
import time
from bs4 import BeautifulSoup
from vapi import phonelocfinder
from vapi.poor import color
from vapi.error import exp
from vapi.bios import biose
from vapi import breach
from vapi import visvapi

class info:
    nickname = None
    name = None
    location = None
    locations = []
    email = ""
    bio = None
    web = None
    bio_s = []
    phone = None


class social:
    save = "./vapi/save/info.txt"
    social_json = "./vapi/vapi_db/social.json"
    config_json = "config.json"
    style = ""
    with open(config_json,"r") as c:
        data = json.loads(c.read())
        style = data["style"]
    with open(social_json, "r") as f:
        data = json.loads(f.read())


def scrape_c(classname, website):
    try:
        if classname.startswith("span::"):
            classname = classname.split("span::")[1]
            req = requests.get(website).text
            soup = BeautifulSoup(req, "html.parser")
            # cll = soup.find(class_=classname)
            cll = soup.find("span", {"class": classname})
            if cll.text != None:
                return cll.text
            else:
                return "nothing"

        elif classname.startswith("div::"):
            classname = classname.split("div::")[1]
            req = requests.get(website).text
            soup = BeautifulSoup(req, "html.parser")
            # cll = soup.find(class_=classname)
            cll = soup.find("div", {"class": classname})
            if cll.text != None:
                cll = cll.text.split()
                out = ""
                for i in cll:
                    out += i + " "
                return out
            else:
                return "nothing"

        elif classname.startswith("p::"):
            classname = classname.split("p::")[1]
            req = requests.get(website).text
            soup = BeautifulSoup(req, "html.parser")
            # cll = soup.find(class_=classname)
            cll = soup.find("p", {"class": classname})
            if cll.text != None:
                return cll.text
            else:
                return "nothing"

        elif classname.startswith("text"):
            cll = requests.get(website).text
            if cll.text != None:
                return cll.text
            else:
                return "nothing"

        elif classname.startswith("ul::"):
            classname = classname.split("ul::")[1]
            req = requests.get(website).text
            soup = BeautifulSoup(req, "html.parser")
            # cll = soup.find(class_=classname)
            cll = soup.find("ul", {"class", classname})
            if cll.text != None:
                return cll.text
            else:
                return "nothing"
        elif classname.startswith("body"):
            req = requests.get(website).text
            soup = BeautifulSoup(req, "html.parser")
            # cll = soup.find(class_=classname)
            cll = soup.body
            if cll.text != None:
                return cll.text
            else:
                return "nothing"

        elif classname.startswith("json::"):
            classname = classname.split("json::")[1]
            req = requests.get(website).text
            data = json.loads(req)
            cll = data[classname]
            if cll.text != None:
                return cll.text
            else:
                return "nothing"
    except:
        return "nothing"


from vapi import phonelocfinder

def itype(clt, dt):
    """
    Non-recursive setter for parsed info fields.
    clt is one of: 'Bio', 'Location', 'Email', 'Website', etc.
    dt is the value extracted for that class/type.
    """
    # Guard: ignore empty / numeric values
    if dt is None or isinstance(dt, (int, float)):
        return

    # Normalize to string for safety
    try:
        val = dt if isinstance(dt, str) else str(dt)
    except Exception:
        return

    # NOTE: Do not call itype() from inside itself. Set fields directly.
    if clt == "Bio":
        # keep original behavior seen elsewhere in code
        try:
            info.bio_s.append(val)
        except Exception:
            pass

        # optional: extract phone once from bio (no recursion)
        try:
            ph = biose(val, "phone_num")
            if ph and ph != "invalid":
                info.phone = ph

                # 🔹 integrate phonelocfinder here
                pl = phonelocfinder.lookup_phone(info.phone, default_region="IN")
                print(
                    f"[+] Phone parse: valid={pl['valid']}, "
                    f"e164={pl['e164']}, country={pl['country']}, "
                    f"carrier={pl['carrier']}, loc={pl['location']}"
                )
                info.phone_info = pl
        except Exception:
            pass

        if getattr(info, "bio", None) in (None, "", "None"):
            info.bio = val
        return

    if clt == "Location":
        # Set location as-is (NO further biose or itype calls)
        info.location = val
        return

    if clt == "Email":
        # basic sanity
        if "@" in val:
            info.email = val
        return

    if clt == "Website":
        info.web = val
        return

    # Add any other simple types here if used by the tool
    # e.g., if clt == "Real Name": info.realname = val
    # Default: nothing
    return



def exp_check(n):
    entry = social.data.get(f"{n}", {})   # get dict for site n, or empty dict
    url = entry.get("url", "")            # default to "" if no 'url'
    code = "0x0"                          # default code
    parm = url                            # default parameter

    try:
        if url:  # only request if URL is present
            req = requests.get(url, timeout=5)
            if req.status_code == 200:
                code = "0x1"
                parm = url
            else:
                code = f"HTTP{req.status_code}"
                parm = url
        else:
            code = "0x2"   # no URL configured
            parm = "missing-url"
    except Exception:
        code = "0x2"
        parm = url or "error"

    return [code, parm]



def run(nick):
    social_links = []
    info.nickname = nick
    # print(f"Hello {nick}!")

    for n in range(1, social.data["count"] + 1):
        look = social.data[f"{n}"]["look"].format(nick)
        problem = False
        try:
            req = requests.get(look)
        except:
            problem = True

        if(social.style=="E0"):
            if problem == False:
                if type(social.data[f"{n}"]["nf"]) == int:
                    if(req.status_code != social.data[f"{n}"]["nf"]):
                        if (social.data[f"{n}"]["cll"] != "None" and scrape_c(social.data[f"{n}"]["cll"], look) != "nothing"):
                            scc = scrape_c(social.data[f"{n}"]["cll"], look)
                            itype(social.data[f"{n}"]["cll_t"], scc)
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f"""[{color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE}]{color.CGREEN}[{color.CWHITE}
                            
        {nick} {color.CBLUE}--> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
        {color.CWHITE}Type : {color.CWHITE2}{social.data[f"{n}"]["type"]}
        {color.CWHITE}Most used Country :{color.CWHITE2} {social.data[f"{n}"]["cn"]}
        {color.CBLUE}[+] {color.CWHITE}{social.data[f"{n}"]["cll_t"]} : {color.CWHITE2}{scc}                   
{color.CGREEN}]{color.CWHITE}""")
                            
                            
                        else:
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f"""[{color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE}]{color.CGREEN}[{color.CWHITE}

        {nick} {color.CBLUE}--> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
        {color.CWHITE}Type : {color.CWHITE2}{social.data[f"{n}"]["type"]}
        {color.CWHITE}Most used Country :{color.CWHITE2} {social.data[f"{n}"]["cn"]}              
{color.CGREEN}]{color.CWHITE}""")
                else:
                    if((social.data[f"{n}"]["nf"] in req.text) == False):
                        if (social.data[f"{n}"]["cll"] != "None" and scrape_c(social.data[f"{n}"]["cll"], look) != "nothing"):
                            scc = scrape_c(social.data[f"{n}"]["cll"], look)
                            itype(social.data[f"{n}"]["cll_t"], scc)
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f"""[{color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE}]{color.CGREEN}[{color.CWHITE}

        {nick} {color.CBLUE}--> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
        {color.CWHITE}Type : {color.CWHITE2}{social.data[f"{n}"]["type"]}
        {color.CWHITE}Most used Country :{color.CWHITE2} {social.data[f"{n}"]["cn"]}
        {color.CBLUE}[+] {color.CWHITE}{social.data[f"{n}"]["cll_t"]} : {color.CWHITE2}{scc}                   
{color.CGREEN}]{color.CWHITE}""")
                            
                        else:
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f"""[{color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE}]{color.CGREEN}[{color.CWHITE}

        {nick} {color.CBLUE}--> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
        {color.CWHITE}Type : {color.CWHITE2}{social.data[f"{n}"]["type"]}
        {color.CWHITE}Most used Country :{color.CWHITE2} {social.data[f"{n}"]["cn"]}                  
{color.CGREEN}]{color.CWHITE}""")

            else:
                expc = exp_check(n)
                print(exp(expc[0],expc[1],nick))
                problem = False
                
        elif(social.style=="E1"):
            if problem == False:
                if type(social.data[f"{n}"]["nf"]) == int:
                    if(req.status_code != social.data[f"{n}"]["nf"]):
                        if (social.data[f"{n}"]["cll"] != "None" and scrape_c(social.data[f"{n}"]["cll"], look) != "nothing"):
                            scc = scrape_c(social.data[f"{n}"]["cll"], look)
                            itype(social.data[f"{n}"]["cll_t"], scc)
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f'''{color.CGREEN}[{time.strftime("%R")}] {color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE} --> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
{color.CBLUE}[!] {color.CWHITE2}{social.data[f"{n}"]["cll_t"]} : {scc}''')
                            
                            
                        else:
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f'''{color.CGREEN}[{time.strftime("%R")}] {color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE} --> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}''')
                else:
                    if((social.data[f"{n}"]["nf"] in req.text) == False):
                        if (social.data[f"{n}"]["cll"] != "None" and scrape_c(social.data[f"{n}"]["cll"], look) != "nothing"):
                            scc = scrape_c(social.data[f"{n}"]["cll"], look)
                            itype(social.data[f"{n}"]["cll_t"], scc)
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f'''{color.CGREEN}[{time.strftime("%R")}] {color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE} --> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}
{color.CBLUE}[!] {color.CWHITE2}{social.data[f"{n}"]["cll_t"]} : {scc}''')
                            
                        else:
                            social_links.append(social.data[f"{n}"]["name"])
                            print(f'''{color.CGREEN}[{time.strftime("%R")}] {color.CWHITE2}{social.data[f"{n}"]["name"]}{color.CWHITE} --> {color.CWHITE2}{social.data[f"{n}"]["look"].format(nick)}''')

            else:
                expc = exp_check(n)
                print(exp(expc[0],expc[1],nick))
                problem = False

    print(f"""
{color.CBLUE}[*]{color.CWHITE2} Vector Social Osint Result :
    Nick Name : {info.nickname}
    Real Name : {info.name}
    Location  : {info.location}
    Email     : {info.email}
    Bio       : {info.bio}
    Web       : {info.web}
    Phone Num : {info.phone}
    """)
    
    
    nickname = info.nickname
    name = info.name 
    locations= info.locations
    email = info.email
    bio_s = info.bio_s
    breach.run(None,nick)
    visvapi.run(nickname,name,locations,email,social_links)
