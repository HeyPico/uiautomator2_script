import uiautomator2 as u2
import time
from utils import app_launch, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def check_price(destination, pickup_time):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=True)
        time.sleep(3)
        accept_permissions(d)
        clear_unexpected_popups(d)
        time.sleep(1)
        # Call login checker
        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        clear_unexpected_popups(d)

        # Continue automation like booking ride
        print("📲 Proceeding to book ride...")
        while not d(text="Search for a destination").exists():
            time.sleep(0.2)
            if d(text="Cari lokasi tujuan").exists(): # add other languages
                # change to english flow
                d(resourceId="com.gojek.app:id/2131364856").click()
                time.sleep(0.2)
                d.swipe(0.5, 0.6, 0.5, 0.5, duration=0.05)
                time.sleep(0.15)
                time.sleep(0.2)
                if d(text="Pilihan bahasa").exists():
                    d(text="Pilihan bahasa").click()
                else:
                    d(textContains="language").click()
                time.sleep(0.2)
                d(textContains="English").click()
                d(resourceId="android:id/button1").click()
                time.sleep(0.2)
        d(text="Search for a destination").click()
        while not d(resourceId="com.gojek.app:id/2131367370").exists():
            time.sleep(0.1)
            print("waiting for search bar")
        d(resourceId="com.gojek.app:id/2131367370").send_keys(destination) # resource id for destination search bar
        while not d(resourceId="com.gojek.app:id/2131380508").exists():
            time.sleep(0.2)
            print("waiting for list")
        # time.sleep()
        if d(resourceId="com.gojek.app:id/2131362500").exists(): # promo
            d(resourceId="com.gojek.app:id/2131362500").click()
        time.sleep(0.2)
        d(resourceId="com.gojek.app:id/2131380508").click() # click first element in the list
        

        # while not d(text="Select via map").exists():
        #     time.sleep(0.1)
        # time.sleep(0.5)
        # d(text="Select via map").click() # this element has no id, just use text
        # # time.sleep(1.5)

        while not d(resourceId="com.gojek.app:id/2131381640").exists():
            time.sleep(0.1)
            print("waiting for next button")
        time.sleep(0.2)

        elNext = find_components(d, "next")
        nextCoord = coordinate_bounds(elNext["bounds"])
        d.click(*nextCoord)
        
        while not d(resourceId="com.gojek.app:id/text_service_pricing").exists():
            time.sleep(0.1)
        time.sleep(0.2)

        foryouComp = find_components(d, "for you")
        foryouCoord = coordinate_bounds(foryouComp["bounds"])
        d.click(*foryouCoord)

        # get all rides
        while not d(resourceId="com.gojek.app:id/text_service_pricing").exists():
            time.sleep(0.1)
        time.sleep(0.3)
        titleComps = find_components_by_id(d, "com.gojek.app:id/2131378741")
        priceComps = find_components_by_id(d, "com.gojek.app:id/text_service_pricing")
        rides = []
        rides = [{"title": titleComp["text"], "price": priceComp["text"]} for titleComp, priceComp in zip(titleComps, priceComps)]
        print(rides)

        return rides


    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
    
if __name__ == "__main__":
    check_price("plaza singapura", "now")
    # d = u2.connect()
    # # sess = d.session("com.gojek.app") 
    # d.app_start("com.gojek.app", stop=False)
    # if d(text="Pilihan bahasa").exists():
    #     d(text="Pilihan bahasa").click()
    # else:
    #     d(text="Language").click()
    # time.sleep(0.2)
    # d(textContains="English").click()
    # d(resourceId="android:id/button1").click()
