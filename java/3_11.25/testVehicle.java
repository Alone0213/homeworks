public class testVehicle {
    public static void showVehicleInfo(Vehicle vehicle) {
        vehicle.showInfo();
    }
    
    public static void main(String[] args) {
        Bike bike = new Bike("蓝色", 2, 15, 180, 1, "张三");
        bike.run();
        bike.showInfo();
        System.out.println("自行车颜色：" + bike.getColor());
        System.out.println("自行车座位数：" + bike.getSeats());
        System.out.println();
        
        Trunk trunk = new Trunk("绿色", 6, 80.0f, 45.0f, 10.5f, "李四");
        trunk.run();
        trunk.showInfo();
        System.out.println("卡车轮子数目：" + trunk.getNumWheel());
        System.out.println("卡车载重：" + trunk.getLoad() + "吨");
        System.out.println();
        
        System.out.println("传递Bike对象：");
        showVehicleInfo(bike); 
        
        System.out.println("传递Trunk对象：");
        showVehicleInfo(trunk); 
        
    }
}
