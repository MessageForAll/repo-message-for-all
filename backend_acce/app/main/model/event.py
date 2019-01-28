import json

class Event():
    id_ordem: str
    id_event_rec: str
    event_number: str
    forecast_date: str
    initial_date: str
    end_date: str
    request_date_rec: str
    result_date_rec: str
    descr_event_type: str
    result: str
    msg: str

    def fill(self, cci_resp: str):
        cci_dict = json.loads(cci_resp)
        
        self.id_ordem = cci_dict["idOrdem"] if "idOrdem" in cci_dict.keys() else ""
        self.id_event_rec = cci_dict["idEventRec"] if "idEventRec" in cci_dict.keys() else ""
        self.event_number = cci_dict["eventNumber"] if "eventNumber" in cci_dict.keys() else ""
        self.forecast_date = cci_dict["forecastDate"] if "forecastDate" in cci_dict.keys() else ""
        self.initial_date = cci_dict["initialDate"] if "initialDate" in cci_dict.keys() else ""
        self.end_date = cci_dict["endDate"] if "endDate" in cci_dict.keys() else ""
        self.request_date_rec = cci_dict["requestDateREC"] if "requestDateREC" in cci_dict.keys() else ""
        self.result_date_rec = cci_dict["resultDateREC"] if "resultDateREC" in cci_dict.keys() else ""
        self.descr_event_type = cci_dict["descrEventType"] if "descrEventType" in cci_dict.keys() else ""
        self.result = cci_dict["result"] if "result" in cci_dict.keys() else ""
        self.msg = cci_dict["msg"] if "msg" in cci_dict.keys() else ""
