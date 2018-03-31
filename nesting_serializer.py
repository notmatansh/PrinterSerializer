from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict
from django.db.utils import IntegrityError


class NestingSerializer(Serializer):
    nesting = {}  # inheriting serializers need to specify a new field name and fields to nest in it

    def save(self, **kwargs):
        data = self.initial_data
        flattened_data = {}
        api_fields = getattr(self.Meta, 'fields')
        model = getattr(self.Meta, 'model')

        for key, value in data.items():
            if key in self.nesting:
                if isinstance(value, dict):
                    for field_name, field_value in value.items():
                        original_field_name = self.nesting[key][field_name]
                        if original_field_name in api_fields:
                            flattened_data[original_field_name] = field_value
            elif key in api_fields:
                flattened_data[key] = value

        try:
            model.objects.get_or_create(**flattened_data)
        except IntegrityError:
            try:
                model.objects.update(**flattened_data)
            except:
                pass
        raise RuntimeError('failed to persist inputted data for %s' % self.__class__.__name__)

    @property
    def data(self):
        super(NestingSerializer, self).is_valid()  # cant call .data before .is_valid
        super(NestingSerializer, self).data  # populates the self._data attribute
        for new_key, value in self.nesting.items():
            if isinstance(value, dict):
                self._data[new_key] = {}
                for nested_key, original_field_name in value.items():
                    self._data[new_key][nested_key] = self._data[original_field_name]
                    del self._data[original_field_name]
        return ReturnDict(self._data, serializer=self)
