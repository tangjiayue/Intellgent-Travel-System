import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

public class JsonDataGenerator {
    private static final ArrayList<String> HOTEL_ID=new ArrayList<>();
    private static final String[] districtsLocation = {"103.957706,30.990463","104.547644,30.410937","103.506478,30.197558","103.92342,30.574884","104.27536,30.556808","103.810906,30.410404","103.464176,30.41029","104.052236,30.691359","104.062415,30.674583","104.043246,30.641849","104.251342,30.8786","103.51226,30.573004","103.673025,30.630183","103.856423,30.681956","104.101452,30.659966","104.117262,30.598726","104.411871,30.86203","104.158593,30.823568","103.647193,30.988763","103.900486,30.795113"};


    private static final ArrayList<Hotel> HOTELS = new ArrayList<>();
    private static JSONArray bookingsArray = new JSONArray();

    public static void main(String[] args) {

        User[] users=getUser();
        readHotelData("hotels.json",users[0].preferredRating,users[0].preferredLocation,users[0].preferredHotelType);
        generateHotelBookings(400,users[0]);

        HOTELS.clear();
        readHotelData("hotels.json",users[1].preferredRating,users[1].preferredLocation,users[1].preferredHotelType);
        generateHotelBookings(400,users[1]);

        HOTELS.clear();
        readHotelData("hotels.json",users[2].preferredRating,users[2].preferredLocation,users[2].preferredHotelType);
        generateHotelBookings(400,users[2]);

        HOTELS.clear();
        readHotelData("hotels.json",users[3].preferredRating,users[3].preferredLocation,users[3].preferredHotelType);
        generateHotelBookings(400,users[3]);

        HOTELS.clear();
        readHotelData("hotels.json",users[4].preferredRating,users[4].preferredLocation,users[4].preferredHotelType);
        generateHotelBookings(400,users[4]);

        HOTELS.clear();
        readHotelData("hotels.json",users[5].preferredRating,users[5].preferredLocation,users[5].preferredHotelType);
        generateHotelBookings(400,users[5]);


//        System.out.println(bookingsArray);

        // 生成booking数据
//        JSONArray bookingsArray = generateHotelBookings(1000); //生成1000个实例
        writeJsonToFile("bookings.json", bookingsArray);
    }

    private static void generateHotelBookings(int count,User user) {
        Random random = new Random();

        for (int i = 0; i < count; i++) {
            JSONObject booking = new JSONObject();
            booking.put("id", i + 1);
            booking.put("hotel_id", getRandomHotelId());
            booking.put("username", user.username);
            booking.put("room_type", getRandomRoomType());
            booking.put("hotel_window", getRandomHotelWindow());
            booking.put("breakfast", getRandomBreakfast());
            String checkInDate = getRandomCheckInDate();
            booking.put("check_in_date", checkInDate);
            booking.put("check_out_date", getRandomCheckOutDate(checkInDate));
            booking.put("booking_time", getRandomBookingTime());

            bookingsArray.put(booking);
        }

    }


