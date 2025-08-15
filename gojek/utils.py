import time
import re
import xml.etree.ElementTree as ET

def app_launch(d):
    try:
        # Look for login screen indicators
        login_keywords = ["login", "sign in", "log in"]
        for keyword in login_keywords:
            if d(textMatches=f"(?i)^{keyword}$").exists():
                print("❌ Not logged in. Please log in first.")
                return True

        # Look for home screen keywords as positive signal
        home_keywords = ["search", "redeem", "adventure"]
        xml = d.dump_hierarchy()  # Get UI XML
        root = ET.fromstring(xml)
        for node in root.iter():
            print("node", node.attrib)
            if node.attrib.get("text") is not None:  # Only include Android widgets
                text = node.attrib.get("text", "")
                for keyword in home_keywords:
                        if keyword in text:
                            return True
        return False
    except Exception as e:
        print("waiting for launch")
        return False
def check_login_status(d):
    """
    Checks whether the user is logged in to the Grab app.
    Returns True if logged in, False otherwise.
    Raises exception if something goes wrong.
    """
    try:
        # Look for login screen indicators
        login_keywords = ["login", "sign in", "log in"]
        for keyword in login_keywords:
            if d(textMatches=f"(?i)^{keyword}$").exists():
                print("❌ Not logged in. Please log in first.")
                return False

        # Look for home screen keywords as positive signal
        home_keywords = ["search", "redeem", "adventure", "save", "simpan"]
        for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in home_keywords:
                                if keyword in text:
                                    return True
                        except Exception as e:
                            print("⚠️ Could not determine login status. Assuming not logged in.")
                            return False

    except Exception as e:
        print(f"[Error] Failed to check login status: {e}")
        return False
    

def clear_unexpected_popups(d):
    """
    Try to close popus.
    """
    print("=== DEBUG: Checking popups ===")

    yes_word = ["ok", "yes", "accept", "allow", "turn on", "awesome"]
    texts = []
    for el in d.xpath("//*").all():
            text = el.attrib.get("text", "").strip()
            texts.append(text.lower())
    try:
        for _ in range(3):  # Multiple attempts in case of multiple layers
            
            if any("welcome" in t.lower() for t in texts):
                    print("Found text with 'welcome'")
                    for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in yes_word:
                                if keyword in text:
                                    print(f"[Match] Trying to click: '{text}'")
                                    el.click()
                                    print(f"[Clicked] Matched: {text}")
                                    break  # stop after one match
                        except Exception as e:
                            print(f"[Error] While processing node: {e}")
        print("=== DEBUG: Checking popups finished ===")
                    
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

def accept_permissions(d):
    """
    Try to accept permissions.
    """
    print("=== DEBUG: Checking permissions ===")
    yes_word = ["ok", "yes", "accept", "allow", "turn on", "awesome"]

    try:
        
        for _ in range(3):  # Multiple attempts in case of multiple layers
            if d(textContains="access").wait(timeout=0.1) or d(textContains="welcome").wait(timeout=0.1):
                    print("Found text with 'access'")
                    for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in yes_word:
                                if keyword in text:
                                    print(f"[Match] Trying to click: '{text}'")
                                    el.click()
                                    print(f"[Clicked] Matched: {text}")
                                    break  # stop after one match
                        except Exception as e:
                            print(f"[Error] While processing node: {e}")
                    print("=== DEBUG: All clickable elements ===")
                    for el in d.xpath("//*").all():
                        text = el.attrib.get("text", "").strip()
        print("=== DEBUG: Checking permissions finished ===")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

def screen_components(d):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    elements = []
    for node in root.iter():
        if (not node.attrib.get("package", "").startswith("com.android")) and node.attrib.get("clickable") == "true":  # Only include Android widgets
            print(node.attrib)
        res_id = node.attrib.get("resource-id", "")
        text = node.attrib.get("text", "")
        if res_id or text:  # Only include elements with at least one property
            elements.append({
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            })
    # Print all elements with both properties
    for elem in elements:
        if elem["resource-id"] and elem["text"]:
            print(f"ID: {elem['resource-id']} | Text: '{elem['text']}' | Class: {elem['class']} | Bounds: {elem['bounds']} | Clickable: {elem['clickable']}")

def find_components(d, text: str):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    for node in root.iter():
        if node.attrib.get("text") is not None and text in node.attrib.get("text").lower():  # Only include Android widgets
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "")
            return {
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            }
def find_components_by_id(d, id: str):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    comps = []
    for node in root.iter():
        if node.attrib.get("resource-id") == id:  # Only include Android widgets
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "")
            comps.append({
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            })
    return comps
def coordinate_bounds(bounds: str):
    x1, y1, x2, y2 = map(int, bounds.strip("[]").replace("][", ",").split(","))
    # Calculate center (x, y)
    center_x = (x1 + x2) // 2 
    center_y = (y1 + y2) // 2 
    return center_x, center_y