public class Bike extends Vehicle {
    private int seats;
    private String ownerName;
    
    // 构造方法
    public Bike(String color, int numWheel, float curSpeed, float curDirection, 
                int seats, String ownerName) {
        super(color, numWheel=2, curSpeed, curDirection); // 调用父类构造方法
        this.seats = seats;
        this.ownerName = ownerName;
    }
    @Override
    public void showInfo() {
        System.out.println("自行车车主姓名：" + ownerName + "，座位数：" + seats);
    }
    
    public int getSeats() {
        return seats;
    }
    
    public void setSeats(int seats) {
        this.seats = seats;
    }
    
    public String getOwnerName() {
        return ownerName;
    }
    
    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }
}
