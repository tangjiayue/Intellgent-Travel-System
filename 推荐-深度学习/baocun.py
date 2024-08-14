import json

data = {
    "bookings": [
        {
            "id": 1,
            "username": "user1",
            "room_type": "Deluxe",
            "hotel_window": "City View",
            "breakfast": "Included",
            "check_in_date": "2023-07-01",
            "check_out_date": "2023-07-05",
            "booking_time": "2023-06-15",
            "hotel_id": "hotel1"
        },
        {
            "id": 2,
            "username": "user2",
            "room_type": "Standard",
            "hotel_window": "Garden View",
            "breakfast": "Not Included",
            "check_in_date": "2023-07-02",
            "check_out_date": "2023-07-06",
            "booking_time": "2023-06-16",
            "hotel_id": "hotel2"
        }
    ],
    "hotels": [
        {
            "id": "hotel1",
            "name": "Hotel Sunshine",
            "address": "123 Sunny Street",
            "location": "Sunnytown",
            "photo": "sunshine.jpg",
            "hotel_type": "Luxury",
            "rating": "4.5"
        },
        {
            "id": "hotel2",
            "name": "Garden Inn",
            "address": "456 Garden Road",
            "location": "Gardenville",
            "photo": "garden.jpg",
            "hotel_type": "Budget",
            "rating": "4.0"
        }
    ]
}

with open('data.json', 'w') as f:
    json.dump(data, f)
