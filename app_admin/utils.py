from bs4 import BeautifulSoup as bs
import re
from typing import Tuple, List

import json

html_data = """
<div class="container_2LmZG1Br6z1iEjEmzF-rDw"><div class="fader_SupTjLNRI5T781t8hgAfj"><div class="leftPanel_3i7hVcv5SxC5_NRIXMU8Wz"><div><div class="title_1tNQ83iPOOgJ6m5fVkxmSw"><h2 data-selenium="specsItemTitle" class="title1_17KKS47kFEQb7ynVBsRb_5 reset_gKJdXkYBaMDV-W3ignvsP primary_ELb2ysditdCtk24iMBTUs">Focusrite 18i8 Specs</h2></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc firstGroupInItem_k8WqCFToyTsIW3AYbSuui" data-selenium="specsItemGroupName">Interface</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Channels of I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span><b>Analog:</b><br>8 Inputs / 6 Outputs at 192 kHz<br><b>Digital:</b><br>10 Inputs / 2 Outputs</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Max Sample Rate/Resolution</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>192 kHz / 24-Bit</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Display and Indicators</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>4 x </b>LEDs (Input Level)<br><b>2 x </b>LEDs (+48V)<br><b>2 x </b>LEDs (Input Selection)<br><b>4 x </b>LEDs (Pad)<br><b>1 x </b>LED (Host Connection)<br><b>1 x </b>LED (MIDI)<br><b>1 x </b>LED (Output Selection)</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Connectivity</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Host Connection</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>USB Type-C (USB 2.0)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Analog I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>2 x </b>Combo XLR-1/4" TRS Balanced/Unbalanced Mic/Line/Hi-Z Input<br><b>2 x </b>Combo XLR-1/4" TRS Balanced Mic/Line Input<br><b>4 x </b>1/4" TRS Balanced Line Input<br><b>4 x </b>1/4" TRS Balanced Line Output<br><b>2 x </b>1/4" TRS Unbalanced Headphone Output</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Phantom Power</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>+48 V, Selectable On/Off (on 4 Channels)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Digital I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>RCA Coaxial S/PDIF Input<br><b>1 x </b>RCA Coaxial S/PDIF Output<br><b>1 x </b>TOSLINK ADAT Input</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">MIDI I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>MIDI 5-Pin In<br><b>1 x </b>MIDI 5-Pin Out</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Memory Card Slot</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><i>None</i></span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Performance</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Frequency Response</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>20 Hz to 20 kHz ±0.1 dB </span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Gain/Trim Range</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic/Line/Hi-Z Inputs:</b><br>56 dB </span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Max Input Level</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic Inputs:</b><br>+9 dBu (Min Gain) <br><b>Hi-Z Inputs:</b><br>+12.5 dBu (Min Gain) <br><b>Line Inputs:</b><br>+22 dBu (Min Gain) </span><span class="infoWrapper_qiCJTr4EX_zRBTRw4Jn_T" data-selenium="specsItemInfoIcon"><span tabindex="0"><svg class="bhIcon info_3z6pSJuDTRLW1xk4wHKMCb" height="14" width="14"><use href="#InfoLightIcon"></use></svg></span></span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Max Output Level</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Line Outputs:</b><br>+15.5 dBu at 0 dBFS (Balanced) <br><b>Headphone Outputs:</b><br>+7 dBu </span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Dynamic Range</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic Inputs:</b><br>111 dBA <br><b>Hi-Z Inputs:</b><br>110 dBA <br><b>Line Inputs:</b><br>110.5 dBA <br><b>Line Outputs:</b><br>108 dBA <br><b>Headphone Outputs:</b><br>104 dBA </span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Impedance</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic Inputs:</b><br>3 Kilohms <br><b>Hi-Z Inputs:</b><br>1.5 Megohms <br><b>Line Inputs:</b><br>60 Kilohms <br><b>Line Outputs:</b><br>430 Ohms <br><b>Headphone Outputs:</b><br>&lt;1 Ohm </span><span class="infoWrapper_qiCJTr4EX_zRBTRw4Jn_T" data-selenium="specsItemInfoIcon"><span tabindex="0"><svg class="bhIcon info_3z6pSJuDTRLW1xk4wHKMCb" height="14" width="14"><use href="#InfoLightIcon"></use></svg></span></span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">THD+N</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic Inputs:</b><br> &lt;0.0012% <br><b>Hi-Z Inputs:</b><br> &lt;0.03% <br><b>Line Inputs:</b><br> &lt;0.002% <br><b>Line Outputs:</b><br> &lt;0.002% <br><b>Headphone Outputs:</b><br> &lt;0.002% </span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">EIN</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>Mic Inputs:</b><br>-128 dB A-Weighted </span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Digital Audio</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Sample Rates</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>Up to 192 kHz (AD/DA Conversion)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Bit Depth</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>Up to 24-Bit (AD/DA Conversion)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Sync Sources</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>ADAT, Internal, S/PDIF</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Compatibility</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">OS Compatibility</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>macOS<br>Windows</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Required Hardware</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>Available USB 2.0 Port<br>USB Cable (Included)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Internet Connection</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>Required for Software/Driver Download</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Power</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Power Requirements</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>AC/DC Power Adapter (Included)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">AC/DC Power Adapter</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>12 VDC at 1 A, Center-Positive (Included)</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Physical</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Anti-Theft Features</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>Kensington Security Slot</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Dimensions</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>9.49 x 6.28 x 2.4" / 24.1 x 15.95 x 6.1&nbsp;cm</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Weight</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>2.9&nbsp;lb / 1.3&nbsp;kg (Without Accessories)<br>3.5&nbsp;lb / 1.6&nbsp;kg (With Accessories)</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Packaging Info</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Package Weight</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>4.7 lb</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Box Dimensions (LxWxH)</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>12.6 x 10.5 x 3.4"</span></td></tr></tbody></table></div></div></div></div></div>
"""

