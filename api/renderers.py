import io

import rest_framework.renderers


class CsvRenderer(rest_framework.renderers.BaseRenderer):
    """
    All renderers should extend this class, setting the `media_type`
    and `format` attributes, and override the `.render()` method.
    """
    format = 'csv'
    media_type = 'text/plain'
    charset = 'utf-8'
    render_style = 'binary'

    def get_rows(self):
        """
        Override me in subclass. See prisoners/renderers.py for example.
        """
        return [('header1', 'header2'),
                ('data1', 'data2'),
                ('data3', 'data4')]

    def render(self, data, media_type=None, renderer_context=None):
        sio = io.StringIO()

        # Can't use `data' since it's paginated, so just rerun the query.
        # view = renderer_context['view']
        # queryset = list(view.filter_queryset(view.get_queryset()))
        queryset = data

        for row in self.get_rows(queryset):
            for i, col in enumerate(row):
                if i:
                    sio.write(u',')
                if col is None:
                    sio.write(u'')
                elif col is True:
                    sio.write(u'Y')
                elif col is False:
                    sio.write(u'N')
                else:
                    sio.write(u'"')
                    sio.write(unicode(col).replace(u'"', u'""'))
                    sio.write(u'"')
            sio.write(u'\n')

        return sio.getvalue().encode('utf-8')
