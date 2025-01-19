from pydantic import BaseModel, Field
from typing import Optional, Literal

class OrderRequest(BaseModel):
    symbol: str = Field(..., description="Instrument symbol (e.g., 'XBTUSD').")
    side: Literal["Buy", "Sell"] = Field(
        "Buy", description="Order side. Valid options: Buy, Sell. Defaults to 'Buy' unless orderQty is negative."
    )
    orderQty: Optional[float] = Field(
        None, description="Order quantity in units of the instrument."
    )
    price: Optional[float] = Field(
        None, description="Optional limit price for 'Limit', 'StopLimit', and 'LimitIfTouched' orders."
    )
    displayQty: Optional[float] = Field(
        None, description="Optional quantity to display in the book. Use 0 for a fully hidden order."
    )
    stopPx: Optional[float] = Field(
        None,
        description=(
            "Optional trigger price for 'Stop', 'StopLimit', 'MarketIfTouched', and 'LimitIfTouched' orders. "
            "Use a price below the current price for stop-sell orders and buy-if-touched orders."
        ),
    )
    clOrdID: Optional[str] = Field(
        None, description="Optional Client Order ID. This clOrdID will come back on the order and any related executions."
    )
    clOrdLinkID: Optional[str] = Field(
        None, description="Optional Client Order Link ID for contingent orders."
    )
    pegOffsetValue: Optional[float] = Field(
        None,
        description=(
            "Optional trailing offset from the current price for 'Stop', 'StopLimit', 'MarketIfTouched', and "
            "'LimitIfTouched' orders. Use a negative offset for stop-sell orders and buy-if-touched orders."
        ),
    )
    pegPriceType: Optional[Literal["MarketPeg", "PrimaryPeg", "TrailingStopPeg"]] = Field(
        None, description="Optional peg price type. Valid options: MarketPeg, PrimaryPeg, TrailingStopPeg."
    )
    ordType: Optional[
        Literal[
            "Market",
            "Limit",
            "Stop",
            "StopLimit",
            "MarketIfTouched",
            "LimitIfTouched",
            "Pegged",
        ]
    ] = Field(
        "Limit",
        description=(
            "Order type. Valid options: Market, Limit, Stop, StopLimit, MarketIfTouched, LimitIfTouched, Pegged. "
            "Defaults to 'Limit' when price is specified. Defaults to 'Stop' when stopPx is specified. "
            "Defaults to 'StopLimit' when price and stopPx are specified."
        ),
    )
    timeInForce: Optional[
        Literal["Day", "GoodTillCancel", "ImmediateOrCancel", "FillOrKill"]
    ] = Field(
        "GoodTillCancel",
        description=(
            "Time in force. Valid options: Day, GoodTillCancel, ImmediateOrCancel, FillOrKill. "
            "Defaults to 'GoodTillCancel' for 'Limit', 'StopLimit', and 'LimitIfTouched' orders."
        ),
    )
    execInst: Optional[
        Literal[
            "ParticipateDoNotInitiate",
            "AllOrNone",
            "MarkPrice",
            "IndexPrice",
            "LastPrice",
            "Close",
            "ReduceOnly",
            "Fixed",
            "LastWithinMark",
        ]
    ] = Field(
        None,
        description=(
            "Optional execution instructions. Valid options: ParticipateDoNotInitiate, AllOrNone, MarkPrice, IndexPrice, "
            "LastPrice, Close, ReduceOnly, Fixed, LastWithinMark. 'AllOrNone' instruction requires displayQty to be 0. "
            "'MarkPrice', 'IndexPrice' or 'LastPrice' instruction valid for 'Stop', 'StopLimit', 'MarketIfTouched', "
            "and 'LimitIfTouched' orders. 'LastWithinMark' instruction valid for 'Stop' and 'StopLimit' with instruction "
            "'LastPrice'. IndexPrice, LastWithMark, Close and ReduceOnly are not applicable to spot trading symbols."
        ),
    )
    contingencyType: Optional[
        Literal["OneCancelsTheOther", "OneTriggersTheOther"]
    ] = Field(
        None, description="Optional contingency type for use with clOrdLinkID. Valid options: OneCancelsTheOther, OneTriggersTheOther."
    )
    text: Optional[str] = Field(
        None, description="Optional order annotation (e.g., 'Take profit')."
    )