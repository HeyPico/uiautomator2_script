# check_price.py
import threading
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
from general import check_login_status, clear_unexpected_popups, accept_permissions, notify_n8n

def confirmation_check_handler(pickup_loc, is_saved_pickup, destination, is_saved_destination, pickup_time):
    print(f"🚖 Booking ride to {destination} at {pickup_time}...")
    try:
        d = u2.connect()
        sess = d.session("com.grabtaxi.passenger") 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()


        # Call login checker
        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        
        while not sess(text="Transport").exists():
            time.sleep(0.2)
            if d(text="Transportasi").exists() or d(text="出行").exists(): # add other languages
                # change to english flow
                d(resourceId="com.grabtaxi.passenger:id/account_entry_point_image").click()
                d(scrollable=True).scroll.toEnd()
                time.sleep(0.2)
                d.swipe(0.5, 0.7, 0.5, 0.5, duration=0.05)
                time.sleep(0.2)
                if d(text="Bahasa").exists():
                    d(text="Bahasa").click()
                else :
                    d(text="Language").click()
                time.sleep(0.3)
                d(className="android.view.View")[2].click()
                time.sleep(0.3)
                d(text="English").click()
                time.sleep(0.2)
                # confirm
                d(resourceId="android:id/button1").click()
                time.sleep(0.3)
        sess(text="Transport").click()

        while not sess(text="Where to?").exists():
            time.sleep(0.1)
        sess(text="Where to?").click()

        while not d(text="Saved").exists():
            time.sleep(0.2)
        
        if pickup_loc != "current_location":
            if is_saved_pickup:
                d(text="Saved").click()
                ls = d(resourceId="com.grabtaxi.passenger:id/list_item_heading")
                for l in ls:
                    if l.get_text().lower() == pickup_loc:
                        l.click()
                        break
            else:
                sess(resourceId="com.grabtaxi.passenger:id/poi_first_search").send_keys(pickup_loc)
                
        if is_saved_destination:
            d(text="Saved").click()
            ls = d(resourceId="com.grabtaxi.passenger:id/list_item_heading")
            for l in ls:
                if l.get_text().lower() == destination:
                    l.click()
                    break
        else:
            sess(resourceId="com.grabtaxi.passenger:id/poi_second_search").send_keys(destination)

        while not sess(resourceId="com.grabtaxi.passenger:id/list_item_with_additional_info_container_parent", instance=0).exists():
            time.sleep(0.1) # Wait for the UI to update
        sess(resourceId="com.grabtaxi.passenger:id/list_item_with_additional_info_container_parent", instance=0).click()
        sess(text="Choose This Pickup").click()

        while not sess(resourceId="com.grabtaxi.passenger:id/xsell_confirmation_item_container").exists():
            time.sleep(0.1) # Wait for the UI to update
        xml_dump = d.dump_hierarchy()
        tree = ET.fromstring(xml_dump)
        ride_infos = []
        # Find the container node for all ride options
        for item in tree.iter():
            if item.attrib.get("resource-id") == "com.grabtaxi.passenger:id/xsell_confirmation_item_container":
                ride_info = {}

                for sub in item.iter():
                    rid = sub.attrib.get("resource-id", "")
                    text = sub.attrib.get("text", "").strip()

                    if rid == "com.grabtaxi.passenger:id/xsell_confirmation_taxi_type_name":
                        ride_info["title"] = text
                    elif rid == "com.grabtaxi.passenger:id/xsell_confirmation_taxi_type_subtitle":
                        ride_info["subtitle"] = text
                    elif rid == "com.grabtaxi.passenger:id/fareTextView":
                        ride_info["price"] = text

                ride_infos.append(ride_info)
        print("📲 Ride confirmation success...")
        return (ride_infos)
    except Exception as e:
        d = u2.connect()
        d.app_start("org.telegram.messenger") 
        print(f"Error occurred: {e}")
        # notify_n8n("1333039921", e)
        return {"message": str(e)}

if __name__ == "__main__":
    confirmation_check_handler("jalan merdeka", "now", "", "", "")
    # d = u2.connect()
    # d.app_start("com.grabtaxi.passenger", stop=False)
    # d(className="android.view.View")[2].click()
    # print("don")
