import 'package:flutter/material.dart';
import 'package:adobe_xd/pinned.dart';
import './xd_home_screen_no_filter.dart';
import 'package:adobe_xd/page_link.dart';
import 'package:flutter_svg/flutter_svg.dart';

class XD_LoginScreen extends StatelessWidget {
  XD_LoginScreen({
    Key? key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff1a1824),
      body: Stack(
        children: <Widget>[
          Pinned.fromPins(
            Pin(start: 33.0, end: 33.0),
            Pin(size: 78.0, middle: 0.7084),
            child: PageLink(
              links: [
                PageLinkInfo(
                  ease: Curves.easeOut,
                  duration: 0.3,
                  pageBuilder: () => XD_HomeScreenNoFilter(),
                ),
              ],
              child: Stack(
                children: <Widget>[
                  Container(
                    decoration: BoxDecoration(
                      color: const Color(0xff587368),
                      borderRadius: BorderRadius.circular(50.0),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0x42000000),
                          offset: Offset(0, 3),
                          blurRadius: 6,
                        ),
                      ],
                    ),
                  ),
                  Align(
                    alignment: Alignment(0.179, -0.094),
                    child: SizedBox(
                      width: 191.0,
                      height: 25.0,
                      child: Text(
                        'Continuar com Google',
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          fontSize: 19,
                          color: const Color(0xffffffff),
                          fontWeight: FontWeight.w700,
                        ),
                        softWrap: false,
                      ),
                    ),
                  ),
                  Pinned.fromPins(
                    Pin(size: 26.5, start: 28.9),
                    Pin(size: 27.0, middle: 0.4792),
                    child:
                        // Adobe XD layer: 'logo-google' (shape)
                        SvgPicture.string(
                      _svg_gs1bmi,
                      allowDrawingOutsideViewBox: true,
                      fit: BoxFit.fill,
                    ),
                  ),
                ],
              ),
            ),
          ),
          Pinned.fromPins(
            Pin(start: 33.0, end: 33.0),
            Pin(size: 78.0, middle: 0.8302),
            child: PageLink(
              links: [
                PageLinkInfo(
                  ease: Curves.easeOut,
                  duration: 0.3,
                  pageBuilder: () => XD_HomeScreenNoFilter(),
                ),
              ],
              child: Stack(
                children: <Widget>[
                  Container(
                    decoration: BoxDecoration(
                      color: const Color(0xff587368),
                      borderRadius: BorderRadius.circular(50.0),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0x4d000000),
                          offset: Offset(0, 3),
                          blurRadius: 6,
                        ),
                      ],
                    ),
                  ),
                  Pinned.fromPins(
                    Pin(size: 213.0, end: 49.0),
                    Pin(size: 25.0, middle: 0.4528),
                    child: Text(
                      'Continuar com Microsoft',
                      style: TextStyle(
                        fontFamily: 'Roboto',
                        fontSize: 19,
                        color: const Color(0xffffffff),
                        fontWeight: FontWeight.w700,
                      ),
                      softWrap: false,
                    ),
                  ),
                  Pinned.fromPins(
                    Pin(size: 29.1, start: 28.9),
                    Pin(size: 29.2, middle: 0.4999),
                    child:
                        // Adobe XD layer: 'logo-microsoft' (group)
                        Stack(
                      children: <Widget>[
                        Align(
                          alignment: Alignment.topLeft,
                          child: SizedBox(
                            width: 14.0,
                            height: 14.0,
                            child: SvgPicture.string(
                              _svg_ighzk4,
                              allowDrawingOutsideViewBox: true,
                            ),
                          ),
                        ),
                        Align(
                          alignment: Alignment.topRight,
                          child: SizedBox(
                            width: 14.0,
                            height: 14.0,
                            child: SvgPicture.string(
                              _svg_ec3205,
                              allowDrawingOutsideViewBox: true,
                            ),
                          ),
                        ),
                        Align(
                          alignment: Alignment.bottomLeft,
                          child: SizedBox(
                            width: 14.0,
                            height: 14.0,
                            child: SvgPicture.string(
                              _svg_x985,
                              allowDrawingOutsideViewBox: true,
                            ),
                          ),
                        ),
                        Align(
                          alignment: Alignment.bottomRight,
                          child: SizedBox(
                            width: 14.0,
                            height: 14.0,
                            child: SvgPicture.string(
                              _svg_ici3bh,
                              allowDrawingOutsideViewBox: true,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          Align(
            alignment: Alignment(0.003, -0.315),
            child: SizedBox(
              width: 294.0,
              height: 135.0,
              child:
                  // Adobe XD layer: 'opus logo' (group)
                  Stack(
                children: <Widget>[
                  Pinned.fromPins(
                    Pin(size: 88.8, start: 0.0),
                    Pin(size: 108.6, end: 1.6),
                    child: Stack(
                      children: <Widget>[
                        Pinned.fromPins(
                          Pin(size: 66.9, start: 0.0),
                          Pin(start: 0.0, end: 14.1),
                          child: SvgPicture.string(
                            _svg_x7z1xj,
                            allowDrawingOutsideViewBox: true,
                            fit: BoxFit.fill,
                          ),
                        ),
                        Pinned.fromPins(
                          Pin(size: 66.8, end: 0.0),
                          Pin(start: 14.2, end: 0.0),
                          child: SvgPicture.string(
                            _svg_xa9bse,
                            allowDrawingOutsideViewBox: true,
                            fit: BoxFit.fill,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Pinned.fromPins(
                    Pin(size: 181.0, end: 0.0),
                    Pin(start: 0.0, end: 0.0),
                    child: Text(
                      'opus',
                      style: TextStyle(
                        fontFamily: 'Aaux Next',
                        fontSize: 94,
                        color: const Color(0xffd9ac25),
                        fontWeight: FontWeight.w100,
                        shadows: [
                          Shadow(
                            color: const Color(0x29000000),
                            offset: Offset(0, 3),
                            blurRadius: 6,
                          )
                        ],
                      ),
                      softWrap: false,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

const String _svg_gs1bmi =
    '<svg viewBox="28.8 24.7 26.5 27.0" ><path transform="translate(-7.46, -7.31)" d="M 62.62921905517578 43.44019317626953 L 62.49277496337891 42.86118316650391 L 49.90782928466797 42.86118316650391 L 49.90782928466797 48.18761444091797 L 57.42716217041016 48.18761444091797 C 56.64648056030273 51.89474487304688 53.02388000488281 53.84613037109375 50.06481170654297 53.84613037109375 C 47.91177749633789 53.84613037109375 45.64220809936523 52.94048309326172 44.14004516601562 51.48478698730469 C 42.53937911987305 49.90886688232422 41.63136672973633 47.76094055175781 41.61628723144531 45.51473999023438 C 41.61628723144531 43.27114105224609 42.62458038330078 41.02693176269531 44.09173202514648 39.55072021484375 C 45.55889129638672 38.07450866699219 47.77471923828125 37.24855041503906 49.97787094116211 37.24855041503906 C 52.50101089477539 37.24855041503906 54.30929565429688 38.58831024169922 54.98551940917969 39.19932556152344 L 58.77054214477539 35.43422698974609 C 57.66021728515625 34.45854187011719 54.6099739074707 31.99999809265137 49.85590744018555 31.99999809265137 L 49.85590744018555 31.99999809265137 C 46.18802261352539 31.99999809265137 42.67107009887695 33.40496826171875 40.1002311706543 35.96736145019531 C 37.56319046020508 38.49050140380859 36.25 42.13906860351562 36.25 45.52439880371094 C 36.25 48.90972137451172 37.49256134033203 52.37596130371094 39.95109939575195 54.91902923583984 C 42.57809448242188 57.63114929199219 46.29850387573242 59.04879760742188 50.12941360473633 59.04879760742188 C 53.61496734619141 59.04879760742188 56.91879653930664 57.68307495117188 59.27349090576172 55.20520782470703 C 61.58832550048828 52.76598358154297 62.78559494018555 49.39092254638672 62.78559494018555 45.85284423828125 C 62.78559494018555 44.36335754394531 62.6358642578125 43.47882843017578 62.62921905517578 43.44019317626953 Z" fill="#ffffff" stroke="none" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_ighzk4 =
    '<svg viewBox="0.0 0.0 13.8 13.8" ><path transform="translate(0.0, 457.0)" d="M 0 -450.0803527832031 L 0 -443.1607666015625 L 6.919610977172852 -443.1607666015625 L 13.8392219543457 -443.1607666015625 L 13.8392219543457 -450.0803527832031 L 13.8392219543457 -457.0000305175781 L 6.919610977172852 -457.0000305175781 L 0 -457.0000305175781 L 0 -450.0803527832031 Z" fill="#ffffff" stroke="none" stroke-width="0.10000000149011612" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_ec3205 =
    '<svg viewBox="15.2 0.0 13.8 13.8" ><path transform="translate(-127.78, 457.0)" d="M 143.0745086669922 -456.9255065917969 C 143.0319213867188 -456.8934936523438 143.0000152587891 -453.7744445800781 143.0000152587891 -450.0058898925781 L 143.0000152587891 -443.1607666015625 L 149.9196166992188 -443.1607666015625 L 156.8392333984375 -443.1607666015625 L 156.8392333984375 -450.0803527832031 L 156.8392333984375 -457.0000305175781 L 149.9941253662109 -457.0000305175781 C 146.2256164550781 -457.0000305175781 143.1064605712891 -456.9681091308594 143.0745086669922 -456.9255065917969 Z" fill="#ffffff" stroke="none" stroke-width="0.10000000149011612" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_x985 =
    '<svg viewBox="0.0 15.3 13.8 13.8" ><path transform="translate(0.0, 328.33)" d="M 0 -306.0803527832031 L 0 -299.1607971191406 L 6.919610977172852 -299.1607971191406 L 13.8392219543457 -299.1607971191406 L 13.8392219543457 -306.0803527832031 L 13.8392219543457 -313.0000305175781 L 6.919610977172852 -313.0000305175781 L 0 -313.0000305175781 L 0 -306.0803527832031 Z" fill="#ffffff" stroke="none" stroke-width="0.10000000149011612" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_ici3bh =
    '<svg viewBox="15.2 15.3 13.8 13.8" ><path transform="translate(-127.78, 328.33)" d="M 143.0212860107422 -306.1123657226562 L 143.05322265625 -299.2139892578125 L 149.9515686035156 -299.18212890625 L 156.8392333984375 -299.1607971191406 L 156.8392333984375 -306.0803527832031 L 156.8392333984375 -313.0000305175781 L 149.9196166992188 -313.0000305175781 L 143.0000152587891 -313.0000305175781 L 143.0212860107422 -306.1123657226562 Z" fill="#ffffff" stroke="none" stroke-width="0.10000000149011612" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_x7z1xj =
    '<svg viewBox="0.0 0.0 66.9 94.5" ><path transform="translate(-1053.07, -607.02)" d="M 1069.840942382812 661.6810302734375 C 1069.840942382812 634.7634887695312 1081.724731445312 612.9419555664062 1096.384155273438 612.9419555664062 C 1103.199340820312 612.9419555664062 1109.414306640625 617.6589965820312 1114.1142578125 625.411376953125 L 1119.921508789062 616.0897216796875 C 1113.1083984375 610.3583984375 1104.936645507812 607.02001953125 1096.150024414062 607.02001953125 C 1072.357666015625 607.02001953125 1053.070190429688 631.49267578125 1053.070190429688 661.6804809570312 C 1053.070190429688 677.4046020507812 1058.30322265625 691.577880859375 1066.680419921875 701.5499267578125 L 1074.436767578125 689.0989990234375 C 1071.536499023438 681.2877197265625 1069.840942382812 671.8483276367188 1069.840942382812 661.6810302734375 Z" fill="#d9ac25" stroke="none" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_xa9bse =
    '<svg viewBox="22.0 14.2 66.8 94.4" ><path transform="translate(-1420.71, -878.65)" d="M 1495.935546875 892.8499755859375 L 1488.442626953125 904.865966796875 C 1491.421142578125 912.7445068359375 1493.166748046875 922.3133544921875 1493.166748046875 932.631103515625 C 1493.166748046875 959.5504150390625 1481.283203125 981.372314453125 1466.623779296875 981.372314453125 C 1459.717651367188 981.372314453125 1453.427856445312 976.528076171875 1448.705932617188 968.5897216796875 L 1442.670288085938 978.2685546875 C 1449.473266601562 983.9725341796875 1457.625610351562 987.2939453125 1466.390625 987.2939453125 C 1490.182861328125 987.2939453125 1509.469970703125 962.8203125 1509.469970703125 932.631103515625 C 1509.469482421875 916.953369140625 1504.26806640625 902.8177490234375 1495.935546875 892.8499755859375 Z" fill="#d9ac25" stroke="none" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
