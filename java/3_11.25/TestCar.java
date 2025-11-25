public class TestCar {
    public static void main(String args[]){
        Car a1=new Car("Car1");
        Car a2=new Car("Car2");
        a1.status();
        a2.status();
        a1.setcarDirection(Math.PI/2);
        a2.setcarDirection(Math.PI);
        a1.setcarSpeed(10);
        a2.setcarSpeed(10);
        a1.changeSpeed(10);
        a2.changeSpeed(-5);
        a1.status();
        a2.status();
    }
}
