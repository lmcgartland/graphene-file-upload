from collections import OrderedDict
from django.forms import FileField
import graphene
from graphene import Field, InputField
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.registry import get_global_registry
from graphene_django.forms.converter import convert_form_field
from graphene_django.forms.types import ErrorType
from graphene_django.forms.mutation import BaseDjangoFormMutation, DjangoModelDjangoFormMutationOptions


def fields_for_form(form, only_fields, exclude_fields):
    fields = OrderedDict()
    file_fields = []
    for name, field in form.fields.items():
        is_not_in_only = only_fields and name not in only_fields
        is_excluded = (
            name
            in exclude_fields  # or
            # name in already_created_fields
        )

        if is_not_in_only or is_excluded:
            continue

        if isinstance(field, FileField):
            file_fields.append(name)

        fields[name] = convert_form_field(field)
    return (fields, file_fields)


class DjangoUploadModelDjangoFormMutationOptions(DjangoModelDjangoFormMutationOptions):
    file_fields = None  # type: array


class BaseDjangoUploadFormMutation(BaseDjangoFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_form(cls, root, info, **input):
        form_kwargs = {}
        pk = input.pop("id", None)
        if pk:
            instance = cls._meta.model._default_manager.get(pk=pk)
            form_kwargs["instance"] = instance

        files_dict = OrderedDict()
        for v in cls._meta.file_fields:
            files_dict[v] = input.pop(v)
        return cls._meta.form_class(input, files_dict, **form_kwargs)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}

        pk = input.pop("id", None)
        if pk:
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class DjangoUploadModelFormMutation(BaseDjangoUploadFormMutation):
    class Meta:
        abstract = True

    errors = graphene.List(ErrorType)

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        form_class=None,
        model=None,
        return_field_name=None,
        only_fields=(),
        exclude_fields=(),
        **options
    ):

        if not form_class:
            raise Exception(
                "form_class is required for DjangoModelFormMutation")

        if not model:
            model = form_class._meta.model

        if not model:
            raise Exception("model is required for DjangoModelFormMutation")

        form = form_class()
        (input_fields, file_fields) = fields_for_form(
            form, only_fields, exclude_fields)
        if "id" not in exclude_fields:
            input_fields["id"] = graphene.ID()

        registry = get_global_registry()
        model_type = registry.get_type_for_model(model)
        return_field_name = return_field_name
        if not return_field_name:
            model_name = model.__name__
            return_field_name = model_name[:1].lower() + model_name[1:]

        output_fields = OrderedDict()
        output_fields[return_field_name] = graphene.Field(model_type)

        _meta = DjangoUploadModelDjangoFormMutationOptions(cls)
        _meta.form_class = form_class
        _meta.model = model
        _meta.return_field_name = return_field_name
        _meta.fields = yank_fields_from_attrs(output_fields, _as=Field)
        _meta.file_fields = file_fields

        input_fields = yank_fields_from_attrs(input_fields, _as=InputField)

        super(DjangoUploadModelFormMutation, cls).__init_subclass_with_meta__(
            _meta=_meta, input_fields=input_fields, **options
        )

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)
