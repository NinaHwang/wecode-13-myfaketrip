import json
import random
import datetime

from django.db.models import Q 
from django.views     import View
from django.http      import JsonResponse, HttpResponse

from flight.models    import Airport, Airline, Flight, Weekday, FlightWeekday


class FlightScheduleView(View):
    def get(self, request):
        go                  = request.GET.get("go", None)   #가는편
        come                = request.GET.get("come", None)    #오는편
        airport_depart_name = request.GET.get("airport_depart", None)   #출발 공항명
        airport_arrive_name = request.GET.get("airport_arrive", None)   #도착 공항명
        start_date          = request.GET.get("start_date", None)   #여행 시작날 출발날짜
        end_date            = request.GET.get("end_date", None)   #여행 마지막날 출발날짜
        airline_list        = request.GET.getlist('airline_list', None)   #항공사 필터 리스트
        seat_class          = request.GET.getlist('seat_class', None)   #좌석 등급 필터 리스트

        q = Q()
        if airline_list:
            q &= Q(airline__name__in = airline_list)
        if seat_class:
            q &= Q(seat_class__in = seat_class)

        if go:
            flight_condition = {
                'depart_date' : start_date,
                'depart'      : airport_depart_name,
                'arrive'      : airport_arrive_name
            }
        elif come:
            flight_condition = {
                'depart_date' : end_date,
                'depart'      : airport_arrive_name,
                'arrive'      : airport_depart_name
            }
        else:
            return JsonResponse({"message":"Not Found URL"}, status=400)

        flights = Flight.objects.select_related("airline","airport_depart","airport_arrive").prefetch_related("flightweekday_set").filter(airport_depart__name = flight_condition['depart'], airport_arrive__name = flight_condition['arrive'], flightweekday__date = flight_condition['depart_date']).filter(q)

        flight_list = [{
            "id"                 : flight.id,
            "airport_depart"     : flight_condition['depart'],
            "airport_arrive"     : flight_condition['arrive'],
            "depart_date"        : flight_condition['depart_date'],
            "depart_weekday"     : FlightWeekday.objects.filter(date = flight_condition['depart_date'], flight_id = flight.id)[0].weekday,
            "flightid"           : flight.flightid,
            "airport_depart_eng" : flight.airport_depart.eng_name,                    
            "airport_arrive_eng" : flight.airport_arrive.eng_name,
            "depart_time"        : flight.depart_time,
            "arrive_time"        : flight.arrive_time,
            "airline"            : flight.airline.name,
            "airline_url"        : flight.airline.logo_url,
            "remain_seats"       : flight.remain_seats,
            "basic_price"        : flight.basic_price,
            "seat_class"         : flight.seat_class
        } for flight in flights]
        low_price = sorted(flight_list, key=lambda k: k['basic_price'])
        return JsonResponse({"message":"SUCCESS!", "flight_list":low_price}, status=200)