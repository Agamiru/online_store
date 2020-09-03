from .models import *
from typing import List, Union, Dict, Tuple
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from app_admin.utils import BhphotovideoTableConverter


class FieldNotFoundError(Exception):
    def __init__(self, fields: List):
        self.fields = fields

    def __str__(self):
        return f"Fields '{self.fields}' not found"


class CreateProduct:

    def __init__(self):
        self.product_model = Product
        self.category_model = Category
        self.sub_category_model_1 = SubCategory1
        self.sub_category_model_2 = SubCategory2
        self.brand_model = Brand
        self.model_name_model = ModelName
        self.main_features_model = MainFeatures
        self.image_model = Image
        self.image_fp = "C:\\Users\\hp\\Desktop\\"
        self.accessories_model = Accessories
        self.bought_together_model = BoughtTogether
        self.product_kwargs = {}
        self.newly_saved = []  # {model: {kwargs used to save}}

    def add_product(
            self, model_name, brand_name, price, item_desc,
            accessories, bought_together, image_name, specs
    ):

        pass

    def get_or_set_category(self):
        model = self.category_model
        name_kwargs, table_name = self.get_kwargs(model)

        return name_kwargs, table_name

    def get_or_set_subcategory_1(self):
        model = self.sub_category_model_1

        name_kwargs, table_name = self.get_kwargs(model)

        return name_kwargs, table_name

    def get_or_set_subcategory_2(self):
        model = self.sub_category_model_2

        name_kwargs, table_name = self.get_kwargs(model)

        return name_kwargs, table_name

    def get_or_set_brand(self):
        model = self.brand_model

        name_kwargs, table_name = self.get_kwargs(model)
        return name_kwargs, table_name

    def get_or_set_model_name(self):
        model = self.model_name_model

        name_kwargs, table_name = self.get_kwargs_unique(model)
        return name_kwargs, table_name

    def get_or_set_image(self):
        model = self.image_model

        file_path_kwargs, table_name = self.get_kwargs_unique(model, "file_path")
        return file_path_kwargs, table_name

    def get_or_set_Accessories(self):
        model = self.accessories_model

        accessories_kwargs = self.get_kwargs_json_array(model, "accessories")
        return accessories_kwargs

    def get_or_set_short_desc(self):
        model = self.accessories_model

        accessories_kwargs = self.get_kwargs_json_array(model, "accessories")
        return accessories_kwargs

    def get_or_set_specs(self):
        pass

    def get_kwargs(self, model, field_name="name"):
        table_name, table_list = self.get_tablename_and_list(model, field_name)
        print(self.prompt_message(table_name, table_list))

        returned_value = []
        exit_loop = False
        while not exit_loop:
            value = input(f"Please type in a product {table_name} name\n").title()
            split_vals = value.split(" ")
            joined_val = "".join(split_vals).capitalize()
            inner_count = 0

            if value in table_list or joined_val in table_list or value.split() in table_list:
                while not inner_count:
                    proceed_or_not = input(
                        f"""'{value}' already exists!
                                Do you want to save a different value? [Y/N]
                                Type [N/n] to use this value
                            """).lower()
                    if proceed_or_not == "y":
                        inner_count += 1
                        break
                    elif proceed_or_not == "n":
                        print("The existing object will be used while saving.")
                        break
                    elif proceed_or_not == "exit":
                        self.system_exit()
                    else:
                        print("Please only Y/N replies")
                        continue

            if inner_count == 1:
                continue
            if value == "exit":
                self.system_exit()

            returned_value.append(value)
            exit_loop = True

        kwargs = {field_name: returned_value[0]}

        return kwargs, table_name

    def update_product_kwargs(self, field_to_save, obj):
        self.product_kwargs.update({field_to_save: obj})

    def wizard(self):
        print("""
        This wizard will guide you through saving a product object 
        """)

        # cat_id
        cat_kwargs, table_name = self.get_or_set_category()
        cat_obj = self.obj_for_product_kwargs(
            self.category_model, table_name, **cat_kwargs)
        self.update_product_kwargs("cat_id", cat_obj)

        # subcat_1_id
        answers = ["y", "n"]
        subcat_1 = None
        while not subcat_1:
            print("Type 'exit' to quit wizard")
            subcat_1 = input("Does this Product have a Subcategory1?  Y/N\n").lower()
            if subcat_1 in answers:
                break
            if subcat_1 == "exit":
                self.system_exit()
            subcat_1 = None
            print("Please only Y/N replies")

        if subcat_1 == "y":
            subcat_kwargs, table_name = self.get_or_set_subcategory_1()
            subcat_kwargs.update({"cat_id": cat_obj})
            subcat_obj = self.obj_for_product_kwargs(
                self.sub_category_model_1, table_name, **subcat_kwargs
            )
            self.update_product_kwargs("subcat_1_id", subcat_obj)

            # subcat_2_id
            subcat_2 = None
            while not subcat_2:
                print("Type 'exit' to quit wizard")
                subcat_2 = input("Does this Product have a Subcategory2?  Y/N\n").lower()
                if subcat_2 in answers:
                    break
                if subcat_1 == "exit":
                    self.system_exit()
                subcat_2 = None
                print("Please only Y/N replies")

            if subcat_2 == "y":
                subcat_kwargs, table_name = self.get_or_set_subcategory_2()
                subcat_kwargs.update({"subcat_id": subcat_obj})
                subcat_2_obj = self.obj_for_product_kwargs(
                    self.sub_category_model_2, table_name, **subcat_kwargs
                )
                self.update_product_kwargs("subcat_2_id", subcat_2_obj)

        # brand
        brand_kwargs, table_name = self.get_or_set_brand()
        brand_obj = self.obj_for_product_kwargs(
            self.brand_model, table_name, **brand_kwargs)
        self.update_product_kwargs("brand", brand_obj)

        # model_name
        model_name_kwargs, table_name = self.get_or_set_model_name()
        model_name_kwargs.update({"brand_id": brand_obj})
        model_name_obj = self.obj_for_product_kwargs(
            self.model_name_model, table_name, **model_name_kwargs
        )
        self.update_product_kwargs("model_name", model_name_obj)

        # image
        image_name_kwargs, table_name = self.get_or_set_image()
        file_name = image_name_kwargs["file_path"]
        image_name_kwargs["file_path"] = self.image_fp + file_name
        image_obj = self.obj_for_product_kwargs(
            self.image_model, table_name, **image_name_kwargs
        )
        self.update_product_kwargs("image", image_obj)

        # Todo: {accessories: accessories_obj}
        # Todo: {bought_together: bought_together_obj}

        # short_desc
        short_desc = input("Please insert a short description\n").title()
        if short_desc == "exit":
            self.system_exit()
        self.update_product_kwargs("short_desc", short_desc)

        # price
        price = input("Please insert a price\n")
        if short_desc == "exit":
            self.system_exit()
        self.update_product_kwargs("price", price)

        # specs
        exit_loop = False
        while not exit_loop:
            try:
                specs_html = input("Please insert specs\n")
                if specs_html == "exit":
                    self.system_exit()
                table = BhphotovideoTableConverter(specs_html)
                json_specs = table.convert()
                self.update_product_kwargs("specs", json_specs)
            except Exception:
                print("Please try check your html data")
                continue
            try:
                # package_dimensions
                package_dims = table.final_dict["Box Dimensions (LxWxH)"]
                self.update_product_kwargs("package_dimensions", package_dims[0])
            except KeyError:
                print("Please try check your html data")
                continue
            try:
                # weight
                weight = table.final_dict["Package Weight"]
                self.update_product_kwargs("weight", weight[0])
            except KeyError:
                print("Please try check your html data")
                continue

            exit_loop = True

        prod = self.product_model(**self.product_kwargs)
        prod.save()

        print(f"""
        Congratulations you've successfully saved the product {prod}
        """)






    def get_possible_accessories(self):
        list_ = list()
        list_.append([obj for obj in self.category_model.objects.all()])
        list_.append([obj for obj in self.sub_category_model_1.objects.all()])
        list_.append([obj for obj in self.sub_category_model_2.objects.all()])

        return list_

    # Model Agnostic
    def check_fields(self, model, **fields) -> Dict:
        checked_field, wrong_fields = [], []
        for name in fields.keys():
            name.lower()
            found = 0
            for field in model._meta.fields:
                if field == name:
                    checked_field.append(field)
                    found += 1
                    break
            if found:
                continue
            wrong_fields.append(name)

        if wrong_fields:
            raise FieldNotFoundError(wrong_fields)

        return fields

    # Model Agnostic
    def get_tablename_and_list(self, model, field_name="name"):
        instance = model()
        all_cat = model.objects.all()     # model
        table_list = [getattr(obj, field_name) for obj in all_cat]
        table_name = instance.__class__.__name__.lower()

        return table_name, table_list

    # Model Agnostic
    def prompt_message(self, table_name: str, table_list: List):
        prompt_message = f"""
        Please select a product {table_name} from: {table_list}
        Else, type in a new {table_name}.\n
        """
        return prompt_message if table_list else f"Create a new product {table_name} name\n"

    # Model Agnostic
    def obj_for_product_kwargs(self, model, table_name, **kwargs):
        returned_obj = []       # Obj to be saved with
        try:
            new_obj = model(**kwargs)
            new_obj.save()
            print(f"""
            New {table_name} object <{kwargs}> successfully saved!
            """)
            returned_obj.append(new_obj)
            self.newly_saved.append({model: kwargs})
        except IntegrityError:
            existing_obj = model.objects.get(**kwargs)
            print(f"""
            Existing {table_name} object <{kwargs}> successfully retrieved!
            """)
            returned_obj.append(existing_obj)

        return returned_obj[0]

    def get_kwargs_unique(self, model, field_name="name"):
        table_name, table_list = self.get_tablename_and_list(model, field_name)
        print(self.prompt_message(table_name, table_list))

        returned_value = []
        exit_loop = False
        while not exit_loop:
            value = input(f"Please type in a product {table_name} {field_name}\n").title()
            split_vals = value.split(" ")
            joined_val = "".join(split_vals).capitalize()

            if value in table_list or joined_val in table_list or value.split() in table_list:
                print("Oops! This value must be unique, please type something else")
                continue

            if value == "exit":
                self.system_exit()

            returned_value.append(value)
            exit_loop = True

        kwargs = {field_name: returned_value[0]}

        return kwargs, table_name

    # def get_kwargs_json_array(self, model, field_name="name"):
    #     # table_name, table_list = self.get_tablename_and_list(model, field_name)
    #     # print(self.prompt_message(table_name, table_list))
    #     all_accessories = [obj for obj in model.objects.all()]
    #     if all_accessories:
    #         self.print_long_list(10, all_accessories)
    #         found = input("Find your item here? [Y/N]").lower()
    #
    #         if found == "y":
    #             item = input("Please copy the item in 'quotes' and paste here -> ")

    def print_long_list(self, no_of_items_per_line, iterable):
        count = 0
        for item in iterable:
            count += 1
            if count % no_of_items_per_line == 0:
                print(item)
                continue
            print(item, end=", ")

    def system_exit(self):
        self.clean_up_db()
        raise SystemExit("You opted out of the wizard")

    def clean_up_db(self):
        if self.newly_saved:
            count = 0
            for dict_ in self.newly_saved:        # {model: {kwargs used to save}}
                for model, kwargs in dict_.items():
                    try:
                        to_delete = model.objects.get(**kwargs)
                        to_delete.delete()
                        count += 1
                    except ObjectDoesNotExist:
                        pass

            print(f"{count} newly created objects successfully deleted")

