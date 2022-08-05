import base64
import dataclasses as dc
from io import BytesIO

from qrcode import QRCode
from qrcode.image.base import BaseImage
from qrcode.image.svg import SvgImage


@dc.dataclass(repr=False)
class QRService:
    stream: BytesIO = dc.field(default_factory=lambda: BytesIO())
    image_factory: BaseImage = dc.field(default_factory=lambda: SvgImage)

    def _prepare_qr_code(self, short_url: str) -> QRCode:
        qr = QRCode(image_factory=self.image_factory)
        qr.add_data(short_url)
        qr.make(fit=True)

        return qr

    def _make_in_memory_image(self, qr: QRCode) -> None:
        # also can be added attrib={'class': 'some-css-class'}
        image = qr.make_image()
        image.save(self.stream)

    def _convert_bytes_to_str(self) -> str:
        return base64.b64encode(self.stream.getvalue()).decode("utf-8")

    def make_qr(self, short_url: str) -> str:
        qr = self._prepare_qr_code(short_url)
        self._make_in_memory_image(qr)

        return self._convert_bytes_to_str()
