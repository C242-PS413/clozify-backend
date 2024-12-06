class Weather:
    def __init__(self, city: str, temp: float, preciptype: list):
        self.city = city
        self.temp = temp
        self.preciptype = preciptype

    def to_dict(self):
        return {
            "city": self.city,
            "temp": self.temp,
            "preciptype": self.preciptype,
        }

    @staticmethod
    def from_dict(data: dict):
        return Weather(
            city=data.get("city", ""),
            temp=data.get("temp", 0.0),
            preciptype=data.get("preciptype", [])
        )