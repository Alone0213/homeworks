public class Trunk extends Vehicle {
    private float load;
    private String ownerName;
    
    public Trunk(String color, int numWheel, float curSpeed, float curDirection, 
                 float load, String ownerName) {
        super(color, numWheel=8, curSpeed, curDirection);
        this.load = load;
        this.ownerName = ownerName;
    }
    
    @Override
    public void showInfo() {
        System.out.println("卡车车主姓名：" + ownerName + "，载重：" + load + "吨");
    }

    public float getLoad() {
        return load;
    }
    
    public void setLoad(float load) {
        this.load = load;
    }
    
    public String getOwnerName() {
        return ownerName;
    }
    
    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }
}
