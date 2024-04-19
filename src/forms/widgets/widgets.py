import wtforms.widgets as wtforms_widgets


class AttrSetter:
    def _attrs(self, params: dict, **kwargs):
        css_class = kwargs.pop('class', '') or kwargs.pop('class', '')
        params_except_class = { key: params[key] for key in set(list(params.keys())) - set(['class']) }
        render_params = {
            'class': '%s %s' % (params.get('class'), css_class)
        }

        return kwargs | render_params | params_except_class


class TextInputWidget(AttrSetter, wtforms_widgets.TextInput):
    def __call__(self, field, **kwargs):
        return super().__call__(field, **self._attrs(**kwargs))

    def _attrs(self, **kwargs):
        return super()._attrs({ 'class': 'form-control' }, **kwargs)


class PasswordInputWidget(TextInputWidget):
    def _attrs(self, **kwargs):
        return super()._attrs(**(kwargs | { 'type': 'password' }))


class CheckboxInputWidget(AttrSetter, wtforms_widgets.CheckboxInput):
    def __call__(self, field, **kwargs):
        return super().__call__(field, **self._attrs(**kwargs))

    def _attrs(self, **kwargs):
        return super()._attrs({ 'class': 'form-check-input' })