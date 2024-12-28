from defusedxml import ElementTree as DET
import xml.etree.ElementTree as ET
import polars as pl
import httpx
import uuid



def charge_list() -> pl.DataFrame:
    "Returns a polars dataframe of UCMJ charges"

    response = httpx.get('https://legalassistance.law.af.mil/AMJAMS/PublicDocket/chargeList.xml')
    response.raise_for_status()

    tree = ET.ElementTree(DET.fromstring(response.text)).getroot()
    data = []

    for element in tree:
        code = element.find("specCode").text
        article = element.find("specArticle").text
        definition = element.find("specDefinition").text

        data.append({"code": code, "article": article, "definition": definition})

    return pl.DataFrame(data)


def base_list() -> pl.DataFrame:
    "Returns a list of USAF bases"

    response = httpx.get('https://legalassistance.law.af.mil/AMJAMS/PublicDocket/baseList.xml')
    response.raise_for_status()

    tree = ET.ElementTree(DET.fromstring(response.text)).getroot()
    data  = []

    for element in tree:
        base = element.find("base").text
        base_name = element.find("baseName").text
        state_abv = element.find("stateAbbrev").text
        state_long = element.find("stateLongName").text
        phone = element.find("basePhone").text

        data.append(
            {
                "base": base,
                "base_name": base_name,
                "state_abv": state_abv,
                "state": state_long,
                "phone_number": phone,
            }
        )
    return pl.DataFrame(data)


def case_list() -> tuple[pl.DataFrame, pl.DataFrame]:
    "Returns two polars dataframe objects. The first contains trail summaries, the second contains associated charges."

    response = httpx.get('https://legalassistance.law.af.mil/AMJAMS/PublicDocket/caseList.1.7.xml')
    element = ET.ElementTree(DET.fromstring(response.text)).getroot().find('trialResults')

    summary_temp = []
    charges_temp = []

    for trial in element:
        trial_id = str(uuid.uuid4())
        trial.attrib.update({'id':trial_id})
        summary_temp.append(trial.attrib)

        for charges in trial:
            if charges.tag == 'charge':

                charges.attrib.update({'id':trial_id})
                charges_temp.append(charges.attrib)

    return pl.DataFrame(summary_temp), pl.DataFrame(charges_temp)