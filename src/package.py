from enum import Enum
import datetime
from utils import format_address

class PackageStatus(Enum):
    AT_HUB = 'at the hub'
    EN_ROUTE = 'en route'
    DELIVERED = 'delivered'

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

    def set_status(self, status: PackageStatus):
        self.status = status

    def get_formatted_address(self):
        return format_address(self.street_address, self.zip_code)
    
    def set_delivery_time(self, time):
        self.delivery_time = time

    def __str__(self):
        return (
            f"Package ID: {self.package_id}\n"
            f"Address: {self.street_address} {self.city}, {self.state} {self.zip_code}\n"
            f"Delivery Deadline: {self.delivery_deadline}\n"
            f"Delivery Time: {self.delivery_time}\n"
            f"Package Weight: {self.weight_kg} kg\n"
            f"Delivery Status: {self.status.value}"
        )