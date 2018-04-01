from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict


class NestingSerializer(Serializer):
    nesting = {}  # inheriting serializers need to specify a new field name and fields to nest in it

    def _nest(self, flat_data, mapping, is_inner_nesting=False):
        nested_data = {}
        for nesting_key, value in mapping.items():
            if isinstance(value, dict):
                # if value is a dict then it contains mappings of keys to original values
                nested_data[nesting_key] = self._nest(flat_data, value, is_inner_nesting=True)

            elif isinstance(value, str):
                # if value is a string the it is the original fields name in the flat data structure
                if value in flat_data:
                    # if the model object does not contain the mapped field skip
                    nested_data[nesting_key] = flat_data[value]
                    del flat_data[value]

        if not is_inner_nesting:
            nested_data.update(flat_data)
        return nested_data

    def _flatten(self):
        pass

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
        self._data = self._nest(self._data, self.nesting)
        return ReturnDict(self._data, serializer=self)

    def is_valid(self, raise_exception=False):
        """

        Args:
            raise_exception: actually ignored, keeping it here in order to preserve the original interface

        Returns:
            bool: except for the bool return value, the actual output of .is_valid() is populating the ._validated_data
            attribute that is required for utilizing .validated_data
        """
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
        return True
        # I cant call the .is_valid() method on NestingSerializer's super (Serializer) because it wont support the
        # scenario where our model has a unique field, so we have to "play its part"

    def save(self, **kwargs):
        """
        Args:
            **kwargs:

        Returns:
            object:
        """
        model = getattr(self.Meta, 'model')
        data = self.validated_data
        if 'id' in data:
            obj_id = data.pop('id')
            if model.objects.filter(id=obj_id).exists():
                obj = model.objects.get(id=obj_id)
                return self.update(obj, data)

        return self.create(data)

    def create(self, validated_data):
        """

        Args:
            validated_data (dict):

        Returns:
            object:
        """
        model = getattr(self.Meta, 'model')
        new_obj = model.objects.create(**validated_data)
        return new_obj

    def update(self, instance, validated_data):
        """

        Args:
            instance:
            validated_data:

        Returns:
            object:
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
