class Mr:
    def clean(message):
        lower_case = Mr.lower(message)
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)

    def lower(message):
        return message.lower()

    def title(message):
        spaced_message = Mr.stripper(message.replace("-", " ").replace("_", " "))
        return spaced_message.title()

    def stripper(message):
        return message.strip()