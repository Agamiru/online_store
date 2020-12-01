from ..models import *
from ..utils import BhphotovideoTableConverter


html = """
<div class="fader_SupTjLNRI5T781t8hgAfj"><div class="leftPanel_3i7hVcv5SxC5_NRIXMU8Wz"><div><div class="title_1tNQ83iPOOgJ6m5fVkxmSw"><h2 data-selenium="specsItemTitle" class="title1_17KKS47kFEQb7ynVBsRb_5 reset_gKJdXkYBaMDV-W3ignvsP primary_ELb2ysditdCtk24iMBTUs">Alesis V25 Specs</h2></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc firstGroupInItem_k8WqCFToyTsIW3AYbSuui" data-selenium="specsItemGroupName">USB / MIDI Controller</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Keyboard</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>25&nbsp;Full-Size&nbsp;Keys,&nbsp;Synth&nbsp;Action&nbsp;with&nbsp;Velocity</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">MIDI Control Surfaces</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>Wheel&nbsp;(Pitch-Bend)<br><b>1 x </b>Wheel&nbsp;(Modulation)<br><b>8 x </b>Pads&nbsp;(Velocity-Sensitive)<br><b>4 x </b>Rotary Encoders<br><b>4 x </b>Buttons&nbsp;(Assignable)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Performance Functions</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>Octave Shift, Transport Controls</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Connectivity</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>USB Type-B&nbsp;</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">OS Compatibility</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>macOS&nbsp;10<br>Windows</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Packaging Info</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Package Weight</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>5.2 lb</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Box Dimensions (LxWxH)</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>24.5 x 10 x 5"</span></td></tr></tbody></table></div></div></div></div>
"""

audio_int_main_f = [
    "Analog Audio I/O", "Host Connection / USB",
    "Sample Rates", "Power Requirements"
]

midi_keyboard_main_f = [
    "Keyboard", "MIDI Control Surfaces", "I/O",
]


def create_product():
    cat_id, created = Category.objects.get_or_create(
        id=1, name="Keyboards",
    )
    subcat1_id, created = SubCategory1.objects.get_or_create(
        id=1, cat_id=cat_id, name="Midi Keyboards",
        alias=json.dumps(["midi controller"])
    )

    brand, created = Brand.objects.get_or_create(
        id=1, name="Alesis",
    )

    model_name, created = ModelName.objects.get_or_create(
        id=1, brand_id=brand, name="V25"
    )

    short_desc = "25-Key USB MIDI Keyboard Controller"
    price = 65000

    specs_json = BhphotovideoTableConverter(html).to_json()

    prod_instance, created = Product.objects.get_or_create(
        id=1, cat_id=cat_id, subcat_1_id=subcat1_id, brand=brand,
        model_name=model_name, short_desc=short_desc, price=price,
        specs=specs_json
    )

    subcat1_main_f, created = SubCategory1MainFeatures.objects.get_or_create(
        subcat_1_id=subcat1_id, features=json.dumps(midi_keyboard_main_f)
    )

    return prod_instance, subcat1_main_f