# Regex Patterns
tag_popper = re.compile(r"^<[^>]+>")    # Pops rows that begin with a tag
span_attr_popper = re.compile(r"^<span\s\w+")    # Pops span tags with attributes
# bold_before_break = re.compile(r"(<b>[^<]+</b>)([^<]*<*b*r*/*>*)")
bold_before_break = re.compile(r"<b>[^<]+</b>[^<]*<*b*r*/*>*")    # Gets all lines of values


def table_to_json_converter(html_table_data):

    table = bs(html_data, features="html.parser").find_all("tr")

    # Contains all table data for that row, first item is the main spec, rest is values.
    table_data = [[cell.text for cell in row.find_all("td")] for row in table]
    print(f"len_table_data: {table_data}\n\n")

    separated_values, no_of_values = populate_lists(html_table_data)
    values_list = json_values_preparer(no_of_values, separated_values)

    assert len(values_list) == len(no_of_values), "Things aren't adding up"
    assert len(values_list) == len(table_data), "Things aren't adding up"

    final_dict = spec_values_dict(table_data, values_list)

    json_data = json.dumps(final_dict, indent=2, ensure_ascii=False)

    return json_data


def spec_values_dict(table_data, values_list) -> dict:
    spec_values_dict = {}
    count = 0
    for value in table_data:
        dict_ = {value[0]: values_list[count]}
        spec_values_dict.update(dict_)
        count += 1

    return spec_values_dict


def populate_lists(html_table_data) -> Tuple[List, List]:

    # Populate separated_values and no_of_values
    separated_values = []    # A list of all separated values
    no_of_values = []    # A list of dictionary pairs {no_items: pairs of values}

    # Find all rows with span tags
    for row in bs(html_table_data, "lxml").find_all("span"):
        # Pop rows with span tags that have attributes
        if span_attr_popper.match(str(row)):
            continue
        print(row)
        line_breaks = len(row.find_all('br')) + 1
        no_of_pairs = len(bold_before_break.findall(str(row)))
        print(f"bold_before_break: {bold_before_break.findall(str(row))}")
        no_of_values.append({line_breaks: no_of_pairs})
        for child in row.descendants:
            # print(child)
            if tag_popper.match(str(child)):
                continue
            separated_values.append(child)

    return separated_values, no_of_values


def json_values_preparer(no_of_values: list, separated_values: list):
    new_list = []       # List with all values in dict or list format
    main_count = 0
    for dict_ in no_of_values:
        for k, v in dict_.items():
            all_values = []
            key_values = []
            dict_2 = {}
            list_2 = []
            # Populate all_values list
            try:
                a = k // v
            except ZeroDivisionError:
                for value_main in separated_values[main_count:main_count + k]:
                    print(separated_values[main_count:main_count + k])
                    all_values.append(value_main)
                for val in all_values:
                    list_2.append(val)
                new_list.append(list_2)
                main_count += k
            else:
                if a == 2:
                    order_count = 0
                    for value_main in separated_values[main_count:main_count + k]:
                        print(separated_values[main_count:main_count + k])
                        all_values.append(value_main)
                    for value_sub in all_values[::2]:
                        key_values.append(value_sub)
                    for item in key_values:
                        if item in all_values:      # todo: might be redundant
                            order_count += 1
                            dict_2.update({item: all_values[order_count]})
                        order_count += 1
                    new_list.append(dict_2)
                    main_count += k
                else:
                    outer_count_ = 0
                    for value_main in separated_values[main_count:main_count + (k + v)]:
                        print(separated_values[main_count:main_count + (k + v)])
                        all_values.append(value_main)
                    for value_sub in all_values[::2]:
                        key_values.append(value_sub)
                    for item in key_values:
                        if item in all_values:      # todo: might be redundant
                            outer_count_ += 1
                            list_2.append(item + "" + all_values[outer_count_])
                        outer_count_ += 1
                    new_list.append(list_2)
                    main_count += k + v

            print(f"main_count: {main_count}")
    return new_list


