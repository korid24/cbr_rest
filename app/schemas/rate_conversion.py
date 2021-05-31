from datetime import date
from decimal import Decimal
from typing import Optional, Any, Final

from pydantic import BaseModel, root_validator, validator

from .choices import NumericCodeEnum, LetterCodeEnum


class ConversionRate(BaseModel):
    name: str
    rate: Decimal
    numeric_code: int
    letter_code: str


class DailyRateMultiply(BaseModel):
    conversion_date: date
    rates: list[ConversionRate]


class DailyRateQueryParams(BaseModel):
    class Errors:
        SHOULD_BE_ONLY_ONE_FILTER_QUERY_PARAMETER: Final[str] = (
            'You must specify either a numeric code or an letter one'
        )
        TODAY_IS_THE_LATEST_DAY_OF_CONVERSION: Final[str] = (
            'Today is the last possible conversion day'
        )

    conversion_date: Optional[date]
    numeric_codes: Optional[list[NumericCodeEnum]]
    letter_codes: Optional[list[LetterCodeEnum]]

    @root_validator
    def validate_codes(cls, values: dict[str, Any]) -> dict[str, Any]: # noqa N805
        if values.get('numeric_codes') and values.get('letter_codes'):
            raise ValueError(cls.Errors.SHOULD_BE_ONLY_ONE_FILTER_QUERY_PARAMETER)
        return values

    @validator('conversion_date')
    def validate(cls, conversion_date):  # noqa N805
        if conversion_date and conversion_date > date.today():
            raise ValueError(cls.Errors.TODAY_IS_THE_LATEST_DAY_OF_CONVERSION)
        return conversion_date or date.today()
