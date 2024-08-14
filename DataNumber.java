import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class DataNumber {

    public static void main(String[] args) {
//        readBookingsData("C:/Users/33925/OneDrive/桌面/bookings（未排序1800个例子）.json");
        readBookingsData("bookings.json");
    }

    private static void readBookingsData(String filePath) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filePath));  // 创建BufferedReader对象读取JSON文件
            StringBuilder jsonContent = new StringBuilder();  // 读取文件内容到StringBuilder
            String line;
            while ((line = reader.readLine()) != null) {
                jsonContent.append(line);
            }
            reader.close();  // 关闭文件读取器

            JSONArray jsonArray = new JSONArray(jsonContent.toString());

            // 统计每个 hotel_id 的出现次数
            Map<String, Integer> hotelIdCounts = new HashMap<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String hotelId = jsonObject.getString("hotel_id");
                hotelIdCounts.put(hotelId, hotelIdCounts.getOrDefault(hotelId, 0) + 1);
            }

            // 将 Map 按照值进行排序（出现次数从大到小）
            List<Map.Entry<String, Integer>> sortedEntries = hotelIdCounts.entrySet().stream()
                    .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                    .collect(Collectors.toList());

            // 获取出现次数最多的前 10 个 hotel_id
            List<String> topHotelIds = sortedEntries.stream()
                    .limit(10)
                    .map(Map.Entry::getKey)
                    .collect(Collectors.toList());

            // 打印结果
            System.out.println("Top 10 hotel_ids by frequency:");
            topHotelIds.forEach(System.out::println);


        } catch (IOException e) {
            e.printStackTrace();
        } catch (org.json.JSONException e) {
            e.printStackTrace();
        }
    }
}

