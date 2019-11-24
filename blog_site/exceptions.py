class HasNoProfile(Exception):

    def __init__(self, value, module, scope):
        self.value = value
        self.module = module
        self.scope = scope

    def __str__(self):
        return f"error {self.value} in {self.module} at {self.scope}"
