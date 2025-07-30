from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict


@dataclass
class BookingOption:
    title: str
    app: str
    price: int
    option_id: str


@dataclass
class SelectedOption:
    title: str
    app: str
    option_id: str


@dataclass
class BookingResult:
    status: Literal["success", "failed"]
    waiting_time: int

@dataclass
class LoginInfo:
    phone_number: str
    otp: str


@dataclass
class TransportBookingData:
    pickup_location: Optional[str] = None  # e.g. "current_location" or address
    is_saved_pickup: bool = False
    destination: Optional[str] = None
    is_saved_destination: bool = False
    time: Optional[str] = "now"  # Future support
    app: Optional[str] = None  # "grab", "gojek", etc.
    is_logged_in: bool = True
    login_info: Optional[LoginInfo] = None
    is_payment_default_exist: bool = True  # "cash", "wallet", etc.
    confirmation_check_done: bool = False
    booking_options: List[BookingOption] = field(default_factory=list)
    selected_option: Optional[SelectedOption] = None
    booking_result: Optional[BookingResult] = None
    cancelled: bool = False


@dataclass
class FlowState:
    flow: Literal["transport_booking"]
    step: Literal[
        "start",
        "awaiting_missing_info",
        "login",
        "login_otp_pending"
        "confirmation_check_pending",
        "awaiting_user_confirmation",
        "booking_in_progress",
        "handle_waiting_time",
        "cancel_and_restart",
        "done"
    ]
    data: TransportBookingData


def parse_booking_options(raw_list):
    return [BookingOption(**opt) for opt in raw_list]

def parse_selected_option(raw):
    return SelectedOption(**raw) if raw else None

def parse_booking_result(raw):
    return BookingResult(**raw) if raw else None

def parse_login_info(raw):
    return LoginInfo(**raw) if raw else None

def fetch_rides(rides):
    booking_options = []
    for i, opt in enumerate(rides):
        booking_options.append(
            BookingOption(
                title=opt["title"],
                app="grab",
                price=opt["price"],
                option_id=f"{opt['title'].lower().replace(' ', '')}-grab-{i:03}"
            )
        )
    return booking_options

@dataclass
class LoginInfo:
    phone_number: str = ""
    otp: str = ""

@dataclass
class FoodItem:
    name: str
    quantity: int = 1
    customization: str = ""

@dataclass
class MenuOption:
    app: str
    price: float
    option_id: str
    orders: List[FoodItem] = field(default_factory=list)

@dataclass
class SelectedOption:
    title: str = ""
    app: str = ""
    option_id: str = ""

@dataclass
class OrderResult:
    status: str = ""
    estimated_delivery_time: int = 0

@dataclass
class FoodOrderData:
    delivery_location: str = ""
    delivery_note: str = ""
    restaurant_name: str = ""
    food_items: List[FoodItem] = field(default_factory=list)
    app: Optional[str] = None
    is_logged_in: bool = True
    login_info: LoginInfo = field(default_factory=LoginInfo)
    is_payment_default_exist: bool = True
    confirmation_check_done: bool = False
    menu_options: List[MenuOption] = field(default_factory=list)
    selected_option: SelectedOption = field(default_factory=SelectedOption)
    order_result: OrderResult = field(default_factory=OrderResult)
    cancelled: bool = False

class MessageLoginInfo:
    qr: str = ""
@dataclass
class MessageAddContact:
    name: str
    number: str
    app: str


@dataclass
class ToOptions:
    to: str
    options: List[str]

def parse_to_options(raw_to_options):
    return [ToOptions(**opt) for opt in raw_to_options]

@dataclass
class MessageData:
    step: str
    app: str
    to: List[str]
    message: str
    add_contact: Optional[MessageAddContact] = None
    to_options: Optional[List[ToOptions]] = None
    image: str = ""
    login_qr: str = ""

def parse_to(raw_to):
    return [str(i) for i in raw_to]
@dataclass
class FlowStateFood:
    flow: str
    step: str
    data: FoodOrderData

# Parsers

def parse_login_info(info) -> LoginInfo:
    info = info or {}  # Ensure it's a dict
    return LoginInfo(
        phone_number=info.get("phone_number", ""),
        otp=info.get("otp", ""),
    )

def parse_food_items(items) -> List[FoodItem]:
    return [FoodItem(**item) for item in items if "name" in item]

def parse_menu_options(options) -> List[MenuOption]:
    return [MenuOption(**opt) for opt in options if "title" in opt]

def parse_selected_option(opt) -> SelectedOption:
    return SelectedOption(**opt) if opt else SelectedOption()

def parse_order_result(result) -> OrderResult:
    return OrderResult(**result) if result else OrderResult()
