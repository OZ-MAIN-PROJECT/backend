from rest_framework.renderers import JSONRenderer
import humps


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is not None:
            data = humps.camelize(data)
        return super().render(data, accepted_media_type, renderer_context)
