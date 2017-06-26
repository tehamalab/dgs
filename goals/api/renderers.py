from rest_framework_csv.renderers import CSVStreamingRenderer


class CSVRenderer (CSVStreamingRenderer):
    results_field = 'results'

    def render(self, data, *args, **kwargs):
        if not isinstance(data, list) and self.results_field in data:
            data = data.get(self.results_field, [])
        return super(CSVRenderer, self).render(data, *args, **kwargs)
