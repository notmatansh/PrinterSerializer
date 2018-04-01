from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict


class NestingSerializer(Serializer):
    nesting = {}  # inheriting serializers need to specify a new field name and fields to nest in it

    def _nest(self, flat_data, mapping, is_inner_nesting=False):
        """
        recursively nesting fields according to a pre-defined mapping
        Args:
            flat_data (dict): this is how the object looks like in the DB, this is our source for field values
            mapping (dict): we traverse the serializers .nesting dict, treating every inner dict as a nesting map
            is_inner_nesting (bool): once we are done "walking" the mapping we still have un-nested fields in the api
                                     this parameter flags that we have returned to the root of our mapping

        Returns:
            dict
        """
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
                    del flat_data[value]  # in order to later grab un-nested fields i clean up nested fields from dict

        if not is_inner_nesting:
            nested_data.update(flat_data)  # grabbing un-nested fields from the original dict
        return nested_data

    def _flatten(self, nested_data, mapping, api_fields):
        """
        recursively flattening nested data according to a pre-defined mapping
        Args:
            nested_data (dict): the data that is to be flattened
            mapping (dict): the mapping defines the correlation between nested fields and original flat fields
            api_fields (list): as we flatten data upon ingesting update/create requests we want to make sure we only
                               pass predefined fields available to the api (mapped in the serializers Meta.fields).
                               the reason this is a parameter is to avoid repeating the getattr operation on every recursion

        Returns:
            dict
        """
        flat_data = {}
        for key, value in nested_data.items():
            if isinstance(value, dict):
                flat_data.update(self._flatten(value, mapping[key], api_fields))

            else:
                if key in api_fields:
                    flat_data[key] = value
                else:
                    original_field_name = mapping[key]
                    if original_field_name in api_fields:
                        flat_data[original_field_name] = value

        return flat_data

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
        self._validated_data = self._flatten(self.initial_data, self.nesting, getattr(self.Meta, 'fields'))
        self._errors = []
        if 'id' in self._validated_data:
            # in order to support update actions (get the serializers .save() method to call .update()) i need to
            # populate self.instance
            model = getattr(self.Meta, 'model')
            obj_id = self._validated_data.pop('id')

            if model.objects.filter(id=obj_id).exists():
                self.instance = model.objects.get(id=obj_id)
        return True
        # I cant call the .is_valid() method on NestingSerializer's super (Serializer) because it wont support the
        # scenario where our model has a unique field, so we have to "play its part"

    def create(self, validated_data):
        model = getattr(self.Meta, 'model')
        new_obj = model.objects.create(**validated_data)
        return new_obj

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
