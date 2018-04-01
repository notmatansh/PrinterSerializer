from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict
from django.db.utils import IntegrityError


class NestingSerializer(Serializer):
    nesting = {}  # inheriting serializers need to specify a new field name and fields to nest in it

    def save(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:
            dict
        """
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

        if 'id' in flattened_data:
            obj_id = flattened_data.pop('id')

            if model.objects.filter(id=obj_id).exists():
                # updating an existing object
                obj = model.objects.get(id=obj_id)
                for k, v in flattened_data.items():
                    setattr(obj, k, v)
                obj.save()
                # retuning a dict of the updated object
                flattened_data['id'] = obj_id
                return flattened_data

        # if we don't have an object with the specified id we will create it but ignore the id passed in the API
        # if an id was not passed via the API then we just create a new object with given data
        new_obj = model.objects.create(**flattened_data)
        flattened_data['id'] = new_obj.id
        return flattened_data

    @property
    def data(self):
        """
        overriding the data property allows me to nest fields after they are validated by our serializer
        also, it allows me to add the id field that otherwise would be removed in serialization. the id fields allows
        me to easily support updating actions on objects via the api without the smallest chance of duplicating objects
        Returns:
            dict
        """
        super(NestingSerializer, self).is_valid()  # cant call .data before .is_valid
        super(NestingSerializer, self).data  # populates the self._data attribute
        self._data['id'] = self.initial_data['id']
        for new_key, value in self.nesting.items():
            if isinstance(value, dict):
                self._data[new_key] = {}
                for nested_key, original_field_name in value.items():
                    self._data[new_key][nested_key] = self._data[original_field_name]
                    del self._data[original_field_name]
        return ReturnDict(self._data, serializer=self)
