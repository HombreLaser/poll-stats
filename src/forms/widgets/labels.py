from wtforms.fields import Label


class CheckboxLabel(Label):
    def __call__(self, text=None, **kwargs):
        return super().__call__(**(kwargs | { 'class': 'form-check-label' }))