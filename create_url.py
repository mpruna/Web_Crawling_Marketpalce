import fire
from urllib.parse import urljoin
import posixpath
import pandas as pd
from datetime import datetime
import os

os.chdir("/home/Bitbucket/web_scraping/auto_scrapers/olx_scrapers/olx_scrapers/spiders")

def validate_options(item_check, item1, item2):
    check: bool = True

    if item_check == "brand_model":
        data = pd.read_json('car-list_v2.json')
        brand_list = data['brand'].tolist()
        models = data[data['brand'] == item1]['models'].tolist()[0]

        check: bool = [(item1 in brand_list) & (item2 in models)][0]

    if item_check == "date_check":
        date = datetime.now().year
        if item1 and item2 is not None:
            check: bool = [(item1 >= 1960) & (item1 <= item2) & (item2 <= date)]
        elif item1 is not None:
            check: bool = item1 >=1960
        else:
            check: bool = item2 <=date

    if item_check == "price_check":
        if item1 and item2 is not None:
            check: bool = [(item1 <= item2) and (item1 >=1000 and item2 <= 1000000)][0]
        elif item1 is not None:
            check: bool = item1 >=1000
        else:
            check: bool = item2 <= 1000000

    if item_check == "fuel_check":
        fuel_list = ['Benzina', 'Diesel', 'Gpl', 'Hybrid', 'Electric']
        check: bool = item1 in fuel_list

    print("End check status: ", check)
    return check


def createurl(brand: str, model: str, y_start: int, y_stop: int, start_p: int, stop_p: int, fuel: str):
    """
    Returns the search parameters from
    base OLX URL: "https://www.olx.ro/auto-masini-moto-ambarcatiuni"
    :param brand: car brand [Volvo, BMW, Audi] etc
    :param model: car model [XC60, X3, A4] etc
    :param y_start: Year when car was built, starting the search from year ...
    :param y_stop: Year when car was built, up to year ...
    :param start_p: Starting price for the car
    :param stop_p: Stopping price for the car
    :param fuel: ['Benzina', 'Diesel, 'Gpl', 'Hybrid', 'Electric']
    """

    base_url = "https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/"
    opt_path = posixpath.join(brand, model)
    return_url= urljoin(base_url, opt_path)

    # Brand and model are mandatory options, this is by design

    # opt = [brand, model, y_start, y_stop, start_p, stop_p, fuel]
    opt_combo = [[brand, model],[y_start, y_stop],[start_p, stop_p], [fuel, True]]
    checks = {"brand_model":opt_combo[0], "date_check":opt_combo[1], "price_check":opt_combo[2], "fuel_check":opt_combo[3]}
    # checks = ["brand_model", "date_check", "price_check", "fuel_check"]
    checks_done = []
    checks_status = True



    for ck in checks.items():
        if (ck[1][0] is not True) and (ck[1][1] is not True):
            check_status = validate_options(ck[0], ck[1][0], ck[1][1])
            checks_done.append(check_status)

        elif (ck[1][0] is not True) or (ck[1][1] is not True):

            if ck[1][0] is True:
                ck[1][0] = None
            if ck[1][1] is True:
                ck[1][1] = None

            check_status = validate_options(ck[0], ck[1][0], ck[1][1])
            checks_done.append(check_status)

    print(checks_done)

    '''
    while check_status:
        pass
    '''
    if check_status == True:
        opt_path=["?search%5Bfilter_float_price%3Afrom%5D=", "search%5Bfilter_float_price%3Ato%5D=", "?search%5Bfilter_float_year%3Afrom%5D=", "search%5Bfilter_float_year%3Ato%5D="]
        opt=[start_p,stop_p]
        return_url = posixpath.join(return_url, opt_path[0], str(opt[0]))
        return_url = posixpath.join(return_url, opt_path[1], str(opt[1]))

    return return_url

def export_url(url):

    cmd="conda env config vars set url="+str(url)
    export_status=os.popen(cmd).read()
    print(export_status)

if __name__ == '__main__':
  url=fire.Fire(createurl)
  export_url(url)
  print(url)

