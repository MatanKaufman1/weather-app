class NoLocation(Exception):
    def __init__(self):
        self.message = " Cant find location."
        super().__init__(self.message)


class NoApiResponse(Exception):
    def __init__(self):
        self.message = "Error while getting API response"
        super().__init__(self.message)


class ErrorProcessingData(Exception):
    def __init__(self):
        self.message = "Error while processing the data"
        super().__init__(self.message)


class ErrorCalculate(Exception):
    def __init__(self):
        self.message = "No valid data for this location"
        super().__init__(self.message)


if __name__ == '__main__':
    pass
