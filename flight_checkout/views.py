import json
import utils

from django.views           import View
from django.core.exceptions import ObjectDoesNotExist
from django.http            import JsonResponse, HttpResponse

from flight.models          import Airport, Airline, Flight, Weekday, FlightWeekday
from flight_checkout.models import BookingInfo


class FlightBookingView(View):
    @utils.signin_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if BookingInfo.objects.filter(user_id = request.user.id).exists():
                return JsonResponse({"message": "Booked Already!"}, status=409)
            else:
                BookingInfo.objects.create(
                    user_id         = request.user.id,
                    start_flight_id = Flight.objects.get(id = data['start_flight_id']).id,
                    end_flight_id   = Flight.objects.get(id = data['end_flight_id']).id,
                    start_date      = data['start_date'],
                    end_date        = data['end_date'],
                    total_people    = data['total_people']
                )
                return JsonResponse({"message": "SUCCESS!"}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Object_DoesNotExist"}, status=400)


    @utils.signin_decorator
    def get(self, request):
        user_id         = request.user.id
        booked_flight   = BookingInfo.objects.select_related("user", "start_flight", "end_flight").get(user_id = user_id)
        start_flight_id = booked_flight.start_flight_id
        end_flight_id   = booked_flight.end_flight_id
        start_flight    = Flight.objects.select_related("airline","airport_depart","airport_arrive").get(id = start_flight_id)
        end_flight      = Flight.objects.select_related("airline","airport_depart","airport_arrive").get(id = end_flight_id)

        start_flight_list = [{
            "depart_airport_name"     : start_flight.airport_depart.name,
            "arrive_airport_name"     : start_flight.airport_arrive.name,
            "depart_airport_eng_name" : start_flight.airport_depart.eng_name,
            "arrive_airport_eng_name" : start_flight.airport_arrive.eng_name,
            "depart_date"             : booked_flight.start_date,
            "airline_name"            : start_flight.airline.name,
            "airline_logo"            : start_flight.airline.logo_url,
            "seat_class"              : start_flight.seat_class,
            'total_people'            : booked_flight.total_people
        }]
        end_flight_list = [{
            "depart_airport_name"     : end_flight.airport_depart.name,
            "arrive_airport_name"     : end_flight.airport_arrive.name,
            "depart_airport_eng_name" : end_flight.airport_depart.eng_name,
            "arrive_airport_eng_name" : end_flight.airport_arrive.eng_name,
            "depart_date"             : booked_flight.end_date,
            "airline_name"            : end_flight.airline.name,
            "airline_logo"            : end_flight.airline.logo_url,
            "seat_class"              : end_flight.seat_class,
            'total_people'            : booked_flight.total_people
        }]
        return JsonResponse({"message": "SUCCESS!", "start_flight": start_flight_list, "end_flight": end_flight_list}, status=200)    