class FormWithDateFields:
    """
    Add field attributes to use a datepicket component
    """

    date_fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.date_fields:
            self.fields[field_name].widget.attrs["data-provide"] = "datepicker"
            self.fields[field_name].widget.attrs["data-date-format"] = "yyyy-mm-dd"
