# Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
class XoneyException(Exception):
    pass


class UnexpectedTradeSideError(XoneyException):
    def __init__(self, side):
        super().__init__(f"Unexpected trade side: {side}")


class InvalidSymbolError(XoneyException):
    def __init__(self, symbol):
        super().__init__(f"Invalid symbol: {symbol}")


class ChartError(XoneyException):
    pass


class IncorrectChartLength(ChartError):
    def __init__(self, lengths):
        lengths = map(str, lengths)
        super().__init__("All arrays must be of the same length. "
                         "Received lengths: " + ", ".join(lengths))


class InvalidChartParameters(ChartError):
    def __init__(self):
        super().__init__("Incorrect parameters of Chart initialization. "
                         "Please check types of parameters")


class UnexpectedParameter(XoneyException):
    def __init__(self, parameter):
        super().__init__(f"Unexpected parameter type: {type(parameter)}.")


class TradingSystemException(XoneyException):
    pass
