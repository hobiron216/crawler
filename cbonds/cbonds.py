
import json
import sys

import requests
from bs4 import BeautifulSoup

# def dict_clean(items21):
#     result = {}
#     for key, value in items21.items():
#         if value is None:
#             value = ''
#         result[key] = value
#     return result

final_data=[]

cookies = {
    'CBONDSSESSID': '9956a071bd386547cae341b2f3efdc3f',
    '_gcl_au': '1.1.575504896.1662005365',
    '_ga': 'GA1.2.1333845716.1662005375',
    '_gid': 'GA1.2.948795534.1662005375',
    'CBONDS_TOKEN1': 'c1e2574e325e87ad8eaf6419d5dd36f142987a946f9f485493cfabc70dde0848',
    'CBONDS_TOKEN2': 'dcfa27320a8b55da16fe26cc1c619639a66730e59a82fb4ec59007fdad773b89499370',
}

headers = {
    'authority': 'cbonds.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'CBONDSSESSID=9956a071bd386547cae341b2f3efdc3f; _gcl_au=1.1.575504896.1662005365; _ga=GA1.2.1333845716.1662005375; _gid=GA1.2.948795534.1662005375; CBONDS_TOKEN1=c1e2574e325e87ad8eaf6419d5dd36f142987a946f9f485493cfabc70dde0848; CBONDS_TOKEN2=dcfa27320a8b55da16fe26cc1c619639a66730e59a82fb4ec59007fdad773b89499370',
    'origin': 'https://cbonds.com',
    'referer': 'https://cbonds.com/bonds/?emitent_subregion_id=0-8&emitent_country_id=0-18y68&emitent_branch_id=0-27wu80.1-zik0zk.2-4zsow&selected_fields=0-hra0hw.1-4fzaww.2-1em8.3-9zy1c.4-1z3m1hg.5-hrx7nk.6-4kyxa8.7-13ztoi.8-9zyfk.9-1z3lyqs.10-hrwidc.11-74.12-13zs3k.13-9zy1c.14-1z3m1hg.15-2.16-4fz4lc.17-13zs5c.18-2gi8.19-1z3m1hg.20-sg&order=document&dir=asc&page=21',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

page=0
offset=-30
while True:
    page=page+1
    offset = offset + 30
    json_data = {
        'filters': [
            {
                'field': 'show_global',
                'operator': 'eq',
                'value': 1,
            },
            {
                'field': 'emitent_subregion_id',
                'operator': 'in',
                'value': [
                    '3',
                ],
            },
            {
                'field': 'emitent_country_id',
                'operator': 'in',
                'value': [
                    '21',
                ],
            },
            {
                'field': 'emitent_branch_id',
                'operator': 'in',
                'value': [
                    '14',
                    '87',
                    '63',
                    '12',
                    '27',
                    '55',
                    '71',
                    '7',
                    '65',
                    '16',
                    '113',
                    '99',
                    '119',
                    '69',
                    '35',
                    '59',
                    '49',
                    '95',
                    '4',
                    '107',
                    '41',
                    '6',
                    '31',
                    '45',
                    '53',
                    '25',
                    '115',
                    '73',
                    '37',
                    '39',
                    '121',
                    '89',
                    '29',
                    '81',
                    '79',
                    '43',
                    '20',
                ],
            },
        ],
        'sorting': [
            {
                'field': 'document',
                'order': 'asc',
            },
        ],
        'quantity': {
            'offset': offset,
            'limit': 30,
            'page': page,
        },
        'lang': 'eng',
        'expand_rel_fields': [
            'emitent_country',
            'status_id',
            'emitent_branch_id',
            'emitent_type',
            'coupon_type_id',
            'kind_id',
            'subkind_id',
        ],
    }
    while True:
        try:
            response = requests.post('https://cbonds.com/bonds/search/', cookies=cookies, headers=headers, json=json_data, timeout=20)
            break
        except requests.exceptions.RequestException as e:
            print("connetion timeout")
            continue

    html =response.json()
    # datas = json.loads(html)
    if html["response"]["items"]:

        for data in html["response"]["items"]:
            issue = data["document"]
            country = data["emitent_country_name"]
            issuer = data["emitent_name"]
            spv = data["formal_emitent_name"]
            sector = data["emitent_type_name"]
            industry = data["emitent_branch_name"]
            currency = data["currency_name"]
            status = data["status_id.lbl"]
            coupon = data["cupon"]
            current_coupon_rate = data["curr_coupon_rate"]
            coupon_frequency = data["cupon_period"]
            day_count_fraction = data["emission_cupon_basis_title"]
            rate_type = "Floating rate"
            reference_rate = data["reference_rate_name"]
            margin = data["margin"]
            interest_payment_type = data["coupon_type_name"]
            announced_volume = data["announced_volume_new"]
            placement_amount = data["announced_volume"]
            outstanding_amount = data["placed_volume"]
            outstanding_face_value_amount = data["remaining_outstand_amount"]
            usd_equivalent = data["usd_volume"]
            nominal_minimum_settlement_amount = data["nominal_price"]
            integral_multiple = data["integral_multiple"]
            outstanding_face_value = data["outstanding_nominal_price"]
            type = data["kind_name"]
            special_type = data["subkind_name"]
            initial_issue_price = data["price_of_primary_placing"]
            yield_at_pricing = data["income_of_primary_placing"]
            listing = data["trading_grounds_full"]
            placement_participants = data["agents"]
            convertible = data["convertable"]
            conversion_terms = data["convert_cond"]
            terms_of_early_redemption = data["offert"]
            additional_information = data["more"]
            foreign_currency_issuer_rating_m = data["emitent_maxratings_msf_foreign_currency"]
            foreign_currency_issue_rating_m = data["maxratings_msf_foreign_currency"]
            local_currency_issuer_rating_m = data["emitent_maxratings_msf_local_currency"]
            local_currency_issue_rating_m = data["maxratings_msf_local_currency"]
            issuer_rating = data["rating_emitent_national_56707"]
            issue_rating = data["rating_emission_56707"]
            maturity = data["maturity_date"]
            put_option = data["offert_date_put"]
            call_option = data["offert_date_call"]
            next_reopening_date = data["next_replacing_date"]
            start_of_placement = data["date_of_start_placing"]
            end_of_placement = data["date_of_end_placing"]
            interest_accrual_date = data["settlement_date"]
            start_of_trading = data["date_of_start_circulation"]
            registration = data["registration_date"]
            program_registration = data["gov_program_registration_date"]
            isin = data["isin_code"]
            isin_144a = data["isin_code_144a"]
            state_registration_number = data["state_reg_number"]
            cusip = data["cusip_regs"]
            cusip_144a = data["cusip_144a"]
            cbonds_id = data["id"]
            wkn = data["emission_wkn_code"]
            wkn_144a = data["emission_wkn_code_144a"]
            state_registration_number_of_program = data["gov_program_state_reg_number"]
            issuer_cbonds_id = data["emitent_id"]
            indicative_price = data["tradings_indicative_price"]
            indicative_yield = data["tradings_yield_effect"]
            duration = data["tradings_duration"]
            if duration == "***":
                duration = 0
            trade_date = data["tradings_maxdate"]
            stock_exchange = data["trading_ground_name"]
            cb_bond_link = data["cb_bond_link"]

            while True:
                try:
                    response = requests.get(cb_bond_link, cookies=cookies, headers=headers, timeout=20)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue

            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            amount_detail = soup.find("div", id="cb_bond_page_param_volume").find("div", class_="value")
            amount_detail = str(amount_detail).replace('''<div class="value">''', "").replace('''</div>''', "").strip()

            result = {
                "issue": issue,
                "country": country,
                "issuer": issuer,
                "spv": spv,
                "sector": sector,
                "industry": industry,
                "currency": currency,
                "status" : status,
                "coupon": coupon,
                "current_coupon_rate": current_coupon_rate,
                "coupon_frequency": coupon_frequency,
                "day_count_fraction": day_count_fraction,
                "rate_type": rate_type,
                "reference_rate": reference_rate,
                "margin": margin,
                "interest_payment_type" : interest_payment_type,
                "announced_volume": announced_volume,
                "placement_amount": placement_amount,
                "outstanding_amount": outstanding_amount,
                "outstanding_face_value_amount": outstanding_face_value_amount,
                "usd_equivalent": usd_equivalent,
                "nominal_minimum_settlement_amount": nominal_minimum_settlement_amount,
                "integral_multiple": integral_multiple,
                "outstanding_face_value": outstanding_face_value,
                "type": type,
                "special_type": special_type,
                "initial_issue_price": initial_issue_price,
                "yield_at_pricing": yield_at_pricing,
                "listing": listing,
                "placement_participants": placement_participants,
                "convertible": convertible,
                "conversion_terms": conversion_terms,
                "terms_of_early_redemption": terms_of_early_redemption,
                "additional_information": additional_information,
                "foreign_currency_issuer_rating_m": foreign_currency_issuer_rating_m,
                "foreign_currency_issue_rating_m": foreign_currency_issue_rating_m,
                "local_currency_issuer_rating_m": local_currency_issuer_rating_m,
                "local_currency_issue_rating_m": local_currency_issue_rating_m,
                "issuer_rating": issuer_rating,
                "issue_rating": issue_rating,
                "maturity": maturity,
                "put_option": put_option,
                "call_option": call_option,
                "next_reopening_date": next_reopening_date,
                "start_of_placement": start_of_placement,
                "end_of_placement": end_of_placement,
                "interest_accrual_date": interest_accrual_date,
                "start_of_trading": start_of_trading,
                "registration": registration,
                "program_registration": program_registration,
                "isin": isin,
                "isin_144a": isin_144a,
                "state_registration_number": state_registration_number,
                "cusip": cusip,
                "cusip_144a": cusip_144a,
                "cbonds_id": cbonds_id,
                "wkn": wkn,
                "wkn_144a": wkn_144a,
                "state_registration_number_of_program": state_registration_number_of_program,
                "issuer_cbonds_id": issuer_cbonds_id,
                "indicative_price": indicative_price,
                "indicative_yield": indicative_yield,
                "duration": duration,
                "trade_date": trade_date,
                "stock_exchange": stock_exchange,
                "amount_detail" : amount_detail

            }
            # result = dict_clean(result)
            final_data.append(result)
            print("page : " + str(page))
        # sys.exit()
    else:
        break

with open("/dataph/one_time_crawling/home/cbonds1-37.json",'w',encoding='utf8') as outfile:
    json.dump(final_data, outfile,  ensure_ascii=False)