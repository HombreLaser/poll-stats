from wtforms import Field


class ListField(Field):
    widget = None

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist
        else:
            self.data = []