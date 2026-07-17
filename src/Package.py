from enum import Enum
import datetime

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
        self.zip_code: int = zip_code
        self.delivery_deadline: datetime.time = delivery_deadline
        self.weight_kg: int = weight_kg
        self.special_notes: str = special_notes
        self.status = PackageStatus.AT_HUB

    def set_status(self, status: PackageStatus):
        self.status = status