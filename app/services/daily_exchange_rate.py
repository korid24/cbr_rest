from datetime import date
from decimal import Decimal
from typing import Optional, NoReturn, Union
from xml.etree import cElementTree

import httpx
from fastapi import HTTPException
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST

from app import schemas


class DailyExchangeRateService:
    CB_REQUEST_URL: str = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx'
    BASE_HEADERS = {'Content-Type': 'text/xml'}
    BASE_PAYLOAD_TEMPLATE = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">\n <soap12:Body>\n '
        '<GetCursOnDate xmlns="http://web.cbr.ru/">\n <On_date> {conversion_date} </On_date>\n '
        '</GetCursOnDate>\n </soap12:Body>\n</soap12:Envelope>'
    )

    @classmethod
    async def get_rate(
            cls,
            conversion_date: Optional[date],
            numeric_codes: list[int],
            letter_codes: list[str],
    ):
        params = await cls._get_serialized_query_params(
            conversion_date=conversion_date,
            numeric_codes=numeric_codes,
            letter_codes=letter_codes,
        )

        cbr_response = await cls._get_cb_response(params['conversion_date'])
        all_rates = await cls._get_rates_from_xml(cbr_response)
        rates = await cls._get_filtered_rates(all_rates, params)
        return schemas.DailyRateMultiply(conversion_date=params['conversion_date'], rates=rates)

    @staticmethod
    async def _get_serialized_query_params(
            conversion_date: Optional[date],
            numeric_codes: Optional[list[int]],
            letter_codes: Optional[list[str]],
    ) -> Union[schemas.DailyRateQueryParams, NoReturn]:

        try:
            schema = schemas.DailyRateQueryParams(
                conversion_date=conversion_date,
                numeric_codes=numeric_codes,
                letter_codes=letter_codes,
            )
        except ValidationError as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e.errors())
        else:
            return schema.dict()

    @classmethod
    async def _get_cb_response(cls, conversion_date: Optional[date] = None) -> str:
        conversion_date = conversion_date or date.today()
        payload = cls.BASE_PAYLOAD_TEMPLATE.format(conversion_date=conversion_date)

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method='post',
                url=cls.CB_REQUEST_URL,
                data=payload,
                headers=cls.BASE_HEADERS,
            )

        return response.text

    @staticmethod
    async def _get_rates_from_xml(xml: str) -> list[schemas.ConversionRate]:
        tree = cElementTree.fromstring(xml)
        rates: list[schemas.ConversionRate] = []

        for element in tree.findall('.//ValuteCursOnDate'):
            name = element.find('.//Vname').text.strip()
            rate = Decimal(
                Decimal(element.find('.//Vcurs').text) / Decimal(element.find('.//Vnom').text),
            )
            numeric_code = int(element.find('.//Vcode').text)
            letter_code = element.find('.//VchCode').text

            currency_rate = schemas.ConversionRate(
                name=name,
                rate=rate,
                numeric_code=numeric_code,
                letter_code=letter_code,
            )

            rates.append(currency_rate)

        return rates

    @staticmethod
    async def _get_filtered_rates(
            rates: list[schemas.ConversionRate],
            params: dict,
    ) -> list[schemas.ConversionRate]:

        filtered_rates = rates

        if numeric_codes := params.get('numeric_codes'):
            filtered_rates = filter(lambda x: x.numeric_code in numeric_codes, rates)
        elif letter_codes := params.get('letter_codes'):
            filtered_rates = filter(lambda x: x.letter_code in letter_codes, rates)

        return list(filtered_rates)