    //数据写入文件
    private static void writeJsonToFile(String filename, JSONArray data) {
        try (FileWriter file = new FileWriter(filename, true)) {
            file.write(data.toString(2)); // 写入格式 JSON
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 随机生成bookings数据
    private static String getRandomHotelId() {


        for (Hotel hotel : HOTELS) {
//            Hotel hotel1=HOTELS.get(new Random().nextInt((int) Math.round(HOTELS.size()*0.0309)));
//            double hotelWeight = hotel1.getSimilarity();
            double hotelWeight = hotel.getSimilarity();
            double randomWeight = new Random().nextDouble();

            if (hotelWeight >= randomWeight) {
                System.out.println("hotelWeight"+hotelWeight);
                System.out.println("randomWeight"+randomWeight);
//                return hotel1.getId();
                return hotel.getId();
            }
        }

        return HOTELS.get(new Random().nextInt(HOTELS.size())).getId(); // 作为后备方案，返回一个随机酒店ID
    }

    private static User[] getUser() {
        User[] users = {
                new User("111", 4.9,"103.900486,30.795113","住宿服务;宾馆酒店;宾馆酒店"),
                new User("333", 4.8,"104.543633,30.408577","住宿服务;宾馆酒店;五星级宾馆"),
                new User("tang", 4.5,"103.505832,30.196505","住宿服务;宾馆酒店;四星级宾馆"),
                new User("liu", 4.7,"103.810906,30.410404","住宿服务;宾馆酒店;三星级宾馆"),
                new User("zhu", 4.3,"104.251342,30.8786","住宿服务;旅馆招待所;旅馆招待所"),
                new User("xiao", 4.6,"104.411871,30.86203","住宿服务;宾馆酒店;宾馆酒店")
        };
        return users;
    }

    private static String getRandomRoomType() {
        String[] roomTypes = {"大床房", "双床房", /* Add more room types */};
        return roomTypes[new Random().nextInt(roomTypes.length)];
    }

    private static String getRandomHotelWindow() {
        String[] windows = {"有窗", "无窗"};
        return windows[new Random().nextInt(windows.length)];
    }

    private static String getRandomBreakfast() {
        String[] breakfasts = {"有", "无"};
        return breakfasts[new Random().nextInt(breakfasts.length)];
    }

    private static String getRandomCheckInDate() {
        LocalDate startDate = LocalDate.of(2024, 1, 1);
        LocalDate endDate = LocalDate.of(2024, 7, 18);
        long startEpochDay = startDate.toEpochDay();
        long endEpochDay = endDate.toEpochDay();

        long randomEpochDay = ThreadLocalRandom.current().nextLong(startEpochDay, endEpochDay);
        LocalDate randomDate = LocalDate.ofEpochDay(randomEpochDay);

        return randomDate.toString();
    }

    private static String getRandomCheckOutDate(String checkInDate) {
        LocalDate checkInLocalDate = LocalDate.parse(checkInDate);
        LocalDate startDate = checkInLocalDate.plusDays(1);  // checkout date should be at least one day after check-in date
        LocalDate endDate = LocalDate.of(2024, 7, 19); // extend by one day to ensure at least one day range for check-out

        long startEpochDay = startDate.toEpochDay();
        long endEpochDay = endDate.toEpochDay();

        long randomEpochDay = ThreadLocalRandom.current().nextLong(startEpochDay, endEpochDay);
        LocalDate randomDate = LocalDate.ofEpochDay(randomEpochDay);

        return randomDate.toString();
    }

    private static String getRandomBookingTime() {
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        return now.format(formatter);
    }

    private static void readHotelData(String filePath, double preferredRating, String preferredLocation, String preferredHotelType) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filePath));  // 创建BufferedReader对象读取JSON文件
            StringBuilder jsonContent = new StringBuilder();  // 读取文件内容到StringBuilder
            String line;
            while ((line = reader.readLine()) != null) {
                jsonContent.append(line);
            }
            reader.close();  // 关闭文件读取器

            JSONArray jsonArray = new JSONArray(jsonContent.toString());
            // 遍历数组并提取每个对象的id
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject item = jsonArray.getJSONObject(i);
                String id = item.getString("id");
                String name = item.getString("name");
                double rating = item.getString("rating")=="" ? 0.0 : Double.parseDouble(item.getString("rating"));  // 如果rating为空，则设为0;
                String location = item.getString("location");
                String hotelType = item.getString("hotel_type");

                Hotel hotel = new Hotel(id, name, rating, location, hotelType);
                double similarity = calculateSimilarity(hotel, preferredRating, preferredLocation, preferredHotelType);
                hotel.setSimilarity(similarity);
                HOTELS.add(hotel);
            }

