public class Vehicle {
    private String color;
    private int numWheel;
    private float curSpeed;
    private float curDirection;
    public Vehicle(String color, int numWheel, float curSpeed, float curDirection) {
        this.color = color;
        this.numWheel = numWheel;
        this.curSpeed = curSpeed;
        this.curDirection = curDirection;
    }
    
    public void run() {
        System.out.println("正在行驶中。");
    }
    
    public void showInfo() {
        System.out.println("交通工具颜色：" + color + "，轮子数目：" + numWheel);
    }

    public String getColor() {
        return color;
    }

    public int getNumWheel() {
        return numWheel;
    }

    public float getCurSpeed() {
        return curSpeed;
    }

    public float getCurDirection() {
        return curDirection;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public void setNumWheel(int numWheel) {
        this.numWheel = numWheel;
    }

    public void setCurSpeed(float curSpeed) {
        this.curSpeed = curSpeed;
    }

    public void setCurDirection(float curDirection) {
        this.curDirection = curDirection;
    }
}
