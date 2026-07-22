from enum import Enum
import datetime
from utils import format_address

class PackageStatus(Enum):
    AT_HUB = 'at the hub'
    EN_ROUTE = 'en route'
    DELIVERED = 'delivered'
    DELAYED = 'delayed'

class Package:
    def __init__(self, package_id, street_address, city, state, zip_code, delivery_deadline, weight_kg, special_notes):
        self.package_id: int = package_id
        self.street_address: str = street_address
        self.city: str = city
        self.state: str = state
        self.zip_code: str = zip_code
        self.delivery_deadline: datetime.time = delivery_deadline
        self.weight_kg: int = weight_kg
        self.special_notes: str = special_notes
        self.status = PackageStatus.AT_HUB
        self.delivery_time = None

    def set_street_address(self, address):
        self.street_address = address

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code

    def set_address(self, street_address, city, state, zip_code):
        self.set_street_address(street_address)
        self.set_city(city)
        self.set_state(state)
        self.set_zip_code(zip_code)

    def set_status(self, status: PackageStatus):
        self.status = status

    def get_formatted_address(self):
        return format_address(self.street_address, self.zip_code)
    
    def get_delivery_time(self):
        return self.delivery_time
    
    def set_delivery_time(self, time):
        self.delivery_time = time

    def __str__(self):
        full_address = f"{self.street_address} {self.city}, {self.state} {self.zip_code}"

        if len(full_address) > 50:
            full_address = full_address[:47] + "..."
        del_time = str(self.delivery_time) if self.delivery_time is not None else "N/A"
        deadline = str(self.delivery_deadline) if self.delivery_deadline is not None else "N/A"

        return (
            f"Package ID: {self.package_id:<2} | "
            f"Address: {full_address:<50} | "
            f"Status: {self.status.value:12} | "
            f"Delivery Time: {del_time:<8} | "
            f"Delivery Deadline: {deadline:<8} | "
            f"Weight: {self.weight_kg:<3} kg"
        )