class BhphotovideoTableConverter:

    tag_popper = re.compile(r"^<[^>]+>")    # Pops rows that begin with a tag
    span_attr_popper = re.compile(r"^<span\s\w+")    # Pops span tags with attributes
    bold_before_break = re.compile(r"<b>[^<]+</b>[^<]*<*b*r*/*>*")    # Gets all lines of values

    def __init__(self, html_table_data):
        self.html_table_data = html_table_data

    def convert(self):

        table = bs(self.html_table_data, features="html.parser").find_all("tr")

        # Contains all table data for that row, first item is the main spec, rest is values.
        table_data = [[cell.text for cell in row.find_all("td")] for row in table]

        separated_values, no_of_values = self._populate_lists()
        values_list = self._json_values_preparer(no_of_values, separated_values)

        assert len(values_list) == len(no_of_values), "Things aren't adding up"
        assert len(values_list) == len(table_data), "Things aren't adding up"

        final_dict = self._spec_values_dict(table_data, values_list)

        json_data = json.dumps(final_dict, indent=2, ensure_ascii=False)

        return json_data

    def _populate_lists(self) -> Tuple[List, List]:

        # Populate separated_values and no_of_values
        separated_values = []    # A list of all separated values
        no_of_values = []    # A list of dictionary pairs {no_items: pairs of values}

        # Find all rows with span tags
        for row in bs(self.html_table_data, "lxml").find_all("span"):
            # Pop rows with span tags that have attributes
            if __class__.span_attr_popper.match(str(row)):
                continue
            line_breaks = len(row.find_all('br')) + 1
            no_of_pairs = len(__class__.bold_before_break.findall(str(row)))
            no_of_values.append({line_breaks: no_of_pairs})
            for child in row.descendants:
                # print(child)
                if __class__.tag_popper.match(str(child)):
                    continue
                separated_values.append(child)

        return separated_values, no_of_values

    @staticmethod
    def _json_values_preparer(no_of_values: list, separated_values: list):

        new_list = []       # List with all values in dict or list format
        main_count = 0
        for dict_ in no_of_values:
            for k, v in dict_.items():
                all_values = []
                key_values = []
                dict_2 = {}
                list_2 = []
                # Populate all_values list
                try:
                    a = k // v
                except ZeroDivisionError:
                    for value_main in separated_values[main_count:main_count + k]:
                        all_values.append(value_main)
                    for val in all_values:
                        list_2.append(val)
                    new_list.append(list_2)
                    main_count += k
                else:
                    if a == 2:
                        order_count = 0
                        for value_main in separated_values[main_count:main_count + k]:
                            all_values.append(value_main)
                        for value_sub in all_values[::2]:
                            key_values.append(value_sub)
                        for item in key_values:
                            if item in all_values:      # todo: might be redundant
                                order_count += 1
                                dict_2.update({item: all_values[order_count]})
                            order_count += 1
                        new_list.append(dict_2)
                        main_count += k
                    else:
                        outer_count_ = 0
                        for value_main in separated_values[main_count:main_count + (k + v)]:
                            all_values.append(value_main)
                        for value_sub in all_values[::2]:
                            key_values.append(value_sub)
                        for item in key_values:
                            if item in all_values:      # todo: might be redundant
                                outer_count_ += 1
                                list_2.append(item + "" + all_values[outer_count_])
                            outer_count_ += 1
                        new_list.append(list_2)
                        main_count += k + v

        return new_list

    def _spec_values_dict(self, table_data, values_list) -> dict:
        spec_values_dict = {}
        count = 0
        for value in table_data:
            dict_ = {value[0]: values_list[count]}
            spec_values_dict.update(dict_)
            count += 1

        return spec_values_dict


# print(table_to_json_converter(html_data))
tabul = BhphotovideoTableConverter(html_data)
print(f"tabul: {tabul.convert()}")