//            HOTELS.sort(Comparator.comparingDouble(Hotel::getSimilarity).reversed());
        } catch (IOException e) {
            e.printStackTrace();
        } catch (org.json.JSONException e) {
            e.printStackTrace();
        }
    }

    private static double calculateSimilarity(Hotel hotel, double preferredRating, String preferredLocation, String preferredHotelType) {
        // 假设评分的权重为0.5，位置的权重为0.3，房间类型的权重为0.2
        double ratingWeight = 0.4;
        double locationWeight = 0.2;
        double hotelTypeWeight = 0.4;

        // 计算评分相似度
        double ratingSimilarity = 1 - Math.abs(hotel.getRating() - preferredRating) / 5.0;

        // 计算位置相似度（简单地以距离为准）
        double locationSimilarity = calculateLocationSimilarity(hotel.getLocation(), preferredLocation);

        // 计算房间类型相似度（简单地用字符串相等判断）
        double roomTypeSimilarity = hotel.getHotelType().equalsIgnoreCase(preferredHotelType) ? 1.0 : 0.0;

        // 计算总相似度
        return ratingWeight * ratingSimilarity + locationWeight * locationSimilarity + hotelTypeWeight * roomTypeSimilarity;
    }

    private static double calculateLocationSimilarity(String hotelLocation, String preferredLocation) {
        String[] hotelCoords = hotelLocation.split(",");
        String[] preferredCoords = preferredLocation.split(",");

        double hotelLat = Double.parseDouble(hotelCoords[1]);
        double hotelLon = Double.parseDouble(hotelCoords[0]);
        double preferredLat = Double.parseDouble(preferredCoords[1]);
        double preferredLon = Double.parseDouble(preferredCoords[0]);

        // 使用简单的欧几里得距离计算相似度，距离越近，相似度越高
        double distance = Math.sqrt(Math.pow(hotelLat - preferredLat, 2) + Math.pow(hotelLon - preferredLon, 2));
        return 1 / (1 + distance); // 距离越小，相似度越大
    }



    static class Hotel {
        private String id;
        private String name;
        private double rating;
        private String location;
        private String hotelType;
        private double similarity;

        public Hotel(String id, String name, double rating, String location, String hotelType) {
            this.id = id;
            this.name = name;
            this.rating = rating;
            this.location = location;
            this.hotelType = hotelType;
        }

        public void setId(String id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public double getRating() {
            return rating;
        }

        public void setRating(double rating) {
            this.rating = rating;
        }

        public String getLocation() {
            return location;
        }

        public void setLocation(String location) {
            this.location = location;
        }

        public String getHotelType() {
            return hotelType;
        }

        public void setHotelType(String hotelType) {
            this.hotelType = hotelType;
        }

        public String getId() {
            return id;
        }

        public double getSimilarity() {
            return similarity;
        }

        public void setSimilarity(double similarity) {
            this.similarity = similarity;
        }

        @Override
        public String toString() {
            return "Hotel{" +
                    "id='" + id + '\'' +
                    ", name='" + name + '\'' +
                    ", rating=" + rating +
                    ", location='" + location + '\'' +
                    ", hotelType='" + hotelType + '\'' +
                    ", similarity=" + similarity +
                    '}';
        }
    }

   static class User{
        String username;
        // 定义用户偏好
        double preferredRating;
        String preferredLocation;
        String preferredHotelType;
        public User(){
            this.username="111";
            this.preferredRating=4.8;
            this.preferredLocation = "103.900486,30.795113";// 假设用户偏好郫都区
            this.preferredHotelType = "住宿服务;宾馆酒店;宾馆酒店";
        }

        public User(String username, double preferredRating, String preferredLocation, String preferredHotelType) {
            this.username = username;
            this.preferredRating = preferredRating;
            this.preferredLocation = preferredLocation;
            this.preferredHotelType = preferredHotelType;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public double getPreferredRating() {
            return preferredRating;
        }

        public void setPreferredRating(double preferredRating) {
            this.preferredRating = preferredRating;
        }

        public String getPreferredLocation() {
            return preferredLocation;
        }

        public void setPreferredLocation(String preferredLocation) {
            this.preferredLocation = preferredLocation;
        }

        public String getPreferredHotelType() {
            return preferredHotelType;
        }

        public void setPreferredHotelType(String preferredHotelType) {
            this.preferredHotelType = preferredHotelType;
        }
    }






























    //生成hotel的json数组
    private static JSONArray generateHotelInformation() {
        JSONArray hotelsArray = new JSONArray();

        for(int n=0;n<districtsLocation.length;n++){
            String districtLocation = districtsLocation[n];
            String aroundUrl = "https://restapi.amap.com/v3/place/around"
                    + "?key=744da9ef5d0a11aadadd0845adfdf13a"
                    + "&keywords=酒店|旅馆|宾馆"
                    + "&location=" + districtLocation
                    + "&radius=10000"
                    + "&offset=30"
                    + "&page=1"
                    + "&extensions=all";
            String response = sendHttpRequest(aroundUrl);

            try {
                JSONObject jsonResponse = new JSONObject(response);
                int status = jsonResponse.getInt("status");
                if (status == 1) {
                    JSONArray pois = jsonResponse.getJSONArray("pois");
                    for (int i = 0; i < pois.length(); i++) {
                        JSONObject poi = pois.getJSONObject(i);

                        String id = poi.optString("id", "");
                        String name = poi.optString("name", "");
                        String rating = poi.getJSONObject("biz_ext").optString("rating").length()>2 ? poi.getJSONObject("biz_ext").optString("rating") : "";
                        String address = poi.optString("address", ""); // 使用optString方法
                        String location = poi.optString("location", "");
                        String type = poi.optString("type", "");
                        String url="";

                        JSONArray photos = poi.getJSONArray("photos");
                        for (int j = 0; j < photos.length(); j++) {
                            JSONObject photo = photos.getJSONObject(j);
                            url = photo.getString("url");
                        }

                        HOTEL_ID.add(id);

                        System.out.println(id+" "+name+" "+rating+" "+address+" "+location+" "+type+" "+url);
                        hotelsArray.put(createHotel(id, name, rating, address, location, url, type));
                    }
                } else {
                    System.out.println("Error: " + jsonResponse.getString("info"));
                }
            } catch (Exception e) {
                e.printStackTrace();
            }

        }


        return hotelsArray;
    }

    //生成json对象
    private static JSONObject createHotel(String id, String name, String rating, String address, String location, String photo, String hotel_type) {
        JSONObject hotel = new JSONObject();
        hotel.put("id", id);
        hotel.put("name", name);
        hotel.put("rating", rating);
        hotel.put("address", address);
        hotel.put("location", location);
        hotel.put("photo", photo);
        hotel.put("hotel_type", hotel_type);

        return hotel;
    }


    //api获取响应
    private static String sendHttpRequest(String urlString) {
        try {
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                return response.toString();
            } else {
                System.out.println("GET 请求失败");
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}
