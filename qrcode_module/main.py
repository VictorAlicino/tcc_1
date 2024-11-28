"""Main entrypoint"""
import sys
import json
import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer


def _main() -> int:
    qr = qrcode.QRCode(
        # Max Error Correction possible
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=100,  # Aumenta a resolução ajustando o tamanho dos módulos
        image_factory=qrcode.image.svg.SvgPathImage
    )
    qr.add_data(
        'https://linktr.ee/mooviprodutora?utm_source=qr_code'
    )
    qr.make(fit=True)

    img = qr.make_image(
        attrib={'class': 'some-css-class'},
        image_factory=StyledPilImage,
        module_drawer=HorizontalBarsDrawer()
    )

    img.save('qr_code.png')

if __name__ == "__main__":
    sys.exit(_main())