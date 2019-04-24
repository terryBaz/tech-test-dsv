import xlrd
import urllib.parse
import xmltodict
from urllib.request import Request, urlopen


def read_xlsx(path):
    wb = xlrd.open_workbook(path)
    return wb.sheet_by_index(0)


def int_str(x):
    return str(int(x))


def build_obj(data):
    _o = {
        "declVal": data[13],
        "declValCur": data[14],
        "wgtUom": data[12],
        "noPce": int_str(data[10]),
        "wgt0": str(data[11]),
        "shpDate": data[1],
        "orgCtry": data[4],
        "orgCity": data[3],
        "orgZip": str(data[2]),
        "dstCtry": data[8],
        "dstCity": data[7],
        "dstZip": str(data[6]),
    }

    if int(_o["noPce"]) > 1:
        for j in range(1, int(_o["noPce"])):
            _o["wgt" + str(j)] = _o["wgt0"]

    return _o


# def build_get_params(o):
#     print(o)
#     _s = ""
#     for key in o:
#         _s = _s + "&" + key + "=" + str(o[key])
#     return _s


def get_results(obj):
    # _params = build_get_params(obj)
    _params = urllib.parse.urlencode(obj)
    _url = "http://dct.dhl.com/data/quotation/?dtbl=N&w0=0&l0=0&h0=0&dimUom=cm&" + _params

    # _url = u''.join(_url).encode('utf-8').strip()

    print(_url)
    req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
    _res = urlopen(req).read()

    return xmltodict.parse(_res)


if __name__ == '__main__':

    loc = ("./data_in/Test 2 - DHL Shipments Report.xlsx")

    sheet = read_xlsx(loc)

    # sheet.cell_value(0, 0)

    for i in range(1, sheet.nrows):
        print(sheet.row_values(i))
        _obj = build_obj(sheet.row_values(i))
        res = get_results(_obj)
        if int(res['quotationResponse']['count']) == 0:
            print('***********************')
        print(res['quotationResponse']['count'])
        # break
    # ETA
    # ETA
    # OK?

    # print(sheet.nrows)
