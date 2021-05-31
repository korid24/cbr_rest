from datetime import date
from typing import Optional

from fastapi import APIRouter, Query

from app import schemas
from app.services import DailyExchangeRateService

router = APIRouter()


@router.get('/daily-rate/', response_model=schemas.DailyRateMultiply)
async def daily_rate(
        conversion_date: Optional[date] = Query(None), # noqa B008
        numeric_codes: Optional[list[schemas.NumericCodeEnum]] = Query(None), # noqa B008
        letter_codes: Optional[list[schemas.LetterCodeEnum]] = Query(None), # noqa B008
):

    return await DailyExchangeRateService.get_rate(conversion_date, numeric_codes, letter_codes)
