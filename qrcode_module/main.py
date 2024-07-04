"""Main entrypoint"""
import sys
import qrcode
import qrcode.image.svg


def _main() -> int:
    qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(attrib={'class': 'some-css-class'})

    with open("qrcode.svg", "w") as f:
        f.write(img.to_string(encoding='unicode'))
    return 0

if __name__ == "__main__":
    sys.exit(_main())