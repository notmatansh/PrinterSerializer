from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict


class NestingSerializer(Serializer):
    nesting = {}  # inheriting serializers need to specify a new field name and fields to nest in it

    def is_valid(self, raise_exception=False):
        flattened_data = {}
        api_fields = getattr(self.Meta, 'fields')

        for key, value in self.initial_data.items():
            if key in self.nesting:
                if isinstance(value, dict):
                    for field_name, field_value in value.items():
                        original_field_name = self.nesting[key][field_name]
                        if original_field_name in api_fields:
                            flattened_data[original_field_name] = field_value
            elif key in api_fields:
                flattened_data[key] = value

        self._validated_data = flattened_data
        # I cant call the .is_valid() method on NestingSerializer's super (Serializer) because it wont support the
        # scenario where our model has a unique field, so we have to "play its part"

    def create(self, validated_data):
        model = getattr(self.Meta, 'model')
        new_obj = model.objects.create(**validated_data)
        # retuning a dict of the created object
        validated_data['id'] = new_obj.id
        return validated_data

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        # retuning a dict of the updated object
        validated_data['id'] = instance.id
        return validated_data

    def save(self, **kwargs):
        model = getattr(self.Meta, 'model')
        data = self.validated_data
        if 'id' in data:
            obj_id = data.pop('id')
            if model.objects.filter(id=obj_id).exists():
                obj = model.objects.get(id=obj_id)
                return self.update(obj, data)

        return self.create(data)

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
